# ARC3.Games: Browser-Based ARCEngine Game Player

Play [ARC-AGI-3](https://arcprize.org/arc-agi/3) and custom [ARCEngine](https://github.com/arcprize/ARCEngine) games.

ARC3.Games creates a virtual Python environment in the browser using [PyScript](https://pyscript.net/), with a minimal `main.py` to expose the Python game to JavaScript.

ARC3.Games can be accessed in "online" mode, where it connects to the database hosted at [https://arc3.games/](https://arc3.games/) for getting autoplay data, statistics, and submitting gameplay, or it can be served in "offline" mode, where it does none of that, but still gets the Python stuff through the CDN of PyScript.

Once you have cloned the repo, do

`python serve.py`

to serve your local copy at port 8000.

Then either go to `index.html` for online mode, or `index_offline.html` for offline mode.

When you (re)load the web page, the browser will request file `pyscript.json`, which defines the required Python packages, and which files to include in the virtual Python environment. `serve.py` serves a virtual `pyscript.json`, where it includes everyting (except specified ignores) in `./environment_files`. So make sure not to put excessively large or many files in it. The script also maintains a physical copy of `pyscript.json`, for when you want to serve it from a static site.