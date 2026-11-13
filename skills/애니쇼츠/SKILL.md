---
name: 애니쇼츠
description: 영상 생성 AI 없이 코드로 55~70초 세로 3D 애니메이션 쇼츠를 만든다 — 진한 외곽선의 2D 콩머리 캐릭터 카드가 손그림 질감의 3D 마을 안에서 움직이고(three.js), Remotion이 프레임마다 찍는다. 한국어 나레이션(수퍼토닉 무료 음성 또는 내 녹음)·한국어 자막·직접 합성한 효과음과 음악. 원본 mromidev/claude-animated-shorts(MIT)를 한국어용으로 고친 판. «애니쇼츠», «애니 쇼츠», «카툰 3D 쇼츠», «3D 애니메이션 쇼츠», «철교 영상처럼», «만화 캐릭터로 이야기 쇼츠» 같은 말에 쓴다. 올리기는 하지 않는다.
---

# 애니쇼츠 (카툰 3D 이야기 쇼츠 · 한국어판)

원본: `원본/SKILL_EN.md` (mromidev/claude-animated-shorts, MIT — `LICENSE`). 이 문서는 **우리 규칙**과 **한국어 흐름**만 덧붙인다.
세부 값·명령·함정은 원본이 정답이다. 순서마다 원본의 같은 번호 절을 함께 읽는다.

## 우리 규칙 (원본의 "User rules"를 대신함)
- **한국어 나레이션**, 존댓말, 한 가지 톤. 숫자·영어는 한글 읽기로 적는다(예: «천팔백삼십일 년»)— 음성이 잘못 읽는 것을 막는다.
- **한국어 자막 켬**: `templates/Captions.tsx` (2~3낱말씩, 흰 글자+검은 테두리, 화면 68% 높이). 원본의 «자막 없음»은 버린다.
- 이야기·캐릭터·목소리는 **우리 것**. 원본의 레퍼런스(남의 채널)는 화풍 공부용 숫자(`원본/reports/`)만 쓰고, 그 채널의 장면·캐릭터를 베끼지 않는다.
- 웃음 포인트는 **조사한 사실**로. 사실에는 출처를 `SCRIPT.md` 맨 위에 적는다. 사역·교육용이면 마지막에 짧은 적용(말씀 한 절 등)을 넣어도 된다.
- 기본 믹스: 음악 +3 dB · 효과음 -6 dB · 목소리 그대로, 최종 -14 LUFS.
- 최종 출력: 1080×1920(빠름) 또는 2K 1440×2560(`--scale 1.3333`, 67초에 약 10분).
- 단계마다 저장. 대본을 사용자가 승인하면 그다음은 쭉 진행.
- **끝나면 정리**: `bash 도구/임시정리.sh` (렌더 임시 묶음 수 GB씩 쌓임).

## 처음 한 번 — 준비
1. 필요: Node 18+, Python 3(numpy·scipy), ffmpeg, 구글 크롬.
2. Remotion 프로젝트 하나(이미 있으면 그대로): `npx create-video@latest` → 빈 템플릿.
3. 그 프로젝트에서: `npm i @remotion/three three @react-three/fiber @react-three/postprocessing postprocessing`
4. `templates/scripts/*` 를 프로젝트 `scripts/` 로, `templates/bridge/` 를 `src/videos/bridge/` 로 복사, `src/Root.tsx` 에 `BridgeShort`(1080×1920, 30fps, `BRIDGE_FRAMES`) 등록 → 예제가 도는지 정지 화면 한 장으로 확인.
5. 소품(선택): Kenney Nature Kit·Holiday Kit(CC0, kenney.nl)의 GLB를 `public/bridge/kenney/<이름>.glb` 로. 이름 목록은 `templates/bridge/world.ts`의 `KENNEY`. 없으면 소품만 빠지고 나머지는 그려진다.
6. 임시 폴더를 넉넉한 곳으로: `export REMOTION_TMP=$HOME/remotion-tmp TEMP=$HOME/remotion-tmp TMP=$HOME/remotion-tmp`

