let palette = ['#FFFFFF', '#CCCCCC', '#999999', '#666666', '#333333', '#000000', '#E53AA3', '#FF7BCC', '#F93C31', '#1E93FF', '#88D8F1', '#FFDC00', '#FF851B', '#921231', '#4FCC30', '#A356D6'];

let canvas_buffer = null;
let canvas = null;
let ctx_buffer = null;
let ctx_canvas = null;

let currentFrame = null;
let currentBackgroundFrame1 = null
let currentBackgroundFrame2 = null;

function createFrame(color) {
    let frame = [];

    for (let y = 0; y < 64; y++) {
        frame.push(new Array(64).fill(color));
    }
    return frame;
}

function generateTransitionFrames(color, addSecond = true) {
    let initialRadius = Math.sqrt(2048);
    let numSteps = 8;
    let stepSize = initialRadius / numSteps;
    let frames = [];

    let addFrame = (step, val) => {
        let radius = step * stepSize;
        let frame = createFrame(0);

        frame.isTrans = true;

        for (let x = 0; x < 64; x++) {
            for (let y = 0; y < 64; y++) {
                let _x = x - 32 + 0.5;
                let _y = y - 32 + 0.5;

                let d = Math.sqrt(_x ** 2 + _y ** 2);

                if (d <= radius) {
                    frame[y][x] = val;
                } else {
                    frame[y][x] = color;
                }
            }
        }
        frames.push(frame);
    }
    for (let i = numSteps; i > -1; i--) {
        addFrame(i, -1);
    }
    if (addSecond) {
        for (let i = 0; i <= numSteps; i++) {
            addFrame(i, -2);
        }
    }
    return frames;
}

function drawFrame(frame, backgroundFrame1, backgroundFrame2) {
    currentFrame = frame;
    currentBackgroundFrame1 = backgroundFrame1;
    currentBackgroundFrame2 = backgroundFrame2;

    ctx_canvas.clearRect(0, 0, 512, 512);
    ctx_buffer.clearRect(0, 0, 512, 512);

    let px = -16;
    let py = -16;

    for (let x = 0; x < 64; x++) {
        for (let y = 0; y < 64; y++) {
            let color = frame[y][x];

            if (color === -1) {
                color = backgroundFrame1[y][x];
            } else if (color === -2) {
                color = backgroundFrame2[y][x];
            }
            ctx_buffer.fillStyle = palette[color];
            ctx_buffer.fillRect(x * 8, y * 8, 8, 8);

            if (framePointerPosition.x === x && framePointerPosition.y === y) {
                px = framePointerPosition.x * 8;
                py = framePointerPosition.y * 8;
            }
        }
    }
    ctx_buffer.strokeStyle = '#88888866';
    ctx_buffer.lineWidth = 0.5;

    for (let x = 0; x < 64; x++) {
        ctx_buffer.beginPath();
        ctx_buffer.moveTo(x * 8 + 0.5, 0 + 0.5);
        ctx_buffer.lineTo(x * 8 + 0.5, 512 + 0.5);
        ctx_buffer.stroke();
    }
    for (let y = 0; y < 64; y++) {
        ctx_buffer.beginPath();
        ctx_buffer.moveTo(0 + 0.5, y * 8 + 0.5);
        ctx_buffer.lineTo(512 + 0.5, y * 8 + 0.5);
        ctx_buffer.stroke();
    }
    if (clickingEnabled) {
        ctx_buffer.strokeStyle = '#FFFFFF';
        ctx_buffer.beginPath();
        ctx_buffer.rect(px - 1 + 0.5, py - 1 + 0.5, 10, 10);
        ctx_buffer.stroke();
    }
    ctx_canvas.drawImage(canvas_buffer, 0, 0);
}

function drawVictory() {
    str = 'VICTORY!!!';

    ctx_canvas.font = '50px Arial';
    ctx_canvas.strokeStyle = '#57C785';

    let width = ctx_canvas.measureText(str).width;

    ctx_canvas.strokeText(str, 256 - width / 2, 256);
}

function drawGameOver() {
    str = 'Game Over!';

    ctx_canvas.font = '50px Arial';
    ctx_canvas.strokeStyle = '#c75757';

    let width = ctx_canvas.measureText(str).width;

    ctx_canvas.strokeText(str, 256 - width / 2, 256);
}

function drawLoading() {
    str = 'Loading Python environment...';

    ctx_canvas.font = '18px Arial';

    let width = ctx_canvas.measureText(str).width;

    ctx_canvas.fillStyle = '#FFFFFF';
    ctx_canvas.fillText(str, 256 - width / 2, 256);
}