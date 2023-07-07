function removeBackspace(str) {
    return str.replace(/\x08/g, '');
  }

function check_ans(correct_ans, id, id2) {
    var answerSpan = document.getElementById(id)
    var answerMathField = (MQ.StaticMath(answerSpan)).latex()
    // Remove { }
    answerMathField = answerMathField.replace(/{|}/g, '');

    // Remove ( )
    answerMathField = answerMathField.replace(/\(|\)/g, '');
    
    // Remove \ and the next character
    answerMathField = answerMathField.replace(/\\./g, '');

    // Remove blank spaces
    correct_ans = correct_ans.replace(/\s+/g, '');
    answerMathField = answerMathField.replace(/\s+/g, '');

    var right_check_icon = document.getElementById('right-check-'+ id2)
    var wrong_check_icon = document.getElementById('wrong-check-'+ id2)

    if (removeBackspace(correct_ans) == removeBackspace(answerMathField)) {
        wrong_check_icon.style.display='none'
        right_check_icon.style.display='block'
    } else {
        wrong_check_icon.style.display='block'
        right_check_icon.style.display='none'
    }
}