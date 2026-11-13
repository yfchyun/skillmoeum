#!/bin/bash
# 스킬모음 설치기 — Claude Code 스킬을 한 줄로 설치합니다.
#   전부:      curl -fsSL https://raw.githubusercontent.com/yfchyun/skillmoeum/main/install.sh | bash
#   하나만:    curl -fsSL https://raw.githubusercontent.com/yfchyun/skillmoeum/main/install.sh | bash -s 미리캔버스
set -e
REPO="yfchyun/skillmoeum"
DEST="$HOME/.claude/skills"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
echo "⬇️  스킬모음 내려받는 중…"
curl -fsSL "https://codeload.github.com/$REPO/tar.gz/main" | tar xz -C "$TMP"
SRC="$(ls -d "$TMP"/*/skills)"
mkdir -p "$DEST"
if [ $# -gt 0 ]; then LIST=("$@"); else LIST=(); for d in "$SRC"/*/; do LIST+=("$(basename "$d")"); done; fi
for name in "${LIST[@]}"; do
  [ -d "$SRC/$name" ] || { echo "❌ '$name' 스킬이 없습니다. 있는 것: $(ls "$SRC" | tr '\n' ' ')"; exit 1; }
  if [ -d "$DEST/$name" ]; then mkdir -p "$HOME/.claude/skills-backup"; mv "$DEST/$name" "$HOME/.claude/skills-backup/$name.$(date +%Y%m%d%H%M%S)"; echo "ℹ️  예전 버전($name)은 ~/.claude/skills-backup 에 보관했습니다"; fi
  cp -R "$SRC/$name" "$DEST/$name"
  find "$DEST/$name" -name '*.sh' -exec chmod +x {} \;
  echo "✅ $name → $DEST/$name"
done
echo "👉 Claude Code를 새로 열면 바로 쓸 수 있습니다."
