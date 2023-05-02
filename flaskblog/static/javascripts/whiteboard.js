// Adapted from https://github.com/TomHumphries/InfiniteCanvasWhiteboard
var socket = io();
var canvas = document.getElementById("whiteboard");
document.oncontextmenu = function () {
    return false;
}
var context = canvas.getContext("2d");

var canvasHistory = [];
var strokeHistory = [];
var socketElements = [];
var actionHistory = [];
var backgroundColour = '#fff'

// Fill Window Width and Height
redraw(scale);
window.addEventListener("resize", (event) => {
    redraw(scale);
});

var drawing = false;
var shiftDown = false;
var ctrlDown = false;
var panning = false;
var rightMouseDown = false;
let penColour = 'black';
let penWidth = 2;
var scale = 1;
const MIN_SCALE = 1;
const MAX_SCALE = 5;

// The scaled width of the screen (ie not the pixels)
function xUnitsScaled() {
    return canvas.clientWidth / scale;
}
// The scaled height of the screen (ie not the pixels)
function yUnitsScaled() {
    return canvas.clientHeight / scale;
}

// ------------- Undo Function  -------------
// Disabled since there is nothing to undo at first
let undoButton = document.getElementById("canvas-undo-btn");
undoButton.disabled = true;
undoButton.addEventListener("click", () =>{
    undoLast()
    if (strokeHistory.length === 0) {
        undoButton.disabled = true;
    }
    }
);

document.addEventListener('keydown', event => {
    if (event.key == "Shift") {
        if (!shiftDown) canvas.style.cursor = 'grab';
        shiftDown = true;
    }
    if (event.key == "Control") ctrlDown = true;
    if (event.key == "z") {
        if (ctrlDown) undoLast();
    }
})
document.addEventListener('keyup', event => {
    if (event.key == "Shift") {
        canvas.style.cursor = 'crosshair';
        shiftDown = false;
    }
    if (event.key == "Control") ctrlDown = false;
})

document.addEventListener('wheel', (event) => {
    if (event.target === canvas) {
      const deltaY = event.deltaY;
      const scaleAmount = -deltaY / 500;
      const newScale = scale * (1 + scaleAmount);

      if (newScale >= MIN_SCALE && newScale <= MAX_SCALE) {
          scale = newScale;
  
          var distX = event.pageX / canvas.clientWidth;
          var distY = event.pageY / canvas.clientHeight;
  
          const unitsZoomedX = xUnitsScaled() * scaleAmount;
          const unitsZoomedY = yUnitsScaled() * scaleAmount;
  
          const unitsAddLeft = unitsZoomedX * distX;
          const unitsAddTop = unitsZoomedY * distY;
  
          offsetX -= unitsAddLeft;
          offsetY -= unitsAddTop;
  
          redraw(scale);
      }
    }
  });
  
document.getElementById("whiteboard-reset-zoom-btn").addEventListener("click", () =>{
    scale = 1;
    offsetX = 0;
    offsetY = 0;
    redraw(scale);
    }
);

document.getElementById("open-whiteboard-btn").addEventListener("click", () =>{
    window.scrollTo(0, 0);
});

// Mouse Event Handlers
canvas.addEventListener('mousedown', onMouseDown, false);
canvas.addEventListener('mouseup', onMouseUp, false);
canvas.addEventListener('mouseout', onMouseUp, false);
canvas.addEventListener('mousemove', throttle(onMouseMove, 25), false);

// Touch Event Handlers 
canvas.addEventListener('touchstart', onTouchStart, { passive: false });
canvas.addEventListener('touchend', onTouchEnd, { passive: false });
canvas.addEventListener('touchcancel', onTouchEnd, { passive: false });
canvas.addEventListener('touchmove', throttle(onTouchMove, 25), { passive: false });


