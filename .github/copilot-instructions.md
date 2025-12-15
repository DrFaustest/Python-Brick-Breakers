# Brick Breaker Game - AI Agent Instructions

## Architecture Overview

This is a **state-based** Pygame application with a singleton settings system. The game uses a **Game → GameState → Components** hierarchy:

- **`Game`** ([game/game.py](../game/game.py)) - Main controller managing state transitions (MainMenu, GamePlay, SettingsMenu, GameOver)
- **`GameState`** ([game/game_state.py](../game/game_state.py)) - Abstract base class for all game states, providing shared access to screen, settings, and color constants
- **State implementations** inherit from `GameState` and implement `update(events)` and `draw()` methods

## Critical Patterns

### Singleton Settings System
**All configuration access MUST use the singleton `Settings` class** ([settings.py](../settings.py)):
```python
from settings import Settings
settings = Settings()
value = settings.get("KEY_NAME")  # Always use get()
settings.set("KEY_NAME", value)   # Persists to settings.json
```
- Settings auto-load from `settings.json` or fall back to defaults in `Settings.defaults`
- Never hardcode values that exist in settings (screen dimensions, colors, speeds, image paths, etc.)
- Add new settings to the `defaults` dict in Settings class

### Game State Pattern
State transitions use string identifiers via `Game.change_state()`:
```python
self.game.change_state("Playing")  # Creates new GamePlay instance
# Valid states: "Playing", "Settings", "GameOver", "MainMenu"
```

### Object Initialization Chain
GamePlay creates and wires all game objects in a specific dependency order:
1. Level → Bricks
2. Paddle
3. Ball (depends on Paddle)
4. UI components (Scoreboard, PlayerLives)
5. Managers (Collision, InputEvent, GameReset) - receive references to game objects

**When adding new game objects**, follow this pattern in [game/game_play.py](../game/game_play.py).

## Component Responsibilities

### Managers (`managers/`)
- **Collision** - Handles all collision detection (ball vs walls/paddle/bricks) and physics responses
- **InputEvent** - Processes keyboard/mouse input for paddle movement and ball launch
- **GameReset** - Resets game state between levels (creates new Level, Ball, updates UI)

### UI Components (`ui/`)
All UI elements are self-contained rendering classes:
- Draw methods take `screen` parameter
- Store their own position and size
- Examples: `Button`, `Scoreboard`, `PlayerLives`, `LevelBanner`

### Objects (`objects/`)
Game entities extending `pg.sprite.Sprite`:
- **Ball** - Tracks position, velocity, spin; has `attached_to_paddle` state
- **Paddle** - Player-controlled; Ball initializes attached to it
- **Brick** - Individual brick with `is_destroyed` flag

## Key Technical Details

### Ball Physics
- Ball uses `pg.math.Vector2` for position and velocity
- Spin mechanics: angular velocity decays with `angular_friction`, affects visual rotation
- Launch angle determined by paddle position: `(paddle_center_relative * 45) + 90` degrees

### Collision Detection
[managers/collision.py](../managers/collision.py) uses:
- `pg.sprite.collide_rect()` for paddle/brick detection
- Manual boundary checks for walls
- `paddle_hit` flag prevents multiple collisions per contact
- Reflection angle based on hit position: `offset * MAX_REFLECTION_ANGLE`

### Level System
[levels/level.py](../levels/level.py) generates procedural brick layouts:
- `generate_brick_map()` creates 2D grid based on `DIFFICULTY` setting
- Level completion checked via `all(brick.is_destroyed for brick in self.bricks)`
- Difficulty increases by 0.2 per level (capped at 10)

## Development Workflows

### Running the Game
```powershell
# Activate venv (already done based on terminal context)
python main.py
```
Virtual environment is in `venv/`. Only dependency: `pygame==2.5.2`

### Adding New UI Elements
1. Create class in `ui/` with `draw(screen)` method
2. Initialize in appropriate `GameState` subclass
3. Call `draw()` in state's `draw()` method
4. Add any images/assets to `img/` and register paths in `Settings.defaults`

### Adding Settings
1. Add to `Settings.defaults` dict with default value
2. Settings automatically persist to `settings.json` on `set()`
3. Use type hints: `Dict[str, Union[int, str, List[str], List[int]]]`

### Asset Management
All asset paths stored in Settings:
- Images: `BALL_IMG`, `PADDLE_IMG`, `BRICK_IMG`, `BACKGROUND_IMG`, etc.
- Sounds: `MUSIC_PLAYLIST` (MIDI and MP3 support)
- Lists for selection: `BACKGROUND_IMAGES`, `BALL_IMAGES`, `PADDLE_IMAGES`

## Common Patterns to Follow

### Type Hints
Always include full type hints on functions/methods:
```python
def create_brick(self, x_index: int, y_index: int) -> Brick:
```

### Docstrings
All classes, methods, and functions require docstrings with Args/Returns sections (see existing code).

### Color Access
Colors defined in Settings, accessed via base class:
```python
class MyState(GameState):
    def __init__(self, game):
        super().__init__(game)
        # self.WHITE, self.GREEN, self.BLACK, self.GRAY auto-available
```

### Event Handling
Events passed as list to `update()`, iterate and check types:
```python
def update(self, events: List[pg.event.Event]) -> None:
    for event in events:
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            # Handle space key
```

## File Organization Conventions
- One class per file (e.g., `ball.py` contains `Ball` class)
- `__init__.py` files present in all package directories but typically empty
- Settings file (`settings.json`) auto-created on first run if missing
- High scores stored in `high_score.csv` (format: name, score)

## Important Notes
- **Logo display** runs before game loop starts (see `LogoDisplay` in [main.py](../main.py))
- Background music managed by `BackgroundMusic` utility, playlist cycles on `pg.USEREVENT`
- FPS defaults to 240 (high for smooth ball physics)
- `GameReset` manager exists to handle level transitions without full state change
