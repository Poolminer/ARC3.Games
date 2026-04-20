let pointer = document.getElementById('pointer');
let pointerHand = document.getElementById('pointer_hand');
let pointerArrow = document.getElementById('pointer_arrow');

let vPointerOverCanvas = false;

let framePointerPosition = {
    "x": -1,
    "y": -1
};

let prevFramePointerPosition = {
    "x": -1,
    "y": -1
};

let pointerPosition = {
    "x": 0,
    "y": 0
};

function elementsFromAbsolutePoint(pageX, pageY) {
    const x = pageX - window.scrollX;
    const y = pageY - window.scrollY;
    return document.elementsFromPoint(x, y);
}

function setPointerPosition(pt) {
    pointer.style.left = `${pt.x}px`;
    pointer.style.top = `${pt.y}px`;

    pointerPosition.x = pt.x;
    pointerPosition.y = pt.y;

    pointerHand.style.display = 'none';
    pointerArrow.style.display = '';

    let hoverElements = elementsFromAbsolutePoint(pt.x, pt.y);

    let _vPointerOverCanvas = vPointerOverCanvas;

    vPointerOverCanvas = false;

    for (let hoverElement of hoverElements) {
        if (hoverElement.tagName === 'BUTTON') {
            if (!hoverElement.disabled) {
                pointerHand.style.display = '';
                pointerArrow.style.display = 'none';
            }
        } else if (hoverElement.tagName === 'CANVAS') {
            vPointerOverCanvas = true;

            let rect = getElementBoundingRect(canvas);

            let offsetX = pt.x - rect.left;
            let offsetY = pt.y - rect.top;

            framePointerPosition.x = clamp(Math.floor(offsetX / 8), 0, 63);
            framePointerPosition.y = clamp(Math.floor(offsetY / 8), 0, 63);

            if (clickingEnabled && currentFrame !== null) {
                drawFrame(currentFrame, currentBackgroundFrame1, currentBackgroundFrame2);
            }
        }
    }
    if (!vPointerOverCanvas && _vPointerOverCanvas) {
        _onCanvasMouseLeave();
    }
}

let pointerMoverIntervalId = -1;
let pointerMoverTimeoutId = -1;

function movePointer(dst, delay) {
    if (pointerMoverIntervalId != -1) {
        window.clearInterval(pointerMoverIntervalId);
        window.clearTimeout(pointerMoverTimeoutId);
    }
    let p0 = pointerPosition;
    let p3 = {
        "x": Math.round(dst.x),
        "y": Math.round(dst.y)
    };
    if (p0.x === p3.x && p0.y === p3.y) {
        pointerMoverTimeoutId = window.setTimeout(() => {
            window.clearTimeout(pointerMoverTimeoutId);
            pointerMoverTimeoutId = -1;
            onPointerStop();
        }, 250 * delay);
        return;
    }
    let dx = p0.x - p3.x;
    let dy = p0.y - p3.y;
    let d = Math.sqrt(dx ** 2 + dy ** 2);
    let numPoints = Math.max(10, d / 10);

    var points = generateHumanLikePath(p0, p3, numPoints);
    var idx = 0;

    pointerMoverIntervalId = window.setInterval(() => {
        var pos = points[idx++];

        if (pos === undefined) {
            window.clearInterval(pointerMoverIntervalId);
            pointerMoverIntervalId = -1;
            onPointerStop();
            return;
        }
        setPointerPosition(pos);
    }, clamp(d, 150, 512) * delay / numPoints);
}

let hoverTarget = null;

function pointerHoverElement(element, delay) {
    hoverTarget = element;

    let margin = 10;
    let rect = getElementBoundingRect(element);
    let dst = {
        "x": Math.round(rect.left + margin + (rect.width - margin * 2) * Math.random()),
        "y": Math.round(rect.top + margin + (rect.height - margin * 2) * Math.random())
    };
    movePointer(dst, delay);
}

