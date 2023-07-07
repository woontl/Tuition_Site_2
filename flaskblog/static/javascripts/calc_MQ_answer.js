function calc_ans() {
  var ans_merged = []
  var answerSpan_arr = document.querySelectorAll("[id^='MQ-field-']")
  for (var i=0; i<answerSpan_arr.length; i++) {
      var answerMathField = MQ.MathField(answerSpan_arr[i])
      ans_merged.push(answerMathField.latex())
  }
  var obj = {
    ans_merged: (ans_merged).join(';'),
  }
  document.getElementById('ans').value = JSON.stringify(obj)
}


