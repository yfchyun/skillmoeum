#!/bin/bash
# 렌더가 끝난 뒤 Remotion 임시 묶음(remotion-webpack-bundle-*, 하나에 ~1.3GB)과 크롬 임시 프로필을 지운다.
# 렌더 중에는 실행하지 말 것. 실행: bash 임시정리.sh
T="${REMOTION_TMP:-$HOME/remotion-tmp}"
pgrep -f "remotion render|remotion still|bridge-stills" >/dev/null && { echo "⏸  렌더가 돌고 있어 정리하지 않습니다."; exit 0; }
for D in "$T" "${TMPDIR:-/tmp}"; do
  [ -d "$D" ] || continue
  n=$(find "$D" -maxdepth 1 \( -name 'remotion-webpack-bundle-*' -o -name 'puppeteer_dev_chrome_profile-*' \) | wc -l | tr -d ' ')
  [ "$n" = 0 ] && continue
  s=$(find "$D" -maxdepth 1 \( -name 'remotion-webpack-bundle-*' -o -name 'puppeteer_dev_chrome_profile-*' \) -exec du -sk {} + | awk '{t+=$1} END{print int(t/1024)}')
  find "$D" -maxdepth 1 \( -name 'remotion-webpack-bundle-*' -o -name 'puppeteer_dev_chrome_profile-*' \) -exec rm -rf {} +
  echo "🧹 $D 에서 ${n}개 · ${s}MB 정리"
done
echo "✅ 정리 끝"
