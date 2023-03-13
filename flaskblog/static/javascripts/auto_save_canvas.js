setInterval(() => {
    var canvas_out1 = document.querySelector("#canvas1");
    var canvas_out2 = document.querySelector("#canvas2");
    var canvas_out3 = document.querySelector("#canvas3");
    var dataURL1 = canvas_out1.toDataURL('image/png');
    var dataURL2 = canvas_out2.toDataURL('image/png');
    var dataURL3 = canvas_out3.toDataURL('image/png');
    var dataURL_arr = [dataURL1,dataURL2,dataURL3]
    fetch('/homework/' + homework_id + '/' + question_id+ '/auto_save_canvas', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        url: dataURL_arr.join('@@@@')
      })
    })
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.error(error);
      });
  }, 10000);
  