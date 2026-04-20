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

# Set to true to display why check win condition is failing
DEBUG = False

# Create sprites dictionary with all sprite definitions
sprites = {
    "adjacent-flipper": Sprite(
        pixels=[
            [7, 6, 7],
            [6, 10, 6],
            [7, 6, 7],
        ],
        name="adjacent-flipper",
        visible=True,
        collidable=True,
        tags=["adjacent-flipper"],
    ),
    "adjacent-flipper-1": Sprite(
        pixels=[
            [7, 7, 7],
            [7, 10, 7],
            [6, 7, 6],
        ],
        name="adjacent-flipper-1",
        visible=True,
        collidable=True,
        tags=["adjacent-flipper"],
    ),
    "adjacent-flipper-2": Sprite(
        pixels=[
            [6, 7, 6],
            [7, 10, 7],
            [7, 7, 7],
        ],
        name="adjacent-flipper-2",
        visible=True,
        collidable=True,
        tags=["adjacent-flipper"],
    ),
    "adjacent-flipper-X": Sprite(
        pixels=[
            [6, 7, 6],
            [7, 10, 7],
            [6, 7, 6],
        ],
        name="adjacent-flipper-X",
        visible=True,
        collidable=True,
        tags=["adjacent-flipper"],
    ),
    "flip-tile": Sprite(
        pixels=[
            [9, 9, 9],
            [9, 9, 9],
            [9, 9, 9],
        ],
        name="flip-tile",
        visible=True,
        collidable=True,
        tags=["flip-tile"],
    ),
    "full-constraint-red": Sprite(
        pixels=[
            [0, 0, 0],
            [0, 8, 0],
            [0, 0, 0],
        ],
        name="full-constraint-red",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "order-display-blue-red": Sprite(
        pixels=[
            [9, 9],
            [9, 9],
            [8, 8],
            [8, 8],
        ],
        name="order-display-blue-red",
        visible=True,
        collidable=True,
    ),
    "plus-constraint-red": Sprite(
        pixels=[
            [2, 0, 2],
            [0, 8, 0],
            [2, 0, 2],
        ],
        name="plus-constraint-red",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-1": Sprite(
        pixels=[
            [0, 2, 2],
            [0, 12, 0],
            [0, 2, 0],
        ],
        name="sprite-1",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-2": Sprite(
        pixels=[
            [12, 12],
            [12, 12],
        ],
        name="sprite-2",
        visible=True,
        collidable=True,
    ),
    "sprite-3": Sprite(
        pixels=[
            [8, 8],
            [8, 8],
            [12, 12],
            [12, 12],
        ],
        name="sprite-3",
        visible=True,
        collidable=True,
    ),
    "sprite-4": Sprite(
        pixels=[
            [0, 0, 0],
            [0, 12, 2],
            [2, 0, 2],
        ],
        name="sprite-4",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-5": Sprite(
        pixels=[
            [9, 9],
            [9, 9],
        ],
        name="sprite-5",
        visible=True,
        collidable=True,
    ),
    "sprite-6": Sprite(
        pixels=[
            [8, 8],
            [8, 8],
        ],
        name="sprite-6",
        visible=True,
        collidable=True,
    ),
    "sprite-7": Sprite(
        pixels=[
            [0, 0, 0],
            [2, 8, 2],
            [2, 2, 2],
        ],
        name="sprite-7",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-8": Sprite(
        pixels=[
            [0, 0, 2],
            [2, 8, 2],
            [2, 2, 2],
        ],
        name="sprite-8",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-9": Sprite(
        pixels=[
            [2, 0, 0],
            [2, 8, 2],
            [2, 2, 2],
        ],
        name="sprite-9",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-10": Sprite(
        pixels=[
            [2, 2, 0],
            [2, 9, 2],
            [2, 0, 0],
        ],
        name="sprite-10",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-11": Sprite(
        pixels=[
            [0, 2, 2],
            [2, 9, 2],
            [0, 0, 2],
        ],
        name="sprite-11",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-12": Sprite(
        pixels=[
            [2, 0, 2],
            [0, 8, 0],
            [2, 0, 2],
        ],
        name="sprite-12",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-13": Sprite(
        pixels=[
            [12, 12],
            [12, 12],
        ],
        name="sprite-13",
        visible=True,
        collidable=True,
    ),
    "sprite-14": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 12, 2],
            [0, 2, 0],
        ],
        name="sprite-14",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-15": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 8, 0],
            [0, 2, 0],
        ],
        name="sprite-15",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-16": Sprite(
        pixels=[
            [2, 0, 2],
            [2, 9, 2],
            [2, 2, 2],
        ],
        name="sprite-16",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-17": Sprite(
        pixels=[
            [2, 0, 2],
            [0, 9, 2],
            [2, 2, 2],
        ],
        name="sprite-17",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-18": Sprite(
        pixels=[
            [2],
        ],
        name="sprite-18",
        visible=True,
        collidable=True,
    ),
    "sprite-19": Sprite(
        pixels=[
            [2],
        ],
        name="sprite-19",
        visible=True,
        collidable=True,
    ),
    "sprite-20": Sprite(
        pixels=[
            [0],
        ],
        name="sprite-20",
        visible=True,
        collidable=True,
    ),
    "sprite-21": Sprite(
        pixels=[
            [6, 6, 6],
            [7, 7, 7],
            [6, 6, 6],
        ],
        name="sprite-21",
        visible=True,
        collidable=True,
    ),
    "sprite-22": Sprite(
        pixels=[
            [6, 6, 6],
            [6, 7, 6],
            [6, 6, 6],
        ],
        name="sprite-22",
        visible=True,
        collidable=True,
    ),
    "sprite-23": Sprite(
        pixels=[
            [6, 6, 6],
            [6, 7, 6],
            [6, 7, 6],
        ],
        name="sprite-23",
        visible=True,
        collidable=True,
    ),
    "sprite-24": Sprite(
        pixels=[
            [6, 6, 6],
            [6, 7, 6],
            [6, 6, 6],
        ],
        name="sprite-24",
        visible=True,
        collidable=True,
    ),
    "sprite-25": Sprite(
        pixels=[
            [6, 7, 6],
            [7, 7, 7],
            [6, 7, 6],
        ],
        name="sprite-25",
        visible=True,
        collidable=True,
    ),
    "sprite-26": Sprite(
        pixels=[
            [2, 0, 2],
            [2, 12, 0],
            [2, 0, 2],
        ],
        name="sprite-26",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-27": Sprite(
        pixels=[
            [0, 0, 0],
            [0, -1, 0],
            [0, 0, 0],
        ],
        name="sprite-27",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-28": Sprite(
        pixels=[
            [0, 2, 2],
            [2, 9, 2],
            [0, 2, 2],
        ],
        name="sprite-28",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-29": Sprite(
        pixels=[
            [12, 12],
            [12, 12],
            [9, 9],
            [9, 9],
        ],
        name="sprite-29",
        visible=True,
        collidable=True,
    ),
    "sprite-30": Sprite(
        pixels=[
            [6, -1, 6],
        ],
        name="sprite-30",
        visible=True,
        collidable=True,
    ),
    "sprite-31": Sprite(
        pixels=[
            [9, 9],
            [9, 9],
        ],
        name="sprite-31",
        visible=True,
        collidable=True,
    ),
    "sprite-32": Sprite(
        pixels=[
            [3, 0, 2],
            [2, 12, 2],
            [2, 0, 2],
        ],
        name="sprite-32",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-33": Sprite(
        pixels=[
            [2, 0, 3],
            [2, 9, 2],
            [2, 2, 0],
        ],
        name="sprite-33",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-34": Sprite(
        pixels=[
            [3, 0, 2],
            [0, 8, 0],
            [0, 2, 2],
        ],
        name="sprite-34",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-35": Sprite(
        pixels=[
            [3, 0, 2],
            [2, 12, 0],
            [2, 2, 0],
        ],
        name="sprite-35",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-36": Sprite(
        pixels=[
            [3, 3, 3],
            [3, 12, 0],
            [2, 2, 3],
        ],
        name="sprite-36",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-37": Sprite(
        pixels=[
            [0, 2, 2],
            [2, 8, 3],
            [3, 3, 3],
        ],
        name="sprite-37",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-38": Sprite(
        pixels=[
            [7, 7, 7],
            [6, 7, 6],
            [6, 6, 6],
        ],
        name="sprite-38",
        visible=True,
        collidable=True,
    ),
    "sprite-39": Sprite(
        pixels=[
            [2, 2, 2],
            [0, 9, 0],
            [0, 2, 0],
        ],
        name="sprite-39",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-40": Sprite(
        pixels=[
            [2, 0, 0],
            [2, 9, 2],
            [2, 2, 2],
        ],
        name="sprite-40",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-41": Sprite(
        pixels=[
            [0, 0, 2],
            [2, 9, 2],
            [2, 2, 2],
        ],
        name="sprite-41",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-42": Sprite(
        pixels=[
            [2, 0, 2],
            [0, 8, 0],
            [2, 2, 2],
        ],
        name="sprite-42",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-43": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 8, 0],
            [2, 2, 0],
        ],
        name="sprite-43",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-44": Sprite(
        pixels=[
            [0, 2, 2],
            [0, 8, 2],
            [2, 2, 2],
        ],
        name="sprite-44",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-45": Sprite(
        pixels=[
            [6, 6, 6],
            [6, 7, 6],
            [6, 6, 7],
        ],
        name="sprite-45",
        visible=True,
        collidable=True,
    ),
    "sprite-46": Sprite(
        pixels=[
            [0, 2, 2],
            [2, 8, 2],
            [2, 2, 2],
        ],
        name="sprite-46",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-47": Sprite(
        pixels=[
            [2, -1, 2],
        ],
        name="sprite-47",
        visible=True,
        collidable=True,
    ),
    "sprite-48": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 12, 2],
            [2, 0, 2],
        ],
        name="sprite-48",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-49": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 9, 2],
            [2, 2, 2],
        ],
        name="sprite-49",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-50": Sprite(
        pixels=[
            [2, 2, 2],
            [0, 8, 2],
            [2, 0, 2],
        ],
        name="sprite-50",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-51": Sprite(
        pixels=[
            [2, 0, 2],
            [2, 8, 0],
            [2, 2, 2],
        ],
        name="sprite-51",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-52": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 9, 2],
            [2, 2, 2],
        ],
        name="sprite-52",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-53": Sprite(
        pixels=[
            [2, 0, 2],
            [2, 12, 2],
            [2, 2, 2],
        ],
        name="sprite-53",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-54": Sprite(
        pixels=[
            [6, 7, 6],
            [7, 7, 7],
            [6, 7, 6],
        ],
        name="sprite-54",
        visible=True,
        collidable=True,
    ),
    "sprite-55": Sprite(
        pixels=[
            [2, 2, 0],
            [2, 8, 2],
            [0, 0, 2],
        ],
        name="sprite-55",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-56": Sprite(
        pixels=[
            [2, 0, 2],
            [2, 8, 2],
            [0, 2, 2],
        ],
        name="sprite-56",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-57": Sprite(
        pixels=[
            [2, 2, 2],
            [0, 9, 2],
            [2, 2, 0],
        ],
        name="sprite-57",
        visible=True,
        collidable=True,
    ),
    "sprite-58": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 9, 0],
            [2, 2, 2],
        ],
        name="sprite-58",
        visible=True,
        collidable=True,
    ),
    "sprite-59": Sprite(
        pixels=[
            [6, 6, 6],
            [7, 6, 7],
            [6, 6, 6],
        ],
        name="sprite-59",
        visible=True,
        collidable=True,
    ),
    "sprite-60": Sprite(
        pixels=[
            [15, 15],
            [15, 15],
        ],
        name="sprite-60",
        visible=True,
        collidable=True,
    ),
    "sprite-61": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 9, 2],
            [0, 2, 2],
        ],
        name="sprite-61",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-62": Sprite(
        pixels=[
            [2, 0, 2],
            [2, 8, 2],
            [2, 2, 2],
        ],
        name="sprite-62",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-63": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 12, 2],
            [2, 0, 2],
        ],
        name="sprite-63",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-64": Sprite(
        pixels=[
            [2, 2, 0],
            [2, 9, 2],
            [2, 2, 2],
        ],
        name="sprite-64",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-65": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 8, 2],
            [0, 2, 2],
        ],
        name="sprite-65",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-66": Sprite(
        pixels=[
            [0, 2, 0],
            [0, 8, 2],
            [2, 0, 2],
        ],
        name="sprite-66",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-67": Sprite(
        pixels=[
            [2, 0, 2],
            [0, 9, 2],
            [0, 2, 0],
        ],
        name="sprite-67",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-68": Sprite(
        pixels=[
            [2],
            [2],
        ],
        name="sprite-68",
        visible=True,
        collidable=True,
    ),
    "sprite-69": Sprite(
        pixels=[
            [8, 8],
            [8, 8],
            [9, 9],
            [9, 9],
        ],
        name="sprite-69",
        visible=True,
        collidable=True,
    ),
    "sprite-70": Sprite(
        pixels=[
            [3, 3, 3],
            [3, 11, 0],
            [3, 0, 2],
        ],
        name="sprite-70",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-71": Sprite(
        pixels=[
            [0, 0, 2],
            [0, 14, 0],
            [3, 3, 3],
        ],
        name="sprite-71",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-72": Sprite(
        pixels=[
            [3, 3, 3],
            [0, 10, 3],
            [0, 0, 3],
        ],
        name="sprite-72",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-73": Sprite(
        pixels=[
            [2, 2, 0],
            [2, 9, 2],
            [0, 0, 0],
        ],
        name="sprite-73",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-74": Sprite(
        pixels=[
            [2, 0, 3],
            [0, 8, 3],
            [2, 0, 3],
        ],
        name="sprite-74",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-75": Sprite(
        pixels=[
            [3, 0, 0],
            [3, 12, 0],
            [3, 0, 2],
        ],
        name="sprite-75",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-76": Sprite(
        pixels=[
            [2, 2, 2],
            [0, 15, 3],
            [3, 3, 3],
        ],
        name="sprite-76",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-77": Sprite(
        pixels=[
            [3, 3, 3],
            [3, 15, 0],
            [2, 2, 0],
        ],
        name="sprite-77",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-78": Sprite(
        pixels=[
            [3, 3, 3],
            [3, 14, 2],
            [3, 0, 0],
        ],
        name="sprite-78",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-79": Sprite(
        pixels=[
            [0, 0, 0],
            [3, 10, 3],
            [3, 3, 3],
        ],
        name="sprite-79",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-80": Sprite(
        pixels=[
            [3, 3, 2],
            [3, 12, 0],
            [2, 0, 2],
        ],
        name="sprite-80",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-81": Sprite(
        pixels=[
            [2, 0, 3],
            [0, 9, 3],
            [2, 0, 3],
        ],
        name="sprite-81",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-82": Sprite(
        pixels=[
            [2, 0, 0],
            [3, 12, 2],
            [3, 3, 3],
        ],
        name="sprite-82",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-83": Sprite(
        pixels=[
            [3, 0, 2],
            [3, 9, 0],
            [3, 3, 3],
        ],
        name="sprite-83",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-84": Sprite(
        pixels=[
            [3, 3, 3],
            [3, 9, 2],
            [3, 0, 2],
        ],
        name="sprite-84",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-85": Sprite(
        pixels=[
            [0, 2, 3],
            [2, 12, 3],
            [3, 3, 3],
        ],
        name="sprite-85",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-86": Sprite(
        pixels=[
            [15, 15],
            [15, 15],
        ],
        name="sprite-86",
        visible=True,
        collidable=True,
    ),
    "sprite-87": Sprite(
        pixels=[
            [2, 2, 3],
            [0, 8, 0],
            [2, 2, 3],
        ],
        name="sprite-87",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-88": Sprite(
        pixels=[
            [3, 0, 0],
            [2, 9, 2],
            [3, 0, 0],
        ],
        name="sprite-88",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-89": Sprite(
        pixels=[
            [12, 12],
            [12, 12],
            [8, 8],
            [8, 8],
        ],
        name="sprite-89",
        visible=True,
        collidable=True,
    ),
    "sprite-90": Sprite(
        pixels=[
            [5],
        ],
        name="sprite-90",
        visible=True,
        collidable=True,
    ),
    "sprite-91": Sprite(
        pixels=[
            [9, 9],
            [9, 9],
        ],
        name="sprite-91",
        visible=True,
        collidable=True,
    ),
    "sprite-92": Sprite(
        pixels=[
            [14, 14],
            [14, 14],
            [10, 10],
            [10, 10],
        ],
        name="sprite-92",
        visible=True,
        collidable=True,
    ),
    "sprite-93": Sprite(
        pixels=[
            [11, 11],
            [11, 11],
        ],
        name="sprite-93",
        visible=True,
        collidable=True,
    ),
    "sprite-94": Sprite(
        pixels=[
            [12, 12],
            [12, 12],
        ],
        name="sprite-94",
        visible=True,
        collidable=True,
    ),
    "sprite-95": Sprite(
        pixels=[
            [9, 9],
            [9, 9],
        ],
        name="sprite-95",
        visible=True,
        collidable=True,
    ),
    "sprite-96": Sprite(
        pixels=[
            [8, 8],
            [8, 8],
        ],
        name="sprite-96",
        visible=True,
        collidable=True,
    ),
    "sprite-97": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2],
        ],
        name="sprite-97",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-98": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2],
        ],
        name="sprite-98",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-99": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2],
        ],
        name="sprite-99",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-100": Sprite(
        pixels=[
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2],
        ],
        name="sprite-100",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-101": Sprite(
        pixels=[
            [14, 14],
            [14, 14],
        ],
        name="sprite-101",
        visible=True,
        collidable=True,
    ),
    "sprite-102": Sprite(
        pixels=[
            [10, 10],
            [10, 10],
        ],
        name="sprite-102",
        visible=True,
        collidable=True,
    ),
    "sprite-103": Sprite(
        pixels=[
            [8, 8],
            [8, 8],
        ],
        name="sprite-103",
        visible=True,
        collidable=True,
    ),
    "sprite-104": Sprite(
        pixels=[
            [9, 9],
            [9, 9],
        ],
        name="sprite-104",
        visible=True,
        collidable=True,
    ),
    "sprite-105": Sprite(
        pixels=[
            [12, 12],
            [12, 12],
        ],
        name="sprite-105",
        visible=True,
        collidable=True,
    ),
    "sprite-106": Sprite(
        pixels=[
            [0, 0, 3],
            [2, 14, 3],
            [0, 2, 3],
        ],
        name="sprite-106",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-107": Sprite(
        pixels=[
            [3, 2, 2],
            [0, 11, 0],
            [3, 2, 3],
        ],
        name="sprite-107",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-108": Sprite(
        pixels=[
            [3, 0, 0],
            [2, 11, 2],
            [3, 3, 2],
        ],
        name="sprite-108",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-110": Sprite(
        pixels=[
            [3, 2, 3],
            [0, 14, 0],
            [3, 2, 3],
        ],
        name="sprite-110",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-111": Sprite(
        pixels=[
            [14, 14],
            [14, 14],
        ],
        name="sprite-111",
        visible=True,
        collidable=True,
    ),
    "sprite-112": Sprite(
        pixels=[
            [11, 11],
            [11, 11],
        ],
        name="sprite-112",
        visible=True,
        collidable=True,
    ),
    "sprite-113": Sprite(
        pixels=[
            [2, 0, 2],
            [3, 14, 0],
            [3, 3, 3],
        ],
        name="sprite-113",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-114": Sprite(
        pixels=[
            [7, 7, 6],
            [7, 10, 7],
            [7, 7, 7],
        ],
        name="sprite-114",
        visible=True,
        collidable=True,
        tags=["adjacent-flipper"],
    ),
    "sprite-115": Sprite(
        pixels=[
            [6],
        ],
        name="sprite-115",
        visible=True,
        collidable=True,
    ),
    "sprite-116": Sprite(
        pixels=[
            [6, 7, 7],
            [7, 10, 7],
            [7, 7, 7],
        ],
        name="sprite-116",
        visible=True,
        collidable=True,
        tags=["adjacent-flipper"],
    ),
    "sprite-117": Sprite(
        pixels=[
            [12, 12],
            [12, 12],
        ],
        name="sprite-117",
        visible=True,
        collidable=True,
    ),
    "sprite-118": Sprite(
        pixels=[
            [8, 8],
            [8, 8],
        ],
        name="sprite-118",
        visible=True,
        collidable=True,
    ),
    "sprite-119": Sprite(
        pixels=[
            [3, 3, 3],
            [2, 14, 3],
            [0, 0, 3],
        ],
        name="sprite-119",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-120": Sprite(
        pixels=[
            [0, 14],
            [0, 0],
        ],
        name="sprite-120",
        visible=True,
        collidable=True,
    ),
    "sprite-121": Sprite(
        pixels=[
            [-1, -1, 6, -1, -1],
            [-1, -1, -1, -1, -1],
            [6, -1, -1, -1, 6],
            [-1, -1, -1, -1, -1],
            [-1, -1, 6, -1, -1],
        ],
        name="sprite-121",
        visible=True,
        collidable=True,
    ),
    "sprite-122": Sprite(
        pixels=[
            [-1, -1, 6, -1, -1],
            [-1, -1, -1, -1, -1],
            [6, -1, -1, -1, 6],
            [-1, -1, -1, -1, -1],
            [-1, -1, 6, -1, -1],
            [-1, -1, -1, -1, -1],
            [6, -1, -1, -1, 6],
            [-1, -1, -1, -1, -1],
            [-1, -1, 6, -1, -1],
        ],
        name="sprite-122",
        visible=True,
        collidable=True,
    ),
    "sprite-123": Sprite(
        pixels=[
            [3, 0, 3],
            [2, 11, 3],
            [3, 0, 3],
        ],
        name="sprite-123",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-124": Sprite(
        pixels=[
            [3, 0, 3],
            [3, 11, 2],
            [3, 0, 3],
        ],
        name="sprite-124",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "sprite-125": Sprite(
        pixels=[
            [11],
        ],
        name="sprite-125",
        visible=True,
        collidable=True,
    ),
    "x-constraint": Sprite(
        pixels=[
            [0, 2, 0],
            [2, 12, 2],
            [0, 2, 0],
        ],
        name="x-constraint",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
    "x-constraint-Copy": Sprite(
        pixels=[
            [2, 2, 0],
            [2, 15, 2],
            [2, 2, 2],
        ],
        name="x-constraint-Copy",
        visible=True,
        collidable=True,
        tags=["constraint-tile"],
    ),
}


# Create levels array with all level definitions
levels = [
    # Level 1
    Level(
        sprites=[
            sprites["flip-tile"].clone().set_position(1, 1),
            sprites["flip-tile"].clone().set_position(5, 1),
            sprites["flip-tile"].clone().set_position(9, 1),
            sprites["flip-tile"].clone().set_position(1, 5),
            sprites["flip-tile"].clone().set_position(9, 5),
            sprites["flip-tile"].clone().set_position(1, 9),
            sprites["flip-tile"].clone().set_position(5, 9),
            sprites["flip-tile"].clone().set_position(9, 9),
            sprites["order-display-blue-red"].clone().set_position(14, 0),
            sprites["plus-constraint-red"].clone().set_position(5, 5),
        ],
        grid_size=(16, 13),
        data={
            "StepCounter": 20,
            "colors": [9, 8],
            "flip-pattern": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        },
    ),
    # Level 2
    Level(
        sprites=[
            sprites["flip-tile"].clone().set_position(1, 1),
            sprites["flip-tile"].clone().set_position(5, 1),
            sprites["flip-tile"].clone().set_position(9, 1),
            sprites["flip-tile"].clone().set_position(1, 5),
            sprites["flip-tile"].clone().set_position(9, 5),
            sprites["flip-tile"].clone().set_position(1, 9),
            sprites["flip-tile"].clone().set_position(5, 9),
            sprites["flip-tile"].clone().set_position(9, 9),
            sprites["sprite-1"].clone().set_position(5, 5),
            sprites["sprite-94"].clone().set_position(14, 0),
            sprites["sprite-95"].clone().set_position(14, 2),
        ],
        grid_size=(16, 13),
        data={
            "StepCounter": 25,
            "colors": [12, 9],
            "flip-pattern": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        },
    ),
    # Level 3
    Level(
        sprites=[
            sprites["flip-tile"].clone().set_position(5, 2),
            sprites["flip-tile"].clone().set_position(9, 2),
            sprites["flip-tile"].clone().set_position(9, 6),
            sprites["flip-tile"].clone().set_position(13, 2),
            sprites["flip-tile"].clone().set_position(17, 2),
            sprites["flip-tile"].clone().set_position(1, 6),
            sprites["flip-tile"].clone().set_position(1, 2),
            sprites["flip-tile"].clone().set_position(5, 10),
            sprites["flip-tile"].clone().set_position(1, 10),
            sprites["flip-tile"].clone().set_position(9, 10),
            sprites["flip-tile"].clone().set_position(13, 10),
            sprites["flip-tile"].clone().set_position(17, 10),
            sprites["flip-tile"].clone().set_position(17, 6),
            sprites["sprite-66"].clone().set_position(5, 6),
            sprites["sprite-67"].clone().set_position(13, 6),
            sprites["sprite-69"].clone().set_position(22, 0),
        ],
        grid_size=(24, 14),
        data={
            "StepCounter": 40,
            "colors": [8, 9],
            "flip-pattern": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        },
    ),
    # Level 4
    Level(
        sprites=[
            sprites["flip-tile"].clone().set_position(5, 1),
            sprites["flip-tile"].clone().set_position(5, 5),
            sprites["flip-tile"].clone().set_position(5, 9),
            sprites["flip-tile"].clone().set_position(9, 9),
            sprites["flip-tile"].clone().set_position(9, 13),
            sprites["flip-tile"].clone().set_position(13, 9),
            sprites["flip-tile"].clone().set_position(13, 5),
            sprites["flip-tile"].clone().set_position(17, 9),
            sprites["flip-tile"].clone().set_position(13, 1),
            sprites["flip-tile"].clone().set_position(9, 1),
            sprites["flip-tile"].clone().set_position(1, 13),
            sprites["flip-tile"].clone().set_position(1, 9),
            sprites["flip-tile"].clone().set_position(5, 17),
            sprites["flip-tile"].clone().set_position(1, 17),
            sprites["flip-tile"].clone().set_position(9, 17),
            sprites["flip-tile"].clone().set_position(13, 17),
            sprites["flip-tile"].clone().set_position(17, 17),
            sprites["flip-tile"].clone().set_position(17, 13),
            sprites["plus-constraint-red"].clone().set_position(5, 13),
            sprites["sprite-3"].clone().set_position(22, 0),
            sprites["sprite-4"].clone().set_position(9, 5),
            sprites["x-constraint"].clone().set_position(13, 13),
        ],
        grid_size=(24, 21),
        data={
            "StepCounter": 60,
            "colors": [8, 12],
            "flip-pattern": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        },
    ),
    # Level 5
    Level(
        sprites=[
            sprites["flip-tile"].clone().set_position(5, 1),
            sprites["flip-tile"].clone().set_position(9, 5),
            sprites["flip-tile"].clone().set_position(9, 9),
            sprites["flip-tile"].clone().set_position(17, 5),
            sprites["flip-tile"].clone().set_position(17, 9),
            sprites["flip-tile"].clone().set_position(13, 1),
            sprites["flip-tile"].clone().set_position(9, 1),
            sprites["flip-tile"].clone().set_position(1, 5),
            sprites["flip-tile"].clone().set_position(5, 9),
            sprites["flip-tile"].clone().set_position(13, 9),
            sprites["flip-tile"].clone().set_position(1, 9),
            sprites["sprite-31"].clone().set_position(22, 0),
            sprites["sprite-32"].clone().set_position(5, 5),
            sprites["sprite-33"].clone().set_position(13, 5),
            sprites["sprite-117"].clone().set_position(22, 2),
            sprites["sprite-118"].clone().set_position(22, 4),
        ],
        grid_size=(24, 13),
        data={
            "StepCounter": 60,
            "colors": [9, 12, 8],
            "flip-pattern": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        },
    ),
    # Level 6
    Level(
        sprites=[
            sprites["flip-tile"].clone().set_position(9, 5),
            sprites["flip-tile"].clone().set_position(9, 9),
            sprites["flip-tile"].clone().set_position(13, 1),
            sprites["flip-tile"].clone().set_position(9, 13),
            sprites["flip-tile"].clone().set_position(5, 5),
            sprites["flip-tile"].clone().set_position(1, 13),
            sprites["flip-tile"].clone().set_position(5, 13),
            sprites["flip-tile"].clone().set_position(13, 9),
            sprites["flip-tile"].clone().set_position(1, 9),
            sprites["flip-tile"].clone().set_position(17, 1),
            sprites["flip-tile"].clone().set_position(17, 9),
            sprites["flip-tile"].clone().set_position(17, 5),
            sprites["flip-tile"].clone().set_position(21, 1),
            sprites["flip-tile"].clone().set_position(21, 5),
            sprites["flip-tile"].clone().set_position(21, 9),
            sprites["sprite-34"].clone().set_position(5, 9),
            sprites["sprite-35"].clone().set_position(13, 5),
            sprites["sprite-36"].clone().set_position(9, 1),
            sprites["sprite-37"].clone().set_position(13, 13),
            sprites["sprite-103"].clone().set_position(26, 0),
            sprites["sprite-104"].clone().set_position(26, 2),
            sprites["sprite-105"].clone().set_position(26, 4),
        ],
        grid_size=(28, 17),
        data={
            "StepCounter": 80,
            "colors": [8, 9, 12],
            "flip-pattern": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        },
    ),
    # Level 7
    Level(
        sprites=[
            sprites["adjacent-flipper"].clone().set_position(5, 9),
            sprites["flip-tile"].clone().set_position(1, 9),
            sprites["flip-tile"].clone().set_position(5, 13),
            sprites["flip-tile"].clone().set_position(9, 9),
            sprites["flip-tile"].clone().set_position(9, 13),
            sprites["flip-tile"].clone().set_position(1, 13),
            sprites["flip-tile"].clone().set_position(5, 5),
            sprites["sprite-78"].clone().set_position(1, 5),
            sprites["sprite-79"].clone().set_position(5, 17),
            sprites["sprite-92"].clone().set_position(14, 0),
            sprites["sprite-119"].clone().set_position(9, 5),
        ],
        grid_size=(16, 21),
        data={
            "StepCounter": 50,
            "colors": [10, 14],
            "flip-pattern": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        },
    ),
    # Level 8
    Level(
        sprites=[
            sprites["adjacent-flipper"].clone().set_position(9, 9),
            sprites["adjacent-flipper"].clone().set_position(9, 5),
            sprites["flip-tile"].clone().set_position(5, 5),
            sprites["flip-tile"].clone().set_position(5, 9),
            sprites["flip-tile"].clone().set_position(13, 9),
            sprites["flip-tile"].clone().set_position(9, 13),
            sprites["flip-tile"].clone().set_position(1, 9),
            sprites["flip-tile"].clone().set_position(13, 5),
            sprites["flip-tile"].clone().set_position(17, 9),
            sprites["flip-tile"].clone().set_position(13, 13),
            sprites["flip-tile"].clone().set_position(9, 1),
            sprites["sprite-70"].clone().set_position(1, 5),
            sprites["sprite-70"].clone().set_position(5, 1),
            sprites["sprite-72"].clone().set_position(17, 5),
            sprites["sprite-102"].clone().set_position(21, 4),
            sprites["sprite-111"].clone().set_position(21, 2),
            sprites["sprite-112"].clone().set_position(21, 0),
            sprites["sprite-113"].clone().set_position(5, 13),
        ],
        grid_size=(23, 17),
        data={
            "StepCounter": 80,
            "colors": [11, 14, 10],
            "flip-pattern": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        },
    ),
    # Level 9
    Level(
        sprites=[
            sprites["adjacent-flipper-1"].clone().set_position(5, 5),
            sprites["adjacent-flipper-1"].clone().set_position(13, 5),
            sprites["adjacent-flipper-1"].clone().set_position(9, 1),
            sprites["adjacent-flipper-1"].clone().set_position(9, 9),
            sprites["adjacent-flipper-1"].clone().set_position(5, 13),
            sprites["adjacent-flipper-1"].clone().set_position(13, 13),
            sprites["adjacent-flipper-1"].clone().set_position(9, 17),
            sprites["flip-tile"].clone().set_position(1, 9),
            sprites["flip-tile"].clone().set_position(17, 9),
            sprites["flip-tile"].clone().set_position(1, 17),
            sprites["flip-tile"].clone().set_position(17, 17),
            sprites["sprite-110"].clone().set_position(9, 5),
            sprites["sprite-110"].clone().set_position(9, 13),
            sprites["sprite-111"].clone().set_position(21, 2),
            sprites["sprite-112"].clone().set_position(21, 0),
            sprites["sprite-123"].clone().set_position(17, 13),
            sprites["sprite-124"].clone().set_position(1, 13),
        ],
        grid_size=(23, 21),
        data={
            "StepCounter": 100,
            "colors": [11, 14],
            "flip-pattern": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        },
    ),
    # Level 10
    Level(
        sprites=[
            sprites["adjacent-flipper"].clone().set_position(13, 9),
            sprites["adjacent-flipper"].clone().set_position(13, 5),
            sprites["adjacent-flipper"].clone().set_position(13, 13),
            sprites["flip-tile"].clone().set_position(9, 5),
            sprites["flip-tile"].clone().set_position(5, 13),
            sprites["flip-tile"].clone().set_position(1, 9),
            sprites["flip-tile"].clone().set_position(17, 13),
            sprites["flip-tile"].clone().set_position(17, 5),
            sprites["flip-tile"].clone().set_position(5, 5),
            sprites["flip-tile"].clone().set_position(13, 1),
            sprites["flip-tile"].clone().set_position(13, 17),
            sprites["sprite-106"].clone().set_position(17, 9),
            sprites["sprite-107"].clone().set_position(5, 9),
            sprites["sprite-108"].clone().set_position(9, 13),
            sprites["sprite-111"].clone().set_position(25, 2),
            sprites["sprite-112"].clone().set_position(25, 0),
            sprites["sprite-114"].clone().set_position(9, 9),
            sprites["sprite-116"].clone().set_position(17, 17),
        ],
        grid_size=(27, 21),
        data={
            "StepCounter": 100,
            "colors": [11, 14],
            "flip-pattern": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        },
    ),
]


BACKGROUND_COLOR = 4

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

UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4
FLIP = 5

TILE_SIZE = 4


class StepCounterUI(RenderableUserDisplay):
    """Draws a *two-sided* step counter (left / right) that grows
    **symmetrically** from the vertical centre, *plus* level-progress bars
    along both the top and bottom screen edges."""

    _path: List[Tuple[int, int]]

    def __init__(self, max_steps: int, total_levels: int = 1, level_index: int = 0):
        self.max_steps = max_steps
        self.current_steps = max_steps
        self.total_levels = max(1, total_levels)
        self.level_index = level_index
        self._path = self._generate_path()  # build once

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
    #  Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _generate_path() -> List[Tuple[int, int]]:
        """
        Return (x, y) coords for the **left / right edges only** (x = 0 and 63),
        ordered so that depletion proceeds outwards *vertically* from the screen
        centre.  The *top* (y = 0) and *bottom* (y = 63) rows are **omitted**
        because they are reserved for the level-progress bars.
        """
        path: List[Tuple[int, int]] = []
        for y in range(1, 63):  # rows 1 … 62
            path.append((0, y))  # left edge pixel
            path.append((63, y))  # right edge pixel
        return path

    # ------------------------------------------------------------------
    #  Render – called each frame
    # ------------------------------------------------------------------
    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        if self.max_steps == 0:
            return frame

        # -------- Energy / step counter (left & right edges) --------
        spent_ratio = (self.max_steps - self.current_steps) / self.max_steps
        spent_pixels = round(len(self._path) * spent_ratio)

        for idx, (x, y) in enumerate(self._path):
            frame[y, x] = YELLOW if idx < spent_pixels else ORANGE

        # -------- Level-progress bars (top & bottom edges) --------
        # `level_index` is 0-based; show progress *through* the current level.
        progress_ratio = (self.level_index + 1) / self.total_levels
        progress_pixels = round(64 * progress_ratio)

        for x in range(64):
            colour = GREEN if x < progress_pixels else WHITE
            frame[0, x] = colour  # top bar
            frame[63, x] = colour  # bottom bar

        return frame


class Ft09(ARCBaseGame):
    def __init__(self) -> None:
        first_level_data = levels[0].get_data("StepCounter") if levels else 0
        max_steps = first_level_data if first_level_data else 0
        self._step_counter_ui = StepCounterUI(max_steps, total_levels=len(levels), level_index=0)

        camera = Camera(width=16, height=16, background=BACKGROUND_COLOR, letter_box=PADDING_COLOR, interfaces=[self._step_counter_ui])

        # Initialize the base game
        super().__init__(game_id="ft09", levels=levels, camera=camera, available_actions=[6])

        # Initialize step counter for first level
        self._setup_level_step_counter()
        # Uncomment this and test functions at the bottom to validate new levels
        # run_all_tests()

    def _setup_level_step_counter(self) -> None:
        """Setup step counter for current level."""
        step_data = self.current_level.get_data("StepCounter")
        if step_data:
            self._step_counter_ui.max_steps = step_data
            self._step_counter_ui.reset_steps()

    def on_set_level(self, level: Level) -> None:
        """Called when the level is set, use this to set level specific data."""

        self._setup_level_step_counter()

        grid_size = self.current_level.grid_size
        self.width = grid_size[0]  # type: ignore
        self.height = grid_size[1]  # type: ignore
        self._step_counter_ui.set_level_info(total_levels=len(levels), level_index=self.level_index)

        self.constraints = self.current_level.get_sprites_by_tag("constraint-tile")
        self.flip_tiles = self.current_level.get_sprites_by_tag("flip-tile")
        self.adjacent_flippers = self.current_level.get_sprites_by_tag("adjacent-flipper")

        # Get the list of color ids for this level
        self.colors = self.current_level.get_data("colors")
        if self.colors is None:
            self.colors = [BLUE, RED]

        self.flip_pattern = self.current_level.get_data("flip-pattern")

        if self.flip_pattern is None:
            self.flip_pattern = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]

        # Recolor flip tiles (3x3)
        for i, tile in enumerate(self.flip_tiles):
            tile.color_remap(tile.pixels[0][0], self.colors[0])
        # Recolor adjacent flippers (just the center at 1,1)
        for i, tile in enumerate(self.adjacent_flippers):
            for y in range(3):
                for x in range(3):
                    if tile.pixels[y][x] != MAGENTA:
                        tile.pixels[y][x] = self.colors[0]

    def step(self) -> None:
        attempted_action = None
        adjacent_flipper = False

        # CLick
        if self.action.id == GameAction.ACTION6:
            # Get x, y from action.data dictionary
            x = self.action.data.get("x", 0)
            y = self.action.data.get("y", 0)

            # Convert display coords to game coords
            coords = self.camera.display_to_grid(x, y)
            if coords:
                game_x, game_y = coords
                # Get the flip tile or adjacent flipper that was clicked on
                sprite = self.current_level.get_sprite_at(game_x, game_y, "flip-tile")
                if not sprite:
                    sprite = self.current_level.get_sprite_at(game_x, game_y, "adjacent-flipper")
                    if sprite:
                        adjacent_flipper = True
                if sprite:
                    self.current_tile = sprite
                    attempted_action = FLIP

        if attempted_action is None:
            self.complete_action()
            return

        # In the 3x3 loop, these are used to get all the surrounding tiles
        pattern_position_offsets = [
            [(-1, -1), (0, -1), (1, -1)],
            [(-1, 0), (0, 0), (1, 0)],
            [(-1, 1), (0, 1), (1, 1)],
        ]

        # Adjacent flippers are a special tile type that when clicked-
        # flip some surrounding tiles, as well as themselves - depending on where-
        # they have magenta pixels on their sprite
        # They have a color that contributes toward the solution,

        # The pattern here is either the adjacent pattern if an adjacent flipper was clicked
        # Otherwise it uses the per-level input pattern in the level data
        # Which might say something like "flip three in a row horizontally" or "flip in a + pattern"
        # For now, all levels have a single tile input pattern

        # Determine which pattern to use for flipping
        if adjacent_flipper:
            # For adjacent-flippers, the pattern is read from its sprite.
            # The center always flips, and any MAGENTA pixels indicate
            # an additional tile to flip
            pattern_to_use = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
            sprite_pixels = self.current_tile.pixels
            for j in range(3):
                for i in range(3):
                    # Assumes MAGENTA is an imported color constant
                    if sprite_pixels[j][i] == MAGENTA:
                        pattern_to_use[j][i] = 1
        else:
            # For regular flip-tiles, use the pattern defined in the level data
            pattern_to_use = self.flip_pattern

        if attempted_action == FLIP:
            for i in range(3):
                for j in range(3):
                    # If the pattern is 1 here, then that means it should flip this tile
                    if pattern_to_use[j][i] == 1:
                        offset_x, offset_y = pattern_position_offsets[j][i]
                        tile_pos = (self.current_tile.x + (offset_x * TILE_SIZE), self.current_tile.y + (offset_y * TILE_SIZE))

                        target_tile = self.current_level.get_sprite_at(tile_pos[0], tile_pos[1], "flip-tile")
                        # adjacent flipper tiles guaranteed have a colored center 1x1 area so check [1][1] instead of [0][0]
                        if not target_tile:
                            target_tile = self.current_level.get_sprite_at(tile_pos[0], tile_pos[1], "adjacent-flipper")
                        if target_tile:
                            color_index = self.colors.index(target_tile.pixels[1][1])
                            color_index = (color_index + 1) % len(self.colors)
                            target_tile.color_remap(target_tile.pixels[1][1], self.colors[color_index])

        if self.check_win_condition():
            self.next_level()
            self.complete_action()
            return

        if not self._step_counter_ui.decrease_step():
            self.lose()

        self.complete_action()

    def check_win_condition(self) -> bool:
        for constraint in self.constraints:
            # Center pixel defines the color of the constraint
            color = constraint.pixels[1][1]

            # Each edge pixel on the constraint places a rule:
            # - WHITE: The adjacent tile MUST be the same color as the center.
            # - Non-WHITE (Gray): The adjacent tile MUST NOT be the same color as the center.

            # Up Left
            is_white = constraint.pixels[0][0] == WHITE
            tx, ty = constraint.x - TILE_SIZE, constraint.y - TILE_SIZE
            tile = self.current_level.get_sprite_at(tx, ty, "flip-tile")
            if not tile:
                tile = self.current_level.get_sprite_at(tx, ty, "adjacent-flipper")

            # Adjacent flippers only have their center colored which is why 1,1 is checked instead of 0,0 (which would work fine for other flip-tiles)
            if tile:
                satisfied = (tile.pixels[1][1] == color) if is_white else (tile.pixels[1][1] != color)
                if not satisfied:
                    if DEBUG:
                        self.debug(f"Check failed for color {color!r} at location ({tx}, {ty})")
                    return False

            # Up
            is_white = constraint.pixels[0][1] == WHITE
            tx, ty = constraint.x, constraint.y - TILE_SIZE
            tile = self.current_level.get_sprite_at(tx, ty, "flip-tile")
            if not tile:
                tile = self.current_level.get_sprite_at(tx, ty, "adjacent-flipper")
            if tile:
                satisfied = (tile.pixels[1][1] == color) if is_white else (tile.pixels[1][1] != color)
                if not satisfied:
                    if DEBUG:
                        self.debug(f"Check failed for color {color!r} at location ({tx}, {ty})")
                    return False

            # Up Right
            is_white = constraint.pixels[0][2] == WHITE
            tx, ty = constraint.x + TILE_SIZE, constraint.y - TILE_SIZE
            tile = self.current_level.get_sprite_at(tx, ty, "flip-tile")
            if not tile:
                tile = self.current_level.get_sprite_at(tx, ty, "adjacent-flipper")
            if tile:
                satisfied = (tile.pixels[1][1] == color) if is_white else (tile.pixels[1][1] != color)
                if not satisfied:
                    if DEBUG:
                        self.debug(f"Check failed for color {color!r} at location ({tx}, {ty})")
                    return False

            # Left
            is_white = constraint.pixels[1][0] == WHITE
            tx, ty = constraint.x - TILE_SIZE, constraint.y
            tile = self.current_level.get_sprite_at(tx, ty, "flip-tile")
            if not tile:
                tile = self.current_level.get_sprite_at(tx, ty, "adjacent-flipper")
            if tile:
                satisfied = (tile.pixels[1][1] == color) if is_white else (tile.pixels[1][1] != color)
                if not satisfied:
                    if DEBUG:
                        self.debug(f"Check failed for color {color!r} at location ({tx}, {ty})")
                    return False

            # Right
            is_white = constraint.pixels[1][2] == WHITE
            tx, ty = constraint.x + TILE_SIZE, constraint.y
            tile = self.current_level.get_sprite_at(tx, ty, "flip-tile")
            if not tile:
                tile = self.current_level.get_sprite_at(tx, ty, "adjacent-flipper")
            if tile:
                satisfied = (tile.pixels[1][1] == color) if is_white else (tile.pixels[1][1] != color)
                if not satisfied:
                    if DEBUG:
                        self.debug(f"Check failed for color {color!r} at location ({tx}, {ty})")
                    return False

            # Down Left
            is_white = constraint.pixels[2][0] == WHITE
            tx, ty = constraint.x - TILE_SIZE, constraint.y + TILE_SIZE
            tile = self.current_level.get_sprite_at(tx, ty, "flip-tile")
            if not tile:
                tile = self.current_level.get_sprite_at(tx, ty, "adjacent-flipper")
            if tile:
                satisfied = (tile.pixels[1][1] == color) if is_white else (tile.pixels[1][1] != color)
                if not satisfied:
                    if DEBUG:
                        self.debug(f"Check failed for color {color!r} at location ({tx}, {ty})")
                    return False

            # Down
            is_white = constraint.pixels[2][1] == WHITE
            tx, ty = constraint.x, constraint.y + TILE_SIZE
            tile = self.current_level.get_sprite_at(tx, ty, "flip-tile")
            if not tile:
                tile = self.current_level.get_sprite_at(tx, ty, "adjacent-flipper")
            if tile:
                satisfied = (tile.pixels[1][1] == color) if is_white else (tile.pixels[1][1] != color)
                if not satisfied:
                    if DEBUG:
                        self.debug(f"Check failed for color {color!r} at location ({tx}, {ty})")
                    return False

            # Down Right
            is_white = constraint.pixels[2][2] == WHITE
            tx, ty = constraint.x + TILE_SIZE, constraint.y + TILE_SIZE
            tile = self.current_level.get_sprite_at(tx, ty, "flip-tile")
            if not tile:
                tile = self.current_level.get_sprite_at(tx, ty, "adjacent-flipper")
            if tile:
                satisfied = (tile.pixels[1][1] == color) if is_white else (tile.pixels[1][1] != color)
                if not satisfied:
                    if DEBUG:
                        self.debug(f"Check failed for color {color!r} at location ({tx}, {ty})")
                    return False
        return True


