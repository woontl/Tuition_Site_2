function add_sub_answer(count) {
  var main_ans = document.getElementById('MQ-field-'+count)
  main_ans.style.display='none'
  var main_ans_openended = document.getElementById('open-ended-MQ-field-'+count)
  main_ans_openended.classList.remove("d-flex");
  main_ans_openended.classList.add("d-none");
  var sub_ans_arr = document.querySelectorAll('[id^=sub-answer-'+count+']')
  for (var i=0; i<sub_ans_arr.length; i++){
    if (sub_ans_arr[i].style.display=='none'){
      sub_ans_arr[i].style.display='block'
      break;
    }
  }
  MQ.MathField(main_ans).latex("")
} 

function del_sub_answer(count) {
  var sub_ans_arr = document.querySelectorAll('[id^=sub-answer-'+count+']')
  for (var i=sub_ans_arr.length-1; i>=0; i--){
    if (sub_ans_arr[i].style.display=='block'){
      var roman_arr = ['i','ii','iii','iv','v','vi']
      var sub_ans = document.getElementById('MQ-field-'+count+'-'+roman_arr[i])
      sub_ans_arr[i].style.display='none'
      if (sub_ans_arr[0].style.display=='none'){
        var main_ans = document.getElementById('MQ-field-'+count)
        main_ans.style.display='block'
        var main_ans_openended = document.getElementById('open-ended-MQ-field-'+count)
        main_ans_openended.classList.remove("d-none");
        main_ans_openended.classList.add("d-flex");
      }
      MQ.MathField(sub_ans).latex("")
      break;
    }
  }
}

function add_main_answer() {
  var main_ans_arr = document.querySelectorAll('[id^=main-answer-]')
  for (var i=1; i<main_ans_arr.length; i++){
    if (main_ans_arr[i].style.display=='none'){
      main_ans_arr[i].style.display=''
      break;
    }
  }
}

function del_main_answer() {
  var main_ans_arr = document.querySelectorAll('[id^=main-answer-]')
  for (var i=main_ans_arr.length-1; i>=1; i--){
    if (main_ans_arr[i].style.display==''){
      var main_ans = document.getElementById('MQ-field-'+(i+1))
      if (main_ans.style.display != 'none'){
        main_ans_arr[i].style.display='none'
        MQ.MathField(main_ans).latex("")
      } else {
        del_sub_answer(i+1)
      }
      break;
    }
  }
}
