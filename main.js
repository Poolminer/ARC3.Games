let metadata = null;

let levelsCompleted = 0;
let levelsTotal = 0;
let availableActions = [];

let gameState = "NOT_PLAYED";

let transitionFrames = generateTransitionFrames(14);
let fadeFrames = generateTransitionFrames(5, false);

let blackFrame = createFrame(5);

let clickingEnabled = false;

let autoplay = false;
let autoplayAll = false;
let autoplayActions = [];
let autoplayActionIndex = 0;
let autoplayDelay = 2;

let levelActionSequence = [];
let fullActionSequence = [];

let animationRenderTimeoutId = -1;

let transitionAntimationFPS = 12;

let onPointerStopListener = nextAutoplayAction;

window._arc3_x = -1;
window._arc3_y = -1;

window._arc3_busy = false;

window._arc3_init_id = 'ls20-9607627b';
window._arc3_init_meta = './environment_files/ls20/9607627b/metadata.json';

window.print = window.console.log;

let clamp = (num, min, max) => Math.min(Math.max(num, min), max);

function getElementBoundingRect(element){
    let rect = element.getBoundingClientRect();

    let absoluteRect = {
        top: rect.top + window.scrollY,
        left: rect.left + window.scrollX,
        right: rect.right + window.scrollX,
        bottom: rect.bottom + window.scrollY,
        width: rect.width,
        height: rect.height
    };
    return absoluteRect;
}

function getFPS() {
    if (metadata === null) {
        return 10;
    }
    if (metadata.default_fps !== undefined) {
        return metadata.default_fps;
    }
    return 10;
}

function getAutoplayActionIndex() {
    if(levelActionSequence.length >= autoplayActions.length){
        return -1;
    }
    for (let i = 0; i < levelActionSequence.length; i++) {
        let a1 = levelActionSequence[i];
        let a2 = autoplayActions[i];

        if (typeof a1 !== typeof a2) {
            return -1;
        }
        if (typeof a1 === 'object') {
            if (a1[0] !== a2[0] || a1[1] !== a2[1]) {
                return -1;
            }
        } else if (levelActionSequence[i] !== autoplayActions[i]) {
            return -1;
        }
    }
    return levelActionSequence.length;
}

function getAutoplay(start = false) {
    if(window._arc3_offline){
        return;
    }
    apiGetSequence((seq) => {
        if (seq === null) {
            autoplayActions = [];
            autoplayActionIndex = 0;
            stopAutoplay();
            return;
        }
        autoplayActions = seq;
        autoplayActionIndex = 0;
        document.getElementById('button_autoplay_all').disabled = false;
        document.getElementById('button_autoplay_level').disabled = false;

        scorecardEnter();

        if (!autoplay && start) {
            startAutoplay();
        }
    });
    apiGetLevelStats((stats) => {
        if (stats === null) {
            return;
        }
        document.getElementById('level_stats').innerText = `Level ${levelsCompleted + 1} of ${metadata.game_id} has ${stats.numSequences} action sequence${stats.numSequences === 1 ? '' : 's'} on record.`;
    });
    if(!window._arc3_offline && !autoplay){
        window.setTimeout(() => {
            updateStats();
        }, 3000);
    }
}

function giveCredits(){
    for(let gallery of library){
        if(gallery.ids.includes(metadata.game_id)){
            let authors = gallery.authors[metadata.game_id];

            if(authors === undefined){
                authors = gallery.authors['default'];
            }
            if(authors.length > 1){
                let html = 'Authors: ';

                for(let i=0; i<authors.length; i++){
                    let author = authors[i];

                    html += author;

                    if(i !== authors.length-1){
                        html += ', ';
                    }
                }
                document.getElementById('authors').innerHTML = html;
            } else {
                document.getElementById('authors').innerHTML = `Author: ${authors[0]}`;
            }
            return;
        }
    }
    document.getElementById('credits').innerHTML = '';
}

function onNewGame() {
    window.clearTimeout(animationRenderTimeoutId);
    window._arc3_busy = false;

    stopAutoplay();

    window.history.replaceState(null, '', `#${metadata.game_id}`)

    document.getElementById('game_title').innerText = metadata.game_id;

    document.getElementById('button_reset').disabled = false;

    giveCredits();

    getAutoplay();
}

function onReset(){
    levelActionSequence.length = 0;

    enableAvailableActionButtons();
    
    clickingEnabled = availableActions.includes(6);
    canvas.style.cursor = clickingEnabled ? 'default' : 'not-allowed';
}

function onFullReset() {
    onReset();

    fullActionSequence.length = 0;

    if (levelsCompleted > 0) {
        levelsCompleted = 0;
        getAutoplay();
    } else {
        levelsCompleted = 0;
    }
    updateLevelText();
    scorecardReset();
}

function setMetadata(data, numLevels, availableActionsJSON) {
    metadata = JSON.parse(data);

    levelsCompleted = 0;
    levelsTotal = numLevels;
    availableActions = JSON.parse(availableActionsJSON);

    onNewGame(metadata);
}

function getNextAutoplayAction() {
    let action = autoplayActions[autoplayActionIndex];

    return action;
}

