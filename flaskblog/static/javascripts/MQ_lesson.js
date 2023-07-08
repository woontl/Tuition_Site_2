let mathFields = document.querySelectorAll("[id^='MQ-field-']");
let lastClickedMathField;

mathFields.forEach(function(mathField) {
  let mathFieldInstance = MQ.MathField(mathField);
    
  mathField.addEventListener("click", function() {
    lastClickedMathField = mathFieldInstance;
  });
});

lastClickedMathField = MQ.MathField(mathFields[0])
lastClickedMathField.focus()

document.getElementById("calc_button_alphabet_x").addEventListener("click", function() {
  lastClickedMathField.cmd("x");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_alphabet_y").addEventListener("click", function() {
  lastClickedMathField.cmd("y");
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

document.getElementById("calc_button_left_bracket").addEventListener("click", function() {
  lastClickedMathField.cmd("(");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_right_bracket").addEventListener("click", function() {
  lastClickedMathField.cmd(")");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_less").addEventListener("click", function() {
  lastClickedMathField.cmd("<");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_more").addEventListener("click", function() {
  lastClickedMathField.cmd(">");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_modulus").addEventListener("click", function() {
  lastClickedMathField.cmd("|");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_comma").addEventListener("click", function() {
  lastClickedMathField.cmd(",");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_less_equal").addEventListener("click", function() {
  lastClickedMathField.cmd("≤");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_more_equal").addEventListener("click", function() {
  lastClickedMathField.cmd("≥");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_sqrt").addEventListener("click", function() {
  lastClickedMathField.cmd("\\sqrt");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_pi").addEventListener("click", function() {
  lastClickedMathField.cmd("π");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_theta").addEventListener("click", function() {
lastClickedMathField.cmd("θ");
lastClickedMathField.focus()
});

document.getElementById("calc_button_lambda").addEventListener("click", function() {
lastClickedMathField.cmd("λ");
lastClickedMathField.focus()
});

document.getElementById("calc_button_digit_7").addEventListener("click", function() {
  lastClickedMathField.cmd("7");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_digit_8").addEventListener("click", function() {
  lastClickedMathField.cmd("8");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_digit_9").addEventListener("click", function() {
  lastClickedMathField.cmd("9");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_divide").addEventListener("click", function() {
  lastClickedMathField.cmd("\\frac");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_digit_4").addEventListener("click", function() {
  lastClickedMathField.cmd("4");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_digit_5").addEventListener("click", function() {
  lastClickedMathField.cmd("5");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_digit_6").addEventListener("click", function() {
  lastClickedMathField.cmd("6");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_times").addEventListener("click", function() {
  lastClickedMathField.cmd("*");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_digit_1").addEventListener("click", function() {
  lastClickedMathField.cmd("1");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_digit_2").addEventListener("click", function() {
  lastClickedMathField.cmd("2");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_digit_3").addEventListener("click", function() {
  lastClickedMathField.cmd("3");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_minus").addEventListener("click", function() {
  lastClickedMathField.cmd("-");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_digit_0").addEventListener("click", function() {
  lastClickedMathField.cmd("0");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_decimal").addEventListener("click", function() {
  lastClickedMathField.cmd(".");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_equal").addEventListener("click", function() {
  lastClickedMathField.cmd("=");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_plus").addEventListener("click", function() {
  lastClickedMathField.cmd("+");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_vector").addEventListener("click", function() {
  lastClickedMathField.cmd("\\vec");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_matrix").addEventListener("click", function() {
  lastClickedMathField.cmd("\\binom");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_deg").addEventListener("click", function() {
  lastClickedMathField.cmd("\\degree");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_rad").addEventListener("click", function() {
  lastClickedMathField.cmd("rad");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_arrow_left").addEventListener("click", function() {
  lastClickedMathField.keystroke('Left')
  lastClickedMathField.focus()
});

document.getElementById("calc_button_arrow_right").addEventListener("click", function() {
  lastClickedMathField.keystroke('Right')
  lastClickedMathField.focus()
});
