"""한국어 대본 → voice.wav(48kHz 모노) + words.json([{"w","s","e"}], 애니쇼츠 story.ts·audio/mix.py 형식)
 실행: python3 목소리.py 대본.txt 출력폴더 [목소리=F1] [빠르기=1.0]
 목소리: 쇼츠만들기의 수퍼토닉(무료) — SHORTS_HOME(쇼츠만들기·수퍼토닉이 있는 폴더) 또는 ~/.claude/skills/쇼츠만들기 의 위 폴더에서 찾는다.
 내 목소리로 녹음했다면: python3 목소리.py 대본.txt 출력폴더 --wav 내녹음.wav  (단어 시간만 만든다)
 단어 시간은 문장마다 실제 말한 구간 안에서, 쉼표 뒤 쉼(무음)을 먼저 찾아 자르고 글자 수 비율로 나눈다 → 나중에 손으로 다듬는다."""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

a = [x for x in sys.argv[1:] if not x.startswith('--')]
대본, 출력 = Path(a[0]), Path(a[1]); 출력.mkdir(parents=True, exist_ok=True)
목소리 = a[2] if len(a) > 2 else 'F1'; 빠르기 = a[3] if len(a) > 3 else '1.0'
내녹음 = sys.argv[sys.argv.index('--wav') + 1] if '--wav' in sys.argv else None
글 = re.sub(r'\s+', ' ', 대본.read_text(encoding='utf-8')).strip()
문장 = [s.strip() for s in re.findall(r'[^.?!…]+[.?!…]*', 글) if s.strip()]
SR = 48000

def 쉼(wav):
    r = subprocess.run(['ffmpeg', '-v', 'info', '-nostats', '-i', str(wav), '-af', 'silencedetect=n=-38dB:d=0.12', '-f', 'null', '-'], capture_output=True, text=True)
    return list(zip(map(float, re.findall(r'silence_start: ([\d.]+)', r.stderr)), map(float, re.findall(r'silence_end: ([\d.]+)', r.stderr))))

def 나누기(말, s0, e0, 쉼들):
    낱 = 말.split(' '); 묶, 지 = [], []
    for x in 낱:
        지.append(x)
        if re.search(r'[,.?!…]$', x): 묶.append(지); 지 = []
    if 지: 묶.append(지)
    구간 = [(s0, e0)]
    안 = [(p, q) for p, q in 쉼들 if p > s0 + 0.1 and q < e0 - 0.05]
    if len(묶) > 1 and len(안) >= len(묶) - 1:
        고 = sorted(sorted(안, key=lambda t: t[1] - t[0], reverse=True)[:len(묶) - 1]); 구간, 앞 = [], s0
        for p, q in 고: 구간.append((앞, p)); 앞 = q
        구간.append((앞, e0))
    else:
        묶 = [낱]
    out = []
    for 말들, (p, q) in zip(묶, 구간):
        전, 쌓 = sum(len(x) for x in 말들), 0
        for x in 말들:
            out.append({'w': x, 's': round(p + (q - p) * 쌓 / 전, 3), 'e': round(p + (q - p) * (쌓 + len(x)) / 전, 3)}); 쌓 += len(x)
    return out

if 내녹음:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 내녹음, '-ac', '1', '-ar', str(SR), str(출력 / 'voice.wav')], check=True)
    길이 = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(출력 / 'voice.wav')], capture_output=True, text=True).stdout)
    쉼들 = 쉼(출력 / 'voice.wav')
    말구간 = [(0.0, 길이)]; 전체 = [' '.join(문장)]
    words = 나누기(전체[0], *말구간[0], 쉼들)
else:
    후보 = [os.environ.get('SHORTS_HOME', ''), str(Path.home() / '.claude/skills/쇼츠만들기/..')]
    집 = next((Path(h).resolve() for h in 후보 if h and (Path(h) / '수퍼토닉').is_dir()), None)
    if not 집:
        sys.exit('❌ 수퍼토닉(쇼츠만들기)을 못 찾았습니다. SHORTS_HOME 을 쇼츠만들기 폴더로 두거나, --wav 내녹음.wav 로 직접 녹음한 파일을 주세요.')
    py = 집 / '수퍼토닉/.venv/bin/python'
    rec = 집 / '쇼츠만들기/도구/수퍼토닉녹음.py'
    tmp = Path(tempfile.mkdtemp())
    일 = [[s, str(tmp / f'{i:02d}.wav')] for i, s in enumerate(문장)]
    (tmp / '일.json').write_text(json.dumps(일, ensure_ascii=False))
    env = dict(os.environ, SHORTS_HOME=str(집))
    r = subprocess.run([str(py), str(rec), 목소리, 빠르기, str(tmp / '일.json')], capture_output=True, text=True, cwd=str(rec.parent), env=env)
    구 = [json.loads(l.split('구간', 1)[1]) for l in r.stdout.splitlines() if l.startswith('구간')]
    if len(구) != len(문장): sys.exit('❌ 녹음 실패\n' + r.stdout[-800:] + r.stderr[-800:])
    # 문장마다 말한 부분만 잘라 0.12초 쉼으로 이어 붙인다
    words, 조각, t = [], [], 0.0
    for (wav, s0, e0, _), 말 in zip(구, 문장):
        s0 = max(0, s0 - 0.03); e0 = e0 + 0.05
        cut = tmp / ('c_' + Path(wav).name)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav, '-ss', f'{s0}', '-to', f'{e0}', '-ac', '1', '-ar', str(SR), str(cut)], check=True)
        쉼들 = [(p + t - s0, q + t - s0) for p, q in 쉼(wav)]
        words += 나누기(말, t + 0.03, t + (e0 - s0) - 0.05, 쉼들)
        조각.append(cut); t += (e0 - s0) + 0.12
    gap = tmp / 'gap.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'anullsrc=r={SR}:cl=mono', '-t', '0.12', str(gap)], check=True)
    lst = tmp / 'l.txt'; lst.write_text(''.join(f"file '{c}'\nfile '{gap}'\n" for c in 조각))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', str(출력 / 'voice.wav')], check=True)
    subprocess.run(['rm', '-rf', str(tmp)])
(출력 / 'words.json').write_text(json.dumps(words, ensure_ascii=False, indent=0))
print(f'✅ {출력}/voice.wav · words.json ({len(words)}단어, 끝 {words[-1]["e"]:.1f}초)')
