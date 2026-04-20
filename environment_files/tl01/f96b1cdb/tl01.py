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

from typing import Any

from arcengine import ARCBaseGame, Camera, GameAction, Level, Sprite

# Create sprites dictionary with all sprite definitions
sprites = {
    "Box": Sprite(
        pixels=[
            [8],
        ],
        name="Box",
        visible=True,
        collidable=True,
    ),
    "Gate": Sprite(
        pixels=[
            [12],
            [12],
            [12],
        ],
        name="Gate",
        visible=True,
        collidable=True,
    ),
    "Goal": Sprite(
        pixels=[
            [11],
        ],
        name="Goal",
        visible=True,
        collidable=True,
        layer=-1,
    ),
    "Level1": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="Level1",
        visible=True,
        collidable=True,
    ),
    "Level2": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -1, -1, -1, 4, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, 4, 4, 4, -1, 4],
            [4, -1, -1, -1, -1, -1, 4, -1, -1, -1, 4],
            [4, 4, 4, -1, 4, -1, -1, -1, -1, -1, 4],
            [4, -1, 4, -1, 4, 4, 4, -1, 4, 4, 4],
            [4, -1, -1, -1, 4, -1, -1, -1, -1, -1, 4],
            [4, -1, 4, 4, 4, -1, 4, -1, -1, -1, 4],
            [4, -1, -1, 4, -1, -1, 4, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, 4, -1, -1, -1, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="Level2",
        visible=True,
        collidable=True,
    ),
    "Level3": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="Level3",
        visible=True,
        collidable=True,
    ),
    "Level4": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, -1, -1, -1, -1, -1, 4, 4, 4],
            [4, 4, 4, -1, -1, -1, -1, -1, 4, 4, 4],
            [4, 4, 4, -1, -1, -1, -1, -1, 4, 4, 4],
            [4, 4, 4, -1, -1, -1, -1, -1, 4, 4, 4],
            [4, 4, 4, -1, -1, -1, -1, -1, 4, 4, 4],
            [4, 4, 4, -1, -1, -1, -1, -1, 4, 4, 4],
            [4, 4, 4, -1, -1, -1, -1, -1, 4, 4, 4],
            [4, 4, 4, -1, -1, -1, -1, -1, 4, 4, 4],
            [4, 4, 4, -1, -1, -1, -1, -1, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="Level4",
        visible=True,
        collidable=True,
    ),
    "Level5": Sprite(
        pixels=[
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, -1, -1, -1, -1, 4, -1, -1, -1, -1, 4],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        ],
        name="Level5",
        visible=True,
        collidable=True,
    ),
    "Player": Sprite(
        pixels=[
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        name="Player",
        visible=True,
        collidable=True,
    ),
}

# Create levels array with all level definitions
levels = [
    # Level 1
    Level(
        sprites=[
            sprites["Goal"].clone().set_position(29, 17).set_scale(6),
            sprites["Level1"].clone().set_position(-1, -1).set_scale(6),
            sprites["Player"].clone().set_position(30, 36),
        ],
        grid_size=(64, 64),
    ),
    # Level 2
    Level(
        sprites=[
            sprites["Goal"].clone().set_position(47, 47).set_scale(6),
            sprites["Level2"].clone().set_position(-1, -1).set_scale(6),
            sprites["Player"].clone().set_position(12, 12),
        ],
        grid_size=(64, 64),
    ),
    # Level 3
    Level(
        sprites=[
            sprites["Gate"].clone().set_position(29, 23).set_scale(6),
            sprites["Goal"].clone().set_position(47, 47).set_scale(6),
            sprites["Level3"].clone().set_position(-1, -1).set_scale(6),
            sprites["Player"].clone().set_position(12, 12),
        ],
        grid_size=(64, 64),
    ),
    # Level 4
    Level(
        sprites=[
            sprites["Box"].clone().set_position(29, 23).set_scale(6),
            sprites["Box"].clone().set_position(35, 23).set_scale(6),
            sprites["Box"].clone().set_position(41, 23).set_scale(6),
            sprites["Box"].clone().set_position(23, 23).set_scale(6),
            sprites["Box"].clone().set_position(17, 23).set_scale(6),
            sprites["Goal"].clone().set_position(29, 47).set_scale(6),
            sprites["Level4"].clone().set_position(-1, -1).set_scale(6),
            sprites["Player"].clone().set_position(30, 12),
        ],
        grid_size=(64, 64),
    ),
    # Level 5
    Level(
        sprites=[
            sprites["Goal"].clone().set_position(17, 35).set_scale(6),
            sprites["Goal"].clone().set_position(53, 35).set_scale(6),
            sprites["Goal"].clone().set_position(41, 17).set_scale(6),
            sprites["Goal"].clone().set_position(23, 23).set_scale(6),
            sprites["Level5"].clone().set_position(-1, -1).set_scale(6),
            sprites["Player"].clone().set_position(12, 12),
            sprites["Player"].clone().set_position(54, 12),
            sprites["Player"].clone().set_position(36, 42),
            sprites["Player"].clone().set_position(12, 48),
        ],
        grid_size=(64, 64),
    ),
]

