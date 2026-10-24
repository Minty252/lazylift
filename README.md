# lazylift.cc

Landing page with a waitlist for the LazyLift browser extension (code in repo tf-match).
German at `/`, English at `/en/`. Static files on GitHub Pages; DNS at Namecheap.

- Edit texts in `build.py`, then `python3 build.py` writes `index.html`, `en/index.html`,
  imprint and privacy policy (DE + EN). Commit the generated files too.
- The waitlist form posts to `https://fastpal.com/api/anfrage` (art "warteliste", Resend mail
  to Moritz); that route allows this origin (CORS). Nothing is stored.
- Fonts are self-hosted in `assets/fonts`; the mail address is only in the HTML as reversed
  base64 and filled in by `assets/site.js`. Asset URLs carry a content hash.
- Until 2026-10-25 this page was fastpal.com/coach (fastpal-next `app/coach`).
