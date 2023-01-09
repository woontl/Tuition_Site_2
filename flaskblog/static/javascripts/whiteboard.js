(function() {
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
  
    var canvas = document.getElementById("canvas1");
    var ctx1 = canvas.getContext("2d");

    var drawing = false;
    var mousePos = {
      x: 0,
      y: 0
    };
    var lastPos = mousePos;
  
    canvas.addEventListener("mousedown", function(e) {
      drawing = true;
      lastPos = getMousePos(canvas, e);
    }, false);
  
    canvas.addEventListener("mouseup", function(e) {
      drawing = false;
    }, false);
  
    canvas.addEventListener("mousemove", function(e) {
      mousePos = getMousePos(canvas, e);
    }, false);
  
    // Add touch event support for mobile
    canvas.addEventListener("touchstart", function(e) {
  
    }, false);
  
    canvas.addEventListener("touchmove", function(e) {
      var touch = e.touches[0];
      var me = new MouseEvent("mousemove", {
        clientX: touch.clientX,
        clientY: touch.clientY
      });
      canvas.dispatchEvent(me);
    }, false);
  
    canvas.addEventListener("touchstart", function(e) {
      mousePos = getTouchPos(canvas, e);
      var touch = e.touches[0];
      var me = new MouseEvent("mousedown", {
        clientX: touch.clientX,
        clientY: touch.clientY
      });
      canvas.dispatchEvent(me);
    }, false);
  
    canvas.addEventListener("touchend", function(e) {
      var me = new MouseEvent("mouseup", {});
      canvas.dispatchEvent(me);
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
        ctx1.strokeStyle = currentcolor
        ctx1.lineWidth = currentfont
        ctx1.moveTo(lastPos.x, lastPos.y);
        ctx1.lineTo(mousePos.x, mousePos.y);
        ctx1.stroke();
        ctx1.beginPath()
        lastPos = mousePos;
      }
    }
  
    // Prevent scrolling when touching the canvas
    document.body.addEventListener("touchstart", function(e) {
      if (e.target == canvas) {
        e.preventDefault();
      }
    }, false);
    document.body.addEventListener("touchend", function(e) {
      if (e.target == canvas) {
        e.preventDefault();
      }
    }, false);
    document.body.addEventListener("touchmove", function(e) {
      if (e.target == canvas) {
        e.preventDefault();
      }
    }, false);
  
    (function drawLoop() {
      requestAnimFrame(drawLoop);
      renderCanvas();
    })();  

    function clearBoard() {
        if (pgnum==1) {
          ctx1.clearRect(0, 0, canvas.width, canvas.height);
        }
    };

    function saveURL() {
        var canvas_out1 = document.querySelector("#canvas1");
        var canvas_out2 = document.querySelector("#canvas2");
        var canvas_out3 = document.querySelector("#canvas3");
        var dataURL1 = canvas_out1.toDataURL('image/png');
        var dataURL2 = canvas_out2.toDataURL('image/png');
        var dataURL3 = canvas_out3.toDataURL('image/png');
        var dataURL_arr = [dataURL1,dataURL2,dataURL3]
        document.getElementById('workings').value = dataURL_arr.join('@@@@');
    }

    function eraseBoard() {
        if (eraser_state == false) {
            temp_color = currentcolor
            temp_font = currentfont
            currentcolor = 'white'
            currentfont = 5
            eraser_state = true;
            eraserBtn.style.backgroundColor = "blue"
            eraserBtn.style.border = "1px solid blue"
        } else if (eraser_state == true) {
            currentcolor = temp_color;
            currentfont = temp_font;
            currentfont = 1
            eraser_state = false;
            eraserBtn.style.backgroundColor = "white"
            eraserBtn.style.border = "1px solid white"
        } 
    };

    function changeblackColor() {
        currentcolor = 'black';
        colorBtn.style.backgroundColor = currentcolor
        colorBtn.style.border = "1px solid" + currentcolor
        eraser_state = false;
        eraserBtn.style.backgroundColor = "white"
        eraserBtn.style.border = "1px solid white"
    };
    function changeredColor() {
        currentcolor = 'red';
        colorBtn.style.backgroundColor = currentcolor
        colorBtn.style.border = "1px solid" + currentcolor
        eraser_state = false;
        eraserBtn.style.backgroundColor = "white"
        eraserBtn.style.border = "1px solid white"
    };
    function changeblueColor() {
        currentcolor = 'blue';
        colorBtn.style.backgroundColor = currentcolor
        colorBtn.style.border = "1px solid" + currentcolor  
        eraser_state = false;
        eraserBtn.style.backgroundColor = "white"
        eraserBtn.style.border = "1px solid white"
        
    };
    function changegreenColor() {
        currentcolor = 'green';
        colorBtn.style.backgroundColor = currentcolor
        colorBtn.style.border = "1px solid" + currentcolor  
        eraser_state = false;
        eraserBtn.style.backgroundColor = "white"
        eraserBtn.style.border = "1px solid white"
    };
    function changeyellowColor() {
        currentcolor = 'yellow';
        colorBtn.style.backgroundColor = currentcolor
        colorBtn.style.border = "1px solid" + currentcolor  
        eraser_state = false;
        eraserBtn.style.backgroundColor = "white"
        eraserBtn.style.border = "1px solid white"
    };

    function changesmallfont() {
        currentfont = 1
        eraser_state = false;
        eraserBtn.style.backgroundColor = "white"
        eraserBtn.style.border = "1px solid white"
        currentcolor = temp_color
    };
    function changemediumfont() {
        currentfont = 5
        eraser_state = false;
        eraserBtn.style.backgroundColor = "white"
        eraserBtn.style.border = "1px solid white"
        currentcolor = temp_color
    };
    function changelargefont() {
        currentfont = 10
        eraser_state = false;
        eraserBtn.style.backgroundColor = "white"
        eraserBtn.style.border = "1px solid white"
        currentcolor = temp_color
    };

    function prevpg(){
      if (pgnum==1){
        pgnum+=2
      } else if (pgnum==2){
        pgnum-=1
      } else if (pgnum==3){
        pgnum-=1
      }
    }

    function nextpg(){
      if (pgnum==1){
        pgnum+=1
      } else if (pgnum==2){
        pgnum+=1
      } else if (pgnum==3){
        pgnum-=2
      }
    }

    //reload canvas with dataURL
    var url = JSON.parse(document.getElementById('workings').value).workings1;
    if (url!=""){
      var img = new Image()
      img.src = url
      img.onload = () => { ctx1.drawImage(img, 0, 0); };
      img.src = url
    }

    // Set up the UI
    var eraser_state = false;
    var pgnum = 1;
    var clearBtn = document.getElementById("canvas-clear-btn");
    var prevBtn = document.getElementById("canvas-prev-btn");
    var nextBtn = document.getElementById("canvas-next-btn");
    var submitBtn = document.getElementById("ans");
    let temp_color = ''
    let temp_font = ''
    var saveBtn = document.getElementById("canvas-save-btn");
    var refreshBtn = document.getElementById("canvas-refresh-btn");
    var eraserBtn = document.getElementById("canvas-eraser-btn");
    var colorBtn = document.getElementById("dropdownMenuButton-color");
    var blackcolorBtn = document.getElementById("canvas-black-color-btn");
    var redcolorBtn = document.getElementById("canvas-red-color-btn");
    var bluecolorBtn = document.getElementById("canvas-blue-color-btn");
    var greencolorBtn = document.getElementById("canvas-green-color-btn");
    var yellowcolorBtn = document.getElementById("canvas-yellow-color-btn");
    var currentcolor = 'black';
    var currentfont = 1;
    var fontBtn = document.getElementById("dropdownMenuButton-font");
    var smallfontBtn = document.getElementById("canvas-small-font-btn");
    var mediumfontBtn = document.getElementById("canvas-medium-font-btn");
    var largefontBtn = document.getElementById("canvas-large-font-btn");

    clearBtn.addEventListener("click", clearBoard)
    prevBtn.addEventListener("click", prevpg)
    nextBtn.addEventListener("click", nextpg)
    submitBtn.addEventListener("click", saveURL)
    eraserBtn.addEventListener("click", eraseBoard)
    blackcolorBtn.addEventListener("click", changeblackColor)
    redcolorBtn.addEventListener("click", changeredColor)
    bluecolorBtn.addEventListener("click", changeblueColor)
    greencolorBtn.addEventListener("click", changegreenColor)
    yellowcolorBtn.addEventListener("click", changeyellowColor)
    smallfontBtn.addEventListener("click", changesmallfont)
    mediumfontBtn.addEventListener("click", changemediumfont)
    largefontBtn.addEventListener("click", changelargefont)

    // resizing
    const canvas_parent = document.querySelector("#canvas_parent")
    function onResize() {
        canvas.height = window.innerHeight;
        canvas.width = canvas_parent.offsetWidth*0.99;
    };
    onResize();

  })();
