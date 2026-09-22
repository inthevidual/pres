# pres

Webbpresentationer på [pres.cptjanst.se](https://pres.cptjanst.se) (GitHub Pages).

Varje deck ligger i sin egen mapp: `template.html` (design + navigering + lösenordsgrind),
`src/slides.html` (slides 2–N, **ej i git**) och `index.html` (byggd, krypterad).

```
DECK_PASSWORD='…' python3 build.py skb2609
```

Sliderna krypteras med AES-256-GCM (PBKDF2-SHA256, 200k iterationer) och dekrypteras i
webbläsaren med WebCrypto. Titelsliden ligger okrypterad som suddig bakgrund bakom modalen.

Tangenter: piltangenter/mellanslag/klick = nästa steg, `Home`/`End`, `F` = helskärm, `#n` i URL:en = slide n.
