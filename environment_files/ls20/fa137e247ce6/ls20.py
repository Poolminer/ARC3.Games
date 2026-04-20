# MIT License
#
# Copyright (c) 2026 ARC Prize Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math
from typing import List, Tuple

import numpy as np
from arcengine import (
    ARCBaseGame,
    Camera,
    GameAction,
    Level,
    RenderableUserDisplay,
    Sprite,
)

"""
Notes on Level Data
StepCounter int - How much energy the player has. 20 for all levels, pickups restore to full
GoalShape int 0-5 - 0 L, 1 T, 2 U, 3 V, 4 W, 5 Z. Use multiple columns for multiple goals. Goal count is determined by goal tagged objects, there must be 1 column for every goal 
GoalColor int 0,10,8,12 - White, light blue, red, or orange. 1 column per goal
GoalRotation int 0 90 180 270 - degrees. 1 column per goal

Same as goal but only one column, sets what shape the player starts with on the bottom left UI display
StartShape
StartColor
StartRotation 

Fog True or False - Limits the player's vision to a small radius (does not currently scale with level size, see UIStepCounter)

Additional development notes:
Align 4x4 objects on the grid
Place a black Goal background down then a GoalShape on top in the bottom right, set the level data to setup a goal. The sprite will automatically be adjusted when the game starts
The player's preview shape will also automatically match the level data. Just leave a HeldShape sprite somewhere in the level (visible set to false) and it will get redrawn on the UI with the correct properties
"""

# Create sprites dictionary with all sprite definitions
sprites = {
    "Energy": Sprite(
        pixels=[
            [15, 15],
            [15, 15],
        ],
        name="Energy",
        visible=True,
        collidable=False,
        tags=["Energy"],
    ),
    "Goal": Sprite(
        pixels=[
            [5, 5, 5, 5],
            [5, 5, 5, 5],
            [5, 5, 5, 5],
            [5, 5, 5, 5],
        ],
        name="Goal",
        visible=True,
        collidable=False,
        tags=["Goal"],
        layer=-3,
    ),
    "GoalShape": Sprite(
        pixels=[
            [9, -1, -1],
            [-1, 0, -1],
            [-1, -1, 0],
        ],
        name="GoalShape",
        visible=True,
        collidable=True,
        tags=["GoalShape"],
    ),
    "HeldShape": Sprite(
        pixels=[
            [9, 0, -1],
            [-1, 0, -1],
            [-1, 0, 0],
        ],
        name="HeldShape",
        visible=False,
        collidable=True,
        tags=["HeldShape"],
        layer=1,
    ),
    "Obstacle": Sprite(
        pixels=[
            [4, 4, 4, 4],
            [4, 4, 4, 4],
            [4, 4, 4, 4],
            [4, 4, 4, 4],
        ],
        name="Obstacle",
        visible=True,
        collidable=True,
        tags=["Obstacle"],
        layer=-1,
    ),
    "Player": Sprite(
        pixels=[
            [12, 12, 12, 12],
            [9, 9, 9, 9],
            [9, 9, 9, 9],
            [9, 9, 9, 9],
        ],
        name="Player",
        visible=True,
        collidable=True,
        tags=["Player"],
        layer=1,
    ),
    "Recolor": Sprite(
        pixels=[
            [0, 10, 8, 12],
            [10, 10, 8, 12],
            [8, 8, 8, 12],
            [12, 12, 12, 12],
        ],
        name="Recolor",
        visible=True,
        collidable=False,
        tags=["Recolor"],
    ),
    "red-overlay": Sprite(
        pixels=[
            [8],
        ],
        name="red-overlay",
        visible=True,
        collidable=True,
    ),
    "Rotate": Sprite(
        pixels=[
            [-1, 0, -1],
            [1, 0, 0],
            [-1, 1, -1],
        ],
        name="Rotate",
        visible=True,
        collidable=True,
        tags=["Rotate"],
    ),
    "ShapeCorner": Sprite(
        pixels=[
            [9, -1, -1],
            [-1, 0, 0],
            [-1, 0, -1],
        ],
        name="ShapeCorner",
        visible=True,
        collidable=False,
        tags=["Shifter"],
    ),
    "ShapeL": Sprite(
        pixels=[
            [9, 0, -1],
            [-1, 0, -1],
            [-1, 0, 0],
        ],
        name="ShapeL",
        visible=True,
        collidable=True,
        layer=1,
    ),
    "ShapeT": Sprite(
        pixels=[
            [9, -1, -1],
            [-1, 0, -1],
            [0, 0, 0],
        ],
        name="ShapeT",
        visible=True,
        collidable=True,
    ),
    "ShapeU": Sprite(
        pixels=[
            [9, -1, -1],
            [0, -1, 0],
            [0, 0, 0],
        ],
        name="ShapeU",
        visible=True,
        collidable=True,
    ),
    "ShapeV": Sprite(
        pixels=[
            [9, 0, -1],
            [0, 0, 0],
            [0, -1, 0],
        ],
        name="ShapeV",
        visible=True,
        collidable=True,
    ),
    "ShapeW": Sprite(
        pixels=[
            [9, -1, 0],
            [-1, 0, 0],
            [0, 0, -1],
        ],
        name="ShapeW",
        visible=True,
        collidable=True,
    ),
    "ShapeZ": Sprite(
        pixels=[
            [9, -1, 0],
            [-1, 0, 0],
            [-1, 0, -1],
        ],
        name="ShapeZ",
        visible=True,
        collidable=False,
        layer=-2,
    ),
}


