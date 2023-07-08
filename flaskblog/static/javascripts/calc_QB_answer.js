function calc_ans() {
  var ans_merged = []
  var answerSpan_arr = document.querySelectorAll("[id^='MQ-field-']")
  for (var i=0; i<answerSpan_arr.length; i++) {
      var answerMathField = MQ.MathField(answerSpan_arr[i])
      ans_merged.push(answerMathField.latex())
      }
  var open_ended_checked = []
  var checkboxes = document.querySelectorAll(".checkbox");
  checkboxes.forEach(function(checkbox) {
    if (checkbox.checked) {
      open_ended_checked.push(1);
    } else{
      open_ended_checked.push(0);
    }
  });
  var obj = {
    ans_merged: (ans_merged).join(';'),
    open_ended_checked: open_ended_checked.join(';')
  }
  document.getElementById('ans').value = JSON.stringify(obj)
}


