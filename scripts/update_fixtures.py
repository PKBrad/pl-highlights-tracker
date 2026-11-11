#!/usr/bin/env python3
"""Fetch the current Premier League season and publish a public fixtures.json."""
import json
import os
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen

TOKEN = os.environ.get("FOOTBALL_DATA_TOKEN")
SEASON = os.environ.get("PL_SEASON", "2026")
URL = f"https://api.football-data.org/v4/competitions/PL/matches?season={SEASON}"

if not TOKEN:
    sys.exit("Missing FOOTBALL_DATA_TOKEN repository secret")

request = Request(URL, headers={"X-Auth-Token": TOKEN, "User-Agent": "pl-highlights-tracker"})
with urlopen(request, timeout=30) as response:
    payload = json.load(response)

matches = []
for match in payload.get("matches", []):
    if match.get("stage") != "REGULAR_SEASON" or not match.get("matchday"):
        continue
    home = (match.get("homeTeam") or {}).get("shortName") or (match.get("homeTeam") or {}).get("name")
    away = (match.get("awayTeam") or {}).get("shortName") or (match.get("awayTeam") or {}).get("name")
    if not home or not away:
        continue
    matches.append({
        "id": str(match["id"]),
        "matchday": int(match["matchday"]),
        "utcDate": match.get("utcDate"),
        "date": match.get("utcDate"),
        "status": match.get("status", "SCHEDULED"),
        "home": home,
        "away": away
    })

matches.sort(key=lambda item: (item["matchday"], item["utcDate"] or ""))
if not matches:
    sys.exit("The API returned no Premier League regular-season fixtures; refusing to overwrite fixtures.json")

output = {
    "season": int(SEASON),
    "competition": "Premier League",
    "generatedAt": datetime.now(timezone.utc).isoformat(),
    "matches": matches
}
with open("fixtures.json", "w", encoding="utf-8") as file:
    json.dump(output, file, ensure_ascii=False, indent=2)
    file.write("\n")

print(f"Published {len(matches)} Premier League fixtures for {SEASON}/{str(int(SEASON)+1)[-2:]}")
