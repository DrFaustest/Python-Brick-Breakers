import os
import pytest
import pygame as pg

@pytest.fixture(autouse=True, scope="session")
def pygame_setup() -> None:
    """Initialize pygame in headless mode for all tests."""
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pg.init()
    pg.display.set_mode((1, 1))
    yield
    pg.quit()

@pytest.fixture()
def screen() -> pg.Surface:
    """Provide a surface for rendering-dependent components."""
    return pg.Surface((800, 600))
