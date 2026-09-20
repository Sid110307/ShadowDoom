# ShadowDoom

ShadowDoom is a terminal-based fantasy game written in Python. It combines a styled text interface with sound effects, randomized encounters, combat, treasure, and lightweight progression.

## Requirements

- Python 3.6 or newer
- Pygame
- Rich
- Tkinter

Tkinter is bundled with many Python installations, but some Linux distributions package it separately.

## Run locally

```sh
git clone https://github.com/Sid110307/ShadowDoom.git
cd ShadowDoom
python -m pip install pygame rich
python ShadowDoom.py
```

For the intended layout, run the game in a maximized terminal window. Audio output must be available for the bundled effects and music.

## Project structure

- `ShadowDoom.py` — game loop, encounters, combat, inventory, and menus
- `utils/tui.py` — terminal rendering helpers
- `utils/audio.py` — audio playback
- `audio/` — bundled sound effects and menu audio
