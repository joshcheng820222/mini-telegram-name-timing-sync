# Acceptance criteria

- Generate Telegram first names with configurable name/time order, timezone, time format, font and emoji.
- Default to `name_time`, so the person's name remains visually first.
- Never commit API credentials, Telegram sessions, runtime configuration or logs.
- Install into an isolated Python virtual environment and manage the process with systemd.
- Support install, update, status and uninstall without copying secrets into the repository.
- Pass unit tests, Python compilation, shell syntax checks and a sandbox installer test.
