function calc_ans() {
  var ans_merged = []
  var answerSpan_arr = document.querySelectorAll("[id^='MQ-field-']")
  for (var i=0; i<answerSpan_arr.length; i++) {
      var answerMathField = MQ.StaticMath(answerSpan_arr[i])
      ans_merged.push(answerMathField.latex())
      }
  document.getElementById('ans').value = (ans_merged).join(';')
}