# Tests to validate if all constraint tiles have their pixels colored correctly

# # A helper dictionary to map a constraint-tile's 3x3 pixel grid to the
# # relative position of the tile it governs.
# # Format: (pixel_y, pixel_x): (offset_x, offset_y)
# # The offset is a multiplier for TILE_SIZE.
# RELATIVE_POSITIONS_MAP = {
#     (0, 0): (-1, -1), (0, 1): (0, -1), (0, 2): (1, -1),
#     (1, 0): (-1, 0),                    (1, 2): (1, 0),
#     (2, 0): (-1, 1), (2, 1): (0, 1), (2, 2): (1, 1)
# }


# def test_dark_gray_pixel_rule_direct():
#     """
#     Directly validates the `levels` array.
#     Checks that a constraint-tile's pixel is DARK_GRAY if the adjacent
#     space holds another constraint-tile or is empty.
#     """
#     print("--- Running Test 1: Dark Gray Pixel Rule (Direct Validation) ---")
#     failures = 0
#     checks = 0

#     for i, level in enumerate(levels):
#         # Create a spatial lookup map for this level's sprites for efficient checking
#         sprite_map = {(s.x, s.y): s for s in level._sprites}

#         # Filter for only the constraint tiles in this level
#         constraint_tiles = [s for s in level._sprites if "constraint-tile" in s.tags]

