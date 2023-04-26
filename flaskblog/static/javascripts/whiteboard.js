// ------------- Initialize -------------
const socket = io();
let canvas1 = document.getElementById('canvas1');
let canvas2 = document.getElementById('canvas2');
let canvas3 = document.getElementById('canvas3');
let ctx1 = canvas1.getContext('2d');
let ctx2 = canvas2.getContext('2d');
let ctx3 = canvas3.getContext('2d');
const canvasMap = {
  1: canvas1,
  2: canvas2,
  3: canvas3
};
const ctxMap = {
  1: ctx1,
  2: ctx2,
  3: ctx3
};
let strokes1 = [];
let strokes2 = [];
let strokes3 = [];
let strokes1_length = 0;
let strokes2_length = 0;
let strokes3_length = 0;
let undone_strokes1 = []
let undone_strokes2 = []
let undone_strokes3 = []
let redone_strokes1 = []
let redone_strokes2 = []
let redone_strokes3 = []
const strokesMap = {
  1: strokes1,
  2: strokes2,
  3: strokes3
};
const strokesMap_length = {
  1: strokes1_length,
  2: strokes2_length,
  3: strokes3_length
};
const undone_strokesMap = {
  1: undone_strokes1,
  2: undone_strokes2,
  3: undone_strokes3
};
const redone_strokesMap = {
  1: redone_strokes1,
  2: redone_strokes2,
  3: redone_strokes3
};


var currentColor = 'black'
var tempColor = 'black'
var currentThickness = 2
var tempThickness = 2
let currentStroke = null;


// ------------- Page/Canvas Change Function -------------
var pgnum = 1;
let page_num = document.getElementById("canvas-pg-num");
let prevBtn = document.getElementById("canvas-prev-btn");
let nextBtn = document.getElementById("canvas-next-btn");
prevBtn.addEventListener("click", function() { 
  if (pgnum==1){
    pgnum+=2
    page_num.textContent = 'Page ' + pgnum +'/3'
  } else if (pgnum==2){
    pgnum-=1
    page_num.textContent = 'Page ' + pgnum +'/3'
  } else if (pgnum==3){
    pgnum-=1
    page_num.textContent = 'Page ' + pgnum +'/3'
  };
  nextBtn.style.opacity = '0.5';
  nextBtn.style.pointerEvents = 'none';
  prevBtn.style.opacity = '0.5';
  prevBtn.style.pointerEvents = 'none';
  setTimeout(function() {
    nextBtn.style.opacity = '1';
    nextBtn.style.pointerEvents = 'auto';
    prevBtn.style.opacity = '1';
    prevBtn.style.pointerEvents = 'auto';
  }, 500);
});
nextBtn.addEventListener("click", function() {
  if (pgnum==1){
    pgnum+=1
    page_num.textContent = 'Page ' + pgnum +'/3'
  } else if (pgnum==2){
    pgnum+=1
    page_num.textContent = 'Page ' + pgnum +'/3'
  } else if (pgnum==3){
    pgnum-=2
    page_num.textContent = 'Page ' + pgnum +'/3'
  };
  nextBtn.style.opacity = '0.5';
  nextBtn.style.pointerEvents = 'none';
  prevBtn.style.opacity = '0.5';
  prevBtn.style.pointerEvents = 'none';
  setTimeout(function() {
    nextBtn.style.opacity = '1';
    nextBtn.style.pointerEvents = 'auto';
    prevBtn.style.opacity = '1';
    prevBtn.style.pointerEvents = 'auto';
  }, 500);
});

// ------------- Eraser Function -------------
let eraserBtn = document.getElementById("canvas-eraser-btn");
var eraser_state = false
eraserBtn.addEventListener("click", function(){
  if (eraser_state == false){
    eraser_state = true
    tempThickness = currentThickness
    tempColor = currentColor
    currentThickness = 60;
    eraserBtn.style.backgroundColor = "#2196F3"
    eraserBtn.style.border = "1px solid #2196F3"
  } else {
    eraser_state = false
    currentThickness = tempThickness
    currentColor = tempColor
    eraserBtn.style.backgroundColor = "black"
    eraserBtn.style.border = "1px solid black"
  }
})

// ------------- Color Function -------------
let colorButtons = document.querySelectorAll("[id^='canvas-color-']");
colorButtons.forEach(button => {
  button.addEventListener('click', () => {
    currentColor = button.dataset.color;
    currentThickness = tempThickness
    document.getElementById("toolbar_colorheader").style.backgroundColor=button.dataset.color
    if (eraser_state == true) {
      eraser_state = false;
      eraserBtn.style.backgroundColor = "black"
      eraserBtn.style.border = "1px solid black"
    } 
  });
});

