MOOD_TEXT = [
    "温暖满足，语气可以温柔些",
    "轻松平和，自然地聊就好",
    "中性，正常发挥",
    "情绪不高，话可以少一些",
    "低落或烦躁，简短冷淡",
]


def build_mood_block(mood: float, delta_val: float) -> str:
    bin_idx = (
        0 if mood > 0.4 else
        1 if mood > 0.1 else
        2 if mood > -0.1 else
        3 if mood > -0.4 else
        4
    )
    trend = ""
    if delta_val >= 0.2:
        trend = "趋势回暖"
    elif delta_val <= -0.3:
        trend = "情绪骤降"

    lines = []
    if trend:
        lines.append(f"{trend}，")
    lines.append(MOOD_TEXT[bin_idx])
    guidance = "".join(lines)

    bpm = max(40, min(130, round(72 + mood * 50)))
    return f"\n【情绪状态】\n{guidance}\n你现在的心跳为{bpm}BPM"
