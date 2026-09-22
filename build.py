#!/usr/bin/env python3
"""Bygger ett lösenordsskyddat deck.

  python3 build.py <deck-dir>

Läser <deck-dir>/template.html och <deck-dir>/src/slides.html (ej i git),
krypterar sliderna med AES-256-GCM (nyckel via PBKDF2-SHA256) och skriver
<deck-dir>/index.html. Lösenordet hämtas från $DECK_PASSWORD eller frågas efter.
"""
import base64, getpass, json, os, secrets, sys, unicodedata
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITER = 200_000

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    deck = Path(sys.argv[1])
    pw = os.environ.get("DECK_PASSWORD") or getpass.getpass("Lösenord: ")
    pw = unicodedata.normalize("NFC", pw).strip().lower().encode()
    salt, iv = secrets.token_bytes(16), secrets.token_bytes(12)
    key = PBKDF2HMAC(hashes.SHA256(), 32, salt, ITER).derive(pw)
    plain = (deck / "src" / "slides.html").read_bytes()
    ct = AESGCM(key).encrypt(iv, plain, None)
    b64 = lambda b: base64.b64encode(b).decode()
    payload = json.dumps({"iter": ITER, "salt": b64(salt), "iv": b64(iv), "ct": b64(ct)})
    html = (deck / "template.html").read_text(encoding="utf-8").replace("__PAYLOAD__", payload)
    (deck / "index.html").write_text(html, encoding="utf-8")
    print(f"skrev {deck/'index.html'} ({len(html):,} tecken, {len(plain):,} bytes krypterade)")

if __name__ == "__main__":
    main()
