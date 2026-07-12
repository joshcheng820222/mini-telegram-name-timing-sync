# Mini Telegram Name Timing Sync

A small self-hosted service that appends the current time to your Telegram display name.

Default display order:

```text
Your Name 03:48 PM
```

The name stays first. `time_name` is still available if you prefer the opposite order.

## Features

- Name-first or time-first display order
- 24-hour, 12-hour, date, weekday and seconds formats
- IANA timezones
- Optional emoji and Unicode font styling
- Telethon session persistence
- systemd service with automatic restart
- Isolated Python virtual environment

## Install

Telegram API credentials are available from <https://my.telegram.org/apps>.

```bash
wget https://raw.githubusercontent.com/joshcheng820222/mini-telegram-name-timing-sync/main/install.sh
chmod +x install.sh
sudo ./install.sh
sudo nano /etc/telegram-name-timing-sync/config.json
sudo systemctl start telegram-name-timing-sync
```

The first start is interactive because Telegram asks for your phone number, login code and possibly your two-step verification password:

```bash
sudo /opt/telegram-name-timing-sync/venv/bin/telegram-name-timing-sync \
  --config /etc/telegram-name-timing-sync/config.json --once
sudo systemctl restart telegram-name-timing-sync
```

## Configuration

| Key | Values | Default |
|---|---|---|
| `display_name` | Any valid Telegram first name | required |
| `timezone` | IANA timezone | `Asia/Shanghai` |
| `time_format` | `24h`, `12h`, `date`, `weekday`, `seconds` | `24h` |
| `order` | `name_time`, `time_name` | `name_time` |
| `font` | `normal`, `math_bold`, `math_sans_bold`, `math_script`, `monospace` | `normal` |
| `emoji` | Optional text/emoji | empty |
| `update_interval` | Seconds, minimum 30 | `60` |

Preview without connecting to Telegram:

```bash
sudo /opt/telegram-name-timing-sync/venv/bin/telegram-name-timing-sync \
  --config /etc/telegram-name-timing-sync/config.json --dry-run
```

## Update

Run the installer again. Existing configuration and Telegram session are preserved.

## Uninstall

```bash
sudo systemctl disable --now telegram-name-timing-sync
sudo rm -f /etc/systemd/system/telegram-name-timing-sync.service
sudo systemctl daemon-reload
sudo rm -rf /opt/telegram-name-timing-sync
# Keep /etc/telegram-name-timing-sync if you may reinstall later.
```

## Security

`config.json`, Telegram session files and logs are ignored by Git. Never publish them. Treat the session file like a password because it grants account access.

## Origin

This is an independent implementation inspired by the workflow of [xmg0828/telegram_time](https://github.com/xmg0828/telegram_time). No upstream source code is bundled because the upstream repository does not declare a software license.

## License

MIT