#         for constraint_tile in constraint_tiles:
#             for (pixel_y, pixel_x), (offset_x, offset_y) in RELATIVE_POSITIONS_MAP.items():
#                 adj_x = constraint_tile.x + (offset_x * TILE_SIZE)
#                 adj_y = constraint_tile.y + (offset_y * TILE_SIZE)

#                 # Find the adjacent tile using our direct lookup map
#                 adjacent_tile = sprite_map.get((adj_x, adj_y))

#                 # This rule applies if the space is empty or holds another constraint tile
#                 if adjacent_tile is None or "constraint-tile" in adjacent_tile.tags:
#                     checks += 1
#                     pixel_color = constraint_tile.pixels[pixel_y][pixel_x]

#                     if pixel_color != DARK_GRAY:
#                         failures += 1
#                         print(f"[FAIL] Level {i+1}, Constraint '{constraint_tile.name}' at ({constraint_tile.x},{constraint_tile.y}):")
#                         print(f"       Pixel at ({pixel_y},{pixel_x}) should be DARK_GRAY ({DARK_GRAY}) because the adjacent tile")
#                         print(f"       at ({adj_x},{adj_y}) is '{getattr(adjacent_tile, 'name', 'None')}'.")
#                         print(f"       Instead, the pixel color is {pixel_color}.\n")

