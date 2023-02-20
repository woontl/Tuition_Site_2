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

    //reload canvas with dataURL
    var url = JSON.parse(document.getElementById('workings').value).workings1;
    if (url!=""){
      var img = new Image()
      img.src = url
      img.onload = () => { ctx1.drawImage(img, 0, 0); };
      img.src = url
    }

    // resizing
    const canvas_parent = document.querySelector("#canvas_parent")
    function onResize() {
        canvas.height = window.innerHeight;
        canvas.width = canvas_parent.offsetWidth*0.99;
    };
    onResize();

    // Variables
    var eraser_state = false;
    var pgnum = 1;
    var clearBtn = document.getElementById("canvas-clear-btn");
    var prevBtn = document.getElementById("canvas-prev-btn");
    var nextBtn = document.getElementById("canvas-next-btn");
    var submitBtn = document.getElementById("ans");
    let temp_color = ''
    let temp_font = ''
    var eraserBtn = document.getElementById("canvas-eraser-btn");
    var currentcolor = 'black';
    var currentfont = 2;
    var page_num = document.getElementById("canvas-pg-num");
    const colorButtons = document.querySelectorAll("[id^='canvas-color-']");

    clearBtn.addEventListener("click", clearBoard)
    prevBtn.addEventListener("click", prevpg)
    nextBtn.addEventListener("click", nextpg)
    submitBtn.addEventListener("click", saveURL)
    eraserBtn.addEventListener("click", eraseBoard)

    // Tools functionalities
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
          currentfont = 25
          eraser_state = true;
          eraserBtn.style.backgroundColor = "white"
          eraserBtn.style.border = "1px solid white"
      } else if (eraser_state == true) {
          currentcolor = temp_color;
          currentfont = temp_font;
          eraser_state = false;
          eraserBtn.style.backgroundColor = "#2196F3"
          eraserBtn.style.border = "1px solid #2196F3"
      } 
    };

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

    // target elements with the "draggable" class
    interact('.draggable')
    .draggable({
      // enable inertial throwing
      inertia: true,
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

})();





