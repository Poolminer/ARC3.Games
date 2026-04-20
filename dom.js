function createGallery() {
    for (let entry of library) {
        let title = document.createElement("h2");
        title.innerText = entry.title;
        document.body.appendChild(title);

        if (entry.description) {
            let description = document.createElement("p");
            description.innerHTML = entry.description;
            document.body.appendChild(description);
        }
        let gallery = document.createElement("div");
        gallery.className = 'gallery';

        let idx = 0;

        for (let id of entry.ids) {
            if (idx++ % 5 === 0) {
                let br = document.createElement("br");
                gallery.appendChild(br);
            }
            let thumbnail = document.createElement("div");
            thumbnail.className = 'thumbnail';

            let split = id.split('-')
            let name = split[0]
            let version = split[1]

            let namecard = document.createElement("div");
            namecard.className = 'namecard';
            namecard.innerText = name

            thumbnail.appendChild(namecard);

            let img = document.createElement("img");
            img.width = 110;
            img.height = 110;
            img.src = `./thumbnails/${id}.png`;

            thumbnail.appendChild(img);

            let metaUrl = `./environment_files/${name}/${version}/metadata.json`;

            thumbnail.addEventListener('mousedown', () => {
                window._arc3_game_id = id;
                window._arc3_game_meta = metaUrl;
            });
            thumbnail.setAttribute('py-click', `on_thumbnail_click`);

            thumbnail.addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    behavior: "smooth"
                });
            });

            if (id === window.location.hash.substring(1)) {
                window._arc3_init_id = id;
                window._arc3_init_meta = metaUrl;
            }
            thumbnail.title = id;
            gallery.appendChild(thumbnail);
        }
        document.body.appendChild(gallery);
    }
}

function createCanvas() {
    canvas_buffer = document.createElement('canvas');
    canvas_buffer.width = 512;
    canvas_buffer.height = 512;

    canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 512;
    canvas.style.width = '512px';
    canvas.style.height = '512px';
    canvas.style.padding = '0';

    canvas.style.borderRadius = '16px';

    canvas.style.position = 'absolute';

    canvas.addEventListener('click', onCanvasClick);
    canvas.addEventListener('mousemove', onCanvasMouseMove);
    canvas.addEventListener('mouseleave', onCanvasMouseLeave);

    document.getElementById('div2').appendChild(canvas);

    ctx_buffer = canvas_buffer.getContext("2d");
    ctx_canvas = canvas.getContext("2d");

    ctx_canvas.imageSmoothingEnabled = false;

    drawFrame(blackFrame);

    drawLoading();
}

let lastCanvasClick = 0;

let lastClickFramePointerPosition = {
    "x": -1,
    "y": -1
};

function addShockwave(x, y) {
    let d = Date.now() - lastCanvasClick;

    let same = lastClickFramePointerPosition.x === framePointerPosition.x && lastClickFramePointerPosition.y === framePointerPosition.y;

    lastClickFramePointerPosition.x = framePointerPosition.x;
    lastClickFramePointerPosition.y = framePointerPosition.y;

    lastCanvasClick = Date.now();

    const wave = document.createElement("div");

    if (d < 500 && same) {
        wave.className = "shockwave red";
    } else {
        wave.className = "shockwave";
    }
    wave.style.left = `${x}px`;
    wave.style.top = `${y}px`;

    document.body.appendChild(wave);

    wave.addEventListener("animationend", () => {
        wave.remove();
    });
}

function getActionButton(action) {
    switch (action) {
        case 0:
            return document.getElementById('button_reset');
        case 1:
            return document.getElementById('button_up');
        case 2:
            return document.getElementById('button_down');
        case 3:
            return document.getElementById('button_left');
        case 4:
            return document.getElementById('button_right');
        case 5:
            return document.getElementById('button_spacebar');
        case 6:
            return document.getElementById('button_click');
        case 7:
            return document.getElementById('button_undo');
    }
}

function disableButtons() {
    for (let a of [1, 2, 3, 4, 5, 6, 7]) {
        getActionButton(a).disabled = true;
    }
}

function enableAvailableActionButtons() {
    disableButtons();

    for (let action of availableActions) {
        let button = getActionButton(action);

        button.disabled = false;
    }
}

function updateLevelText() {
    document.getElementById('game_level_info').innerText = `LEVEL ${levelsCompleted + 1} / ${levelsTotal}`;
}

function applyButtonDownStyle(button) {
    button.pressedAt = Date.now();
    button.classList.add('active');
}

function removeExpiredButtonDownStyles() {
    let buttons = document.getElementsByTagName('button');

    for (let button of buttons) {
        if (button.id.includes('autoplay')) {
            continue;
        }
        if (button.pressedAt !== undefined) {
            let d = Date.now() - button.pressedAt;

            if (d > 85) {
                button.classList.remove('active');
            }
        }
    }
}
window.setInterval(removeExpiredButtonDownStyles, 25);

let updateStats = () => {
    apiGetStatsSum((stats) => {
        if (stats === null) {
            return;
        }
        document.getElementById('games_stats').innerHTML = `There are ${stats.numGames} games, with a total of ${stats.numLevels} levels.<br>There are ${stats.numSequences} action sequences on record.`;
    });
};
if(!window._arc3_offline){
    updateStats();
}