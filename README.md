# Premier League Highlights Tracker

A mobile-friendly Premier League highlights checklist hosted with GitHub Pages.

The app shell is in `index.html`. Automatic fixtures will be supplied as `fixtures.json` by a scheduled GitHub Actions workflow, keeping any football-data API token out of the browser. Watched match IDs are currently saved in this browser on this device; cross-device sync would require a database and sign-in.