# Create levels array with all level definitions
levels = [
    # Level 1
    Level(
        sprites=[
            sprites["Goal"].clone().set_position(16, 8),
            sprites["GoalShape"].clone().set_position(17, 9),
            sprites["HeldShape"].clone().set_position(0, 23).set_scale(3),
            sprites["Obstacle"].clone().set_position(0, 28),
            sprites["Obstacle"].clone().set_position(4, 28),
            sprites["Obstacle"].clone().set_position(8, 28),
            sprites["Obstacle"].clone().set_position(8, 24),
            sprites["Obstacle"].clone().set_position(4, 24),
            sprites["Obstacle"].clone().set_position(0, 24),
            sprites["Obstacle"].clone().set_position(0, 20),
            sprites["Obstacle"].clone().set_position(0, 16),
            sprites["Obstacle"].clone().set_position(0, 12),
            sprites["Obstacle"].clone().set_position(0, 8),
            sprites["Obstacle"].clone().set_position(0, 4),
            sprites["Obstacle"].clone(),
            sprites["Obstacle"].clone().set_position(4, 0),
            sprites["Obstacle"].clone().set_position(8, 0),
            sprites["Obstacle"].clone().set_position(12, 0),
            sprites["Obstacle"].clone().set_position(16, 0),
            sprites["Obstacle"].clone().set_position(20, 0),
            sprites["Obstacle"].clone().set_position(24, 0),
            sprites["Obstacle"].clone().set_position(28, 0),
            sprites["Obstacle"].clone().set_position(28, 4),
            sprites["Obstacle"].clone().set_position(28, 8),
            sprites["Obstacle"].clone().set_position(28, 12),
            sprites["Obstacle"].clone().set_position(28, 16),
            sprites["Obstacle"].clone().set_position(28, 20),
            sprites["Obstacle"].clone().set_position(28, 24),
            sprites["Obstacle"].clone().set_position(28, 28),
            sprites["Obstacle"].clone().set_position(24, 28),
            sprites["Obstacle"].clone().set_position(20, 28),
            sprites["Obstacle"].clone().set_position(16, 28),
            sprites["Obstacle"].clone().set_position(12, 28),
            sprites["Obstacle"].clone().set_position(4, 20),
            sprites["Obstacle"].clone().set_position(8, 12),
            sprites["Obstacle"].clone().set_position(8, 8),
            sprites["Obstacle"].clone().set_position(12, 24),
            sprites["Obstacle"].clone().set_position(24, 4),
            sprites["Player"].clone().set_position(20, 24),
            sprites["ShapeCorner"].clone().set_position(16, 16),
        ],
        grid_size=(32, 32),
        data={
            "StepCounter": 22,
            "GoalShape": 1,
            "GoalColor": 0,
            "GoalRotation": 0,
            "StartShape": 0,
            "StartColor": 0,
            "StartRotation": 0,
            "Fog": False,
        },
    ),
    # Level 2
    Level(
        sprites=[
            sprites["Energy"].clone().set_position(5, 5),
            sprites["Goal"].clone().set_position(4, 20),
            sprites["GoalShape"].clone().set_position(5, 21),
            sprites["HeldShape"].clone().set_position(0, 23).set_scale(3),
            sprites["Obstacle"].clone().set_position(0, 28),
            sprites["Obstacle"].clone().set_position(4, 28),
            sprites["Obstacle"].clone().set_position(8, 28),
            sprites["Obstacle"].clone().set_position(8, 24),
            sprites["Obstacle"].clone().set_position(4, 24),
            sprites["Obstacle"].clone().set_position(0, 24),
            sprites["Obstacle"].clone().set_position(0, 20),
            sprites["Obstacle"].clone().set_position(0, 16),
            sprites["Obstacle"].clone().set_position(0, 12),
            sprites["Obstacle"].clone().set_position(0, 8),
            sprites["Obstacle"].clone().set_position(0, 4),
            sprites["Obstacle"].clone(),
            sprites["Obstacle"].clone().set_position(4, 0),
            sprites["Obstacle"].clone().set_position(8, 0),
            sprites["Obstacle"].clone().set_position(12, 0),
            sprites["Obstacle"].clone().set_position(16, 0),
            sprites["Obstacle"].clone().set_position(20, 0),
            sprites["Obstacle"].clone().set_position(24, 0),
            sprites["Obstacle"].clone().set_position(28, 0),
            sprites["Obstacle"].clone().set_position(28, 4),
            sprites["Obstacle"].clone().set_position(28, 8),
            sprites["Obstacle"].clone().set_position(28, 12),
            sprites["Obstacle"].clone().set_position(28, 16),
            sprites["Obstacle"].clone().set_position(28, 20),
            sprites["Obstacle"].clone().set_position(28, 24),
            sprites["Obstacle"].clone().set_position(28, 28),
            sprites["Obstacle"].clone().set_position(24, 28),
            sprites["Obstacle"].clone().set_position(20, 28),
            sprites["Obstacle"].clone().set_position(16, 28),
            sprites["Obstacle"].clone().set_position(12, 28),
            sprites["Obstacle"].clone().set_position(12, 16),
            sprites["Obstacle"].clone().set_position(24, 4),
            sprites["Obstacle"].clone().set_position(8, 20),
            sprites["Obstacle"].clone().set_position(16, 20),
            sprites["Obstacle"].clone().set_position(16, 16),
            sprites["Obstacle"].clone().set_position(20, 16),
            sprites["Obstacle"].clone().set_position(12, 12),
            sprites["Obstacle"].clone().set_position(20, 12),
            sprites["Obstacle"].clone().set_position(8, 16),
            sprites["Player"].clone().set_position(12, 20),
            sprites["ShapeCorner"].clone().set_position(16, 12),
        ],
        grid_size=(32, 32),
        data={
            "StepCounter": 22,
            "GoalShape": 2,
            "GoalColor": 0,
            "GoalRotation": 0,
            "StartShape": 4,
            "StartColor": 0,
            "StartRotation": 0,
            "Fog": False,
        },
    ),
    # Level 3
    Level(
        sprites=[
            sprites["Energy"].clone().set_position(9, 9),
            sprites["Energy"].clone().set_position(57, 5),
            sprites["Energy"].clone().set_position(29, 29),
            sprites["Energy"].clone().set_position(9, 49),
            sprites["Energy"].clone().set_position(37, 53),
            sprites["Energy"].clone().set_position(5, 21),
            sprites["Goal"].clone().set_position(28, 4),
            sprites["GoalShape"].clone().set_position(29, 5),
            sprites["HeldShape"].clone().set_position(1, 54).set_scale(3),
            sprites["Obstacle"].clone(),
            sprites["Obstacle"].clone().set_position(4, 0),
            sprites["Obstacle"].clone().set_position(8, 0),
            sprites["Obstacle"].clone().set_position(12, 0),
            sprites["Obstacle"].clone().set_position(16, 0),
            sprites["Obstacle"].clone().set_position(20, 0),
            sprites["Obstacle"].clone().set_position(24, 0),
            sprites["Obstacle"].clone().set_position(28, 0),
            sprites["Obstacle"].clone().set_position(32, 0),
            sprites["Obstacle"].clone().set_position(36, 0),
            sprites["Obstacle"].clone().set_position(40, 0),
            sprites["Obstacle"].clone().set_position(44, 0),
            sprites["Obstacle"].clone().set_position(48, 0),
            sprites["Obstacle"].clone().set_position(52, 0),
            sprites["Obstacle"].clone().set_position(56, 0),
            sprites["Obstacle"].clone().set_position(60, 0),
            sprites["Obstacle"].clone().set_position(60, 4),
            sprites["Obstacle"].clone().set_position(60, 8),
            sprites["Obstacle"].clone().set_position(60, 12),
            sprites["Obstacle"].clone().set_position(60, 16),
            sprites["Obstacle"].clone().set_position(60, 20),
            sprites["Obstacle"].clone().set_position(60, 24),
            sprites["Obstacle"].clone().set_position(60, 28),
            sprites["Obstacle"].clone().set_position(60, 32),
            sprites["Obstacle"].clone().set_position(60, 36),
            sprites["Obstacle"].clone().set_position(60, 40),
            sprites["Obstacle"].clone().set_position(60, 44),
            sprites["Obstacle"].clone().set_position(60, 48),
            sprites["Obstacle"].clone().set_position(60, 52),
            sprites["Obstacle"].clone().set_position(60, 56),
            sprites["Obstacle"].clone().set_position(60, 60),
            sprites["Obstacle"].clone().set_position(0, 60),
            sprites["Obstacle"].clone().set_position(4, 60),
            sprites["Obstacle"].clone().set_position(8, 60),
            sprites["Obstacle"].clone().set_position(12, 60),
            sprites["Obstacle"].clone().set_position(16, 60),
            sprites["Obstacle"].clone().set_position(20, 60),
            sprites["Obstacle"].clone().set_position(24, 60),
            sprites["Obstacle"].clone().set_position(28, 60),
            sprites["Obstacle"].clone().set_position(32, 60),
            sprites["Obstacle"].clone().set_position(36, 60),
            sprites["Obstacle"].clone().set_position(40, 60),
            sprites["Obstacle"].clone().set_position(44, 60),
            sprites["Obstacle"].clone().set_position(48, 60),
            sprites["Obstacle"].clone().set_position(52, 60),
            sprites["Obstacle"].clone().set_position(56, 60),
            sprites["Obstacle"].clone().set_position(0, 4),
            sprites["Obstacle"].clone().set_position(0, 8),
            sprites["Obstacle"].clone().set_position(0, 12),
            sprites["Obstacle"].clone().set_position(0, 16),
            sprites["Obstacle"].clone().set_position(0, 20),
            sprites["Obstacle"].clone().set_position(0, 24),
            sprites["Obstacle"].clone().set_position(0, 28),
            sprites["Obstacle"].clone().set_position(0, 32),
            sprites["Obstacle"].clone().set_position(0, 36),
            sprites["Obstacle"].clone().set_position(0, 40),
            sprites["Obstacle"].clone().set_position(0, 44),
            sprites["Obstacle"].clone().set_position(0, 48),
            sprites["Obstacle"].clone().set_position(0, 52),
            sprites["Obstacle"].clone().set_position(0, 56),
            sprites["Obstacle"].clone().set_position(0, 60),
            sprites["Obstacle"].clone().set_position(52, 4),
            sprites["Obstacle"].clone().set_position(48, 4),
            sprites["Obstacle"].clone().set_position(48, 8),
            sprites["Obstacle"].clone().set_position(44, 4),
            sprites["Obstacle"].clone().set_position(44, 8),
            sprites["Obstacle"].clone().set_position(48, 16),
            sprites["Obstacle"].clone().set_position(52, 16),
            sprites["Obstacle"].clone().set_position(52, 32),
            sprites["Obstacle"].clone().set_position(44, 20),
            sprites["Obstacle"].clone().set_position(48, 32),
            sprites["Obstacle"].clone().set_position(44, 32),
            sprites["Obstacle"].clone().set_position(40, 28),
            sprites["Obstacle"].clone().set_position(40, 24),
            sprites["Obstacle"].clone().set_position(36, 24),
            sprites["Obstacle"].clone().set_position(36, 20),
            sprites["Obstacle"].clone().set_position(32, 20),
            sprites["Obstacle"].clone().set_position(32, 16),
            sprites["Obstacle"].clone().set_position(32, 12),
            sprites["Obstacle"].clone().set_position(32, 4),
            sprites["Obstacle"].clone().set_position(32, 8),
            sprites["Obstacle"].clone().set_position(4, 8),
            sprites["Obstacle"].clone().set_position(4, 4),
            sprites["Obstacle"].clone().set_position(8, 4),
            sprites["Obstacle"].clone().set_position(12, 4),
            sprites["Obstacle"].clone().set_position(4, 12),
            sprites["Obstacle"].clone().set_position(4, 16),
            sprites["Obstacle"].clone().set_position(8, 56),
            sprites["Obstacle"].clone().set_position(20, 56),
            sprites["Obstacle"].clone().set_position(20, 52),
            sprites["Obstacle"].clone().set_position(20, 48),
            sprites["Obstacle"].clone().set_position(20, 44),
            sprites["Obstacle"].clone().set_position(16, 48),
            sprites["Obstacle"].clone().set_position(8, 44),
            sprites["Obstacle"].clone().set_position(8, 40),
            sprites["Obstacle"].clone().set_position(8, 36),
            sprites["Obstacle"].clone().set_position(12, 36),
            sprites["Obstacle"].clone().set_position(12, 44),
            sprites["Obstacle"].clone().set_position(12, 40),
            sprites["Obstacle"].clone().set_position(16, 44),
            sprites["Obstacle"].clone().set_position(32, 56),
            sprites["Obstacle"].clone().set_position(40, 52),
            sprites["Obstacle"].clone().set_position(44, 52),
            sprites["Obstacle"].clone().set_position(48, 48),
            sprites["Obstacle"].clone().set_position(44, 48),
            sprites["Obstacle"].clone().set_position(52, 48),
            sprites["Obstacle"].clone().set_position(52, 52),
            sprites["Obstacle"].clone().set_position(56, 52),
            sprites["Obstacle"].clone().set_position(56, 56),
            sprites["Obstacle"].clone().set_position(56, 48),
            sprites["Obstacle"].clone().set_position(48, 44),
            sprites["Obstacle"].clone().set_position(48, 40),
            sprites["Obstacle"].clone().set_position(48, 36),
            sprites["Obstacle"].clone().set_position(52, 36),
            sprites["Obstacle"].clone().set_position(44, 44),
            sprites["Obstacle"].clone().set_position(32, 36),
            sprites["Obstacle"].clone().set_position(28, 40),
            sprites["Obstacle"].clone().set_position(28, 36),
            sprites["Obstacle"].clone().set_position(28, 32),
            sprites["Obstacle"].clone().set_position(24, 32),
            sprites["Obstacle"].clone().set_position(24, 36),
            sprites["Obstacle"].clone().set_position(20, 32),
            sprites["Obstacle"].clone().set_position(4, 56),
            sprites["Obstacle"].clone().set_position(4, 52),
            sprites["Obstacle"].clone().set_position(8, 52),
            sprites["Player"].clone().set_position(24, 56),
            sprites["Recolor"].clone().set_position(36, 44),
            sprites["ShapeCorner"].clone().set_position(13, 33),
        ],
        grid_size=(64, 64),
        data={
            "StepCounter": 22,
            "GoalShape": 5,
            "GoalColor": 12,
            "GoalRotation": 0,
            "StartShape": 0,
            "StartColor": 0,
            "StartRotation": 0,
            "Fog": False,
        },
    ),
    # Level 4
    Level(
        sprites=[
            sprites["Energy"].clone().set_position(53, 53),
            sprites["Energy"].clone().set_position(13, 57),
            sprites["Energy"].clone().set_position(57, 29),
            sprites["Energy"].clone().set_position(37, 9),
            sprites["Energy"].clone().set_position(13, 21),
            sprites["Goal"].clone().set_position(48, 12),
            sprites["GoalShape"].clone().set_position(49, 13),
            sprites["HeldShape"].clone().set_position(1, 54).set_scale(3),
            sprites["Obstacle"].clone(),
            sprites["Obstacle"].clone().set_position(4, 0),
            sprites["Obstacle"].clone().set_position(8, 0),
            sprites["Obstacle"].clone().set_position(12, 0),
            sprites["Obstacle"].clone().set_position(16, 0),
            sprites["Obstacle"].clone().set_position(20, 0),
            sprites["Obstacle"].clone().set_position(24, 0),
            sprites["Obstacle"].clone().set_position(28, 0),
            sprites["Obstacle"].clone().set_position(32, 0),
            sprites["Obstacle"].clone().set_position(36, 0),
            sprites["Obstacle"].clone().set_position(40, 0),
            sprites["Obstacle"].clone().set_position(44, 0),
            sprites["Obstacle"].clone().set_position(48, 0),
            sprites["Obstacle"].clone().set_position(52, 0),
            sprites["Obstacle"].clone().set_position(56, 0),
            sprites["Obstacle"].clone().set_position(60, 0),
            sprites["Obstacle"].clone().set_position(0, 4),
            sprites["Obstacle"].clone().set_position(32, 4),
            sprites["Obstacle"].clone().set_position(36, 4),
            sprites["Obstacle"].clone().set_position(40, 4),
            sprites["Obstacle"].clone().set_position(60, 4),
            sprites["Obstacle"].clone().set_position(0, 8),
            sprites["Obstacle"].clone().set_position(60, 8),
            sprites["Obstacle"].clone().set_position(0, 12),
            sprites["Obstacle"].clone().set_position(20, 12),
            sprites["Obstacle"].clone().set_position(56, 12),
            sprites["Obstacle"].clone().set_position(60, 12),
            sprites["Obstacle"].clone().set_position(0, 16),
            sprites["Obstacle"].clone().set_position(4, 16),
            sprites["Obstacle"].clone().set_position(20, 16),
            sprites["Obstacle"].clone().set_position(24, 16),
            sprites["Obstacle"].clone().set_position(28, 16),
            sprites["Obstacle"].clone().set_position(52, 16),
            sprites["Obstacle"].clone().set_position(56, 16),
            sprites["Obstacle"].clone().set_position(60, 16),
            sprites["Obstacle"].clone().set_position(0, 20),
            sprites["Obstacle"].clone().set_position(4, 20),
            sprites["Obstacle"].clone().set_position(8, 20),
            sprites["Obstacle"].clone().set_position(28, 20),
            sprites["Obstacle"].clone().set_position(52, 20),
            sprites["Obstacle"].clone().set_position(56, 20),
            sprites["Obstacle"].clone().set_position(60, 20),
            sprites["Obstacle"].clone().set_position(0, 24),
            sprites["Obstacle"].clone().set_position(8, 24),
            sprites["Obstacle"].clone().set_position(12, 24),
            sprites["Obstacle"].clone().set_position(24, 24),
            sprites["Obstacle"].clone().set_position(28, 24),
            sprites["Obstacle"].clone().set_position(32, 24),
            sprites["Obstacle"].clone().set_position(36, 24),
            sprites["Obstacle"].clone().set_position(60, 24),
            sprites["Obstacle"].clone().set_position(0, 28),
            sprites["Obstacle"].clone().set_position(12, 28),
            sprites["Obstacle"].clone().set_position(16, 28),
            sprites["Obstacle"].clone().set_position(20, 28),
            sprites["Obstacle"].clone().set_position(24, 28),
            sprites["Obstacle"].clone().set_position(48, 28),
            sprites["Obstacle"].clone().set_position(52, 28),
            sprites["Obstacle"].clone().set_position(60, 28),
            sprites["Obstacle"].clone().set_position(0, 32),
            sprites["Obstacle"].clone().set_position(16, 32),
            sprites["Obstacle"].clone().set_position(20, 32),
            sprites["Obstacle"].clone().set_position(24, 32),
            sprites["Obstacle"].clone().set_position(48, 32),
            sprites["Obstacle"].clone().set_position(60, 32),
            sprites["Obstacle"].clone().set_position(0, 36),
            sprites["Obstacle"].clone().set_position(4, 36),
            sprites["Obstacle"].clone().set_position(24, 36),
            sprites["Obstacle"].clone().set_position(28, 36),
            sprites["Obstacle"].clone().set_position(32, 36),
            sprites["Obstacle"].clone().set_position(36, 36),
            sprites["Obstacle"].clone().set_position(60, 36),
            sprites["Obstacle"].clone().set_position(0, 40),
            sprites["Obstacle"].clone().set_position(60, 40),
            sprites["Obstacle"].clone().set_position(0, 44),
            sprites["Obstacle"].clone().set_position(20, 44),
            sprites["Obstacle"].clone().set_position(44, 44),
            sprites["Obstacle"].clone().set_position(48, 44),
            sprites["Obstacle"].clone().set_position(60, 44),
            sprites["Obstacle"].clone().set_position(0, 48),
            sprites["Obstacle"].clone().set_position(20, 48),
            sprites["Obstacle"].clone().set_position(24, 48),
            sprites["Obstacle"].clone().set_position(28, 48),
            sprites["Obstacle"].clone().set_position(40, 48),
            sprites["Obstacle"].clone().set_position(44, 48),
            sprites["Obstacle"].clone().set_position(60, 48),
            sprites["Obstacle"].clone().set_position(0, 52),
            sprites["Obstacle"].clone().set_position(4, 52),
            sprites["Obstacle"].clone().set_position(8, 52),
            sprites["Obstacle"].clone().set_position(20, 52),
            sprites["Obstacle"].clone().set_position(24, 52),
            sprites["Obstacle"].clone().set_position(40, 52),
            sprites["Obstacle"].clone().set_position(44, 52),
            sprites["Obstacle"].clone().set_position(60, 52),
            sprites["Obstacle"].clone().set_position(0, 56),
            sprites["Obstacle"].clone().set_position(4, 56),
            sprites["Obstacle"].clone().set_position(8, 56),
            sprites["Obstacle"].clone().set_position(20, 56),
            sprites["Obstacle"].clone().set_position(24, 56),
            sprites["Obstacle"].clone().set_position(40, 56),
            sprites["Obstacle"].clone().set_position(60, 56),
            sprites["Obstacle"].clone().set_position(0, 60),
            sprites["Obstacle"].clone().set_position(4, 60),
            sprites["Obstacle"].clone().set_position(8, 60),
            sprites["Obstacle"].clone().set_position(12, 60),
            sprites["Obstacle"].clone().set_position(16, 60),
            sprites["Obstacle"].clone().set_position(20, 60),
            sprites["Obstacle"].clone().set_position(24, 60),
            sprites["Obstacle"].clone().set_position(28, 60),
            sprites["Obstacle"].clone().set_position(32, 60),
            sprites["Obstacle"].clone().set_position(36, 60),
            sprites["Obstacle"].clone().set_position(40, 60),
            sprites["Obstacle"].clone().set_position(44, 60),
            sprites["Obstacle"].clone().set_position(48, 60),
            sprites["Obstacle"].clone().set_position(52, 60),
            sprites["Obstacle"].clone().set_position(56, 60),
            sprites["Obstacle"].clone().set_position(60, 60),
            sprites["Obstacle"].clone().set_position(56, 56),
            sprites["Obstacle"].clone().set_position(52, 56),
            sprites["Obstacle"].clone().set_position(56, 52),
            sprites["Player"].clone().set_position(32, 52),
            sprites["Recolor"].clone().set_position(28, 40),
            sprites["Rotate"].clone().set_position(8, 8),
            sprites["ShapeCorner"].clone().set_position(52, 40),
        ],
        grid_size=(64, 64),
        data={
            "StepCounter": 22,
            "GoalShape": 5,
            "GoalColor": 10,
            "GoalRotation": 270,
            "StartShape": 0,
            "StartColor": 0,
            "StartRotation": 0,
            "Fog": False,
        },
    ),
    # Level 5
    Level(
        sprites=[
            sprites["Energy"].clone().set_position(5, 45),
            sprites["Energy"].clone().set_position(29, 25),
            sprites["Energy"].clone().set_position(49, 13),
            sprites["Energy"].clone().set_position(57, 33),
            sprites["Energy"].clone().set_position(29, 49),
            sprites["Goal"].clone().set_position(32, 12),
            sprites["GoalShape"].clone().set_position(33, 13),
            sprites["HeldShape"].clone().set_position(1, 54).set_scale(3),
            sprites["Obstacle"].clone(),
            sprites["Obstacle"].clone().set_position(4, 0),
            sprites["Obstacle"].clone().set_position(8, 0),
            sprites["Obstacle"].clone().set_position(12, 0),
            sprites["Obstacle"].clone().set_position(16, 0),
            sprites["Obstacle"].clone().set_position(20, 0),
            sprites["Obstacle"].clone().set_position(24, 0),
            sprites["Obstacle"].clone().set_position(28, 0),
            sprites["Obstacle"].clone().set_position(32, 0),
            sprites["Obstacle"].clone().set_position(36, 0),
            sprites["Obstacle"].clone().set_position(40, 0),
            sprites["Obstacle"].clone().set_position(44, 0),
            sprites["Obstacle"].clone().set_position(48, 0),
            sprites["Obstacle"].clone().set_position(52, 0),
            sprites["Obstacle"].clone().set_position(56, 0),
            sprites["Obstacle"].clone().set_position(60, 0),
            sprites["Obstacle"].clone().set_position(0, 4),
            sprites["Obstacle"].clone().set_position(8, 4),
            sprites["Obstacle"].clone().set_position(12, 4),
            sprites["Obstacle"].clone().set_position(48, 4),
            sprites["Obstacle"].clone().set_position(52, 4),
            sprites["Obstacle"].clone().set_position(56, 4),
            sprites["Obstacle"].clone().set_position(60, 4),
            sprites["Obstacle"].clone().set_position(0, 8),
            sprites["Obstacle"].clone().set_position(4, 8),
            sprites["Obstacle"].clone().set_position(8, 8),
            sprites["Obstacle"].clone().set_position(12, 8),
            sprites["Obstacle"].clone().set_position(16, 8),
            sprites["Obstacle"].clone().set_position(20, 8),
            sprites["Obstacle"].clone().set_position(40, 8),
            sprites["Obstacle"].clone().set_position(60, 8),
            sprites["Obstacle"].clone().set_position(0, 12),
            sprites["Obstacle"].clone().set_position(8, 12),
            sprites["Obstacle"].clone().set_position(20, 12),
            sprites["Obstacle"].clone().set_position(24, 12),
            sprites["Obstacle"].clone().set_position(40, 12),
            sprites["Obstacle"].clone().set_position(44, 12),
            sprites["Obstacle"].clone().set_position(60, 12),
            sprites["Obstacle"].clone().set_position(0, 16),
            sprites["Obstacle"].clone().set_position(24, 16),
            sprites["Obstacle"].clone().set_position(56, 16),
            sprites["Obstacle"].clone().set_position(60, 16),
            sprites["Obstacle"].clone().set_position(0, 20),
            sprites["Obstacle"].clone().set_position(24, 20),
            sprites["Obstacle"].clone().set_position(60, 20),
            sprites["Obstacle"].clone().set_position(0, 24),
            sprites["Obstacle"].clone().set_position(4, 24),
            sprites["Obstacle"].clone().set_position(8, 24),
            sprites["Obstacle"].clone().set_position(12, 24),
            sprites["Obstacle"].clone().set_position(24, 24),
            sprites["Obstacle"].clone().set_position(36, 24),
            sprites["Obstacle"].clone().set_position(60, 24),
            sprites["Obstacle"].clone().set_position(0, 28),
            sprites["Obstacle"].clone().set_position(4, 28),
            sprites["Obstacle"].clone().set_position(8, 28),
            sprites["Obstacle"].clone().set_position(12, 28),
            sprites["Obstacle"].clone().set_position(16, 28),
            sprites["Obstacle"].clone().set_position(20, 28),
            sprites["Obstacle"].clone().set_position(24, 28),
            sprites["Obstacle"].clone().set_position(60, 28),
            sprites["Obstacle"].clone().set_position(0, 32),
            sprites["Obstacle"].clone().set_position(4, 32),
            sprites["Obstacle"].clone().set_position(8, 32),
            sprites["Obstacle"].clone().set_position(12, 32),
            sprites["Obstacle"].clone().set_position(20, 32),
            sprites["Obstacle"].clone().set_position(24, 32),
            sprites["Obstacle"].clone().set_position(60, 32),
            sprites["Obstacle"].clone().set_position(0, 36),
            sprites["Obstacle"].clone().set_position(8, 36),
            sprites["Obstacle"].clone().set_position(12, 36),
            sprites["Obstacle"].clone().set_position(36, 36),
            sprites["Obstacle"].clone().set_position(40, 36),
            sprites["Obstacle"].clone().set_position(44, 36),
            sprites["Obstacle"].clone().set_position(48, 36),
            sprites["Obstacle"].clone().set_position(60, 36),
            sprites["Obstacle"].clone().set_position(0, 40),
            sprites["Obstacle"].clone().set_position(60, 40),
            sprites["Obstacle"].clone().set_position(0, 44),
            sprites["Obstacle"].clone().set_position(8, 44),
            sprites["Obstacle"].clone().set_position(12, 44),
            sprites["Obstacle"].clone().set_position(60, 44),
            sprites["Obstacle"].clone().set_position(0, 48),
            sprites["Obstacle"].clone().set_position(4, 48),
            sprites["Obstacle"].clone().set_position(8, 48),
            sprites["Obstacle"].clone().set_position(24, 48),
            sprites["Obstacle"].clone().set_position(32, 48),
            sprites["Obstacle"].clone().set_position(36, 48),
            sprites["Obstacle"].clone().set_position(48, 48),
            sprites["Obstacle"].clone().set_position(60, 48),
            sprites["Obstacle"].clone().set_position(0, 52),
            sprites["Obstacle"].clone().set_position(4, 52),
            sprites["Obstacle"].clone().set_position(8, 52),
            sprites["Obstacle"].clone().set_position(32, 52),
            sprites["Obstacle"].clone().set_position(36, 52),
            sprites["Obstacle"].clone().set_position(60, 52),
            sprites["Obstacle"].clone().set_position(0, 56),
            sprites["Obstacle"].clone().set_position(4, 56),
            sprites["Obstacle"].clone().set_position(8, 56),
            sprites["Obstacle"].clone().set_position(12, 56),
            sprites["Obstacle"].clone().set_position(32, 56),
            sprites["Obstacle"].clone().set_position(60, 56),
            sprites["Obstacle"].clone().set_position(0, 60),
            sprites["Obstacle"].clone().set_position(4, 60),
            sprites["Obstacle"].clone().set_position(8, 60),
            sprites["Obstacle"].clone().set_position(12, 60),
            sprites["Obstacle"].clone().set_position(16, 60),
            sprites["Obstacle"].clone().set_position(20, 60),
            sprites["Obstacle"].clone().set_position(24, 60),
            sprites["Obstacle"].clone().set_position(28, 60),
            sprites["Obstacle"].clone().set_position(32, 60),
            sprites["Obstacle"].clone().set_position(36, 60),
            sprites["Obstacle"].clone().set_position(40, 60),
            sprites["Obstacle"].clone().set_position(44, 60),
            sprites["Obstacle"].clone().set_position(48, 60),
            sprites["Obstacle"].clone().set_position(52, 60),
            sprites["Obstacle"].clone().set_position(56, 60),
            sprites["Obstacle"].clone().set_position(60, 60),
            sprites["Player"].clone().set_position(48, 20),
            sprites["Recolor"].clone().set_position(48, 28),
            sprites["Rotate"].clone().set_position(24, 40),
            sprites["ShapeCorner"].clone().set_position(20, 40),
        ],
        grid_size=(64, 64),
        data={
            "StepCounter": 22,
            "GoalShape": 2,
            "GoalColor": 12,
            "GoalRotation": 0,
            "StartShape": 0,
            "StartColor": 0,
            "StartRotation": 0,
            "Fog": False,
        },
    ),
    # Level 6
    Level(
        sprites=[
            sprites["Energy"].clone().set_position(57, 5),
            sprites["Energy"].clone().set_position(29, 9),
            sprites["Energy"].clone().set_position(41, 25),
            sprites["Energy"].clone().set_position(13, 29),
            sprites["Energy"].clone().set_position(53, 45),
            sprites["Goal"].clone().set_position(28, 52),
            sprites["GoalShape"].clone().set_position(29, 53),
            sprites["HeldShape"].clone().set_position(1, 54).set_scale(3),
            sprites["Obstacle"].clone(),
            sprites["Obstacle"].clone().set_position(4, 0),
            sprites["Obstacle"].clone().set_position(8, 0),
            sprites["Obstacle"].clone().set_position(12, 0),
            sprites["Obstacle"].clone().set_position(16, 0),
            sprites["Obstacle"].clone().set_position(20, 0),
            sprites["Obstacle"].clone().set_position(24, 0),
            sprites["Obstacle"].clone().set_position(28, 0),
            sprites["Obstacle"].clone().set_position(32, 0),
            sprites["Obstacle"].clone().set_position(36, 0),
            sprites["Obstacle"].clone().set_position(40, 0),
            sprites["Obstacle"].clone().set_position(44, 0),
            sprites["Obstacle"].clone().set_position(48, 0),
            sprites["Obstacle"].clone().set_position(52, 0),
            sprites["Obstacle"].clone().set_position(56, 0),
            sprites["Obstacle"].clone().set_position(60, 0),
            sprites["Obstacle"].clone().set_position(0, 4),
            sprites["Obstacle"].clone().set_position(8, 4),
            sprites["Obstacle"].clone().set_position(24, 4),
            sprites["Obstacle"].clone().set_position(36, 4),
            sprites["Obstacle"].clone().set_position(60, 4),
            sprites["Obstacle"].clone().set_position(0, 8),
            sprites["Obstacle"].clone().set_position(44, 8),
            sprites["Obstacle"].clone().set_position(48, 8),
            sprites["Obstacle"].clone().set_position(56, 8),
            sprites["Obstacle"].clone().set_position(60, 8),
            sprites["Obstacle"].clone().set_position(0, 12),
            sprites["Obstacle"].clone().set_position(48, 12),
            sprites["Obstacle"].clone().set_position(52, 12),
            sprites["Obstacle"].clone().set_position(56, 12),
            sprites["Obstacle"].clone().set_position(60, 12),
            sprites["Obstacle"].clone().set_position(0, 16),
            sprites["Obstacle"].clone().set_position(16, 16),
            sprites["Obstacle"].clone().set_position(20, 16),
            sprites["Obstacle"].clone().set_position(24, 16),
            sprites["Obstacle"].clone().set_position(28, 16),
            sprites["Obstacle"].clone().set_position(32, 16),
            sprites["Obstacle"].clone().set_position(48, 16),
            sprites["Obstacle"].clone().set_position(52, 16),
            sprites["Obstacle"].clone().set_position(60, 16),
            sprites["Obstacle"].clone().set_position(0, 20),
            sprites["Obstacle"].clone().set_position(12, 20),
            sprites["Obstacle"].clone().set_position(16, 20),
            sprites["Obstacle"].clone().set_position(20, 20),
            sprites["Obstacle"].clone().set_position(24, 20),
            sprites["Obstacle"].clone().set_position(28, 20),
            sprites["Obstacle"].clone().set_position(32, 20),
            sprites["Obstacle"].clone().set_position(36, 20),
            sprites["Obstacle"].clone().set_position(52, 20),
            sprites["Obstacle"].clone().set_position(60, 20),
            sprites["Obstacle"].clone().set_position(0, 24),
            sprites["Obstacle"].clone().set_position(12, 24),
            sprites["Obstacle"].clone().set_position(16, 24),
            sprites["Obstacle"].clone().set_position(20, 24),
            sprites["Obstacle"].clone().set_position(24, 24),
            sprites["Obstacle"].clone().set_position(28, 24),
            sprites["Obstacle"].clone().set_position(32, 24),
            sprites["Obstacle"].clone().set_position(36, 24),
            sprites["Obstacle"].clone().set_position(52, 24),
            sprites["Obstacle"].clone().set_position(56, 24),
            sprites["Obstacle"].clone().set_position(60, 24),
            sprites["Obstacle"].clone().set_position(0, 28),
            sprites["Obstacle"].clone().set_position(44, 28),
            sprites["Obstacle"].clone().set_position(48, 28),
            sprites["Obstacle"].clone().set_position(52, 28),
            sprites["Obstacle"].clone().set_position(60, 28),
            sprites["Obstacle"].clone().set_position(0, 32),
            sprites["Obstacle"].clone().set_position(40, 32),
            sprites["Obstacle"].clone().set_position(44, 32),
            sprites["Obstacle"].clone().set_position(48, 32),
            sprites["Obstacle"].clone().set_position(60, 32),
            sprites["Obstacle"].clone().set_position(0, 36),
            sprites["Obstacle"].clone().set_position(8, 36),
            sprites["Obstacle"].clone().set_position(36, 36),
            sprites["Obstacle"].clone().set_position(40, 36),
            sprites["Obstacle"].clone().set_position(44, 36),
            sprites["Obstacle"].clone().set_position(60, 36),
            sprites["Obstacle"].clone().set_position(0, 40),
            sprites["Obstacle"].clone().set_position(24, 40),
            sprites["Obstacle"].clone().set_position(36, 40),
            sprites["Obstacle"].clone().set_position(40, 40),
            sprites["Obstacle"].clone().set_position(56, 40),
            sprites["Obstacle"].clone().set_position(60, 40),
            sprites["Obstacle"].clone().set_position(0, 44),
            sprites["Obstacle"].clone().set_position(36, 44),
            sprites["Obstacle"].clone().set_position(40, 44),
            sprites["Obstacle"].clone().set_position(60, 44),
            sprites["Obstacle"].clone().set_position(0, 48),
            sprites["Obstacle"].clone().set_position(36, 48),
            sprites["Obstacle"].clone().set_position(48, 48),
            sprites["Obstacle"].clone().set_position(52, 48),
            sprites["Obstacle"].clone().set_position(60, 48),
            sprites["Obstacle"].clone().set_position(0, 52),
            sprites["Obstacle"].clone().set_position(16, 52),
            sprites["Obstacle"].clone().set_position(20, 52),
            sprites["Obstacle"].clone().set_position(52, 52),
            sprites["Obstacle"].clone().set_position(56, 52),
            sprites["Obstacle"].clone().set_position(60, 52),
            sprites["Obstacle"].clone().set_position(0, 56),
            sprites["Obstacle"].clone().set_position(48, 56),
            sprites["Obstacle"].clone().set_position(52, 56),
            sprites["Obstacle"].clone().set_position(60, 56),
            sprites["Obstacle"].clone().set_position(0, 60),
            sprites["Obstacle"].clone().set_position(4, 60),
            sprites["Obstacle"].clone().set_position(8, 60),
            sprites["Obstacle"].clone().set_position(12, 60),
            sprites["Obstacle"].clone().set_position(16, 60),
            sprites["Obstacle"].clone().set_position(20, 60),
            sprites["Obstacle"].clone().set_position(24, 60),
            sprites["Obstacle"].clone().set_position(28, 60),
            sprites["Obstacle"].clone().set_position(32, 60),
            sprites["Obstacle"].clone().set_position(36, 60),
            sprites["Obstacle"].clone().set_position(40, 60),
            sprites["Obstacle"].clone().set_position(44, 60),
            sprites["Obstacle"].clone().set_position(48, 60),
            sprites["Obstacle"].clone().set_position(52, 60),
            sprites["Obstacle"].clone().set_position(56, 60),
            sprites["Obstacle"].clone().set_position(60, 60),
            sprites["Obstacle"].clone().set_position(4, 56),
            sprites["Obstacle"].clone().set_position(4, 52),
            sprites["Obstacle"].clone().set_position(8, 56),
            sprites["Obstacle"].clone().set_position(8, 52),
            sprites["Player"].clone().set_position(16, 36),
            sprites["Recolor"].clone().set_position(8, 44),
            sprites["Rotate"].clone().set_position(8, 12),
            sprites["ShapeCorner"].clone().set_position(16, 36),
        ],
        grid_size=(64, 64),
        data={
            "StepCounter": 22,
            "GoalShape": 3,
            "GoalColor": 0,
            "GoalRotation": 0,
            "StartShape": 1,
            "StartColor": 12,
            "StartRotation": 90,
            "Fog": False,
        },
    ),
    # Level 7
    Level(
        sprites=[
            sprites["Energy"].clone().set_position(29, 17),
            sprites["Energy"].clone().set_position(45, 21),
            sprites["Energy"].clone().set_position(13, 53),
            sprites["Energy"].clone().set_position(53, 37),
            sprites["Energy"].clone().set_position(5, 25),
            sprites["Energy"].clone().set_position(21, 21),
            sprites["Energy"].clone().set_position(25, 33),
            sprites["Energy"].clone().set_position(37, 53),
            sprites["Energy"].clone().set_position(53, 49),
            sprites["Energy"].clone().set_position(25, 57),
            sprites["Energy"].clone().set_position(5, 41),
            sprites["Goal"].clone().set_position(40, 12),
            sprites["Goal"].clone().set_position(12, 8),
            sprites["GoalShape"].clone().set_position(41, 13),
            sprites["GoalShape"].clone().set_position(13, 9),
            sprites["HeldShape"].clone().set_position(1, 54).set_scale(3),
            sprites["Obstacle"].clone(),
            sprites["Obstacle"].clone().set_position(4, 0),
            sprites["Obstacle"].clone().set_position(8, 0),
            sprites["Obstacle"].clone().set_position(12, 0),
            sprites["Obstacle"].clone().set_position(16, 0),
            sprites["Obstacle"].clone().set_position(20, 0),
            sprites["Obstacle"].clone().set_position(24, 0),
            sprites["Obstacle"].clone().set_position(28, 0),
            sprites["Obstacle"].clone().set_position(32, 0),
            sprites["Obstacle"].clone().set_position(36, 0),
            sprites["Obstacle"].clone().set_position(40, 0),
            sprites["Obstacle"].clone().set_position(44, 0),
            sprites["Obstacle"].clone().set_position(48, 0),
            sprites["Obstacle"].clone().set_position(52, 0),
            sprites["Obstacle"].clone().set_position(56, 0),
            sprites["Obstacle"].clone().set_position(60, 0),
            sprites["Obstacle"].clone().set_position(0, 4),
            sprites["Obstacle"].clone().set_position(4, 4),
            sprites["Obstacle"].clone().set_position(20, 4),
            sprites["Obstacle"].clone().set_position(24, 4),
            sprites["Obstacle"].clone().set_position(28, 4),
            sprites["Obstacle"].clone().set_position(56, 4),
            sprites["Obstacle"].clone().set_position(60, 4),
            sprites["Obstacle"].clone().set_position(0, 8),
            sprites["Obstacle"].clone().set_position(4, 8),
            sprites["Obstacle"].clone().set_position(44, 8),
            sprites["Obstacle"].clone().set_position(56, 8),
            sprites["Obstacle"].clone().set_position(60, 8),
            sprites["Obstacle"].clone().set_position(0, 12),
            sprites["Obstacle"].clone().set_position(44, 12),
            sprites["Obstacle"].clone().set_position(48, 12),
            sprites["Obstacle"].clone().set_position(52, 12),
            sprites["Obstacle"].clone().set_position(56, 12),
            sprites["Obstacle"].clone().set_position(60, 12),
            sprites["Obstacle"].clone().set_position(0, 16),
            sprites["Obstacle"].clone().set_position(16, 16),
            sprites["Obstacle"].clone().set_position(20, 16),
            sprites["Obstacle"].clone().set_position(24, 16),
            sprites["Obstacle"].clone().set_position(44, 16),
            sprites["Obstacle"].clone().set_position(48, 16),
            sprites["Obstacle"].clone().set_position(52, 16),
            sprites["Obstacle"].clone().set_position(56, 16),
            sprites["Obstacle"].clone().set_position(60, 16),
            sprites["Obstacle"].clone().set_position(0, 20),
            sprites["Obstacle"].clone().set_position(8, 20),
            sprites["Obstacle"].clone().set_position(28, 20),
            sprites["Obstacle"].clone().set_position(60, 20),
            sprites["Obstacle"].clone().set_position(0, 24),
            sprites["Obstacle"].clone().set_position(60, 24),
            sprites["Obstacle"].clone().set_position(0, 28),
            sprites["Obstacle"].clone().set_position(60, 28),
            sprites["Obstacle"].clone().set_position(0, 32),
            sprites["Obstacle"].clone().set_position(60, 32),
            sprites["Obstacle"].clone().set_position(0, 36),
            sprites["Obstacle"].clone().set_position(24, 36),
            sprites["Obstacle"].clone().set_position(48, 40),
            sprites["Obstacle"].clone().set_position(60, 36),
            sprites["Obstacle"].clone().set_position(0, 40),
            sprites["Obstacle"].clone().set_position(52, 40),
            sprites["Obstacle"].clone().set_position(56, 40),
            sprites["Obstacle"].clone().set_position(60, 40),
            sprites["Obstacle"].clone().set_position(0, 44),
            sprites["Obstacle"].clone().set_position(20, 44),
            sprites["Obstacle"].clone().set_position(24, 44),
            sprites["Obstacle"].clone().set_position(52, 44),
            sprites["Obstacle"].clone().set_position(60, 44),
            sprites["Obstacle"].clone().set_position(0, 48),
            sprites["Obstacle"].clone().set_position(16, 48),
            sprites["Obstacle"].clone().set_position(20, 48),
            sprites["Obstacle"].clone().set_position(24, 48),
            sprites["Obstacle"].clone().set_position(40, 44),
            sprites["Obstacle"].clone().set_position(60, 48),
            sprites["Obstacle"].clone().set_position(0, 52),
            sprites["Obstacle"].clone().set_position(60, 52),
            sprites["Obstacle"].clone().set_position(0, 56),
            sprites["Obstacle"].clone().set_position(20, 56),
            sprites["Obstacle"].clone().set_position(28, 44),
            sprites["Obstacle"].clone().set_position(36, 56),
            sprites["Obstacle"].clone().set_position(48, 56),
            sprites["Obstacle"].clone().set_position(60, 56),
            sprites["Obstacle"].clone().set_position(0, 60),
            sprites["Obstacle"].clone().set_position(4, 60),
            sprites["Obstacle"].clone().set_position(8, 60),
            sprites["Obstacle"].clone().set_position(12, 60),
            sprites["Obstacle"].clone().set_position(16, 60),
            sprites["Obstacle"].clone().set_position(20, 60),
            sprites["Obstacle"].clone().set_position(24, 60),
            sprites["Obstacle"].clone().set_position(28, 60),
            sprites["Obstacle"].clone().set_position(32, 60),
            sprites["Obstacle"].clone().set_position(36, 60),
            sprites["Obstacle"].clone().set_position(40, 60),
            sprites["Obstacle"].clone().set_position(44, 60),
            sprites["Obstacle"].clone().set_position(48, 60),
            sprites["Obstacle"].clone().set_position(52, 60),
            sprites["Obstacle"].clone().set_position(56, 60),
            sprites["Obstacle"].clone().set_position(60, 60),
            sprites["Obstacle"].clone().set_position(4, 56),
            sprites["Obstacle"].clone().set_position(8, 56),
            sprites["Obstacle"].clone().set_position(8, 52),
            sprites["Obstacle"].clone().set_position(4, 52),
            sprites["Obstacle"].clone().set_position(56, 36),
            sprites["Obstacle"].clone().set_position(16, 40),
            sprites["Obstacle"].clone().set_position(32, 44),
            sprites["Obstacle"].clone().set_position(36, 44),
            sprites["Obstacle"].clone().set_position(40, 40),
            sprites["Obstacle"].clone().set_position(44, 40),
            sprites["Player"].clone().set_position(36, 32),
            sprites["Recolor"].clone().set_position(52, 28),
            sprites["Recolor"].clone().set_position(8, 24),
            sprites["Rotate"].clone().set_position(28, 24),
            sprites["ShapeCorner"].clone().set_position(16, 36),
        ],
        grid_size=(64, 64),
        data={
            "StepCounter": 22,
            "GoalShape": [1, 2],
            "GoalColor": [8, 10],
            "GoalRotation": [0, 180],
            "StartShape": 1,
            "StartColor": 12,
            "StartRotation": 90,
            "Fog": False,
        },
    ),
    # Level 8
    Level(
        sprites=[
            sprites["Energy"].clone().set_position(13, 21),
            sprites["Energy"].clone().set_position(25, 33),
            sprites["Energy"].clone().set_position(33, 17),
            sprites["Energy"].clone().set_position(13, 41),
            sprites["Energy"].clone().set_position(21, 49),
            sprites["Energy"].clone().set_position(13, 57),
            sprites["Energy"].clone().set_position(29, 49),
            sprites["Energy"].clone().set_position(45, 57),
            sprites["Energy"].clone().set_position(45, 41),
            sprites["Energy"].clone().set_position(57, 37),
            sprites["Energy"].clone().set_position(56, 21),
            sprites["Energy"].clone().set_position(45, 29),
            sprites["Goal"].clone().set_position(48, 12),
            sprites["GoalShape"].clone().set_position(49, 13),
            sprites["HeldShape"].clone().set_position(1, 54).set_scale(3),
            sprites["Obstacle"].clone(),
            sprites["Obstacle"].clone().set_position(4, 0),
            sprites["Obstacle"].clone().set_position(8, 0),
            sprites["Obstacle"].clone().set_position(12, 0),
            sprites["Obstacle"].clone().set_position(16, 0),
            sprites["Obstacle"].clone().set_position(20, 0),
            sprites["Obstacle"].clone().set_position(24, 0),
            sprites["Obstacle"].clone().set_position(28, 0),
            sprites["Obstacle"].clone().set_position(32, 0),
            sprites["Obstacle"].clone().set_position(36, 0),
            sprites["Obstacle"].clone().set_position(40, 0),
            sprites["Obstacle"].clone().set_position(44, 0),
            sprites["Obstacle"].clone().set_position(48, 0),
            sprites["Obstacle"].clone().set_position(52, 0),
            sprites["Obstacle"].clone().set_position(56, 0),
            sprites["Obstacle"].clone().set_position(60, 0),
            sprites["Obstacle"].clone().set_position(0, 4),
            sprites["Obstacle"].clone().set_position(4, 4),
            sprites["Obstacle"].clone().set_position(8, 4),
            sprites["Obstacle"].clone().set_position(12, 4),
            sprites["Obstacle"].clone().set_position(16, 4),
            sprites["Obstacle"].clone().set_position(20, 4),
            sprites["Obstacle"].clone().set_position(24, 4),
            sprites["Obstacle"].clone().set_position(28, 4),
            sprites["Obstacle"].clone().set_position(44, 4),
            sprites["Obstacle"].clone().set_position(48, 4),
            sprites["Obstacle"].clone().set_position(52, 4),
            sprites["Obstacle"].clone().set_position(56, 4),
            sprites["Obstacle"].clone().set_position(60, 4),
            sprites["Obstacle"].clone().set_position(0, 8),
            sprites["Obstacle"].clone().set_position(4, 8),
            sprites["Obstacle"].clone().set_position(8, 8),
            sprites["Obstacle"].clone().set_position(12, 8),
            sprites["Obstacle"].clone().set_position(16, 8),
            sprites["Obstacle"].clone().set_position(20, 8),
            sprites["Obstacle"].clone().set_position(24, 8),
            sprites["Obstacle"].clone().set_position(28, 8),
            sprites["Obstacle"].clone().set_position(48, 8),
            sprites["Obstacle"].clone().set_position(52, 8),
            sprites["Obstacle"].clone().set_position(56, 8),
            sprites["Obstacle"].clone().set_position(60, 8),
            sprites["Obstacle"].clone().set_position(0, 12),
            sprites["Obstacle"].clone().set_position(4, 12),
            sprites["Obstacle"].clone().set_position(8, 12),
            sprites["Obstacle"].clone().set_position(12, 12),
            sprites["Obstacle"].clone().set_position(16, 12),
            sprites["Obstacle"].clone().set_position(24, 12),
            sprites["Obstacle"].clone().set_position(52, 12),
            sprites["Obstacle"].clone().set_position(56, 12),
            sprites["Obstacle"].clone().set_position(60, 12),
            sprites["Obstacle"].clone().set_position(0, 16),
            sprites["Obstacle"].clone().set_position(4, 16),
            sprites["Obstacle"].clone().set_position(8, 16),
            sprites["Obstacle"].clone().set_position(12, 16),
            sprites["Obstacle"].clone().set_position(24, 16),
            sprites["Obstacle"].clone().set_position(52, 16),
            sprites["Obstacle"].clone().set_position(56, 16),
            sprites["Obstacle"].clone().set_position(60, 16),
            sprites["Obstacle"].clone().set_position(0, 20),
            sprites["Obstacle"].clone().set_position(4, 20),
            sprites["Obstacle"].clone().set_position(8, 20),
            sprites["Obstacle"].clone().set_position(60, 20),
            sprites["Obstacle"].clone().set_position(0, 24),
            sprites["Obstacle"].clone().set_position(60, 24),
            sprites["Obstacle"].clone().set_position(0, 28),
            sprites["Obstacle"].clone().set_position(60, 28),
            sprites["Obstacle"].clone().set_position(0, 32),
            sprites["Obstacle"].clone().set_position(28, 32),
            sprites["Obstacle"].clone().set_position(60, 32),
            sprites["Obstacle"].clone().set_position(0, 36),
            sprites["Obstacle"].clone().set_position(4, 36),
            sprites["Obstacle"].clone().set_position(24, 36),
            sprites["Obstacle"].clone().set_position(28, 36),
            sprites["Obstacle"].clone().set_position(60, 36),
            sprites["Obstacle"].clone().set_position(0, 40),
            sprites["Obstacle"].clone().set_position(4, 40),
            sprites["Obstacle"].clone().set_position(8, 40),
            sprites["Obstacle"].clone().set_position(24, 40),
            sprites["Obstacle"].clone().set_position(28, 40),
            sprites["Obstacle"].clone().set_position(60, 40),
            sprites["Obstacle"].clone().set_position(0, 44),
            sprites["Obstacle"].clone().set_position(4, 44),
            sprites["Obstacle"].clone().set_position(8, 44),
            sprites["Obstacle"].clone().set_position(24, 44),
            sprites["Obstacle"].clone().set_position(28, 44),
            sprites["Obstacle"].clone().set_position(40, 44),
            sprites["Obstacle"].clone().set_position(44, 44),
            sprites["Obstacle"].clone().set_position(60, 44),
            sprites["Obstacle"].clone().set_position(0, 48),
            sprites["Obstacle"].clone().set_position(4, 48),
            sprites["Obstacle"].clone().set_position(24, 48),
            sprites["Obstacle"].clone().set_position(44, 48),
            sprites["Obstacle"].clone().set_position(48, 48),
            sprites["Obstacle"].clone().set_position(60, 48),
            sprites["Obstacle"].clone().set_position(0, 52),
            sprites["Obstacle"].clone().set_position(4, 52),
            sprites["Obstacle"].clone().set_position(8, 52),
            sprites["Obstacle"].clone().set_position(48, 52),
            sprites["Obstacle"].clone().set_position(48, 44),
            sprites["Obstacle"].clone().set_position(60, 52),
            sprites["Obstacle"].clone().set_position(0, 56),
            sprites["Obstacle"].clone().set_position(4, 56),
            sprites["Obstacle"].clone().set_position(8, 56),
            sprites["Obstacle"].clone().set_position(48, 56),
            sprites["Obstacle"].clone().set_position(52, 56),
            sprites["Obstacle"].clone().set_position(56, 56),
            sprites["Obstacle"].clone().set_position(60, 56),
            sprites["Obstacle"].clone().set_position(0, 60),
            sprites["Obstacle"].clone().set_position(4, 60),
            sprites["Obstacle"].clone().set_position(8, 60),
            sprites["Obstacle"].clone().set_position(12, 60),
            sprites["Obstacle"].clone().set_position(16, 60),
            sprites["Obstacle"].clone().set_position(20, 60),
            sprites["Obstacle"].clone().set_position(24, 60),
            sprites["Obstacle"].clone().set_position(28, 60),
            sprites["Obstacle"].clone().set_position(32, 60),
            sprites["Obstacle"].clone().set_position(36, 60),
            sprites["Obstacle"].clone().set_position(40, 60),
            sprites["Obstacle"].clone().set_position(44, 60),
            sprites["Obstacle"].clone().set_position(48, 60),
            sprites["Obstacle"].clone().set_position(52, 60),
            sprites["Obstacle"].clone().set_position(56, 60),
            sprites["Obstacle"].clone().set_position(60, 60),
            sprites["Obstacle"].clone().set_position(52, 40),
            sprites["Obstacle"].clone().set_position(56, 40),
            sprites["Obstacle"].clone().set_position(52, 44),
            sprites["Obstacle"].clone().set_position(16, 16),
            sprites["Obstacle"].clone().set_position(20, 12),
            sprites["Obstacle"].clone().set_position(52, 52),
            sprites["Obstacle"].clone().set_position(56, 52),
            sprites["Obstacle"].clone().set_position(52, 48),
            sprites["Obstacle"].clone().set_position(56, 48),
            sprites["Obstacle"].clone().set_position(56, 44),
            sprites["Player"].clone().set_position(40, 4),
            sprites["Recolor"].clone().set_position(12, 32),
            sprites["Rotate"].clone().set_position(24, 20),
            sprites["ShapeCorner"].clone().set_position(52, 36),
        ],
        grid_size=(64, 64),
        data={
            "StepCounter": 22,
            "GoalShape": 1,
            "GoalColor": 12,
            "GoalRotation": 90,
            "StartShape": 3,
            "StartColor": 10,
            "StartRotation": 180,
            "Fog": True,
        },
    ),
]