function onTouchStart(evt) {
    if (evt.touches.length == 1) {
        panning = false;
        drawing = true;

        lastTouches[0] = evt.touches[0];

    } else if (evt.touches.length >= 2) {
        panning = true;
        drawing = false;
        removeAllDots();

        lastTouches[0] = evt.touches[0];
        lastTouches[1] = evt.touches[1];
    }
}
function onTouchEnd(e) {
    if (drawing) {
        emitStroke();
        strokeHistory.push({ vectors: currentStroke, colour: penColour, thickness: penWidth})
        actionHistory.push(currentStroke)
        currentStroke = [];
        redraw(scale);
        undoButton.disabled = false;
    }
    panning = false;
    drawing = false;

}
function onTouchMove(evt) {

    const touch1X = evt.touches[0].pageX;
    const touch1Y = evt.touches[0].pageY;
    const touch1Xprev = lastTouches[0].pageX;
    const touch1Yprev = lastTouches[0].pageY;

    if (panning) {
        // if panning there is more than 1 touch.
        // get the mid point of the first 2 touches

        const touch2X = evt.touches[1].pageX;
        const touch2Y = evt.touches[1].pageY;
        const midX = (touch1X + touch2X) / 2;
        const midY = (touch1Y + touch2Y) / 2;
        const hypot = Math.sqrt(Math.pow((touch1X - touch2X), 2) + Math.pow((touch1Y - touch2Y), 2));

        const touch2Xprev = lastTouches[1].pageX;
        const touch2Yprev = lastTouches[1].pageY;
        const midXprev = (touch1Xprev + touch2Xprev) / 2;
        const midYprev = (touch1Yprev + touch2Yprev) / 2;
        const hypotPrev = Math.sqrt(Math.pow((touch1Xprev - touch2Xprev), 2) + Math.pow((touch1Yprev - touch2Yprev), 2));

        var zoomAmount = hypot / hypotPrev;
        scale = scale * zoomAmount;
        const scaleAmount = 1 - zoomAmount;

        // calc how many pixels the touches have moved in the x and y direction
        const panX = midX - midXprev;
        const panY = midY - midYprev;
        // scale this movement based on the zoom level
        offsetX += (panX / scale);
        offsetY += (panY / scale);

        // Get the relative position of the middle of the zoom.
        // 0, 0 would be top left. 
        // 0, 1 would be top right etc.
        var zoomRatioX = midX / canvas.clientWidth;
        var zoomRatioY = midY / canvas.clientHeight;

        const unitsZoomedX = xUnitsScaled() * scaleAmount;
        const unitsZoomedY = yUnitsScaled() * scaleAmount;

        const unitsAddLeft = unitsZoomedX * zoomRatioX;
        const unitsAddTop = unitsZoomedY * zoomRatioY;

        offsetX += unitsAddLeft;
        offsetY += unitsAddTop;


        redraw(scale)
    } else if (drawing) {
        if (currentStroke.length == 0) {
            // need to add the first touch
            addToStroke(toTrueX(touch1Xprev), toTrueY(touch1Yprev), penColour, penWidth);
        }
        drawLine(touch1Xprev, touch1Yprev, touch1X, touch1Y, penColour, penWidth);
        addToStroke(toTrueX(touch1X), toTrueY(touch1Y), penColour, penWidth);
    }

    lastTouches[0] = evt.touches[0];
    lastTouches[1] = evt.touches[1];
}

function onMouseDown(evt) {

    if (evt.button == 2) {
        rightMouseDown = true;
    } else {
        rightMouseDown = false;
    }

    cursorX = evt.pageX;
    cursorY = evt.pageY;
    cursorXprev = evt.pageX;
    cursorYprev = evt.pageY;

    if (shiftDown || rightMouseDown) {
        canvas.style.cursor = 'grabbing';
        drawing = false;
        panning = true;
        removeAllDots();
    } else {
        panning = false;
        drawing = true;
        addToStroke((cursorX / scale) - offsetX, (cursorY / scale) - offsetY, penColour, penWidth);
    }
}

function removeAllDots() {
    const dots = document.getElementsByClassName('dot');
    for (let i = 0; i < dots.length; i++) {
        const dot = dots[i];
        dot.remove();
    }
}

var cursorX = null;
var cursorY = null;
var cursorXprev = null;
var cursorYprev = null;
const lastTouches = [null, null];
var offsetX = 0;
var offsetY = 0;
var currentStroke = [];
function onMouseMove(evt) {
    cursorX = evt.pageX;
    cursorY = evt.pageY;

    if (panning) {
        offsetX += (cursorX - cursorXprev) / scale;
        offsetY += (cursorY - cursorYprev) / scale;
        redraw(scale)
    } else if (drawing) {
        addToStroke(toTrueX(cursorX), toTrueY(cursorY), penColour, penWidth);
        drawLine(cursorXprev, cursorYprev, cursorX, cursorY, penColour, penWidth);
    }
    const trueX = (cursorX / scale) - offsetX;
    const trueY = (cursorY / scale) - offsetY;

    cursorXprev = cursorX;
    cursorYprev = cursorY;
}

