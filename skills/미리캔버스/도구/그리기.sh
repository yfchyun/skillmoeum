#!/bin/bash
# HTML 한 장 → PNG 한 장 (크롬 헤드리스) · 미리캔버스에 올릴 그림 만들기
# 실행: bash 그리기.sh <파일.html[?v=쪽]> <너비> <높이> <출력.png>
set -e
IN="$1"; W="$2"; H="$3"; OUT="$4"
[ -z "$OUT" ] && { echo "쓰는 법: bash 그리기.sh 파일.html 1080 1350 결과.png"; exit 1; }
FILE="${IN%%\?*}"; Q=""; [ "$IN" != "$FILE" ] && Q="?${IN#*\?}"
ABS="$(cd "$(dirname "$FILE")" && pwd)/$(basename "$FILE")"
OUTABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
for C in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "/c/Program Files/Google/Chrome/Application/chrome.exe" "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" "$(command -v google-chrome || true)" "$(command -v chromium || true)"; do
  [ -n "$C" ] && [ -x "$C" ] && CHROME="$C" && break
done
[ -z "$CHROME" ] && { echo "❌ 구글 크롬이 없습니다. https://www.google.com/chrome 에서 설치하세요."; exit 2; }
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --virtual-time-budget=8000 \
  --window-size="$W,$H" --screenshot="$OUTABS" "file://$ABS$Q" >/dev/null 2>&1
[ -s "$OUTABS" ] && echo "✅ $OUTABS (${W}×${H})" || { echo "❌ 그림을 못 만들었습니다"; exit 3; }