function nextAutoplayAction() {
    if (!autoplay) {
        return;
    }
    if (hoverTarget !== null) {
        applyButtonDownStyle(hoverTarget);
        hoverTarget = null;
    }
    let action = autoplayActions[autoplayActionIndex++];

    if (action !== undefined) {
        if (typeof action === 'object') {
            window._arc3_x = action[0];
            window._arc3_y = action[1];

            let rect = getElementBoundingRect(canvas);

            let x = rect.left + action[0] * 8 + 4;
            let y = rect.top + action[1] * 8 + 4;

            addShockwave(x, y);

            getActionButton(6).click();

            window._arc3_x = -1;
            window._arc3_y = -1;
        } else {
            if (getActionButton(action).disabled) {
                nextAutoplayAction();
                return;
            }
            getActionButton(action).click();
        }
    } else {
        stopAutoplay();
    }
}

function startAutoplay() {
    autoplay = true;

    autoplayActionIndex = getAutoplayActionIndex();

    let nextAction = getNextAutoplayAction();
    if (typeof nextAction === 'object') {
        let rect = getElementBoundingRect(canvas);

        movePointer({
            "x": rect.left + nextAction[0] * 8 + 4,
            "y": rect.top + nextAction[1] * 8 + 4
        }, autoplayDelay);
    } else {
        let button = getActionButton(nextAction);

        pointerHoverElement(button, autoplayDelay);
    }
}

function checkAutoplayAvailability() {
    if(window._arc3_offline){
        return;
    }
    let available = gameState === 'NOT_FINISHED' && autoplayActions.length !== 0 && getAutoplayActionIndex() !== -1;

    document.getElementById('button_autoplay_all').disabled = !available;
    document.getElementById('button_autoplay_level').disabled = !available;
}

function stopAutoplay() {
    if (!autoplay) {
        return;
    }
    autoplay = false;

    var button = document.getElementById('button_autoplay_all');
    button.classList.remove('active');

    var button = document.getElementById('button_autoplay_level');
    button.classList.remove('active');

    checkAutoplayAvailability();

    movePointer({
        "x": -32,
        "y": -32
    }, autoplayDelay);
}

function actionResult(data) {
    let frameData = JSON.parse(data);
    let frames = frameData.frame;
    let backgroundFrame1;
    let backgroundFrame2;
    let fps = getFPS();
    let won = frameData.state === 'WIN';
    let lost = frameData.state === 'GAME_OVER';

    gameState = frameData.state;

    if (frameData.action_input.id === 0) {
        levelActionSequence.length = 0;

        if (frameData.full_reset) {
            onFullReset();
        } else {
            onReset();
        }
    } else if (frameData.action_input.id === 6) {
        levelActionSequence.push([frameData.action_input.data.x, frameData.action_input.data.y]);
    } else {
        levelActionSequence.push(frameData.action_input.id);
    }
    checkAutoplayAvailability();
    scorecardRefresh();

    if (frameData.levels_completed > levelsCompleted) {
        fullActionSequence = fullActionSequence.concat(levelActionSequence);

        levelActionSequence.length = 0;

        submitSequence(metadata.game_id, fullActionSequence, frameData.state);
    }
    if (lost || won) {
        clickingEnabled = false;
        disableButtons();
        frames = frameData.frame.slice(0, frameData.frame.length - 1).concat(fadeFrames);
        backgroundFrame1 = frameData.frame[frameData.frame.length - 1];
        backgroundFrame2 = blackFrame;
        scorecardClose();
    } else {
        if (frameData.levels_completed > levelsCompleted) {
            levelsCompleted = frameData.levels_completed;
            updateLevelText();
            frames = frameData.frame.slice(0, frameData.frame.length - 2).concat(transitionFrames);
            backgroundFrame1 = frameData.frame[frameData.frame.length - 2];
            backgroundFrame2 = frameData.frame[frameData.frame.length - 1];

            if (autoplay) {
                if (!autoplayAll) {
                    stopAutoplay();
                }
                getAutoplay(autoplayAll);
            } else {
                getAutoplay();
            }
        }
    }
    let autoplayFn = () => {
        let nextAction = getNextAutoplayAction();

        if (nextAction !== undefined) {
            if (typeof nextAction === 'object') {
                let rect = getElementBoundingRect(canvas);

                movePointer({
                    "x": rect.left + nextAction[0] * 8 + 4,
                    "y": rect.top + nextAction[1] * 8 + 4
                }, autoplayDelay);
            } else {
                let button = getActionButton(nextAction);

                pointerHoverElement(button, autoplayDelay);
            }
        } else {
            stopAutoplay();
        }
    };
    let idx = 0;

    let renderNextFrame = () => {
        let frame = frames[idx++];

        drawFrame(frame, backgroundFrame1, backgroundFrame2);

        if (idx === frames.length) {
            window._arc3_busy = false;

            if (won) {
                drawVictory();
            } else if (lost) {
                drawGameOver();
            }
            if (autoplay) {
                autoplayFn();
            }
        } else {
            animationRenderTimeoutId = window.setTimeout(renderNextFrame, 1000 / (frame.isTrans ? transitionAntimationFPS : fps));
        }
    };
    renderNextFrame();
}