BACKGROUND_COLOR = 9

PADDING_COLOR = 9


class Tl01(ARCBaseGame):
    def __init__(self) -> None:
        camera = Camera(background=BACKGROUND_COLOR, letter_box=PADDING_COLOR)
        self.animation_frames = 0
        self.animation_dx = 0
        self.animation_dy = 0
        self.start_x = 0
        self.start_y = 0
        self.selected_player_index = 0

        # Action history for undo
        self.action_history: list[dict[str, Any]] = []

        super().__init__(
            game_id="tl01",
            levels=levels,
            camera=camera,
            available_actions=[1, 2, 3, 4, 5, 6, 7],
        )

    def step(self) -> None:
        # Handle animation
        if self.animation_frames > 0:
            players = self.current_level.get_sprites_by_name("Player")
            if players:
                player = players[self.selected_player_index]
                step_x = self.animation_dx
                step_y = self.animation_dy
                player.move(step_x, step_y)
                self.animation_frames -= 1

                if self.animation_frames == 0:
                    # Check if ALL players are on goals
                    if self._all_players_on_goals():
                        self.next_level()
                    self.complete_action()
            return

        # Handle new actions
        dx, dy = 0, 0
        if self.action.id == GameAction.ACTION1:  # Up
            dy = -6
        elif self.action.id == GameAction.ACTION2:  # Down
            dy = 6
        elif self.action.id == GameAction.ACTION3:  # Left
            dx = -6
        elif self.action.id == GameAction.ACTION4:  # Right
            dx = 6
        elif self.action.id == GameAction.ACTION5:  # Toggle gates
            gates = self.current_level.get_sprites_by_name("Gate")
            for gate in gates:
                if gate.rotation == 0:
                    gate.set_rotation(90)
                else:
                    gate.set_rotation(0)
            # Track this action
            self.action_history.append({"type": "toggle_gates"})
            self.complete_action()
            return
        elif self.action.id == GameAction.ACTION6:  # Click to select player or remove box
            x = self.action.data["x"]
            y = self.action.data["y"]

            grid_coords = self.camera.display_to_grid(x, y)
            if grid_coords:
                gx, gy = grid_coords
                clicked_sprite = self.current_level.get_sprite_at(gx, gy)

                if clicked_sprite and clicked_sprite.name == "Player":
                    # Player selection
                    players = self.current_level.get_sprites_by_name("Player")
                    clicked_index = players.index(clicked_sprite)

                    # Track old selection
                    old_index = self.selected_player_index

                    # Deselect old player (set to ID 1)
                    if players:
                        players[old_index].color_remap(None, 2)

                    # Select new player (set to ID 0)
                    self.selected_player_index = clicked_index
                    clicked_sprite.color_remap(None, 0)

                    self.action_history.append({"type": "select_player", "old_index": old_index, "new_index": clicked_index})
                elif clicked_sprite and clicked_sprite.name.startswith("Box"):
                    # Track removed box info before removing
                    self.action_history.append(
                        {
                            "type": "remove_box",
                            "box": clicked_sprite.clone(),  # Save the box
                        }
                    )
                    self.current_level.remove_sprite(clicked_sprite)
                else:
                    # No box removed or player selected, track as no-op
                    self.action_history.append({"type": "no_op"})
            self.complete_action()
            return
        elif self.action.id == GameAction.ACTION7:  # Undo
            if self.action_history:
                last_action = self.action_history.pop()

                if last_action["type"] == "move":
                    # Reverse the movement
                    players = self.current_level.get_sprites_by_name("Player")
                    if players:
                        player = players[last_action["player_index"]]
                        player.move(-last_action["dx"], -last_action["dy"])
                elif last_action["type"] == "toggle_gates":
                    # Toggle gates again (same as action 5)
                    gates = self.current_level.get_sprites_by_name("Gate")
                    for gate in gates:
                        if gate.rotation == 0:
                            gate.set_rotation(90)
                        else:
                            gate.set_rotation(0)
                elif last_action["type"] == "remove_box":
                    # Put the box back
                    self.current_level.add_sprite(last_action["box"])
                elif last_action["type"] == "select_player":
                    # Restore previous selection
                    players = self.current_level.get_sprites_by_name("Player")
                    if players:
                        # Deselect current
                        players[last_action["new_index"]].color_remap(None, 2)
                        # Reselect old
                        players[last_action["old_index"]].color_remap(None, 0)
                        self.selected_player_index = last_action["old_index"]
                # no_op doesn't need reversal

            self.complete_action()
            return
        else:
            self.complete_action()
            return

        # Movement logic
        if dx != 0 or dy != 0:
            players = self.current_level.get_sprites_by_name("Player")
            if players:
                player = players[self.selected_player_index]

                # Check collision by temporarily moving
                original_x = player.x
                original_y = player.y
                player.move(dx, dy)

                # Check for collisions at new position
                wall_collision = False
                for sprite in self.current_level.get_sprites():
                    if sprite != player and sprite.name != "Goal" and player.collides_with(sprite):
                        wall_collision = True
                        break

                # Move back to original position
                player.set_position(original_x, original_y)

                if not wall_collision:
                    # Track successful movement
                    self.action_history.append({"type": "move", "dx": dx, "dy": dy, "player_index": self.selected_player_index})
                    self.animation_frames = 6
                    self.animation_dx = dx // 6
                    self.animation_dy = dy // 6
                else:
                    # Failed move, track as no-op
                    self.action_history.append({"type": "no_op"})
                    self.complete_action()
            else:
                self.complete_action()
        else:
            self.complete_action()

    def _all_players_on_goals(self) -> bool:
        """Check if all players are currently on goals."""
        players = self.current_level.get_sprites_by_name("Player")
        goals = self.current_level.get_sprites_by_name("Goal")

        if not players or not goals:
            return False

        # Check that every player is on at least one goal
        for player in players:
            player_on_goal = False
            for goal in goals:
                if player.collides_with(goal):
                    player_on_goal = True
                    break
            if not player_on_goal:
                return False

        return True

    def on_set_level(self, level: Level) -> None:
        self.animation_frames = 0
        self.animation_dx = 0
        self.animation_dy = 0
        # Clear action history when changing levels
        self.action_history = []

        # Auto-select player closest to 0,0
        players = level.get_sprites_by_name("Player")
        if players:
            # Find closest player to 0,0
            min_distance = float("inf")
            closest_index = 0
            for i, player in enumerate(players):
                distance = (player.x**2 + player.y**2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_index = i

            # Set all players to ID 2 (unselected), except the selected one to ID 0
            for i, player in enumerate(players):
                if i == closest_index:
                    player.color_remap(None, 0)
                else:
                    player.color_remap(None, 2)

            self.selected_player_index = closest_index