BACKGROUND_COLOR = 3
PADDING_COLOR = 3

UNCOLORED = -1
WHITE = 0
OFF_WHITE = 1
GRAY = 2
DARK_GRAY = 3
OFF_BLACK = 4
BLACK = 5
MAGENTA = 6
PINK = 7
RED = 8
BLUE = 9
LIGHT_BLUE = 10
YELLOW = 11
ORANGE = 12
MAROON = 13
GREEN = 14
PURPLE = 15

TILE_SIZE = 4

STEPS_PER_ENERGY = 20


class StepCounterUI(RenderableUserDisplay):
    """
    Draws purple dots along the top left to represent energy, large red dots along the top right
    to represent lives, the held shape in the bottom left, and the level index indicator along the bottom middle
    """

    _path: List[Tuple[int, int]]

    def __init__(self, game: "Ls20", max_steps: int, total_levels: int = 1, level_index: int = 0):
        self.game = game
        self.max_steps = max_steps
        self.current_steps = max_steps
        self.total_levels = max(1, total_levels)
        self.level_index = level_index

    # ------------------------------------------------------------------
    #  Public helpers
    # ------------------------------------------------------------------
    def set_steps(self, steps: int) -> None:
        self.current_steps = max(0, min(steps, self.max_steps))

    def decrease_step(self) -> bool:
        if self.current_steps > 0:
            self.current_steps -= 1
        return self.current_steps > 0

    def reset_steps(self) -> None:
        self.current_steps = self.max_steps

    def set_level_info(self, total_levels: int, level_index: int) -> None:
        self.total_levels = max(1, total_levels)
        self.level_index = min(level_index - 1, total_levels - 1)

    # ------------------------------------------------------------------
    #  Render – called each frame
    # ------------------------------------------------------------------
    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0 or self.game.respawning:
            return frame

        # Limited vision, enable with level data. Used in level 8
        player_half_size = 1.5
        if self.game.fog:
            for i in range(64):
                for j in range(64):
                    if math.dist((i, j), (self.game.player.y + player_half_size, self.game.player.x + player_half_size)) > 14.0:
                        frame[i, j] = BLACK

        # Draw energy display, squares along the top of the screen
        for i in range(self.max_steps):
            start_x = 2 + i * 2
            start_y = 2
            frame[start_y, start_x] = PURPLE if self.max_steps - i - 1 < self.current_steps else DARK_GRAY

        # Draw level counter, rectangles along the bottom of the screen
        for i in range(self.total_levels):
            start_x = 12 + i * 5
            start_y = 62
            for w in range(4):
                frame[start_y, start_x + w] = GREEN if i <= self.level_index else DARK_GRAY

        # Render the held shape to the UI
        if self.game.held_shape:
            sprite = self.game.held_shape.render()
            start_x = 1
            start_y = 54
            for i in range(self.game.held_shape.height):
                for w in range(self.game.held_shape.width):
                    if sprite[i][w] != -1:
                        frame[start_y + i, start_x + w] = sprite[i][w]

        # Draw the life counter
        for count in range(3):
            start_x = 64 - 12 + 4 * count
            start_y = 1
            for y in range(2):
                for x in range(2):
                    frame[start_y + y, start_x + x] = RED if self.game.lives > count else DARK_GRAY

        return frame


