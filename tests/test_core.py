from datetime import datetime

import pytz
import pytest

from mini_telegram_name_timing_sync.core import build_display_name, format_time

BASE = {
    "display_name": "Josh",
    "timezone": "Asia/Shanghai",
    "time_format": "24h",
    "font": "normal",
}
NOW = pytz.timezone("Asia/Shanghai").localize(datetime(2026, 7, 12, 15, 48))


def test_name_first_is_default():
    assert build_display_name(BASE, NOW) == "Josh 15:48"


def test_time_first_remains_supported():
    assert build_display_name({**BASE, "order": "time_name"}, NOW) == "15:48 Josh"


def test_emoji_sits_between_name_and_time():
    assert build_display_name({**BASE, "emoji": "🎓"}, NOW) == "Josh 🎓 15:48"


def test_math_style_applies_to_ascii_and_digits():
    result = build_display_name({**BASE, "font": "math_bold"}, NOW)
    assert result == "𝐉𝐨𝐬𝐡 𝟏𝟓:𝟒𝟖"


def test_weekday_format():
    assert format_time(NOW, "weekday") == "周日 15:48"


def test_invalid_order_is_rejected():
    with pytest.raises(ValueError):
        build_display_name({**BASE, "order": "sideways"}, NOW)
