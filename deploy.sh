#!/bin/sh
# tft.jihwan.kim 배포: 사이트에 필요한 정적 파일만 /srv/www/tft.jihwan.kim 로 복사한다.
# (GitHub Pages는 push만 하면 따로 반영된다.)
set -e
cd "$(dirname "$0")"
DEST=/srv/www/tft.jihwan.kim
sudo mkdir -p "$DEST/fonts"
sudo install -m 644 index.html comps.html augment-icons.json "$DEST/"
sudo rsync -a --delete --include='*.woff2' --include='OFL.txt' --exclude='*' fonts/ "$DEST/fonts/"
sudo chown -R root:root "$DEST"
sudo find "$DEST" -type d -exec chmod 755 {} + -o -type f -exec chmod 644 {} +
echo "배포 완료: $DEST"
