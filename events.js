function onPointerStop() {
    onPointerStopListener();
}

function onCanvasClick(e) {
    if (!clickingEnabled) {
        return;
    }
    if (autoplay) {
        stopAutoplay();
    }
    addShockwave(e.pageX, e.pageY);
    window._arc3_x = framePointerPosition.x;
    window._arc3_y = framePointerPosition.y;
    getActionButton(6).click();
    window._arc3_x = -1;
    window._arc3_y = -1;
}

function onCanvasMouseMove(e) {
    if (autoplay) {
        return;
    }
    framePointerPosition.x = clamp(Math.floor(e.offsetX / 8), 0, 63);
    framePointerPosition.y = clamp(Math.floor(e.offsetY / 8), 0, 63);

    if (clickingEnabled && currentFrame !== null && framePointerPosition.x !== prevFramePointerPosition && framePointerPosition.y !== prevFramePointerPosition) {
        drawFrame(currentFrame, currentBackgroundFrame1, currentBackgroundFrame2);

        prevFramePointerPosition.x = framePointerPosition.x;
        prevFramePointerPosition.y = framePointerPosition.y;
    }
}

function _onCanvasMouseLeave(e) {
    framePointerPosition.x = -1;
    framePointerPosition.y = -1;

    prevFramePointerPosition.x = -1;
    prevFramePointerPosition.y = -1;

    if (clickingEnabled && currentFrame !== null) {
        drawFrame(currentFrame, currentBackgroundFrame1, currentBackgroundFrame2);
    }
}

function onCanvasMouseLeave(e) {
    if (autoplay) {
        return;
    }
    framePointerPosition.x = -1;
    framePointerPosition.y = -1;

    prevFramePointerPosition.x = -1;
    prevFramePointerPosition.y = -1;

    if (clickingEnabled && currentFrame !== null) {
        drawFrame(currentFrame, currentBackgroundFrame1, currentBackgroundFrame2);
    }
}

document.addEventListener('keydown', (e) => {
    switch (e.key) {
        case '1':
        case 'w':
        case 'W':
        case 'ArrowUp':
        case '2':
        case 's':
        case 'S':
        case 'ArrowDown':
        case '3':
        case 'a':
        case 'A':
        case 'ArrowLeft':
        case '4':
        case 'd':
        case 'D':
        case 'ArrowRight':
        case '5':
        case ' ':
        case 'z':
        case 'Z':
        case ' ':
            e.preventDefault();
            break;
    }
});

document.addEventListener('keyup', (e) => {
    let fn = (action) => {
        e.preventDefault();

        if (autoplay && e.isTrusted) {
            stopAutoplay();
        }
        getActionButton(action).click();
    };
    switch (e.key) {
        case '1':
        case 'w':
        case 'W':
        case 'ArrowUp':
            fn(1);
            break;
        case '2':
        case 's':
        case 'S':
        case 'ArrowDown':
            fn(2);
            break;
        case '3':
        case 'a':
        case 'A':
        case 'ArrowLeft':
            fn(3);
            break;
        case '4':
        case 'd':
        case 'D':
        case 'ArrowRight':
            fn(4);
            break;
        case '5':
        case ' ':
            fn(5);
            break;
        case 'z':
        case 'Z':
        case ' ':
            fn(7);
            break;
    }
});

document.getElementById('button_download_game').addEventListener('click', downloadGame);

let link_timed_out = false;

document.getElementById('button_copy_link').addEventListener('click', () => {
    if (metadata === null || link_timed_out) {
        return;
    }
    navigator.clipboard.writeText(`${window.location.protocol}//${window.location.host}/#${metadata.game_id}`).then(() => {
        let span = document.getElementById('link_copied');

        span.innerText = 'Link copied';

        link_timed_out = true;

        window.setTimeout(() => {
            span.innerText = '';
            link_timed_out = false;
        }, 2000);
    });
});

if(!window._arc3_offline){
    document.getElementById('button_autoplay_all').addEventListener('click', () => {
        if (autoplay) {
            if (autoplayAll) {
                stopAutoplay();
            } else {
                autoplayAll = true;
                document.getElementById('button_autoplay_level').classList.remove('active');
                document.getElementById('button_autoplay_all').classList.add('active');
            }
        } else if(window._arc3_busy){
            autoplayAll = true;
            document.getElementById('button_autoplay_all').classList.add('active');
            startAutoplay();
        }
    });

    document.getElementById('button_autoplay_level').addEventListener('click', () => {
        if (autoplay) {
            if (!autoplayAll) {
                stopAutoplay();
            } else {
                autoplayAll = false;
                document.getElementById('button_autoplay_all').classList.remove('active');
                document.getElementById('button_autoplay_level').classList.add('active');
            }
        } else if(!window._arc3_busy){
            autoplayAll = false;
            document.getElementById('button_autoplay_level').classList.add('active');
            startAutoplay();
        }
    });
    document.getElementById('button_autoplay_min').addEventListener('click', () => {
        autoplayDelay += 0.25;
        autoplayDelay = Math.min(15, autoplayDelay);
        document.getElementById('autoplay_fps').innerText = `${Math.round(1 / (1 + autoplayDelay) * 100)}%`;
    });
    document.getElementById('button_autoplay_plus').addEventListener('click', () => {
        autoplayDelay -= 0.25;
        autoplayDelay = Math.max(0, autoplayDelay);
        document.getElementById('autoplay_fps').innerText = `${Math.round(1 / (1 + autoplayDelay) * 100)}%`;
    });
    document.getElementById('autoplay_fps').innerText = `${Math.round(1 / (1 + autoplayDelay) * 100)}%`;
}

for (let i = 0; i < 8; i++) {
    let button = getActionButton(i);

    button.addEventListener('click', (e) => {
        if (autoplay && e.isTrusted) {
            stopAutoplay();
        }
    });
}