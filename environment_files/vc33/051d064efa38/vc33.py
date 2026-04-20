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

import json
from typing import TypedDict

import numpy as np
from arcengine import ARCBaseGame, Camera, GameAction, Level, RenderableUserDisplay, Sprite

# Create sprites dictionary with all sprite definitions
sprites = {
    "duck-1": Sprite(
        pixels=[
            [11, 11],
            [11, 11],
        ],
        name="duck-1",
        visible=True,
        collidable=True,
        tags=["Duck0"],
    ),
    "marker-1": Sprite(
        pixels=[
            [11],
        ],
        name="marker-1",
        visible=True,
        collidable=True,
        tags=["Marker0"],
        layer=1,
    ),
    "marker-2": Sprite(
        pixels=[
            [14],
        ],
        name="marker-2",
        visible=True,
        collidable=True,
        tags=["Marker0"],
        layer=1,
    ),
    "pump-1": Sprite(
        pixels=[
            [8],
        ],
        name="pump-1",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump1"],
        layer=1,
    ),
    "pump-2": Sprite(
        pixels=[
            [8],
        ],
        name="pump-2",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump1"],
        layer=1,
    ),
    "sprite-3": Sprite(
        pixels=[
            [14, 14],
            [14, 14],
        ],
        name="sprite-3",
        visible=True,
        collidable=True,
        tags=["Duck0"],
    ),
    "sprite-4": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-4",
        visible=True,
        collidable=True,
        tags=["Wall0"],
    ),
    "sprite-5": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-5",
        visible=True,
        collidable=True,
        tags=["Wall1"],
    ),
    "sprite-6": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-6",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump2"],
        layer=1,
    ),
    "sprite-7": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-7",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump0"],
        layer=1,
    ),
    "sprite-8": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-8",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump1"],
        layer=1,
    ),
    "sprite-9": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-9",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump3"],
        layer=1,
    ),
    "sprite-10": Sprite(
        pixels=[
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
        ],
        name="sprite-10",
        visible=True,
        collidable=True,
        tags=["Water0"],
    ),
    "sprite-11": Sprite(
        pixels=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        name="sprite-11",
        visible=True,
        collidable=True,
        tags=["Water1"],
    ),
    "sprite-12": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        name="sprite-12",
        visible=True,
        collidable=True,
        tags=["Water2"],
    ),
    "sprite-13": Sprite(
        pixels=[
            [14],
        ],
        name="sprite-13",
        visible=True,
        collidable=True,
        tags=["Marker0"],
        layer=1,
    ),
    "sprite-14": Sprite(
        pixels=[
            [14, 14],
            [14, 14],
        ],
        name="sprite-14",
        visible=True,
        collidable=True,
        tags=["Duck0"],
    ),
    "sprite-15": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-15",
        visible=True,
        collidable=True,
        tags=["Wall0"],
    ),
    "sprite-16": Sprite(
        pixels=[
            [5],
        ],
        name="sprite-16",
        visible=True,
        collidable=True,
        tags=["Wall0"],
    ),
    "sprite-17": Sprite(
        pixels=[
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
        ],
        name="sprite-17",
        visible=True,
        collidable=True,
        tags=["Water0"],
    ),
    "sprite-18": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-18",
        visible=True,
        collidable=True,
        tags=["Wall1"],
    ),
    "sprite-19": Sprite(
        pixels=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        name="sprite-19",
        visible=True,
        collidable=True,
        tags=["Water1"],
    ),
    "sprite-20": Sprite(
        pixels=[
            [10],
        ],
        name="sprite-20",
        visible=True,
        collidable=True,
    ),
    "sprite-21": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        name="sprite-21",
        visible=True,
        collidable=True,
        tags=["Water2"],
    ),
    "sprite-22": Sprite(
        pixels=[
            [14, 14],
            [14, 14],
        ],
        name="sprite-22",
        visible=True,
        collidable=True,
        tags=["Duck1"],
    ),
    "sprite-23": Sprite(
        pixels=[
            [11],
        ],
        name="sprite-23",
        visible=True,
        collidable=True,
        tags=["Marker0"],
    ),
    "sprite-24": Sprite(
        pixels=[
            [14],
        ],
        name="sprite-24",
        visible=True,
        collidable=True,
        tags=["Marker1"],
    ),
    "sprite-25": Sprite(
        pixels=[
            [11, 11],
            [11, 11],
        ],
        name="sprite-25",
        visible=True,
        collidable=True,
        tags=["Duck0"],
    ),
    "sprite-26": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-26",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump0"],
        layer=1,
    ),
    "sprite-27": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-27",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump2"],
        layer=1,
    ),
    "sprite-28": Sprite(
        pixels=[
            [6, -1, -1, -1, -1, -1, 6],
        ],
        name="sprite-28",
        visible=True,
        collidable=True,
    ),
    "sprite-29": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-29",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump1"],
        layer=1,
    ),
    "sprite-30": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-30",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump3"],
        layer=1,
    ),
    "sprite-31": Sprite(
        pixels=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        name="sprite-31",
        visible=True,
        collidable=True,
        tags=["Water0"],
    ),
    "sprite-32": Sprite(
        pixels=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        name="sprite-32",
        visible=True,
        collidable=True,
        tags=["Water1"],
    ),
    "sprite-33": Sprite(
        pixels=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        name="sprite-33",
        visible=True,
        collidable=True,
        tags=["Water2"],
    ),
    "sprite-34": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        name="sprite-34",
        visible=True,
        collidable=True,
        tags=["Water3"],
    ),
    "sprite-35": Sprite(
        pixels=[
            [5],
            [5],
            [-1],
            [-1],
            [-1],
            [-1],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-35",
        visible=True,
        collidable=True,
        tags=["Wall0"],
    ),
    "sprite-36": Sprite(
        pixels=[
            [5],
            [5],
            [-1],
            [-1],
            [-1],
            [-1],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-36",
        visible=True,
        collidable=True,
        tags=["Wall1"],
    ),
    "sprite-37": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [-1],
            [-1],
            [-1],
            [-1],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-37",
        visible=True,
        collidable=True,
        tags=["Wall2"],
    ),
    "sprite-38": Sprite(
        pixels=[
            [11, 11],
            [11, 11],
        ],
        name="sprite-38",
        visible=True,
        collidable=True,
        tags=["Duck0"],
    ),
    "sprite-39": Sprite(
        pixels=[
            [11],
        ],
        name="sprite-39",
        visible=True,
        collidable=True,
        tags=["Marker0"],
    ),
    "sprite-40": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-40",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump0"],
        layer=1,
    ),
    "sprite-41": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-41",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump2"],
        layer=1,
    ),
    "sprite-42": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-42",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump4"],
        layer=1,
    ),
    "sprite-43": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-43",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump1"],
        layer=1,
    ),
    "sprite-44": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-44",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump3"],
        layer=1,
    ),
    "sprite-45": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-45",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump5"],
        layer=1,
    ),
    "sprite-46": Sprite(
        pixels=[
            [1],
            [1],
            [1],
            [1],
        ],
        name="sprite-46",
        visible=True,
        collidable=True,
        tags=["Gate", "Gate0"],
        layer=1,
    ),
    "sprite-47": Sprite(
        pixels=[
            [1],
            [1],
            [1],
            [1],
        ],
        name="sprite-47",
        visible=True,
        collidable=True,
        tags=["Gate", "Gate1"],
        layer=1,
    ),
    "sprite-48": Sprite(
        pixels=[
            [1],
            [1],
            [1],
            [1],
        ],
        name="sprite-48",
        visible=True,
        collidable=True,
        tags=["Gate", "Gate2"],
        layer=1,
    ),
    "sprite-49": Sprite(
        pixels=[
            [5],
        ],
        name="sprite-49",
        visible=True,
        collidable=True,
    ),
    "sprite-50": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-50",
        visible=True,
        collidable=True,
        tags=["Wall1"],
    ),
    "sprite-51": Sprite(
        pixels=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        name="sprite-51",
        visible=True,
        collidable=True,
        tags=["Water0"],
    ),
    "sprite-52": Sprite(
        pixels=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        name="sprite-52",
        visible=True,
        collidable=True,
        tags=["Water1"],
    ),
    "sprite-53": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [-1],
            [-1],
            [-1],
            [-1],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-53",
        visible=True,
        collidable=True,
        tags=["Wall0"],
    ),
    "sprite-54": Sprite(
        pixels=[
            [1],
            [1],
            [1],
            [1],
        ],
        name="sprite-54",
        visible=True,
        collidable=True,
        tags=["Gate", "Gate0"],
        layer=1,
    ),
    "sprite-55": Sprite(
        pixels=[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        name="sprite-55",
        visible=True,
        collidable=True,
        tags=["Water2"],
    ),
    "sprite-56": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-56",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump0"],
        layer=1,
    ),
    "sprite-57": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-57",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump1"],
        layer=1,
    ),
    "sprite-58": Sprite(
        pixels=[
            [11, 11],
            [11, 11],
        ],
        name="sprite-58",
        visible=True,
        collidable=True,
        tags=["Duck0"],
    ),
    "sprite-59": Sprite(
        pixels=[
            [11],
        ],
        name="sprite-59",
        visible=True,
        collidable=True,
        tags=["Marker0"],
    ),
    "sprite-60": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-60",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump2"],
        layer=1,
    ),
    "sprite-61": Sprite(
        pixels=[
            [6],
        ],
        name="sprite-61",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump1"],
    ),
    "sprite-62": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-62",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump3"],
        layer=1,
    ),
    "sprite-63": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-63",
        visible=True,
        collidable=True,
    ),
    "sprite-64": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-64",
        visible=True,
        collidable=True,
    ),
    "sprite-65": Sprite(
        pixels=[
            [2],
            [2],
            [2],
            [2],
        ],
        name="sprite-65",
        visible=True,
        collidable=True,
    ),
    "sprite-66": Sprite(
        pixels=[
            [2],
            [2],
            [2],
            [2],
        ],
        name="sprite-66",
        visible=True,
        collidable=True,
    ),
    "sprite-67": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [-1],
            [-1],
            [-1],
            [-1],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-67",
        visible=True,
        collidable=True,
        tags=["Wall0"],
    ),
    "sprite-68": Sprite(
        pixels=[
            [1],
            [1],
            [1],
            [1],
        ],
        name="sprite-68",
        visible=True,
        collidable=True,
        tags=["Gate0", "Gate"],
        layer=1,
    ),
    "sprite-69": Sprite(
        pixels=[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        name="sprite-69",
        visible=True,
        collidable=True,
        tags=["Water0"],
    ),
    "sprite-70": Sprite(
        pixels=[
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        name="sprite-70",
        visible=True,
        collidable=True,
        tags=["Water1"],
    ),
    "sprite-71": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-71",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump0"],
        layer=1,
    ),
    "sprite-72": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-72",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump1"],
        layer=1,
    ),
    "sprite-73": Sprite(
        pixels=[
            [11, 11],
            [11, 11],
        ],
        name="sprite-73",
        visible=True,
        collidable=True,
        tags=["Duck1"],
    ),
    "sprite-74": Sprite(
        pixels=[
            [14, 14],
            [14, 14],
        ],
        name="sprite-74",
        visible=True,
        collidable=True,
        tags=["Duck0"],
    ),
    "sprite-75": Sprite(
        pixels=[
            [11],
        ],
        name="sprite-75",
        visible=True,
        collidable=True,
        tags=["Marker1"],
        layer=1,
    ),
    "sprite-76": Sprite(
        pixels=[
            [14],
        ],
        name="sprite-76",
        visible=True,
        collidable=True,
        tags=["Marker0"],
        layer=1,
    ),
    "sprite-77": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [-1],
            [-1],
            [-1],
            [-1],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-77",
        visible=True,
        collidable=True,
        tags=["Wall1"],
    ),
    "sprite-78": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-78",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump2"],
        layer=1,
    ),
    "sprite-79": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-79",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump3"],
        layer=1,
    ),
    "sprite-80": Sprite(
        pixels=[
            [1],
            [1],
            [1],
            [1],
        ],
        name="sprite-80",
        visible=True,
        collidable=True,
        tags=["Gate1", "Gate"],
        layer=1,
    ),
    "sprite-81": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, -1],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
        name="sprite-81",
        visible=True,
        collidable=True,
        tags=["Water2"],
    ),
    "sprite-82": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-82",
        visible=True,
        collidable=True,
    ),
    "sprite-83": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [-1],
            [-1],
            [-1],
            [5],
        ],
        name="sprite-83",
        visible=True,
        collidable=True,
        tags=["Wall1"],
    ),
    "sprite-84": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [-1],
            [-1],
            [-1],
            [5],
            [5],
        ],
        name="sprite-84",
        visible=True,
        collidable=True,
        tags=["Wall0"],
    ),
    "sprite-85": Sprite(
        pixels=[
            [1],
            [1],
            [1],
        ],
        name="sprite-85",
        visible=True,
        collidable=True,
        tags=["Gate0", "Gate"],
        layer=1,
    ),
    "sprite-86": Sprite(
        pixels=[
            [1],
            [1],
            [1],
        ],
        name="sprite-86",
        visible=True,
        collidable=True,
        tags=["Gate1", "Gate"],
        layer=1,
    ),
    "sprite-87": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4],
        ],
        name="sprite-87",
        visible=True,
        collidable=True,
    ),
    "sprite-88": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-88",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump2"],
        layer=1,
    ),
    "sprite-89": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-89",
        visible=True,
        collidable=True,
    ),
    "sprite-90": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-90",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump0"],
        layer=1,
    ),
    "sprite-91": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-91",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump1"],
        layer=1,
    ),
    "sprite-92": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        name="sprite-92",
        visible=True,
        collidable=True,
        tags=["Water0"],
    ),
    "sprite-93": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
        name="sprite-93",
        visible=True,
        collidable=True,
        tags=["Water1"],
    ),
    "sprite-94": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        name="sprite-94",
        visible=True,
        collidable=True,
        tags=["Water2"],
    ),
    "sprite-95": Sprite(
        pixels=[
            [11],
        ],
        name="sprite-95",
        visible=True,
        collidable=True,
        tags=["Marker0"],
    ),
    "sprite-96": Sprite(
        pixels=[
            [11, 11],
            [11, 11],
        ],
        name="sprite-96",
        visible=True,
        collidable=True,
        tags=["Duck0"],
    ),
    "sprite-97": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-97",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump3"],
        layer=1,
    ),
    "sprite-98": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-98",
        visible=True,
        collidable=True,
        tags=["Wall2"],
    ),
    "sprite-99": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [-1],
            [-1],
            [-1],
            [-1],
            [5],
            [5],
            [5],
        ],
        name="sprite-99",
        visible=True,
        collidable=True,
        tags=["Wall0"],
    ),
    "sprite-100": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [-1],
            [-1],
            [-1],
            [-1],
            [5],
            [5],
            [5],
        ],
        name="sprite-100",
        visible=True,
        collidable=True,
        tags=["Wall1"],
    ),
    "sprite-101": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [-1],
            [-1],
            [-1],
            [-1],
            [5],
            [5],
            [5],
            [5],
        ],
        name="sprite-101",
        visible=True,
        collidable=True,
        tags=["Wall3"],
    ),
    "sprite-102": Sprite(
        pixels=[
            [5, 5, 5, 5, 5, 5, 5],
        ],
        name="sprite-102",
        visible=True,
        collidable=True,
    ),
    "sprite-103": Sprite(
        pixels=[
            [5, 5, 5, 5, 5, 5],
        ],
        name="sprite-103",
        visible=True,
        collidable=True,
    ),
    "sprite-104": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-104",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump4"],
        layer=1,
    ),
    "sprite-105": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-105",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump6"],
        layer=1,
    ),
    "sprite-106": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-106",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump2"],
        layer=1,
    ),
    "sprite-107": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-107",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump0"],
        layer=1,
    ),
    "sprite-108": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-108",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump3"],
        layer=1,
    ),
    "sprite-109": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-109",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump7"],
        layer=1,
    ),
    "sprite-110": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-110",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump5"],
        layer=1,
    ),
    "sprite-111": Sprite(
        pixels=[
            [8],
        ],
        name="sprite-111",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump1"],
        layer=1,
    ),
    "sprite-112": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        name="sprite-112",
        visible=True,
        collidable=True,
        tags=["Water0"],
    ),
    "sprite-113": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
        name="sprite-113",
        visible=True,
        collidable=True,
        tags=["Water1"],
    ),
    "sprite-114": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        name="sprite-114",
        visible=True,
        collidable=True,
        tags=["Water3"],
    ),
    "sprite-115": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        name="sprite-115",
        visible=True,
        collidable=True,
        tags=["Water4"],
    ),
    "sprite-116": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        name="sprite-116",
        visible=True,
        collidable=True,
        tags=["Water2"],
    ),
    "sprite-117": Sprite(
        pixels=[
            [11],
        ],
        name="sprite-117",
        visible=True,
        collidable=True,
        tags=["Marker0"],
        layer=1,
    ),
    "sprite-118": Sprite(
        pixels=[
            [11, 11],
            [11, 11],
        ],
        name="sprite-118",
        visible=True,
        collidable=True,
        tags=["Duck0"],
    ),
    "sprite-119": Sprite(
        pixels=[
            [1],
            [1],
            [1],
            [1],
        ],
        name="sprite-119",
        visible=True,
        collidable=True,
        tags=["Gate0", "Gate"],
        layer=2,
    ),
    "sprite-120": Sprite(
        pixels=[
            [1],
            [1],
            [1],
            [1],
        ],
        name="sprite-120",
        visible=True,
        collidable=True,
        tags=["Gate1", "Gate"],
        layer=2,
    ),
    "sprite-121": Sprite(
        pixels=[
            [1],
            [1],
            [1],
            [1],
        ],
        name="sprite-121",
        visible=True,
        collidable=True,
        tags=["Gate2", "Gate"],
        layer=1,
    ),
    "sprite-122": Sprite(
        pixels=[
            [1],
            [1],
            [1],
            [1],
        ],
        name="sprite-122",
        visible=True,
        collidable=True,
        tags=["Gate3", "Gate"],
        layer=2,
    ),
    "sprite-123": Sprite(
        pixels=[
            [14, 14],
            [14, 14],
        ],
        name="sprite-123",
        visible=True,
        collidable=True,
        tags=["Duck1"],
    ),
    "sprite-124": Sprite(
        pixels=[
            [14],
        ],
        name="sprite-124",
        visible=True,
        collidable=True,
        tags=["Marker1"],
        layer=1,
    ),
    "sprite-125": Sprite(
        pixels=[
            [15, 15],
            [15, 15],
        ],
        name="sprite-125",
        visible=True,
        collidable=True,
        tags=["Duck2"],
    ),
    "sprite-126": Sprite(
        pixels=[
            [15],
        ],
        name="sprite-126",
        visible=True,
        collidable=True,
        tags=["Marker2"],
        layer=1,
    ),
    "sprite-127": Sprite(
        pixels=[
            [5],
        ],
        name="sprite-127",
        visible=True,
        collidable=True,
    ),
    "valve-1": Sprite(
        pixels=[
            [9],
        ],
        name="valve-1",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump0"],
        layer=1,
    ),
    "valve-2": Sprite(
        pixels=[
            [9],
        ],
        name="valve-2",
        visible=True,
        collidable=True,
        tags=["Pump", "Pump0"],
        layer=1,
    ),
    "wall-1": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="wall-1",
        visible=True,
        collidable=True,
        tags=["Wall0"],
    ),
    "wall-2": Sprite(
        pixels=[
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
            [5],
        ],
        name="wall-2",
        visible=True,
        collidable=True,
        tags=["Wall0"],
    ),
    "water-1": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
        name="water-1",
        visible=True,
        collidable=True,
        tags=["Water0"],
    ),
    "water-2": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        name="water-2",
        visible=True,
        collidable=True,
        tags=["Water1"],
    ),
    "water-3": Sprite(
        pixels=[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        name="water-3",
        visible=True,
        collidable=True,
        tags=["Water0"],
    ),
    "water-4": Sprite(
        pixels=[
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        name="water-4",
        visible=True,
        collidable=True,
        tags=["Water1"],
    ),
}

# Create levels array with all level definitions
levels = [
    # Level 1
    Level(
        sprites=[
            sprites["duck-1"].clone().set_position(10, 11),
            sprites["marker-1"].clone().set_position(6, 10),
            sprites["pump-1"].clone().set_position(7, 15),
            sprites["valve-1"].clone().set_position(5, 15),
            sprites["wall-1"].clone().set_position(6, 5),
            sprites["water-1"].clone().set_position(0, 8),
            sprites["water-2"].clone().set_position(7, 13),
        ],
        grid_size=(16, 16),
        data={
            "Ducks": '[{"duck": "Duck0", "water": "Water1", "marker": "Marker0"}]',
            "Markers": '[{"marker": "Marker0", "wall": "Wall0"}]',
            "Pumps": '[{"pump": "Pump0", "from_water": "Water1", "to_water": "Water0"}, {"pump": "Pump1", "from_water": "Water0", "to_water": "Water1"}]',
            "Walls": '[{"wall": "Wall0", "water_left": "Water0", "water_right": "Water1"}]',
            "StepCounter": 50,
            "Waters": "[]",
        },
    ),
    # Level 2
    Level(
        sprites=[
            sprites["marker-2"].clone().set_position(4, 10),
            sprites["pump-2"].clone().set_position(5, 15),
            sprites["sprite-3"].clone().set_position(9, 7),
            sprites["sprite-82"].clone().set_position(5, 15),
            sprites["valve-2"].clone().set_position(3, 15),
            sprites["wall-2"].clone().set_position(4, 5),
            sprites["water-3"].clone().set_position(0, 8),
            sprites["water-4"].clone().set_position(5, 9),
        ],
        grid_size=(16, 16),
        data={
            "Ducks": '[{"duck": "Duck0", "water": "Water1", "marker": "Marker0"}]',
            "Markers": '[{"marker": "Marker0", "wall": "Wall0"}]',
            "Pumps": '[{"pump":"Pump0","from_water":"Water1","to_water":"Water0"},{"pump":"Pump1","from_water":"Water0","to_water":"Water1"}]',
            "Walls": '[{"wall": "Wall0", "water_left": "Water0", "water_right": "Water1"}]',
            "StepCounter": 20,
            "Waters": "[]",
        },
    ),
    # Level 3
    Level(
        sprites=[
            sprites["sprite-4"].clone().set_position(2, 2),
            sprites["sprite-5"].clone().set_position(8, 6),
            sprites["sprite-6"].clone().set_position(7, 15),
            sprites["sprite-7"].clone().set_position(1, 15),
            sprites["sprite-8"].clone().set_position(3, 15),
            sprites["sprite-9"].clone().set_position(9, 15),
            sprites["sprite-10"].clone().set_position(0, 3),
            sprites["sprite-11"].clone().set_position(3, 14),
            sprites["sprite-12"].clone().set_position(9, 15),
            sprites["sprite-13"].clone().set_position(8, 11),
            sprites["sprite-14"].clone().set_position(11, 13),
        ],
        grid_size=(16, 16),
        data={
            "Ducks": '[{"duck": "Duck0", "water": "Water2", "marker": "Marker0"}]',
            "Markers": '[{"marker": "Marker0", "wall": "Wall1"}]',
            "Pumps": '[{"pump":"Pump0","from_water":"Water1","to_water":"Water0"},{"pump":"Pump1","from_water":"Water0","to_water":"Water1"},{"pump":"Pump2","from_water":"Water2","to_water":"Water1"},{"pump":"Pump3","from_water":"Water1","to_water":"Water2"}]',
            "Walls": '[{"wall": "Wall0", "water_left": "Water0", "water_right": "Water1"}, {"wall": "Wall1", "water_left": "Water1", "water_right": "Water2"}]',
            "StepCounter": 25,
            "Waters": "[]",
        },
    ),
    # Level 4
    Level(
        sprites=[
            sprites["sprite-15"].clone().set_position(2, 6),
            sprites["sprite-16"].clone().set_position(2, 8),
            sprites["sprite-17"].clone().set_position(0, 11),
            sprites["sprite-18"].clone().set_position(8, 3),
            sprites["sprite-19"].clone().set_position(3, 13),
            sprites["sprite-21"].clone().set_position(9, 5),
            sprites["sprite-22"].clone().set_position(11, 3),
            sprites["sprite-23"].clone().set_position(2, 9),
            sprites["sprite-24"].clone().set_position(8, 9),
            sprites["sprite-25"].clone().set_position(4, 11),
            sprites["sprite-26"].clone().set_position(1, 15),
            sprites["sprite-27"].clone().set_position(7, 15),
            sprites["sprite-29"].clone().set_position(3, 15),
            sprites["sprite-30"].clone().set_position(9, 15),
        ],
        grid_size=(16, 16),
        data={
            "Ducks": '[{"duck": "Duck0", "water": "Water1", "marker": "Marker0"}, {"duck": "Duck1", "water": "Water2", "marker": "Marker1"}]',
            "Markers": '[{"marker": "Marker0", "wall": "Wall0"}, {"marker": "Marker1", "wall": "Wall1"}]',
            "Pumps": '[{"pump":"Pump0","from_water":"Water1","to_water":"Water0"},{"pump":"Pump1","from_water":"Water0","to_water":"Water1"},{"pump":"Pump2","from_water":"Water2","to_water":"Water1"},{"pump":"Pump3","from_water":"Water1","to_water":"Water2"}]',
            "Walls": '[{"wall": "Wall0", "water_left": "Water0", "water_right": "Water1"}, {"wall": "Wall1", "water_left": "Water1", "water_right": "Water2"}]',
            "StepCounter": 30,
            "Waters": "[]",
        },
    ),
    # Level 5
    Level(
        sprites=[
            sprites["sprite-50"].clone().set_position(11, 6),
            sprites["sprite-51"].clone().set_position(0, 7),
            sprites["sprite-52"].clone().set_position(6, 13),
            sprites["sprite-53"].clone().set_position(5, 2),
            sprites["sprite-54"].clone().set_position(5, 6),
            sprites["sprite-55"].clone().set_position(12, 15),
            sprites["sprite-56"].clone().set_position(4, 15),
            sprites["sprite-57"].clone().set_position(6, 15),
            sprites["sprite-58"].clone().set_position(1, 5),
            sprites["sprite-59"].clone().set_position(11, 12),
            sprites["sprite-60"].clone().set_position(10, 15),
            sprites["sprite-62"].clone().set_position(12, 15),
        ],
        grid_size=(16, 16),
        data={
            "Ducks": '[{"duck": "Duck0", "water": "Water0", "marker": "Marker0"}]',
            "Markers": '[{"marker": "Marker0", "wall": "Wall1"}]',
            "Pumps": '[{"pump":"Pump0","from_water":"Water1","to_water":"Water0"},{"pump":"Pump1","from_water":"Water0","to_water":"Water1"},{"pump":"Pump2","from_water":"Water2","to_water":"Water1"},{"pump":"Pump3","from_water":"Water1","to_water":"Water2"}]',
            "Walls": '[{"wall": "Wall0", "water_left": "Water0", "water_right": "Water1", "gate": "Gate0"}, {"wall": "Wall1", "water_left": "Water1", "water_right": "Water2"}]',
            "StepCounter": 30,
            "Waters": "[]",
        },
    ),
    # Level 6
    Level(
        sprites=[
            sprites["sprite-31"].clone().set_position(0, 20),
            sprites["sprite-32"].clone().set_position(6, 18),
            sprites["sprite-33"].clone().set_position(12, 20),
            sprites["sprite-34"].clone().set_position(18, 3),
            sprites["sprite-35"].clone().set_position(5, 10),
            sprites["sprite-36"].clone().set_position(11, 8),
            sprites["sprite-37"].clone().set_position(17, 2),
            sprites["sprite-38"].clone().set_position(1, 18),
            sprites["sprite-39"].clone().set_position(17, 5),
            sprites["sprite-40"].clone().set_position(4, 23),
            sprites["sprite-41"].clone().set_position(10, 23),
            sprites["sprite-42"].clone().set_position(16, 23),
            sprites["sprite-43"].clone().set_position(6, 23),
            sprites["sprite-44"].clone().set_position(12, 23),
            sprites["sprite-45"].clone().set_position(18, 23),
            sprites["sprite-46"].clone().set_position(5, 12),
            sprites["sprite-47"].clone().set_position(11, 10),
            sprites["sprite-48"].clone().set_position(17, 8),
        ],
        grid_size=(24, 24),
        data={
            "Ducks": '[{"duck": "Duck0", "water": "Water0", "marker": "Marker0"}]',
            "Markers": '[{"marker": "Marker0", "wall": "Wall2"}]',
            "Pumps": '[{"pump":"Pump0","from_water":"Water1","to_water":"Water0"},{"pump":"Pump1","from_water":"Water0","to_water":"Water1"},{"pump":"Pump2","from_water":"Water2","to_water":"Water1"},{"pump":"Pump3","from_water":"Water1","to_water":"Water2"},{"pump":"Pump4","from_water":"Water3","to_water":"Water2"},{"pump":"Pump5","from_water":"Water2","to_water":"Water3"}]',
            "Walls": '[{"wall": "Wall0", "water_left": "Water0", "water_right": "Water1", "gate": "Gate0"}, {"wall": "Wall1", "water_left": "Water1", "water_right": "Water2", "gate": "Gate1"}, {"wall": "Wall2", "water_left": "Water2", "water_right": "Water3", "gate": "Gate2" }]',
            "StepCounter": 100,
            "Waters": "[]",
        },
    ),
    # Level 7
    Level(
        sprites=[
            sprites["sprite-67"].clone().set_position(4, 2),
            sprites["sprite-68"].clone().set_position(4, 6),
            sprites["sprite-69"].clone().set_position(0, 12),
            sprites["sprite-70"].clone().set_position(5, 10),
            sprites["sprite-71"].clone().set_position(3, 15),
            sprites["sprite-72"].clone().set_position(5, 15),
            sprites["sprite-73"].clone().set_position(13, 2),
            sprites["sprite-74"].clone().set_position(1, 10),
            sprites["sprite-75"].clone().set_position(4, 11),
            sprites["sprite-76"].clone().set_position(10, 3),
            sprites["sprite-77"].clone().set_position(10, 2),
            sprites["sprite-78"].clone().set_position(9, 15),
            sprites["sprite-79"].clone().set_position(11, 15),
            sprites["sprite-80"].clone().set_position(10, 6),
            sprites["sprite-81"].clone().set_position(11, 4),
        ],
        grid_size=(16, 16),
        data={
            "Ducks": '[{"duck": "Duck0", "water": "Water0", "marker": "Marker0"}, {"duck": "Duck1", "water": "Water2", "marker": "Marker1"}]',
            "Markers": '[{"marker": "Marker0", "wall": "Wall1"}, {"marker": "Marker1", "wall": "Wall0"}]',
            "Walls": '[{"wall": "Wall0", "water_left": "Water0", "water_right": "Water1", "gate": "Gate0"}, {"wall": "Wall1", "water_left": "Water1", "water_right": "Water2", "gate": "Gate1"}]',
            "Pumps": '[{"pump":"Pump0","from_water":"Water1","to_water":"Water0"},{"pump":"Pump1","from_water":"Water0","to_water":"Water1"},{"pump":"Pump2","from_water":"Water2","to_water":"Water1"},{"pump":"Pump3","from_water":"Water1","to_water":"Water2"}]',
            "StepCounter": 50,
            "Waters": "[]",
        },
    ),
    # Level 8
    Level(
        sprites=[
            sprites["sprite-83"].clone().set_position(7, 0),
            sprites["sprite-84"].clone().set_position(7, 8),
            sprites["sprite-85"].clone().set_position(7, 11),
            sprites["sprite-86"].clone().set_position(7, 4),
            sprites["sprite-87"].clone().set_position(0, 9),
            sprites["sprite-88"].clone().set_position(6, 8),
            sprites["sprite-90"].clone().set_position(6, 15),
            sprites["sprite-91"].clone().set_position(8, 15),
            sprites["sprite-92"].clone().set_position(0, 14),
            sprites["sprite-93"].clone().set_position(8, 10),
            sprites["sprite-94"].clone().set_position(0, 6),
            sprites["sprite-95"].clone().set_position(7, 2),
            sprites["sprite-96"].clone().set_position(2, 12),
            sprites["sprite-97"].clone().set_position(8, 8),
        ],
        grid_size=(16, 16),
        data={
            "Ducks": '[{"duck": "Duck0", "water": "Water0", "marker": "Marker0"}]',
            "Markers": '[{"marker": "Marker0", "wall": "Wall1"}]',
            "Walls": '[{"wall": "Wall0", "water_left": "Water0", "water_right": "Water1", "gate": "Gate0"}, {"wall": "Wall1", "water_left": "Water1", "water_right": "Water2", "gate": "Gate1"}]',
            "Pumps": '[{"pump":"Pump0","from_water":"Water1","to_water":"Water0"},{"pump":"Pump1","from_water":"Water0","to_water":"Water1"},{"pump":"Pump2","from_water":"Water1","to_water":"Water2"},{"pump":"Pump3","from_water":"Water2","to_water":"Water1"}]',
            "Waters": '[{"water": "Water0", "min_height": 10, "max_height": 16}, {"water": "Water1", "min_height": 0, "max_height": 16}, {"water": "Water2", "min_height": 0, "max_height": 9}]',
            "StepCounter": 50,
        },
    ),
    # Level 9
    Level(
        sprites=[
            sprites["sprite-98"].clone().set_position(7, 12),
            sprites["sprite-99"].clone().set_position(7, 0),
            sprites["sprite-100"].clone().set_position(16, 0),
            sprites["sprite-101"].clone().set_position(16, 12),
            sprites["sprite-102"].clone().set_position(0, 12),
            sprites["sprite-103"].clone().set_position(18, 12),
            sprites["sprite-104"].clone().set_position(6, 23),
            sprites["sprite-105"].clone().set_position(15, 23),
            sprites["sprite-106"].clone().set_position(15, 11),
            sprites["sprite-107"].clone().set_position(6, 11),
            sprites["sprite-108"].clone().set_position(17, 11),
            sprites["sprite-109"].clone().set_position(17, 23),
            sprites["sprite-110"].clone().set_position(8, 23),
            sprites["sprite-111"].clone().set_position(8, 11),
            sprites["sprite-112"].clone().set_position(0, 8),
            sprites["sprite-113"].clone().set_position(8, 20),
            sprites["sprite-114"].clone().set_position(0, 14),
            sprites["sprite-115"].clone().set_position(17, 21),
            sprites["sprite-116"].clone().set_position(17, 7),
            sprites["sprite-117"].clone().set_position(16, 14),
            sprites["sprite-118"].clone().set_position(2, 6),
            sprites["sprite-119"].clone().set_position(7, 5),
            sprites["sprite-120"].clone().set_position(16, 5),
            sprites["sprite-122"].clone().set_position(16, 16),
            sprites["sprite-123"].clone().set_position(19, 5),
            sprites["sprite-124"].clone().set_position(7, 18),
            sprites["sprite-125"].clone().set_position(20, 19),
            sprites["sprite-126"].clone().set_position(7, 2),
            sprites["sprite-127"].clone().set_position(17, 12),
        ],
        grid_size=(24, 24),
        data={
            "Ducks": '[{"duck": "Duck0", "water": "Water0", "marker": "Marker0"}, {"duck": "Duck1", "water": "Water2", "marker": "Marker1"}, {"duck": "Duck2", "water": "Water4", "marker": "Marker2"}]',
            "Markers": '[{"marker": "Marker0", "wall": "Wall3"}, {"marker": "Marker1", "wall": "Wall2"}, {"marker": "Marker2", "wall": "Wall0"}]',
            "Walls": '[{"wall":"Wall0","water_left":"Water0","water_right":"Water1","gate":"Gate0"},{"wall":"Wall1","water_left":"Water1","water_right":"Water2","gate":"Gate1"},{"wall":"Wall2","water_left":"Water3","water_right":"Water1"},{"wall":"Wall3","water_left":"Water1","water_right":"Water4","gate":"Gate3"}]',
            "Pumps": '[{"pump":"Pump0","from_water":"Water1","to_water":"Water0"},{"pump":"Pump1","from_water":"Water0","to_water":"Water1"},{"pump":"Pump2","from_water":"Water2","to_water":"Water1"},{"pump":"Pump3","from_water":"Water1","to_water":"Water2"},{"pump":"Pump4","from_water":"Water1","to_water":"Water3"},{"pump":"Pump5","from_water":"Water3","to_water":"Water1"},{"pump":"Pump6","from_water":"Water4","to_water":"Water1"},{"pump":"Pump7","from_water":"Water1","to_water":"Water4"}]',
            "Waters": '[{"water":"Water0","min_height":0,"max_height":12},{"water":"Water1","min_height":0,"max_height":24},{"water":"Water2","min_height":0,"max_height":12},{"water":"Water3","min_height":13,"max_height":24},{"water":"Water4","min_height":13,"max_height":24}]',
            "StepCounter": 100,
        },
    ),
]


def ensure_list_2d(data: list) -> list[list]:  # type: ignore
    if isinstance(data[0], list):
        return data
    else:
        return [data]


BACKGROUND_COLOR = 2

PADDING_COLOR = 3

HIGH_ENERGY_COLOR = 14
LOW_ENERGY_COLOR = 11
CRITICAL_ENERGY_COLOR = 8

GATE_READY_COLOR = 12
GATE_UNREADY_COLOR = 1


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

WATER_COLOR = WHITE


class Duck(TypedDict):
    duck: Sprite
    water: Sprite
    marker: Sprite


class Marker(TypedDict):
    marker: Sprite
    wall: Sprite


class Wall(TypedDict):
    wall: Sprite
    water_left: Sprite
    water_right: Sprite
    gate: Sprite | None


class Pump(TypedDict):
    pump: Sprite
    from_water: Sprite
    to_water: Sprite


class Water(TypedDict):
    water: Sprite
    min_height: int
    max_height: int


class Lerp:
    _sprite: Sprite
    _target: tuple[int, int]

    def __init__(self, sprite: Sprite, target: tuple[int, int]) -> None:
        self._sprite = sprite
        self._target = target

    def next(self) -> bool:
        start = (self._sprite.x, self._sprite.y)
        target = self._target

        dx = target[0] - start[0]
        dy = target[1] - start[1]

        # If sprite has reached the target, interpolation complete
        if dx == 0 and dy == 0:
            return True

        # Move along the axis with the greater distance
        if abs(dx) >= abs(dy):
            new_coords = (start[0] + np.sign(dx), start[1])
        else:
            new_coords = (start[0], start[1] + np.sign(dy))

        self._sprite.set_position(new_coords[0], new_coords[1])

        return False


class Animation:
    _lerps: list[Lerp]
    _current_frame: int

    def __init__(self, interps: list[Lerp]) -> None:
        self._lerps = interps
        self._current_frame = 0

    def next(self) -> bool:
        lerp = self._lerps[self._current_frame]

        # If the current lerp is completed
        if lerp.next():
            # Increment the frame
            self._current_frame += 1

            # If the animation is complete
            if self._current_frame == len(self._lerps):
                return True

        # The animation is not complete
        return False


class StepCounterUI(RenderableUserDisplay):
    """A UI element that displays a step counter along the top of the screen."""

    def __init__(self, max_steps: int):
        """Initialize the step counter UI.

        Args:
            max_steps: Maximum number of steps allowed
        """
        self.max_steps = max_steps
        self.current_steps = max_steps

    def set_steps(self, steps: int) -> None:
        """Set the current number of steps remaining."""
        self.current_steps = max(0, min(steps, self.max_steps))

    def decrease_step(self) -> bool:
        """Decrease step counter by 1. Returns True if steps remaining, False if reached 0."""
        if self.current_steps > 0:
            self.current_steps -= 1
        return self.current_steps > 0

    def reset_steps(self) -> None:
        """Reset steps to maximum."""
        self.current_steps = self.max_steps

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        """Render the moves bar on the left side."""
        if self.max_steps == 0:
            return frame

        # Calculate how much of the bar should be filled
        fill_percentage = self.current_steps / self.max_steps
        pixels_to_fill = round(64 * fill_percentage)  # 64 is the screen height

        color = HIGH_ENERGY_COLOR
        if fill_percentage < 0.5:
            color = CRITICAL_ENERGY_COLOR
        elif fill_percentage < 0.75:
            color = LOW_ENERGY_COLOR

        # Draw the horizontal bar
        for x in range(64):
            if (x) < pixels_to_fill:
                frame[0, x] = color  # Full
            else:
                frame[0, x] = 0  # Empty

        return frame


class ProgressUI(RenderableUserDisplay):
    _level_count: int
    _current_level: int
    _block_size: int
    _spacing: int
    _offset_y: int
    _filled_color: int
    _empty_color: int
    _active_color: int

    def __init__(
        self,
        level_count: int,
        block_size: int = 1,
        spacing: int = 5,
        offset_y: int = 4,
        filled_color: int = 14,
        active_color: int = 11,
        empty_color: int = 0,
    ) -> None:
        self._level_count = level_count
        self._block_size = block_size
        self._spacing = spacing
        self._offset_y = offset_y
        self._filled_color = filled_color
        self._active_color = active_color
        self._empty_color = empty_color
        self._current_level = 0

    def set_current_level(self, current_level: int) -> None:
        self._current_level = current_level

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        """Draws a centered level bar composed of blocks."""
        frame_width = frame.shape[1]
        level_count = self._level_count
        block_size = self._block_size
        y = self._offset_y
        total_bar_width = level_count * block_size + (level_count - 1) * self._spacing

        # Center the bar, ensuring symmetry for both even and odd widths
        x = (frame_width - total_bar_width) // 2

        # Draw filled blocks up to current level
        for _ in range(self._current_level):
            self._draw_block(frame, x, y, block_size, self._filled_color)
            x += block_size + self._spacing

        # Draw active block
        self._draw_block(frame, x, y, block_size, self._active_color)
        x += block_size + self._spacing

        # Draw empty blocks for remaining levels
        for _ in range(self._current_level + 1, level_count):
            self._draw_block(frame, x, y, block_size, self._empty_color)
            x += block_size + self._spacing

        return frame

    def _draw_block(self, frame: np.ndarray, x: int, y: int, size: int, color: int) -> None:
        """Draws a square block of the given size with bottom-right corner at (x+1, y)."""
        for dy in range(size):
            for dx in range(size):
                frame[y - dy, x + dx] = color


class GateUI(RenderableUserDisplay):
    _markers: dict[Sprite, Sprite]

    def __init__(self) -> None:
        super().__init__()

        self._markers = dict()

    def render_interface(self, frame: np.ndarray) -> np.ndarray:
        for sprite in self._markers.values():
            frame = self.draw_sprite(frame, sprite, sprite.x, sprite.y)

        return frame

    def reset_markers(self) -> None:
        self._markers = dict()

    def add_gate_marker(self, gate_sprite: Sprite, width: int) -> None:
        if width == 16:
            row = [0, -1, -1, -1, -1, -1, -1, 0]
            marker = Sprite(
                pixels=[row] * ((gate_sprite.height * 4) - 2),
                x=gate_sprite.x * 4 - 2,
                y=gate_sprite.y * 4 + 1,
            )
        else:
            marker = Sprite(
                pixels=[
                    [0, -1, -1, 0],
                    [0, -1, -1, 0],
                    [0, -1, -1, 0],
                    [0, -1, -1, 0],
                    [0, -1, -1, 0],
                    [0, -1, -1, 0],
                ],
                x=gate_sprite.x * 2 + 7,
                y=gate_sprite.y * 2 + 9,
            )

        self._markers[gate_sprite] = marker

    def remove_gate_marker(self, gate_sprite: Sprite) -> None:
        if gate_sprite in self._markers:
            del self._markers[gate_sprite]


class Vc33(ARCBaseGame):
    """A game where the player opens valves."""

    _step_counter_ui: StepCounterUI
    _progress_ui: ProgressUI
    _gate_ui: GateUI

    _ducks: list[Duck]
    _markers: list[Marker]
    _pumps: list[Pump]
    _waters: list[Water]
    _walls: list[Wall]

    def __init__(self) -> None:
        """Initialize the ValveCheck game."""
        # Initialize ui
        self._step_counter_ui = StepCounterUI(0)
        self._progress_ui = ProgressUI(len(levels))
        self._gate_ui = GateUI()

        # Create camera with background and padding colors
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            interfaces=[
                self._step_counter_ui,
                self._progress_ui,
                self._gate_ui,
            ],
        )

        # Initialize the base game
        super().__init__(game_id="vc33", levels=levels, camera=camera)

    def setup_level_step_counter(self) -> None:
        """Setup step counter for current level."""
        step_data = self.current_level.get_data("StepCounter")
        self._step_counter_ui.max_steps = step_data or 1000
        self._step_counter_ui.reset_steps()

    def setup_progress(self) -> None:
        self._progress_ui.set_current_level(self._current_level_index)

    def setup_gate(self) -> None:
        self._gate_ui.reset_markers()

    def get_sprite_by_tag(self, tag: str) -> Sprite:
        return self.current_level.get_sprites_by_tag(tag)[0]

    def on_set_level(self, level: Level) -> None:
        """Called when the level is set, use this to set level specific data."""

        # Setup UI
        self.setup_level_step_counter()
        self.setup_progress()
        self.setup_gate()

        self._current_animation = None
        self._ducks = []
        self._markers = []
        self._pumps = []
        self._waters = []
        self._walls = []

        duck_json = self.current_level.get_data("Ducks")
        duck_list = json.loads(duck_json)
        for row in duck_list:
            self._ducks.append(
                {
                    "duck": self.get_sprite_by_tag(row["duck"]),
                    "water": self.get_sprite_by_tag(row["water"]),
                    "marker": self.get_sprite_by_tag(row["marker"]),
                }
            )

        marker_json = self.current_level.get_data("Markers")
        marker_list = json.loads(marker_json)
        for row in marker_list:
            self._markers.append(
                {
                    "marker": self.get_sprite_by_tag(row["marker"]),
                    "wall": self.get_sprite_by_tag(row["wall"]),
                }
            )

        pump_json = self.current_level.get_data("Pumps")
        pump_list = json.loads(pump_json)
        for row in pump_list:
            self._pumps.append(
                {
                    "pump": self.get_sprite_by_tag(row["pump"]),
                    "from_water": self.get_sprite_by_tag(row["from_water"]),
                    "to_water": self.get_sprite_by_tag(row["to_water"]),
                }
            )

        water_json = self.current_level.get_data("Waters")
        water_list = json.loads(water_json)
        for row in water_list:
            self._waters.append(
                {
                    "water": self.get_sprite_by_tag(row["water"]),
                    "min_height": row["min_height"],
                    "max_height": row["max_height"],
                }
            )

        wall_json = self.current_level.get_data("Walls")
        wall_list = json.loads(wall_json)
        for row in wall_list:
            self._walls.append(
                {
                    "wall": self.get_sprite_by_tag(row["wall"]),
                    "water_left": self.get_sprite_by_tag(row["water_left"]),
                    "water_right": self.get_sprite_by_tag(row["water_right"]),
                    "gate": self.get_sprite_by_tag(row["gate"]) if "gate" in row else None,
                }
            )

    def check_win_condition(self) -> bool:
        """Check if all ducks are aligned with marker"""

        for duck in self._ducks:
            marker = self.get_marker(duck["marker"])
            wall = self.get_wall(marker["wall"])

            # If the duck is at the right height and in the right water
            is_correct = duck["duck"].y + 1 == duck["marker"].y and (duck["water"] == wall["water_left"] or duck["water"] == wall["water_right"])

            if not is_correct:
                return False

        return True

    def get_wall_for_gate(self, gate_sprite: Sprite) -> Wall:
        for w in self._walls:
            if w["gate"] == gate_sprite:
                return w

        raise Exception("Not found")

    def get_wall(self, wall_sprite: Sprite) -> Wall:
        for w in self._walls:
            if w["wall"] == wall_sprite:
                return w

        raise Exception("Not found")

    def get_pump(self, pump_sprite: Sprite) -> Pump:
        for p in self._pumps:
            if p["pump"] == pump_sprite:
                return p

        raise Exception("Not found")

    def get_marker(self, marker_sprite: Sprite) -> Marker:
        for m in self._markers:
            if m["marker"] == marker_sprite:
                return m

        raise Exception("Not found")

    def get_water(self, marker_sprite: Sprite) -> Water | None:
        for m in self._waters:
            if m["water"] == marker_sprite:
                return m

        return None

    def get_walls_for_water(self, water_sprite: Sprite) -> list[Wall]:
        """Finds the walls that bound `waterSprite`"""
        bounding_walls = [w for w in self._walls if (w["water_left"] == water_sprite or w["water_right"] == water_sprite)]
        return bounding_walls

    def gate_can_open(self, gate_sprite: Sprite) -> bool:
        # If water levels on each side of the gate are equal and the water is at the bottom of the gate
        wall = self.get_wall_for_gate(gate_sprite)
        return wall["water_left"].y == wall["water_right"].y and wall["water_left"].y == gate_sprite.y + gate_sprite.height

    def get_coords_for_water(self, water_sprite: Sprite) -> tuple[int, int]:
        return (water_sprite.x + (water_sprite.width // 2) - 1, water_sprite.y - 2)

    def set_gate_color(self, gate_sprite: Sprite) -> None:
        if self.gate_can_open(gate_sprite):
            gate_sprite.color_remap(None, GATE_READY_COLOR)
            self._gate_ui.add_gate_marker(gate_sprite, self.camera.width)
        else:
            gate_sprite.color_remap(None, GATE_UNREADY_COLOR)
            self._gate_ui.remove_gate_marker(gate_sprite)

    def set_gate_colors(self) -> None:
        # Ensure all gates are marked as ready or not
        for wall in self._walls:
            if wall["gate"]:
                self.set_gate_color(wall["gate"])

    def flow_water(self, from_water: Sprite, to_water: Sprite) -> bool:
        """Returns whether flowing water was successful"""
        from_water_obj = self.get_water(from_water)
        if from_water_obj:
            max_height = from_water_obj["max_height"]
        else:
            max_height = self.camera.height

        to_water_obj = self.get_water(to_water)
        if to_water_obj:
            min_height = to_water_obj["min_height"]

            # If there is a duck on the water, lower the possible height
            if any(duck["water"] == to_water for duck in self._ducks):
                min_height += 2
        else:
            # Find the walls that bound `to_water`
            to_bounding_walls = self.get_walls_for_water(to_water)
            wall_height = max(w["wall"].y for w in to_bounding_walls)
            min_height = wall_height

        # If `from_water` is not empty and `to_water` is not going to spill over the wall
        if from_water.y < max_height and to_water.y > min_height:
            # Resize water sprites

            from_water.move(0, 1)
            new_pixels = from_water.pixels[:-1]
            from_water.pixels = new_pixels

            to_water.move(0, -1)
            tens_row = np.full((1, to_water.pixels.shape[1]), WATER_COLOR)
            new_pixels = np.vstack([to_water.pixels, tens_row])
            to_water.pixels = new_pixels

            # Ensure ducks are placed on top of water
            for duck in self._ducks:
                if from_water == duck["water"] or to_water == duck["water"]:
                    coords = self.get_coords_for_water(duck["water"])
                    duck["duck"].set_position(coords[0], coords[1])

            # Ensure all gates are marked as ready or not
            self.set_gate_colors()

            return True
        return False

    def use_pump(self, pump_sprite: Sprite) -> bool:
        """Returns whether the pump was used"""
        pump = self.get_pump(pump_sprite)

        return self.flow_water(pump["from_water"], pump["to_water"])

    def create_gate_animation(self, gate_sprite: Sprite) -> Animation:
        wall = self.get_wall_for_gate(gate_sprite)

        # Create the gate opening animation
        duck_lerps = []

        ducks_on_left = [duck for duck in self._ducks if duck["water"] == wall["water_left"]]
        ducks_on_right = [duck for duck in self._ducks if duck["water"] == wall["water_right"]]

        # Assign ducks to the opposite water and create a lerp animation
        for duck in ducks_on_left:
            duck["water"] = wall["water_right"]
            duck_lerps.append(Lerp(duck["duck"], self.get_coords_for_water(duck["water"])))

        for duck in ducks_on_right:
            duck["water"] = wall["water_left"]
            duck_lerps.append(Lerp(duck["duck"], self.get_coords_for_water(duck["water"])))

        # Create lerps for moving the gate up then down again
        gate_open_lerp = Lerp(gate_sprite, (gate_sprite.x, gate_sprite.y - gate_sprite.height))
        gate_close_lerp = Lerp(gate_sprite, (gate_sprite.x, gate_sprite.y))

        animation = Animation([gate_open_lerp] + duck_lerps + [gate_close_lerp])

        return animation

    def step(self) -> None:
        """Step the game forward based on the current action."""

        pump_was_used = False

        if self._current_animation:
            # If the animation is finished
            if self._current_animation.next():
                # Stop the animation
                self._current_animation = None

                # Ensure all gates are colored properly
                self.set_gate_colors()
            else:
                # If the animation is not finished, do not complete the action
                return
        else:
            if self.action.id == GameAction.ACTION6:
                # Get x, y from action.data dictionary
                x = self.action.data.get("x", 0)
                y = self.action.data.get("y", 0)

                # Convert display coords to game coords
                coords = self.camera.display_to_grid(x, y)
                if coords:
                    game_x, game_y = coords

                    sprite = self.current_level.get_sprite_at(game_x, game_y)
                    if sprite:
                        if "Pump" in sprite.tags:
                            pump_was_used = self.use_pump(sprite)
                        elif "Gate" in sprite.tags:
                            # If the gate can be opened, create an animation and do not complete the action
                            if self.gate_can_open(sprite):
                                self._current_animation = self.create_gate_animation(sprite)  # type: ignore
                                self._gate_ui.remove_gate_marker(sprite)
                                return

        # Check win condition
        if self.check_win_condition():
            self.next_level()
        # If a pump was used, deduct energy
        elif pump_was_used and not self._step_counter_ui.decrease_step():
            self.lose()

        self.complete_action()
