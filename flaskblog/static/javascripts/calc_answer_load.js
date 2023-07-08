function load_ans(temp_ans) {
  var dest = document.querySelectorAll("[id^='answer-input']")
  var ans_arr = temp_ans.split(";")
  if (temp_ans == "") {
    pass
  } else {
    for (var i = 0; i < dest.length; i++){
      dest[i].innerHTML += ans_arr[i]
    }
  }
}