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
  
    var canvas2 = document.getElementById("canvas2");
    var ctx2 = canvas2.getContext("2d");

    var drawing = false;
    var mousePos = {
      x: 0,
      y: 0
    };
    var lastPos = mousePos;
    var strokes2 = []; // stack to stores strokes for undo
    var undoneStrokes2 = [];
  
    canvas2.addEventListener("mousedown", function(e) {
      drawing = true;
      lastPos = getMousePos(canvas2, e);
    }, false);
  
    canvas2.addEventListener("mouseup", function(e) {
      drawing = false;
      // push the current stroke onto the undo stack
      strokes2.push(ctx2.getImageData(0, 0, canvas2.width, canvas2.height));
    }, false);
  
    canvas2.addEventListener("mousemove", function(e) {
      mousePos = getMousePos(canvas2, e);
    }, false);
  
    // Add touch event support for mobile
    canvas2.addEventListener("touchstart", function(e) {
    }, false);
  
    canvas2.addEventListener("touchmove", function(e) {
      var touch = e.touches[0];
      var me = new MouseEvent("mousemove", {
        clientX: touch.clientX,
        clientY: touch.clientY
      });
      canvas2.dispatchEvent(me);
    }, false);
  
    canvas2.addEventListener("touchstart", function(e) {
      mousePos = getTouchPos(canvas2, e);
      var touch = e.touches[0];
      var me = new MouseEvent("mousedown", {
        clientX: touch.clientX,
        clientY: touch.clientY
      });
      canvas2.dispatchEvent(me);
    }, false);
  
    canvas2.addEventListener("touchend", function(e) {
      var me = new MouseEvent("mouseup", {});
      canvas2.dispatchEvent(me);
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
        ctx2.strokeStyle = currentcolor
        ctx2.lineWidth = currentfont
        ctx2.moveTo(lastPos.x, lastPos.y);
        ctx2.lineTo(mousePos.x, mousePos.y);
        ctx2.stroke();
        ctx2.beginPath()
        lastPos = mousePos;
      }
    }
  
    // Prevent scrolling when touching the canvas
    document.body.addEventListener("touchstart", function(e) {
      if (e.target == canvas2) {
        e.preventDefault();
      }
    }, false);
    document.body.addEventListener("touchend", function(e) {
      if (e.target == canvas2) {
        e.preventDefault();
      }
    }, false);
    document.body.addEventListener("touchmove", function(e) {
      if (e.target == canvas2) {
        e.preventDefault();
      }
    }, false);
  
    (function drawLoop() {
      requestAnimFrame(drawLoop);
      renderCanvas();
    })();  

    //reload canvas with dataURL
    var url = JSON.parse(document.getElementById('workings').value).workings2;
    if (url!=""){
      var img = new Image()
      img.src = url
      img.onload = () => { ctx2.drawImage(img, 0, 0); };
      img.src = url
    }

    // resizing
    const canvas_parent = document.querySelector("#canvas_parent")
    function onResize() {
        canvas2.height = window.innerHeight;
        canvas2.width = canvas_parent.offsetWidth*0.99;
    };
    onResize();

    // Variables
    var eraser_state = false;
    var pgnum = 1;
    var canClick = true;
    var clearBtn = document.getElementById("canvas-clear-btn");
    var prevBtn = document.getElementById("canvas-prev-btn");
    var nextBtn = document.getElementById("canvas-next-btn");
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
      if (pgnum==2) {
        ctx2.clearRect(0, 0, canvas2.width, canvas2.height);
      }
  };

    function undoLastStroke() {
      if (pgnum==2){
        if (strokes2.length > 0) {
          var lastStroke = strokes2.pop();
          undoneStrokes2.push(lastStroke);
          ctx2.clearRect(0, 0, canvas2.width, canvas2.height);
          strokes2.forEach(stroke => ctx2.putImageData(stroke, 0, 0));
          if (strokes2.length == 0) {
            var url = JSON.parse(document.getElementById('workings').value).workings2;
            var img = new Image()
            img.src = url
            img.onload = () => { ctx2.drawImage(img, 0, 0); };
          }
        }
      }
    }

    function redoLastStroke() {
      if (pgnum==2){
        if (undoneStrokes2.length > 0) {
          var lastUndoneStroke = undoneStrokes2.pop();
          strokes2.push(lastUndoneStroke);
          ctx2.putImageData(lastUndoneStroke, 0, 0);
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