#     print(f"Test 1 Complete. Checks: {checks}, Failures: {failures}\n")
#     return failures

# def test_white_or_gray_pixel_rule_direct():
#     """
#     Directly validates the `levels` array.
#     Checks that a constraint-tile's pixel is WHITE or GRAY if the adjacent
#     space holds a 'flip-tile' or an 'adjacent-flipper'.
#     """
#     print("--- Running Test 2: White/Gray Pixel Rule (Direct Validation) ---")
#     failures = 0
#     checks = 0

#     for i, level in enumerate(levels):
#         # Create a spatial lookup map for this level's sprites
#         sprite_map = {(s.x, s.y): s for s in level._sprites}

#         # Filter for only the constraint tiles in this level
#         constraint_tiles = [s for s in level._sprites if "constraint-tile" in s.tags]

#         for constraint_tile in constraint_tiles:
#             for (pixel_y, pixel_x), (offset_x, offset_y) in RELATIVE_POSITIONS_MAP.items():
#                 adj_x = constraint_tile.x + (offset_x * TILE_SIZE)
#                 adj_y = constraint_tile.y + (offset_y * TILE_SIZE)

#                 # Find the adjacent tile using our direct lookup map
#                 adjacent_tile = sprite_map.get((adj_x, adj_y))

#                 # This rule applies only if a flippable tile exists at the location
#                 if adjacent_tile and ("flip-tile" in adjacent_tile.tags or "adjacent-flipper" in adjacent_tile.tags):
#                     checks += 1
#                     pixel_color = constraint_tile.pixels[pixel_y][pixel_x]