function onMouseUp(e) {
    if (drawing) {
        emitStroke();
        strokeHistory.push({ vectors: currentStroke, colour: penColour, thickness: penWidth})
        actionHistory.push(currentStroke)
        currentStroke = [];
        redraw(scale);
        undoButton.disabled = false;
    }
    canvas.style.cursor = 'crosshair';
    rightMouseDown = false;
    panning = false;
    drawing = false;
}
function undoLast() {
    if (actionHistory.length == 0) return;
    const toUndo = actionHistory.pop();
    removeFromHistory(toUndo);
    socket.emit('delete', {
        data: toUndo
    })
}
function removeFromHistory(stroke) {
    for (let i = strokeHistory.length - 1; i >= 0; i--) {
        const historyElement = strokeHistory[i];
        if (strokesEqual(historyElement.vectors, stroke)) {
            strokeHistory.splice(i, 1);
            redraw(scale);
            return;
        }
    }
}

function strokesEqual(strokeAVectors, strokeBVectors) {
    if (strokeAVectors.length != strokeBVectors.length) return false;
    for (let i = 0; i < strokeAVectors.length; i++) {
        const strokeAVector = strokeAVectors[i];
        const strokeBVector = strokeBVectors[i];
        if (!vectorsEqual(strokeAVector, strokeBVector)) return false;
    }
    return true;
}

function vectorsEqual(vectorA, vectorB) {
    if (vectorA.length != vectorB.length) return;
    for (let i = 0; i < vectorA.length; i++) {
        const elementA = vectorA[i];
        const elementB = vectorB[i];
        if (elementA != elementB) return false
    }
    return true;
}

// ------------- Clear Function -------------
let clearBtn = document.getElementById("whiteboard-clear-btn");
clearBtn.addEventListener('click', () => {
    clearWhiteboard()
    socket.emit('clear')
})
function clearWhiteboard (){
    context.fillRect(0, 0, canvas.width, canvas.height);
    canvasHistory = [];
    strokeHistory = [];
    actionHistory = [];
    undoButton.disabled = true;
}

// ------------- Color Function -------------
let colorButtons = document.querySelectorAll("[id^='canvas-color-']");
colorButtons.forEach(button => {
  button.addEventListener('click', () => {
    penColour = button.dataset.color;
    document.getElementById("toolbar_colorheader").style.backgroundColor=button.dataset.color
    if (eraser_state == true) {
        eraser_state = false;
        eraserBtn.style.backgroundColor = "black"
        eraserBtn.style.border = "1px solid black"
        penWidth = 2
      } 
  });
});

// ------------- Eraser Function -------------
let eraserBtn = document.getElementById("canvas-eraser-btn");
var eraser_state = false
eraserBtn.addEventListener('click', () => {
    if (eraser_state == false){
        eraser_state = true
        penWidth = 50
        tempColor = penColour
        penColour = 'white';
        eraserBtn.style.backgroundColor = "#2196F3"
        eraserBtn.style.border = "1px solid #2196F3"
    } else {
        eraser_state = false
        penWidth = 2
        penColour = tempColor
        eraserBtn.style.backgroundColor = "black"
        eraserBtn.style.border = "1px solid black"
    }
});

function drawLine(x0, y0, x1, y1, colour, thickness) {
    context.beginPath();
    context.moveTo(x0, y0);
    context.lineTo(x1, y1);
    context.strokeStyle = colour;
    context.lineWidth = thickness;
    context.stroke();
}

function addToStroke(x0, y0, colour, thickness) {
    currentStroke.push([x0, y0]);
}
function drawStroke({ vectors, colour, thickness }) {
    context.beginPath();
    context.lineJoin = "round";
    context.lineCap = "round";
    if (!vectors[0]) return;
    context.moveTo(toScreenX(vectors[0][0]), toScreenY(vectors[0][1]));
    for (let i = 0; i < vectors.length; i++) {
        let x0 = toScreenX(vectors[i][0])
        let y0 = toScreenY(vectors[i][1])
        context.lineTo(x0, y0);
    }
    context.strokeStyle = colour;
    context.lineWidth = thickness;
    context.stroke();

}
function emitStroke() {
    socket.emit('stroke', {
        data: { vectors: currentStroke, colour: penColour, thickness: penWidth }
    });
}
function emitStrokes(strokes) {
    socket.emit('strokes', {
        data: strokes
    });
}

function toScreenX(xTrue) {
    return (xTrue + offsetX) * scale
}
function toScreenY(yTrue) {
    return (yTrue + offsetY) * scale
}
function toTrueX(xScreen) {
    return (xScreen / scale) - offsetX
}
function toTrueY(yScreen) {
    return (yScreen / scale) - offsetY
}