function generateHumanLikePath(p0, p3, numPoints) {
    const dx = p3.x - p0.x;
    const dy = p3.y - p0.y;
    const dist = Math.hypot(dx, dy);

    if (dist === 0) {
        return [{ x: p0.x, y: p0.y }];
    }

    function rand(min, max) {
        return min + Math.random() * (max - min);
    }

    function lerp(a, b, t) {
        return a + (b - a) * t;
    }

    function rotate(x, y, angle) {
        const c = Math.cos(angle);
        const s = Math.sin(angle);
        return {
            x: x * c - y * s,
            y: x * s + y * c
        };
    }

    function makeEaseInOut() {
        const a = 1.8 + Math.random() * 0.8; // 1.8 .. 2.6

        return function (t) {
            return t < 0.5
                ? 0.5 * Math.pow(2 * t, a)
                : 1 - 0.5 * Math.pow(2 * (1 - t), a);
        };
    }

    const easeInOut = makeEaseInOut();

    function cubicBezierPointAt(p0, p1, p2, p3, t) {
        const mt = 1 - t;
        return {
            x:
                mt * mt * mt * p0.x +
                3 * mt * mt * t * p1.x +
                3 * mt * t * t * p2.x +
                t * t * t * p3.x,
            y:
                mt * mt * mt * p0.y +
                3 * mt * mt * t * p1.y +
                3 * mt * t * t * p2.y +
                t * t * t * p3.y
        };
    }

    function createControlPoints(p0, p3) {
        const dx = p3.x - p0.x;
        const dy = p3.y - p0.y;
        const dist = Math.hypot(dx, dy);

        const ux = dx / dist;
        const uy = dy / dist;

        // Bend both handles to the same side.
        const side = Math.random() < 0.5 ? -1 : 1;

        // Slightly straighter on long moves.
        const angleMin = Math.PI / 18; // 10 deg
        const angleMax = Math.PI / 5;  // 36 deg
        const distanceFactor = Math.min(1, 200 / dist);
        const maxAngle = angleMin + (angleMax - angleMin) * distanceFactor;

        const a1 = side * rand(angleMin, maxAngle);
        const a2 = side * rand(angleMin, maxAngle);

        const len1 = dist * rand(0.28, 0.40);
        const len2 = dist * rand(0.28, 0.40);

        const v1 = rotate(ux * len1, uy * len1, a1);
        const v2 = rotate(-ux * len2, -uy * len2, a2);

        return {
            p1: { x: p0.x + v1.x, y: p0.y + v1.y },
            p2: { x: p3.x + v2.x, y: p3.y + v2.y }
        };
    }

    const { p1, p2 } = createControlPoints(p0, p3);

    // One random low-frequency wobble profile across the whole path.
    const wobble1 = rand(-1, 1);
    const wobble2 = rand(-1, 1);
    const wobbleAmp = Math.min(6, dist * 0.03);

    const points = [];

    for (let i = 0; i <= numPoints; i++) {
        const t = i / numPoints;
        const te = easeInOut(t);

        const base = cubicBezierPointAt(p0, p1, p2, p3, te);

        // Approximate tangent from endpoints for a simple normal direction.
        const tangentX = dx / dist;
        const tangentY = dy / dist;
        const normalX = -tangentY;
        const normalY = tangentX;

        // Smooth envelope: zero at ends, strongest in middle.
        const envelope = Math.sin(Math.PI * t);

        // Simple smooth wobble using interpolation between two random values.
        const wobble = lerp(wobble1, wobble2, t);

        points.push({
            x: base.x + normalX * wobble * wobbleAmp * envelope,
            y: base.y + normalY * wobble * wobbleAmp * envelope
        });
    }

    // Force exact endpoints.
    points[0] = { x: p0.x, y: p0.y };
    points[points.length - 1] = { x: p3.x, y: p3.y };

    return points;
}