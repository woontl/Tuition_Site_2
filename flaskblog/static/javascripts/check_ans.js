function removeBackspace(str) {
    return str.replace(/\x08/g, '');
  }

function check_ans(correct_ans, id, id2) {
    var answerSpan = document.getElementById(id)
    var answerMathField = (MQ.StaticMath(answerSpan)).latex()
    console.log(answerMathField)
    // Remove { }
    answerMathField = answerMathField.replace(/{|}/g, '');

    // Remove ( )
    answerMathField = answerMathField.replace(/\(|\)/g, '');
    
    // Remove \ and the next character if its a f
    answerMathField = answerMathField.replace(/\\(.)/g, (match, nextChar) => {
        if (['f', 'r', 'v', 'b'].includes(nextChar)) {
          return ''; // Remove both \ and the next character ('f', 'r', or 'v')
        } else {
          return nextChar; // Remove only the backslash (\)
        }
    });
        

    // Remove blank spaces
    correct_ans = correct_ans.replace(/\s+/g, '');
    answerMathField = answerMathField.replace(/\s+/g, '');

    var right_check_icon = document.getElementById('right-check-'+ id2)
    var wrong_check_icon = document.getElementById('wrong-check-'+ id2)

    console.log(correct_ans)
    console.log(answerMathField)

    if (removeBackspace(correct_ans) == removeBackspace(answerMathField)) {
        wrong_check_icon.style.display='none'
        right_check_icon.style.display='block'
    } else {
        wrong_check_icon.style.display='block'
        right_check_icon.style.display='none'
    }
}