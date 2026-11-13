// 한국어 자막(애니쇼츠 우리 규칙): words.json([{w,s,e}]) 을 2~3낱말씩 묶어 화면 아래쪽 가운데에 띄운다.
// 흰 굵은 글자 + 두꺼운 검은 테두리 · 낱말 묶음이 바뀔 때 딱 바뀜 · 픽셀 값은 1080x1920 기준으로 화면 높이에 맞춰 늘어남.
// 쓰는 법(Root.tsx 의 새 구성): <AbsoluteFill><BridgeShort /><Captions words={words} /></AbsoluteFill>
//   words 는 import words from "../../../public/<이름>/words.json" 처럼 불러오거나 staticFile 로 읽는다.
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

type Word = { w: string; s: number; e: number };

const group = (words: Word[]) => {
  const out: Word[][] = [];
  let cur: Word[] = [];
  for (const w of words) {
    cur.push(w);
    const len = cur.reduce((a, x) => a + x.w.length, 0);
    if (len >= 9 || cur.length >= 3 || /[.,?!…]$/.test(w.w)) { out.push(cur); cur = []; }
  }
  if (cur.length) out.push(cur);
  return out;
};

export const Captions: React.FC<{ words: Word[]; top?: number; size?: number }> = ({ words, top = 0.68, size = 84 }) => {
  const f = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const t = f / fps;
  const k = height / 1920;
  const groups = React.useMemo(() => group(words), [words]);
  const g = groups.find((x) => t >= x[0].s - 0.05 && t <= x[x.length - 1].e + 0.12);
  if (!g) return null;
  const stroke = 14 * k;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", top: `${top * 100}%`, width: "100%", textAlign: "center", padding: `0 ${60 * k}px`,
        fontFamily: "'Black Han Sans', 'Pretendard', sans-serif", fontWeight: 900, fontSize: size * k, lineHeight: 1.15, color: "#fff",
        WebkitTextStroke: `${stroke}px #000`, paintOrder: "stroke fill", wordBreak: "keep-all" }}>
        {g.map((w) => w.w.replace(/[.,]$/, "")).join(" ")}
      </div>
    </AbsoluteFill>
  );
};
