# Brick Breaker Game

## Overview
Brick Breaker is a modern Python-based game built with Pygame-CE, featuring dynamic moving bricks, multi-ball mechanics, and advanced collision detection. Break all bricks to progress through increasingly challenging levels.

## Key Features
- **Moving Bricks:** 15% of bricks move left/right, freezing when >50% of their row is filled. Destroying them spawns bonus balls.
- **Multi-Ball System:** Start with one ball; destroy moving bricks to earn additional balls. All balls bounce off each other with momentum preservation.
- **Advanced Collision Detection:** Row-based optimization for efficient brick collision checking with predictive collision handling.
- **Dynamic Physics:** Realistic ball physics with spin mechanics, angle variation on bounces, and anti-stuck detection.
- **Level Progression:** Procedurally generated levels with difficulty scaling (1-10) and 15 total bricks spawning per level.
- **Leaderboard:** High score tracking with persistent CSV storage (top 10 scores).
- **Settings & Customization:** Configurable difficulty, volume, ball/paddle/background images, and music playlist.
- **Windowed & Exe:** Play in-window or as a standalone .exe with bundled assets.

## Prerequisites
- **Python 3.11+** (tested on Python 3.14)
- **Pygame-CE 2.5.6** (Community Edition for modern Python support)

## Installation

### From Source
1. Clone the repository:
   ```bash
   git clone https://github.com/DrFaustest/Python-Brick-Breakers.git
   cd Python-Brick-Breakers
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   source venv/bin/activate     # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install pygame-ce==2.5.6
   ```

4. Run the game:
   ```bash
   python main.py
   ```

### From Executable
Download `dist/BrickBreaker.exe` and run it directly—all assets and dependencies are bundled.

## How to Play
- **Move Paddle:** Arrow keys (left/right) or mouse
- **Launch Ball:** Spacebar or left-click while ball is attached to paddle
- **Objective:** Break all bricks to advance to the next level
- **Game Over:** Lose all 3 lives (ball falls below paddle 3 times)

### Gameplay Tips
- Destroy **moving bricks** to spawn bonus balls for coverage
- Hit the paddle near the edges for sharper angles
- Use multiple balls to clear harder levels faster

## Testing

Run the test suite to verify game integrity:
```bash
.\venv\Scripts\python.exe -m pytest
```

Tests cover:
- Ball launch and paddle movement
- Level brick organization and collision-row optimization
- Brick collision/removal and scoring
- Ball-to-ball collision physics
- Anti-stuck safety at screen borders

## Building the Executable

To build a standalone one-file, windowed .exe (Windows only):

```bash
.\venv\Scripts\pip.exe install pyinstaller
.\venv\Scripts\python.exe -m PyInstaller --noconfirm --onefile --windowed --name BrickBreaker --clean ^
  --add-data "img;img" --add-data "sound;sound" --add-data "settings.json;." --add-data "high_score.csv;." main.py
```

Output: `dist/BrickBreaker.exe`

**Flags used:**
- `--onefile`: Single executable file (slower startup, portable)
- `--windowed`: No console window (cleaner user experience)
- `--add-data`: Bundles images, sounds, and config files

## Project Structure
```
Python-Brick-Breakers/
├── main.py                 # Entry point
├── game/                   # Game states (MainMenu, GamePlay, GameOver, SettingsMenu)
├── objects/                # Game entities (Ball, Paddle, Brick, MovingBrick)
├── levels/                 # Level generation and management
├── managers/               # Collision, input, and game reset logic
├── ui/                     # UI components (Scoreboard, Button, Slider, etc.)
├── utils/                  # Utilities (BackgroundMusic, ScoreSaver)
├── img/                    # Game assets (backgrounds, balls, paddles, bricks)
├── sound/                  # Background music (MIDI and MP3)
├── tests/                  # Test suite (pytest)
├── settings.py             # Singleton Settings class for configuration
├── settings.json           # User settings (auto-generated on first run)
├── high_score.csv          # Leaderboard data
└── requirements.txt        # Python dependencies
```

## Architecture
- **State Pattern:** Game uses a state machine (MainMenu → GamePlay → GameOver)
- **Singleton Settings:** All configuration centralized and persisted to JSON
- **Row-Based Optimization:** Bricks organized by row for O(1) collision lookup
- **Collision System:** Predictive detection with cooldowns prevents glitching

For detailed architecture and code patterns, see [.github/copilot-instructions.md](.github/copilot-instructions.md).

## Configuration
Edit `settings.json` to customize:
- `DIFFICULTY`: Game difficulty (1-10)
- `VOLUME`: Music volume (0.0-1.0)
- `BALL_IMAGES`, `PADDLE_IMAGES`, `BACKGROUND_IMAGES`: Asset selection
- `MUSIC_PLAYLIST`: Background music files
- `SCREEN_WIDTH`, `SCREEN_HEIGHT`: Window dimensions

## Known Issues
None. All core features tested and working.

## Future Enhancements
- Power-ups (slow motion, wider paddle, ball expansion)
- Particle effects and sound effects
- Difficulty modes (easy/normal/hard)
- Local multiplayer
- Mobile/touch support

## Contributing
Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push and open a pull request
5. Ensure all tests pass (`pytest`)

## License
This project is licensed under the [MIT License](LICENSE.md).

## Acknowledgments
- [Pygame-CE](https://github.com/pygame-ce/pygame-ce) for the excellent Community Edition
- Inspired by classic Breakout/Brick Breaker arcade games
- Built with Python 3.14 and modern development practices



