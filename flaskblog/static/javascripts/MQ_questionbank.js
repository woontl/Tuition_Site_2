let mathFields = document.querySelectorAll("[id^='MQ-field-']");
let lastClickedMathField;

mathFields.forEach(function(mathField) {
  let mathFieldInstance = MQ.MathField(mathField);
    
  mathField.addEventListener("click", function() {
    lastClickedMathField = mathFieldInstance;
  });
});

let ans_mathFields = document.querySelectorAll(".mq-editable-field");

ans_mathFields.forEach(function(ans_mathField) {
  let mathFieldInstance = MQ.MathField(ans_mathField);
    
  ans_mathField.addEventListener("click", function() {
    lastClickedMathField = mathFieldInstance;
  });
});

document.getElementById("calc_button_plus").addEventListener("click", function() {
  lastClickedMathField.cmd("+");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_minus").addEventListener("click", function() {
  lastClickedMathField.cmd("-");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_times").addEventListener("click", function() {
  lastClickedMathField.cmd("*");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_divide").addEventListener("click", function() {
    lastClickedMathField.cmd("\\frac");
    lastClickedMathField.focus()
});

document.getElementById("calc_button_sqrt").addEventListener("click", function() {
    lastClickedMathField.cmd("\\sqrt");
    lastClickedMathField.focus()
});

document.getElementById("calc_button_superscript").addEventListener("click", function() {
    lastClickedMathField.cmd("\\superscript");
    lastClickedMathField.focus()
});

document.getElementById("calc_button_subscript").addEventListener("click", function() {
    lastClickedMathField.cmd("\\subscript");
    lastClickedMathField.focus()
});

document.getElementById("calc_button_less").addEventListener("click", function() {
    lastClickedMathField.cmd("<");
    lastClickedMathField.focus()
});

document.getElementById("calc_button_less_equal").addEventListener("click", function() {
    lastClickedMathField.cmd("≤");
    lastClickedMathField.focus()
});

document.getElementById("calc_button_more").addEventListener("click", function() {
    lastClickedMathField.cmd(">");
    lastClickedMathField.focus()
});

document.getElementById("calc_button_more_equal").addEventListener("click", function() {
    lastClickedMathField.cmd("≥");
    lastClickedMathField.focus()
});

document.getElementById("calc_button_pi").addEventListener("click", function() {
    lastClickedMathField.cmd("π");
    lastClickedMathField.focus()
});

document.getElementById("calc_button_static").addEventListener("click", function() {
  lastClickedMathField.cmd('【')
  lastClickedMathField.cmd('】')
});
