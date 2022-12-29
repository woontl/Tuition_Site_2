
window.addEventListener('load', ()=> {
    var canvas = document.querySelector("#canvas");
    var ctx = canvas.getContext('2d')
    const canvas_parent = document.querySelector("#canvas_parent")

    //reload canvas with dataURL
    var url = document.getElementById('workings').value;
    var img = new Image()
    img.src = url
    img.onload = () => { ctx.drawImage(img, 0, 0); };
    img.src = url


    //Resizing
    function onResize() {
        canvas.height = window.innerHeight;
        canvas.width = canvas_parent.offsetWidth;
    };


    //variables
    let painting = false;
    var eraser_state = false;
    let temp_color = ''
    let temp_font = ''
    var submitBtn = $('#ans');
    var clearBtn = $('#canvas-clear-btn');
    var saveBtn = $('#canvas-save-btn');
    var refreshBtn = $('#canvas-refresh-btn');
    var eraserBtn = $('#canvas-eraser-btn');
    var colorBtn = $('.color-btn');
    colorBtn.css('border', '1px solid ' + 'black');  
    colorBtn.css('background-color', 'black');
    var blackcolorBtn = $('#canvas-black-color-btn');
    var redcolorBtn = $('#canvas-red-color-btn');
    var bluecolorBtn = $('#canvas-blue-color-btn');
    var greencolorBtn = $('#canvas-green-color-btn');
    var yellowcolorBtn = $('#canvas-yellow-color-btn');
    var currentcolor = 'black';
    var currentfont = 1;
    var fontBtn = $('.font-btn');
    var smallfontBtn = $('#canvas-small-font-btn');
    var mediumfontBtn = $('#canvas-medium-font-btn');
    var largefontBtn = $('#canvas-large-font-btn');

    //functions
    function startPosition(e){
        painting = true;
        draw(e, currentcolor)
    }

    function finishedPosition(){
        painting = false;
        ctx.beginPath();
    }
    function eraseBoard() {
        if (eraser_state == false) {
            temp_color = currentcolor
            temp_font = currentfont
            currentcolor = 'white';
            currentfont = 5;
            eraserBtn.css('border', '1px solid ' + 'blue');  
            eraserBtn.css('background-color', 'blue');
            eraser_state = true;
        } else if (eraser_state == true) {
            currentcolor = temp_color;
            currentfont = temp_font;
            eraserBtn.css('border', '1px solid ' + 'white');  
            eraserBtn.css('background-color', 'white');
            eraser_state = false;
        } 
    };
    function changeblackColor() {
        currentcolor = 'black';
        colorBtn.css('border', '1px solid ' + currentcolor);  
        colorBtn.css('background-color', currentcolor);
    };
    function changeredColor() {
        currentcolor = 'red';
        colorBtn.css('border', '1px solid ' + currentcolor);  
        colorBtn.css('background-color', currentcolor);
    };
    function changeblueColor() {
        currentcolor = 'blue';
        colorBtn.css('border', '1px solid ' + currentcolor);  
        colorBtn.css('background-color', currentcolor);
    };
    function changegreenColor() {
        currentcolor = 'green';
        colorBtn.css('border', '1px solid ' + currentcolor);  
        colorBtn.css('background-color', currentcolor);
    };
    function changeyellowColor() {
        currentcolor = 'yellow';
        colorBtn.css('border', '1px solid ' + currentcolor);  
        colorBtn.css('background-color', currentcolor);
    };
    function changesmallfont() {
        currentfont = 1
    };
    function changemediumfont() {
        currentfont = 5
    };
    function changelargefont() {
        currentfont = 10
    };

    function draw(e, currentcolor){
        if (!painting) return;
        ctx.strokeStyle = currentcolor;
        ctx.lineWidth = currentfont;
        ctx.lineCap = "round";
        
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
        ctx.beginpath();
        ctx.moveTo(e.offsetX, e.offsetY);
    }

    function clearBoard() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    };

    function saveURL() {
        var canvas_out = document.querySelector("#canvas");
        var dataURL = canvas_out.toDataURL('image/png');
        document.getElementById('workings').value = dataURL;
    }
    
    //EventListeners
    canvas.addEventListener('pointerdown', startPosition);
    canvas.addEventListener('pointerup', finishedPosition);
    canvas.addEventListener('pointerout', finishedPosition);
    canvas.addEventListener('pointermove', draw);

    // canvas.addEventListener('touchstart', startPosition);
    // canvas.addEventListener('touchend', finishedPosition);
    // canvas.addEventListener('touchcancel', finishedPosition);
    // canvas.addEventListener('touchmove', draw);

    //onclick buttons
    clearBtn.on('click', clearBoard);
    refreshBtn.on('click', saveURL);
    saveBtn.on('click', saveURL);
    eraserBtn.on('click', eraseBoard);
    blackcolorBtn.on('click', changeblackColor);
    redcolorBtn.on('click', changeredColor);
    bluecolorBtn.on('click', changeblueColor);
    greencolorBtn.on('click', changegreenColor);
    yellowcolorBtn.on('click', changeyellowColor);
    smallfontBtn.on('click', changesmallfont);
    mediumfontBtn.on('click', changemediumfont);
    largefontBtn.on('click', changelargefont);
    submitBtn.on('click', saveURL);

    window.addEventListener('resize', onResize);
    onResize();
});