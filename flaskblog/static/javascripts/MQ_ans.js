var answerSpan_arr = document.querySelectorAll("[id^='MQ-field-']")
for (var i=0; i<answerSpan_arr.length; i++) {
    var answerMathField = MQ.MathField(answerSpan_arr[i], {
        handlers: {
        edit: function() {
            var enteredMath = answerMathField.latex(); // Get entered math in LaTeX format
            checkAnswer(enteredMath);
        }
        }
    });
}

var MQSpan = document.getElementById('MQ_span');
MQ.StaticMath(MQSpan);