## 만드는 순서 (원본 Pipeline 1~11과 같은 번호)
1. **주제·사실** — 눈에 보이는 원인→결과가 있는 실화 하나 + 일상 비유 하나. 출처 확인(검색).
2. **대본** (초당 약 4~5음절, 55~70초 ≈ 한국어 250~330자). 공식(`원본/STYLE_BIBLE.md`):
   훅(역설을 사실처럼 첫 문장) → 배경(연도·장소) → 점점 커지는 사건 3~4개 → 무너지는 순간 → «다행히… / 불행히…» →
   «알고 보니,»(원본의 "You see,") 원리 + 일상 비유 → 그 뒤 생긴 규칙 → 반전. 화면에 이미 보이는 걸 말로 설명하지 않는다.
   `templates/SCRIPT_example.md` 꼴로 `SCRIPT.md` 를 쓰고 **사용자 승인**을 받는다.
3. **목소리** — `python3 도구/목소리.py SCRIPT본문.txt <작업폴더>/voice F1 1.0`
   → `voice.wav`(48kHz) + `words.json`(`[{w,s,e}]`). 목소리: M1~M5(남)·F1~F5(여). 직접 녹음했으면 `--wav 내녹음.wav`.
   단어 시간은 자동으로 대략 맞춰지니 **눈에 띄는 낱말(펀치 단어)은 손으로 다듬는다**. 이후 모든 것은 words.json 기준.
4. **샷 계획** — `templates/bridge/` 를 `src/videos/<이름>/` 로 복사, 새 구성 등록, `story.ts` 의 SHOTS·XFADE·FLASH_AT·CAMS·KICKS·dofAt·FOREGROUND 를 새 이야기로. 반응은 그 낱말 0~3프레임 앞.
5. **세계** (lights·shade·build·paint·world.ts) — 새 장소. 원본 «Final look values»의 숫자를 지킨다.
6. **캐릭터** (toon·cast·cardshade.ts) — 우리 인물. 한복·교복 등도 `Pen` API로 그린다. 3.5등신, 콩머리.
7. **후처리** (Bridge.tsx·ink·lensblur·grade) — 순서 고정: 외곽선 → 렌즈 흐림 → 빛번짐 → 톤맵 → 색보정.
   자막: 새 구성에서 `<Captions words={words} />` 를 화면 위에 얹는다.
8. **소리** (`templates/audio/` → `<작업폴더>/audio/`) — timeline.py 를 새 story.ts 에 맞추고 sfx·music·mix 실행 → mix.wav. 화면 시간을 먼저 고정하고 소리는 맨 나중.
9. **정지 화면 점검** — `node scripts/bridge-stills.mjs out/<이름>/x_ 100,400,900 0.5`
   벽 안에 박힌 카메라·얼굴 가린 소품·엉뚱한 색을 먼저 잡는다. 비교 기준이 필요하면 `python scripts/sbs_sheet.py out.jpg --ours … --ref …`(--ref 에는 사용자가 정한 참고 화면). 검증 에이전트에게 1~3장씩 보여 주고 짧은 판정.
10. **최종 렌더** — `npx remotion render src/index.ts <구성> out/<이름>/video.mp4 --codec h264 --crf 16 [--scale 1.3333]`
    소리 붙이기: `ffmpeg -i video.mp4 -i mix.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k final.mp4`
    QA: `python scripts/short_qa.py final.mp4 out/<이름>/qa shots.json` (shots.json 은 `scripts/bridge_shots.py`). 걸린 것 고치고 다시.
11. **전달** — 최종 mp4 를 사용자에게 보내고, 중간 정지 화면·QA 낱장·임시 묶음을 지운다(`도구/임시정리.sh`). 업로드는 사용자가 한다.

## 레퍼런스 맞추기 (특정 화풍에 더 가깝게 할 때)
원본 «Look-match loop»: 참고 화면을 **숫자로** 재서(`원본/reports/` 7편이 그 예) → 부위별 담당(cam/world/mat/char/post) 샌드박스에서 고치고 → `scripts/bridge_merge.py` 로 합치고 → 검증 에이전트가 10점 만점 채점. 사용자가 시킨 만큼만 돈다(비용·시간 큼).

## 하지 않는 것
- 남의 채널 장면·캐릭터·대본 베끼기, 레퍼런스 화면을 올리거나 보내기.
- 유튜브·인스타에 대신 올리기.
- 렌더 중 임시 폴더 지우기(정리는 렌더가 없을 때만).
