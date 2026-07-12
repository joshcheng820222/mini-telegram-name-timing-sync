from __future__ import annotations

import argparse
import asyncio
import json
import logging
import signal
from pathlib import Path

from telethon import TelegramClient, functions
from telethon.errors import FloodWaitError

from .core import build_display_name

LOG = logging.getLogger("telegram-name-timing-sync")


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    required = ("api_id", "api_hash", "display_name")
    missing = [key for key in required if not config.get(key)]
    if missing:
        raise ValueError("missing config keys: " + ", ".join(missing))
    config["api_id"] = int(config["api_id"])
    return config


async def run(config_path: Path, once: bool = False, dry_run: bool = False) -> None:
    config = load_config(config_path)
    interval = max(30, int(config.get("update_interval", 60)))
    session = config_path.parent / "telegram"
    if dry_run:
        print(build_display_name(config))
        return

    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for signum in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(signum, stop.set)

    async with TelegramClient(str(session), config["api_id"], config["api_hash"]) as client:
        LOG.info("Connected to Telegram")
        while not stop.is_set():
            target = build_display_name(config)
            current = await client.get_me()
            if current.first_name != target:
                try:
                    await client(functions.account.UpdateProfileRequest(first_name=target))
                    LOG.info("Display name updated: %s", target)
                except FloodWaitError as error:
                    LOG.warning("Telegram rate limit: waiting %ss", error.seconds)
                    try:
                        await asyncio.wait_for(stop.wait(), timeout=error.seconds)
                    except asyncio.TimeoutError:
                        pass
            if once:
                break
            try:
                await asyncio.wait_for(stop.wait(), timeout=interval)
            except asyncio.TimeoutError:
                pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Synchronize Telegram display name with current time")
    parser.add_argument("--config", type=Path, default=Path("/etc/telegram-name-timing-sync/config.json"))
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    asyncio.run(run(args.config, once=args.once, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