// ------------- Thickness Function -------------
let thicknessSlider = document.getElementById("thickness-slider");
thicknessSlider.onchange = function() {
  currentThickness = this.value;
  tempThickness = currentThickness
  currentColor = document.getElementById("toolbar_colorheader").style.backgroundColor
  tempColor = currentColor
  if (eraser_state == true) {
    eraser_state = false;
    eraserBtn.style.backgroundColor = "black"
    eraserBtn.style.border = "1px solid black"
  } 
};

// ------------- Whiteboard Resize Function  -------------
const canvas_parent = document.querySelector("#canvas_parent")
var scale = 3
function onResize(pgnum) {
    canvasMap[pgnum].height = window.innerHeight*1.5*scale;
    canvasMap[pgnum].width = canvas_parent.offsetWidth*0.99*scale;
    canvasMap[pgnum].style.width = canvas_parent.offsetWidth*0.99 + 'px';
    canvasMap[pgnum].style.height = window.innerHeight*1.5 + 'px';
};
onResize(1);
onResize(2);
onResize(3);
window.onload = ('resize', function(pgnum){
  onResize(pgnum)
  socket.emit('resize-board', pgnum);
});
window.addEventListener('resize', function(pgnum){
  onResize(pgnum)
  socket.emit('resize-board', pgnum);
});

// ------------- Undo Function  -------------
// Disabled since there is nothing to undo at first
let undoButton = document.getElementById("canvas-undo-btn");
undoButton.disabled = true;
undoButton.onclick = function() {
  let undo_stroke = strokesMap[pgnum].pop();
  undone_strokesMap[pgnum].push(undo_stroke);
  if (strokesMap[pgnum].length === strokesMap_length[pgnum]) {
    undoButton.disabled = true;
  }
  if (undone_strokesMap[pgnum].length !== 0) {
    redoButton.disabled = false;
  }
  socket.emit('stroke-delete', pgnum);
};

// ------------- Redo Function  -------------
// Disabled since there is nothing to redo at first
let redoButton = document.getElementById("canvas-redo-btn");
redoButton.disabled = true;
redoButton.onclick = function() {
  let redo_stroke = undone_strokesMap[pgnum].pop();
  redone_strokesMap[pgnum].push(redo_stroke);
  strokesMap[pgnum].push(redo_stroke)
  if (undone_strokesMap[pgnum].length === 0) {
      redoButton.disabled = true;
  }
  if (strokesMap[pgnum].length !== strokesMap_length[pgnum]) {
    undoButton.disabled = false;
}
  socket.emit('stroke-add', redo_stroke, pgnum);
};

// ------------- Clear Function  -------------
let clearButton = document.getElementById("canvas-clear-btn");
clearButton.onclick = function() {
  clearBoard(pgnum);
  strokesMap[pgnum].length = 0 // clear list
  strokesMap_length[pgnum] = 0
  undone_strokesMap[pgnum] = []
  redone_strokesMap[pgnum] = []
  undoButton.disabled = true
  redoButton.disabled = true
  socket.emit('clear-board', pgnum);
};
function clearBoard(pgnum) {
  ctxMap[pgnum].clearRect(0, 0, canvasMap[pgnum].width, canvasMap[pgnum].height);
}
socket.on('clear-board', function(pgnum){
  clearBoard(pgnum)
});

// ------------- Draw Function  -------------
function drawNewPoint(e) {
    if (currentStroke === null)
        return;

    // cross-browser canvas coordinates
    let x = (e.offsetX || e.layerX - canvas1.offsetLeft)*scale;
    let y = (e.offsetY || e.layerY - canvas1.offsetTop)*scale;

    currentStroke.points.push({x: x, y: y});
    drawOnCanvas(currentStroke.points, currentStroke.color, currentStroke.thickness, pgnum);
    socket.emit('stroke-update', {x: x, y: y}, pgnum)
}

function drawOnCanvas(plots, color, thickness, pgnum_t) {
    ctxMap[pgnum_t].beginPath();
    ctxMap[pgnum_t].moveTo(plots[0].x, plots[0].y);

    for(let i = 1; i < plots.length; i++) {
      ctxMap[pgnum_t].lineTo(plots[i].x, plots[i].y);
    }

    ctxMap[pgnum_t].lineWidth = thickness;
    ctxMap[pgnum_t].strokeStyle = color;
    ctxMap[pgnum_t].stroke();
}

socket.on('draw-new-stroke', function(data) {
  drawOnCanvas(data.points, data.color, data.thickness, data.pgnum);
});

socket.on('draw-strokes', function(data) {
  for (let i = 0; i < data.length; i++) {
      let stroke = data[i];
      drawOnCanvas(stroke.points, stroke.color, stroke.thickness, pgnum);
  }
});