// socket.on('drawing', onDrawingEvent);
socket.on('stroke', onStrokeEvent);
socket.on('strokes', onStrokesEvent);
socket.on('delete', onUndoStrokeEvent);
socket.on('disconnect', onDisconnect);
socket.on('clear', clearWhiteboard);
socket.on('save', saveURL);

function onUndoStrokeEvent(data) {
    removeFromHistory(data.data);
}
function onStrokeEvent(data) {
    strokeHistory.push(data.data);
    drawStroke(data.data);
}
function onStrokesEvent(data) {
    strokeHistory = [...data.data, ...strokeHistory];
    redraw(scale);
}

// another user drawing
function onDrawingEvent(data) {
    canvasHistory.push({ x0: data.x0, y0: data.y0, x1: data.x1, y1: data.y1, colour: data.colour, thickness: data.thickness });
    drawLine((data.x0 + offsetX) * scale, (data.y0 + offsetY) * scale, (data.x1 + offsetX) * scale, (data.y1 + offsetY) * scale, data.colour, data.thickness);
}
function onDisconnect(data) {
    const dot = document.getElementById(data);
    if (!dot) return;
    dot.remove();
}
function setDocumentTitle(colour) {
    if (colour == lightBackgroundColour) {
        document.title = 'Infiniboards';
    } else {
        document.title = 'Infiniboards';
    }
}

function createDot(socketId) {
    const dot = document.createElement('div')
    dot.className = "dot";
    dot.id = socketId;
    dot.style.position = 'fixed';
    document.body.appendChild(dot);
    return dot;
}
function onHistoryEvent(drawHistory) {
    strokeHistory = drawHistory.history;
    backgroundColour = drawHistory.backgroundColour;
    redraw(scale);
}
function redraw(scale = 1) {
    canvas.width = document.body.clientWidth; //document.width is obsolete
    canvas.height = document.body.clientHeight; //document.height is obsolete
    // Set Background Colour
    context.fillStyle = backgroundColour;
    context.fillRect(0, 0, canvas.width, canvas.height);
    strokeHistory.forEach(data => {
        drawStroke({ vectors: data.vectors, colour: data.colour, thickness: data.thickness*scale })
    });
}

// limit the number of events per second
function throttle(callback, delay) {
    var previousCall = new Date().getTime();
    return function () {
        var time = new Date().getTime();

        if ((time - previousCall) >= delay) {
            previousCall = time;
            callback.apply(null, arguments);
        }
    };
}

// https://stackoverflow.com/a/30832210/10159640 Saving strokes as JSON
var submitBtn = document.getElementById("ans");
submitBtn.addEventListener("click", saveURL)
function saveURL() {
    let data = JSON.stringify(strokeHistory);
    document.getElementById('workings').value = data
    socket.emit('save', data)
}

// load image
function load() {   
    data = JSON.parse(document.getElementById('workings').value)
    onStrokesEvent({data:data});
    emitStrokes(data);
}
window.addEventListener('load', load)

// ------------- Toolbar Drag Function -------------
interact('.draggable')
.draggable({
  // enable inertial throwing
  inertia: {
    resistance: 15
  },
  ignoreFrom: '#toolbar_colorheader, #toolbar_fontheader, #canvas-eraser-btn, #canvas-undo-btn , #toolbar_color_collapse, #toolbar_font_collapse',
  // keep the element within the area of it's parent
  modifiers: [
    interact.modifiers.restrictRect({
      restriction: 'parent',
      endOnly: true
    })
  ],
  // enable autoScroll
  autoScroll: true,
  

  listeners: {
    // call this function on every dragmove event
    move: dragMoveListener,

    // call this function on every dragend event
    end (event) {
      var textEl = event.target.querySelector('p')

      textEl && (textEl.textContent =
        'moved a distance of ' +
        (Math.sqrt(Math.pow(event.pageX - event.x0, 2) +
                  Math.pow(event.pageY - event.y0, 2) | 0))
          .toFixed(2) + 'px')
    }
  }
})
function dragMoveListener (event) {
    var target = event.target
    // keep the dragged position in the data-x/data-y attributes
    var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx
    var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy
    // translate the element
    target.style.transform = 'translate(' + x + 'px, ' + y + 'px)'
    // update the posiion attributes
    target.setAttribute('data-x', x)
    target.setAttribute('data-y', y)
}
// this function is used later in the resizing and gesture demos
window.dragMoveListener = dragMoveListener