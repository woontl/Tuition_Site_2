(function() {
  // Canvas drawing setup
  window.requestAnimFrame = (function(callback) {
    return window.requestAnimationFrame ||
      window.webkitRequestAnimationFrame ||
      window.mozRequestAnimationFrame ||
      window.oRequestAnimationFrame ||
      window.msRequestAnimaitonFrame ||
      function(callback) {
        window.setTimeout(callback, 1000 / 60);
      };
  })();

  var canvas3 = document.getElementById("canvas3");
  var ctx3 = canvas3.getContext("2d");

  var drawing = false;
  var mousePos = {
    x: 0,
    y: 0
  };
  var lastPos = mousePos;
  var strokes3 = []; // stack to stores strokes for undo
  var undoneStrokes3 = [];

  canvas3.addEventListener("mousedown", function(e) {
    drawing = true;
    lastPos = getMousePos(canvas3, e);
  }, false);

  canvas3.addEventListener("mouseup", function(e) {
    drawing = false;
    // push the current stroke onto the undo stack
    strokes3.push(ctx3.getImageData(0, 0, canvas3.width, canvas3.height));
  }, false);

  canvas3.addEventListener("mousemove", function(e) {
    mousePos = getMousePos(canvas3, e);
  }, false);

  // Add touch event support for mobile
  canvas3.addEventListener("touchstart", function(e) {
  }, false);

  canvas3.addEventListener("touchmove", function(e) {
    var touch = e.touches[0];
    var me = new MouseEvent("mousemove", {
      clientX: touch.clientX,
      clientY: touch.clientY
    });
    canvas3.dispatchEvent(me);
  }, false);

  canvas3.addEventListener("touchstart", function(e) {
    mousePos = getTouchPos(canvas3, e);
    var touch = e.touches[0];
    var me = new MouseEvent("mousedown", {
      clientX: touch.clientX,
      clientY: touch.clientY
    });
    canvas3.dispatchEvent(me);
  }, false);

  canvas3.addEventListener("touchend", function(e) {
    var me = new MouseEvent("mouseup", {});
    canvas3.dispatchEvent(me);
  }, false);

  function getMousePos(canvasDom, mouseEvent) {
    var rect = canvasDom.getBoundingClientRect();
    return {
      x: mouseEvent.clientX - rect.left,
      y: mouseEvent.clientY - rect.top
    }
  }

  function getTouchPos(canvasDom, touchEvent) {
    var rect = canvasDom.getBoundingClientRect();
    return {
      x: touchEvent.touches[0].clientX - rect.left,
      y: touchEvent.touches[0].clientY - rect.top
    }
  }

  function renderCanvas() {
    if (drawing) {
      ctx3.strokeStyle = currentcolor
      ctx3.lineWidth = currentfont
      ctx3.moveTo(lastPos.x, lastPos.y);
      ctx3.lineTo(mousePos.x, mousePos.y);
      ctx3.stroke();
      ctx3.beginPath()
      lastPos = mousePos;
    }
  }

  // Prevent scrolling when touching the canvas
  document.body.addEventListener("touchstart", function(e) {
    if (e.target == canvas3) {
      e.preventDefault();
    }
  }, false);
  document.body.addEventListener("touchend", function(e) {
    if (e.target == canvas3) {
      e.preventDefault();
    }
  }, false);
  document.body.addEventListener("touchmove", function(e) {
    if (e.target == canvas3) {
      e.preventDefault();
    }
  }, false);

  (function drawLoop() {
    requestAnimFrame(drawLoop);
    renderCanvas();
  })();  

  //reload canvas with dataURL
  var url = JSON.parse(document.getElementById('workings').value).workings3;
  if (url!=""){
    var img = new Image()
    img.src = url
    img.onload = () => { ctx3.drawImage(img, 0, 0); };
    img.src = url
  }

  // resizing
  const canvas_parent = document.querySelector("#canvas_parent")
  function onResize() {
      canvas3.height = window.innerHeight;
      canvas3.width = canvas_parent.offsetWidth*0.99;
  };
  onResize();

  // Variables
  var eraser_state = false;
  var pgnum = 1;
  var clearBtn = document.getElementById("canvas-clear-btn");
  var prevBtn = document.getElementById("canvas-prev-btn");
  var nextBtn = document.getElementById("canvas-next-btn");
  var canClick = true;
  var eraserBtn = document.getElementById("canvas-eraser-btn");
  var undoBtn = document.getElementById("canvas-undo-btn");
  var redoBtn = document.getElementById("canvas-redo-btn");
  let temp_color = 'black'
  let temp_font = 2
  var currentcolor = document.getElementById("toolbar_colorheader").style.backgroundColor
  var currentfont = 2;
  var page_num = document.getElementById("canvas-pg-num");
  const colorButtons = document.querySelectorAll("[id^='canvas-color-']");

  clearBtn.addEventListener("click", clearBoard)
  prevBtn.addEventListener("click", function() {
    if (canClick) {
      canClick = false;
      setTimeout(function() {
        canClick = true;
      }, 10); 
      prevpg();
    }
  });
  nextBtn.addEventListener("click", function() {
    if (canClick) {
      canClick = false;
      setTimeout(function() {
        canClick = true;
      }, 10); 
      nextpg();
    }
  });
  eraserBtn.addEventListener("click", eraseBoard)
  undoBtn.addEventListener('click', undoLastStroke);
  redoBtn.addEventListener('click', redoLastStroke);


  // Tools functionalities
  function clearBoard() {
    if (pgnum==3) {
      ctx3.clearRect(0, 0, canvas3.width, canvas3.height);
    }
};

  function undoLastStroke() {
    if (pgnum==3){
      if (strokes3.length > 0) {
        var lastStroke = strokes3.pop();
        undoneStrokes3.push(lastStroke);
        ctx3.clearRect(0, 0, canvas3.width, canvas3.height);
        strokes3.forEach(stroke => ctx3.putImageData(stroke, 0, 0));
        if (strokes3.length == 0) {
          var url = JSON.parse(document.getElementById('workings').value).workings3;
          var img = new Image()
          img.src = url
          img.onload = () => { ctx3.drawImage(img, 0, 0); };
        }
      }
    }
  }

  function redoLastStroke() {
    if (pgnum==3){
      if (undoneStrokes3.length > 0) {
        var lastUndoneStroke = undoneStrokes3.pop();
        strokes3.push(lastUndoneStroke);
        ctx3.putImageData(lastUndoneStroke, 0, 0);
      }
    }
  }
  

  function prevpg(){
    if (pgnum==1){
      pgnum+=2
      page_num.textContent = 'Page ' + pgnum +'/3'
    } else if (pgnum==2){
      pgnum-=1
      page_num.textContent = 'Page ' + pgnum +'/3'
    } else if (pgnum==3){
      pgnum-=1
      page_num.textContent = 'Page ' + pgnum +'/3'
    }
  }

  function nextpg(){
    if (pgnum==1){
      pgnum+=1
      page_num.textContent = 'Page ' + pgnum +'/3'
    } else if (pgnum==2){
      pgnum+=1
      page_num.textContent = 'Page ' + pgnum +'/3'
    } else if (pgnum==3){
      pgnum-=2
      page_num.textContent = 'Page ' + pgnum +'/3'
    }
  }

  function eraseBoard() {
    if (eraser_state == false) {
        temp_color = currentcolor
        temp_font = currentfont
        currentcolor = 'white'
        currentfont = 25
        eraser_state = true;
        eraserBtn.style.backgroundColor = "#2196F3"
        eraserBtn.style.border = "1px solid #2196F3"
    } else if (eraser_state == true) {
        currentcolor = temp_color;
        currentfont = temp_font;
        eraser_state = false;
        eraserBtn.style.backgroundColor = "black"
        eraserBtn.style.border = "1px solid black"
    } 
  };


  // Handle color change
  colorButtons.forEach(button => {
    button.addEventListener('click', () => {
      currentcolor = button.dataset.color;
      currentfont = temp_font
      document.getElementById("toolbar_colorheader").style.backgroundColor=button.dataset.color
      if (eraser_state == true) {
        eraser_state = false;
        eraserBtn.style.backgroundColor = "#2196F3"
        eraserBtn.style.border = "1px solid #2196F3"
      } 
    });
  });


  // Handle font change
  fontSizeSlider.addEventListener('input', () => {
    currentfont = fontSizeSlider.value;
  });

})();