class Ls20(ARCBaseGame):
    def __init__(self) -> None:
        first_level_data = levels[0].get_data("StepCounter") if levels else 0
        max_steps = first_level_data if first_level_data else 0
        self._step_counter_ui = StepCounterUI(self, max_steps, total_levels=len(levels), level_index=0)
        self.shapes = []
        self.colors = [WHITE, LIGHT_BLUE, RED, ORANGE]
        self.rotations = [0, 90, 180, 270]

        self.shapes.append(sprites["ShapeL"])
        self.shapes.append(sprites["ShapeT"])
        self.shapes.append(sprites["ShapeU"])
        self.shapes.append(sprites["ShapeV"])
        self.shapes.append(sprites["ShapeW"])
        self.shapes.append(sprites["ShapeZ"])
        # Limited vision mechanic for a late level
        self.fog = False

        camera = Camera(width=16, height=16, background=BACKGROUND_COLOR, letter_box=PADDING_COLOR, interfaces=[self._step_counter_ui])

        # Initialize the base game
        super().__init__(game_id="ls20", levels=levels, camera=camera, available_actions=[1, 2, 3, 4])

        # Initialize step counter for first level
        self._setup_level_step_counter()

    def _setup_level_step_counter(self) -> None:
        """Setup step counter for current level."""
        step_data = self.current_level.get_data("StepCounter")
        if step_data:
            self._step_counter_ui.max_steps = step_data
            self._step_counter_ui.reset_steps()

    def on_set_level(self, level: Level) -> None:
        """Called when the level is set, use this to set level specific data."""
        self.player = self.current_level.get_sprites_by_tag("Player")[0]
        self.held_shape = self.current_level.get_sprites_by_tag("HeldShape")[0]
        self.goal_shapes = self.current_level.get_sprites_by_tag("GoalShape")
        self.goals = self.current_level.get_sprites_by_tag("Goal")
        self.goals_fulfilled = [False] * len(self.goal_shapes)

        self.shape_index = 0
        self.color_index = 0
        self.rotation_index = 0
        self._setup_level_step_counter()
        grid_size = self.current_level.grid_size
        self.width = grid_size[0]  # type: ignore
        self.height = grid_size[1]  # type: ignore
        self._step_counter_ui.set_level_info(total_levels=len(levels), level_index=self.level_index)

        self.goal_rotation_indices = []
        self.goal_color_indices = []
        self.fog = self.current_level.get_data("Fog")

        # convert all to lists
        self.goal_shape_indices = self.current_level.get_data("GoalShape")
        if isinstance(self.goal_shape_indices, int):
            self.goal_shape_indices = [self.goal_shape_indices]

        goal_rots_temp = self.current_level.get_data("GoalRotation")
        if isinstance(goal_rots_temp, int):
            goal_rots_temp = [goal_rots_temp]

        goal_colors_temp = self.current_level.get_data("GoalColor")
        if isinstance(goal_colors_temp, int):
            goal_colors_temp = [goal_colors_temp]

        # Procedurally set the goal's appearance based on the level data
        for i in range(len(self.goals)):
            self.goal_rotation_indices.append(self.rotations.index(goal_rots_temp[i]))
            self.goal_color_indices.append(self.colors.index(goal_colors_temp[i]))
            self.goal_shapes[i].pixels = self.shapes[self.goal_shape_indices[i]].pixels.copy()
            self.goal_shapes[i].color_remap(WHITE, self.colors[self.goal_color_indices[i]])
            self.goal_shapes[i].set_rotation(self.rotations[self.goal_rotation_indices[i]])

        # Same for held shape
        self.set_held_shape_start_properties()
        self.red_overlay = sprites["red-overlay"].clone()
        self.current_level.add_sprite(self.red_overlay)
        self.red_overlay.set_visible(False)
        self.lives = 3
        self.removed_energy: List[Sprite] = []
        self.removed_goals: List[Sprite] = []
        self.removed_goal_shapes: List[Sprite] = []
        self.respawning = False
        self.spawn_pos_x = self.player.x
        self.spawn_pos_y = self.player.y

    def get_sprites_in_rect(self, x: int, y: int, width: int, height: int) -> List[Sprite]:
        """Get all sprites contained in the given rect

        Args:
            x: The x coordinate
            y: The y coordinate
            width: width of the rect
            height: height of the rect
        """
        sprites = self.current_level._sprites
        return [s for s in sprites if s.x >= x and s.x < x + width and s.y >= y and s.y < y + height]

    def step(self) -> None:
        # End respawn animation/red overlay
        if self.respawning:
            self.red_overlay.set_visible(False)
            self.respawning = False
            self.complete_action()
            return

        # Movement
        dx = 0
        dy = 0
        moved = False
        if self.action.id == GameAction.ACTION1:  # Move Up
            dy = -1
            moved = True
        elif self.action.id == GameAction.ACTION2:  # Move Down
            dy = 1
            moved = True
        elif self.action.id == GameAction.ACTION3:  # Move Left
            dx = -1
            moved = True
        elif self.action.id == GameAction.ACTION4:  # Move Right
            dx = 1
            moved = True

        if not moved:
            self.complete_action()
            return

        got_energy = False
        new_x, new_y = self.player.x + dx * TILE_SIZE, self.player.y + dy * TILE_SIZE
        hit_sprites = self.get_sprites_in_rect(new_x, new_y, TILE_SIZE, TILE_SIZE)

        # Handle each hit sprite (or don't move and return if obstacle is hit)
        for sprite in hit_sprites:
            if sprite.tags is None:
                break
            elif "Obstacle" in sprite.tags:
                self.complete_action()
                return
            elif "Energy" in sprite.tags:
                # Refill energy - track to skip decreasing step on refill
                # Save removed energy to re-add on respawn if the player dies
                got_energy = True
                self._step_counter_ui.set_steps(self._step_counter_ui.current_steps + STEPS_PER_ENERGY)
                self.removed_energy.append(sprite)
                self.current_level.remove_sprite(sprite)
            elif "Shifter" in sprite.tags:
                self.shape_index = (self.shape_index + 1) % len(self.shapes)
                self.held_shape.pixels = self.shapes[self.shape_index].pixels.copy()
                self.held_shape.color_remap(WHITE, self.colors[self.color_index])
            elif "Recolor" in sprite.tags:
                new_index = (self.color_index + 1) % len(self.colors)
                self.held_shape.color_remap(self.colors[self.color_index], self.colors[new_index])
                self.color_index = new_index
            elif "Rotate" in sprite.tags:
                self.rotation_index = (self.rotation_index + 1) % 4
                self.held_shape.set_rotation(self.rotations[self.rotation_index])

        self.player.set_position(new_x, new_y)

        if self.check_win_condition():
            self.next_level()
            self.complete_action()
            return

        # Got energy this step, don't decrease. Feels wrong not filling up the bar when you land on it
        if not got_energy and not self._step_counter_ui.decrease_step():
            # Reset all level data, flash red with the overlay if just losing a life
            # lose if out of lives
            self.lives -= 1
            if self.lives == 0:
                self.lose()
                self.complete_action()
                return
            # 1 tick Red overlay, full screen
            self.red_overlay.set_visible(True)
            self.red_overlay.set_scale(64)
            self.red_overlay.set_position(0, 0)

            self.respawning = True
            # reset level to initial state
            self.goals_fulfilled = [False] * len(self.goals)
            self.player.set_position(self.spawn_pos_x, self.spawn_pos_y)
            # reset shape
            self.set_held_shape_start_properties()
            for energy in self.removed_energy:
                self.current_level.add_sprite(energy)
            for goal in self.removed_goals:
                self.current_level.add_sprite(goal)
            for goal_shape in self.removed_goal_shapes:
                self.current_level.add_sprite(goal_shape)
            self.removed_energy = []
            self.removed_goals = []
            self.removed_goal_shapes = []
            self._step_counter_ui.set_steps(self._step_counter_ui.max_steps)
            return
        self.complete_action()

    # Setup held shape to match level data
    def set_held_shape_start_properties(self) -> None:
        self.rotation_index = self.rotations.index(self.current_level.get_data("StartRotation"))
        self.color_index = self.colors.index(self.current_level.get_data("StartColor"))
        self.shape_index = self.current_level.get_data("StartShape")
        self.held_shape.pixels = self.shapes[self.shape_index].pixels.copy()
        self.held_shape.color_remap(WHITE, self.colors[self.color_index])
        self.held_shape.set_rotation(self.rotations[self.rotation_index])

    def check_win_condition(self) -> bool:
        # Check every goal in the lists, and if the player is standing on them with the right held shape/properties
        # That goal gets marked as satisfied, and removed from the level if there are multiple
        # If there are not multiple, the level is complete
        for i, goal in enumerate(self.goals):
            if not self.goals_fulfilled[i] and self.shape_index == self.goal_shape_indices[i] and self.color_index == self.goal_color_indices[i] and self.rotation_index == self.goal_rotation_indices[i] and self.player.x == goal.x and self.player.y == goal.y:
                self.goals_fulfilled[i] = True
                # This goal is fulfilled, remove it from the level to indicate that it is complete (for levels with multiple goal tiles)
                self.removed_goals.append(self.goals[i])
                self.removed_goal_shapes.append(self.goal_shapes[i])
                self.current_level.remove_sprite(self.goals[i])
                self.current_level.remove_sprite(self.goal_shapes[i])

        for i in range(len(self.goals_fulfilled)):
            if not self.goals_fulfilled[i]:
                return False
        return True
