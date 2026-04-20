import json

from arcengine import GameAction, ActionInput, GameState
from pyscript import web, when
from pyscript import window

from importlib import import_module

game = None

def load_game_class(full_id: str) -> type:
    game_id, version_id = full_id.split("-", 1)
    module_name = f"environment_files.{game_id}.{version_id}.{game_id}"
    class_name = game_id.capitalize()
    module = import_module(module_name)

    return getattr(module, class_name)

def perform_simple_action(action: GameAction):
    if game is None or window._arc3_busy:
        return
    
    window._arc3_busy = True

    action_input = ActionInput(id=action)

    frame_data = game.perform_action(action_input)

    window.actionResult(str(frame_data))

def perform_complex_action(x: int, y: int):
    if game is None or window._arc3_busy:
        return
    
    window._arc3_busy = True

    action_input = ActionInput(id=GameAction.ACTION6)

    action_input.data = {
        "x": x,
        "y": y
    }
    frame_data = game.perform_action(action_input)

    window.actionResult(str(frame_data))

def init_game(id: str, metadata_file: str):
    global game

    game = load_game_class(id)()

    with open(metadata_file, 'r') as file:
        num_levels = len(game._levels)

        window.setMetadata(file.read(), num_levels, json.dumps(game._available_actions))

    perform_simple_action(GameAction.RESET)

def on_thumbnail_click(_):
    init_game(window._arc3_game_id, window._arc3_game_meta)

@when("click", "#button_up")
def button_up(_):
    perform_simple_action(GameAction.ACTION1)

@when("click", "#button_down")
def button_up(_):
    perform_simple_action(GameAction.ACTION2)

@when("click", "#button_left")
def button_up(_):
    perform_simple_action(GameAction.ACTION3)

@when("click", "#button_right")
def button_up(_):
    perform_simple_action(GameAction.ACTION4)

@when("click", "#button_spacebar")
def button_up(_):
    perform_simple_action(GameAction.ACTION5)

@when("click", "#button_click")
def button_up(_):
    if window._arc3_x == -1:
        return
    perform_complex_action(window._arc3_x, window._arc3_y)

@when("click", "#button_undo")
def button_up(_):
    perform_simple_action(GameAction.ACTION7)

@when("click", "#button_reset")
def button_up(_):
    perform_simple_action(GameAction.RESET)

init_game(window._arc3_init_id, window._arc3_init_meta)