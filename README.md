# 스킬모음

목회·사역 현장에서 쓰는 Claude Code 스킬 모음입니다.

## 한 줄 설치

모든 스킬:

```bash
curl -fsSL https://raw.githubusercontent.com/yfchyun/skillmoeum/main/install.sh | bash
```

하나만 (예: 미리캔버스):

```bash
curl -fsSL https://raw.githubusercontent.com/yfchyun/skillmoeum/main/install.sh | bash -s 미리캔버스
```

설치 후 Claude Code를 새로 열면 됩니다.

## 들어 있는 스킬

| 스킬 | 하는 일 |
|---|---|
| 미리캔버스 | 안내서·글로 미리캔버스 규격 홍보물(인스타 피드·카드뉴스·스토리·페이스북·썸네일·A4) PNG를 만들고, 미리캔버스에서 마무리하는 법을 안내합니다. 구글 크롬 필요. |
| 애니쇼츠 | 영상 AI 없이 코드(three.js + Remotion)로 2D 캐릭터가 3D 마을에서 움직이는 55~70초 세로 애니 쇼츠를 만듭니다. 한국어 나레이션(수퍼토닉·내 녹음)·한국어 자막·합성 효과음/음악. 원본 [mromidev/claude-animated-shorts](https://github.com/mromidev/claude-animated-shorts) (MIT)를 한국어용으로 고친 판. Node·Python(numpy·scipy)·ffmpeg 필요. |

## 라이선스·출처
- 애니쇼츠: 원본 MIT 라이선스(`skills/애니쇼츠/LICENSE`). 원본의 레퍼런스 화면(다른 채널)은 넣지 않았습니다.

## 사진 출처
`skills/미리캔버스/본보기/사진출처.txt` 참고 (위키미디어 공용, CC BY 3.0 · 퍼블릭 도메인).