#                     if pixel_color not in [WHITE, GRAY]:
#                         failures += 1
#                         print(f"[FAIL] Level {i+1}, Constraint '{constraint_tile.name}' at ({constraint_tile.x},{constraint_tile.y}):")
#                         print(f"       Pixel at ({pixel_y},{pixel_x}) should be WHITE ({WHITE}) or GRAY ({GRAY}) because the adjacent tile")
#                         print(f"       at ({adj_x},{adj_y}) is '{adjacent_tile.name}'.")
#                         print(f"       Instead, the pixel color is {pixel_color}.\n")

#     print(f"Test 2 Complete. Checks: {checks}, Failures: {failures}\n")
#     return failures

# def run_all_tests():
#     """Runs all defined standalone tests and reports a summary."""
#     print("=========================================================")
#     print("      RUNNING DIRECT VALIDATION OF LEVEL DATA      ")
#     print("=========================================================\n")

#     total_failures = 0
#     total_failures += test_dark_gray_pixel_rule_direct()
#     total_failures += test_white_or_gray_pixel_rule_direct()

#     print("---------------------------------------------------------")
#     if total_failures == 0:
#         print("✅ SUCCESS: All level data validation tests passed!")
#     else:
#         print(f"❌ FAILURE: A total of {total_failures} validation errors were found.")
#     print("=========================================================")