function startDraw(e) {
    if (eraser_state == true) {
        currentColor = '#FFFFFF';
    }

    // Hack to draw even if cursor doesn't move
    let x = (e.offsetX || e.layerX - canvas1.offsetLeft)*scale;
    let y = (e.offsetY || e.layerY - canvas1.offsetTop)*scale;

    currentStroke = {
        thickness: currentThickness,
        color: currentColor,
        points: [{x: x-1, y: y-1}],
    };

    socket.emit('stroke-start', currentStroke, pgnum);

    drawNewPoint(e);
}

function endDraw() {
  strokesMap[pgnum].push(currentStroke);
  currentStroke = null;
  undoButton.disabled = false;
  undone_strokesMap[pgnum] = []
  redone_strokesMap[pgnum] = []
  redoButton.disabled = true
}

// ------------- Mouse Support  -------------
canvas1.addEventListener('mousedown', startDraw, false);
canvas1.addEventListener('mousemove', drawNewPoint, false);
canvas1.addEventListener('mouseup', endDraw, false);
canvas2.addEventListener('mousedown', startDraw, false);
canvas2.addEventListener('mousemove', drawNewPoint, false);
canvas2.addEventListener('mouseup', endDraw, false);
canvas3.addEventListener('mousedown', startDraw, false);
canvas3.addEventListener('mousemove', drawNewPoint, false);
canvas3.addEventListener('mouseup', endDraw, false);

// ------------- Touch Support  -------------
canvas1.addEventListener("touchmove", function(e) {
  e.preventDefault()
  var touch = e.touches[0];
  var me = new MouseEvent("mousemove", {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  canvas1.dispatchEvent(me);
}, false);
canvas2.addEventListener("touchmove", function(e) {
  e.preventDefault()
  var touch = e.touches[0];
  var me = new MouseEvent("mousemove", {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  canvas2.dispatchEvent(me);
}, false);
canvas3.addEventListener("touchmove", function(e) {
  e.preventDefault()
  var touch = e.touches[0];
  var me = new MouseEvent("mousemove", {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  canvas3.dispatchEvent(me);
}, false);
canvas1.addEventListener("touchstart", function(e) {
  e.preventDefault()
  mousePos = getTouchPos(canvas1, e);
  var touch = e.touches[0];
  var me = new MouseEvent("mousedown", {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  canvas1.dispatchEvent(me);
}, false);
canvas2.addEventListener("touchstart", function(e) {
  e.preventDefault()
  mousePos = getTouchPos(canvas2, e);
  var touch = e.touches[0];
  var me = new MouseEvent("mousedown", {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  canvas2.dispatchEvent(me);
}, false);
canvas3.addEventListener("touchstart", function(e) {
  e.preventDefault()
  mousePos = getTouchPos(canvas3, e);
  var touch = e.touches[0];
  var me = new MouseEvent("mousedown", {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  canvas3.dispatchEvent(me);
}, false);
canvas1.addEventListener("touchend", function(e) {
  e.preventDefault()
  var me = new MouseEvent("mouseup", {});
  canvas1.dispatchEvent(me);
}, false);
canvas2.addEventListener("touchend", function(e) {
  e.preventDefault()
  var me = new MouseEvent("mouseup", {});
  canvas2.dispatchEvent(me);
}, false);
canvas3.addEventListener("touchend", function(e) {
  e.preventDefault()
  var me = new MouseEvent("mouseup", {});
  canvas3.dispatchEvent(me);
}, false);

function getTouchPos(canvasDom, touchEvent) {
  var rect = canvasDom.getBoundingClientRect();
  return {
    x: (touchEvent.touches[0].clientX - rect.left)*scale,
    y: (touchEvent.touches[0].clientY - rect.top)*scale
  }
}

// ------------- Load Canvas with Saved Function  -------------
socket.on('load-strokes1', function(data) {
  for (let i = 0; i < data.length; i++) {
      let stroke = data[i];
      drawOnCanvas(stroke.points, stroke.color, stroke.thickness, 1);
      strokes1.push(stroke)
  }
  strokesMap_length[1] = strokes1.length
});
socket.on('load-strokes2', function(data) {
  for (let i = 0; i < data.length; i++) {
      let stroke = data[i];
      drawOnCanvas(stroke.points, stroke.color, stroke.thickness, 2);
      strokes2.push(stroke)
  }
  strokesMap_length[2] = strokes2.length
});
socket.on('load-strokes3', function(data) {
  for (let i = 0; i < data.length; i++) {
      let stroke = data[i];
      drawOnCanvas(stroke.points, stroke.color, stroke.thickness, 3);
      strokes3.push(stroke)
  }
  strokesMap_length[3] = strokes3.length
});

// ------------- Toolbar Drag Function -------------
interact('.draggable')
.draggable({
  // enable inertial throwing
  inertia: {
    resistance: 15
  },
  ignoreFrom: '#toolbar_colorheader, #toolbar_fontheader, #canvas-eraser-btn, #canvas-redo-btn, #canvas-undo-btn , #toolbar_color_collapse, #toolbar_font_collapse',
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