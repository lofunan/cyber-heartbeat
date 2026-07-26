"""
cyber-heartbeat CLI demo
模拟一轮对话，展示情绪积温 → BPM 的变化
"""
import time
import random
from engine import load_mood, tick_mood, accumulate, mood_to_bpm, mood_to_strength, detect_arrhythmia
from prompt import build_mood_block

DELTA_LABELS = ["warm", "neutral", "cool", "hurt"]

def simulate():
    print("=" * 48)
    print("  [heart] cyber-heartbeat - 情绪积温演示")
    print("=" * 48)

    current_mood = tick_mood()
    data = load_mood()
    last_updated = data.get("updated_at", 0)

    print(f"\n初始情绪: {current_mood:.3f}")
    print(f"初始 BPM: {mood_to_bpm(current_mood)}")
    print()

    for step in range(8):
        label = random.choice(DELTA_LABELS)
        if step == 0:
            label = "warm"
        elif step == 3:
            label = "hurt"
        elif step == 6:
            label = "neutral"

        current_mood = accumulate(label, current_mood, last_updated)
        last_updated = time.time()

        bpm = mood_to_bpm(current_mood)
        strength = mood_to_strength(current_mood)
        arrhythmia = detect_arrhythmia()
        block = build_mood_block(current_mood, MOOD_DELTA_MAP.get(label, 0))

        print(f"  [{step + 1}] 用户 → {label:>8s}")
        print(f"      mood: {current_mood:+.3f}  BPM: {bpm}  "
              f"强度: {strength}  {'[心律不齐]' if arrhythmia else ''}")
        print(f"      {block}")
        print()

    print("=" * 48)
    print("  [OK] 演示完成 - 打开 heart.html 可看粒子动画")
    print("=" * 48)


# ── 让 demo.py 能用 MOOD_DELTA_MAP ──
from engine import MOOD_DELTA_MAP

if __name__ == "__main__":
    simulate()
