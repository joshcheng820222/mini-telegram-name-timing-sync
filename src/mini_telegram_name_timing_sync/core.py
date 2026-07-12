from __future__ import annotations

from datetime import datetime
from typing import Mapping

import pytz

DIGIT_MAP = str.maketrans("0123456789", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗")
LETTER_STYLES = {
    "math_bold": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳",
    "math_sans_bold": "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇",
    "math_script": "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏",
    "monospace": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣",
}
ASCII_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
WEEKDAYS = "一二三四五六日"


def style_text(text: str, style: str) -> str:
    if style == "normal":
        return text
    result = text.translate(DIGIT_MAP)
    letters = LETTER_STYLES.get(style)
    return result.translate(str.maketrans(ASCII_LETTERS, letters)) if letters else result


def format_time(now: datetime, mode: str) -> str:
    formats = {
        "24h": "%H:%M",
        "12h": "%I:%M %p",
        "date": "%m-%d %H:%M",
        "seconds": "%H:%M:%S",
    }
    if mode == "weekday":
        return f"周{WEEKDAYS[now.weekday()]} {now:%H:%M}"
    if mode not in formats:
        raise ValueError(f"unsupported time_format: {mode}")
    return now.strftime(formats[mode])


def build_display_name(config: Mapping, now: datetime | None = None) -> str:
    tz = pytz.timezone(str(config.get("timezone", "Asia/Shanghai")))
    if now is None:
        now = datetime.now(tz)
    elif now.tzinfo is None:
        now = tz.localize(now)
    else:
        now = now.astimezone(tz)

    name = str(config["display_name"]).strip()
    emoji = str(config.get("emoji", "")).strip()
    time_text = format_time(now, str(config.get("time_format", "24h")))
    order = str(config.get("order", "name_time"))
    if order == "name_time":
        parts = [name, emoji, time_text]
    elif order == "time_name":
        parts = [time_text, name, emoji]
    else:
        raise ValueError("order must be name_time or time_name")
    return style_text(" ".join(part for part in parts if part), str(config.get("font", "normal")))
