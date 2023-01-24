// var answerSpan_arr = document.querySelectorAll("[id^='MQ-field-']")
// for (var i=0; i<answerSpan_arr.length; i++) {
//     var answerMathField = MQ.MathField(answerSpan_arr[i], {
//         handlers: {
//         edit: function() {
//             var enteredMath = answerMathField.latex(); // Get entered math in LaTeX format
//             checkAnswer(enteredMath);
//         }
//         }
//     });
// }

// var MQSpan = document.getElementById('MQ_span');
// MQ.StaticMath(MQSpan);

let mathFields = document.querySelectorAll("[id^='MQ-field-']");
let lastClickedMathField;

mathFields.forEach(function(mathField) {
  let mathFieldInstance = MQ.MathField(mathField);
    
  mathField.addEventListener("click", function() {
    lastClickedMathField = mathFieldInstance;
  });
});

document.getElementById("calc_button_plus").addEventListener("click", function() {
  lastClickedMathField.cmd("+");
});

document.getElementById("calc_button_minus").addEventListener("click", function() {
  lastClickedMathField.cmd("-");
});

document.getElementById("calc_button_times").addEventListener("click", function() {
  lastClickedMathField.cmd("*");
});

document.getElementById("calc_button_divide").addEventListener("click", function() {
    lastClickedMathField.cmd("\\frac");
});

document.getElementById("calc_button_sqrt").addEventListener("click", function() {
    lastClickedMathField.cmd("\\sqrt");
});

document.getElementById("calc_button_superscript").addEventListener("click", function() {
    lastClickedMathField.cmd("\\superscript");
});

document.getElementById("calc_button_subscript").addEventListener("click", function() {
    lastClickedMathField.cmd("\\subscript");
});

document.getElementById("calc_button_less").addEventListener("click", function() {
    lastClickedMathField.cmd("<");
});

document.getElementById("calc_button_less_equal").addEventListener("click", function() {
    lastClickedMathField.cmd("≤");
});

document.getElementById("calc_button_more").addEventListener("click", function() {
    lastClickedMathField.cmd(">");
});

document.getElementById("calc_button_more_equal").addEventListener("click", function() {
    lastClickedMathField.cmd("≥");
});

document.getElementById("calc_button_pi").addEventListener("click", function() {
    lastClickedMathField.cmd("π");
});