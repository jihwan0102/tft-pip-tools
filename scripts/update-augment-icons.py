#!/usr/bin/env python3
"""Regenerate augment-icons.json: augment apiName -> CommunityDragon icon path.

MetaTFT's augment icons are bare glyphs; CommunityDragon has the in-game
icons with their rarity colouring, but its full data file is ~24MB, too
heavy to load on a phone. Run this after a new set or patch:

    python3 scripts/update-augment-icons.py
"""
import json
import os
import urllib.request

COMPS_URL = "https://api-hc.metatft.com/tft-comps-api/comps_data?queue=1100"
LOOKUP_URL = "https://data.metatft.com/lookups/{}_latest_ko_kr.json"
CDRAGON_URL = "https://raw.communitydragon.org/latest/cdragon/tft/en_us.json"
OUT = os.path.join(os.path.dirname(__file__), "..", "augment-icons.json")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "tft-pip-tools"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def main():
    comps = get(COMPS_URL)
    tft_set = comps["results"]["data"].get("tft_set") or comps["tft_set"]
    augments = get(LOOKUP_URL.format(tft_set))["augments"]
    cdragon = {i["apiName"]: i for i in get(CDRAGON_URL)["items"]}
    icons = {}
    for a in augments:
        icon = (cdragon.get(a["apiName"]) or {}).get("icon")
        # Placeholder art ("missing-t1" etc.) is worse than MetaTFT's glyph.
        if icon and "/missing-" not in icon.lower():
            icons[a["apiName"]] = icon.lower().rsplit(".", 1)[0]
    with open(OUT, "w") as f:
        json.dump({"set": tft_set, "icons": dict(sorted(icons.items()))}, f, indent=0, ensure_ascii=False)
        f.write("\n")
    print(f"{tft_set}: {len(icons)}/{len(augments)} augments")


if __name__ == "__main__":
    main()
