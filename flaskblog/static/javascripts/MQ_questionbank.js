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

document.getElementById("calc_button_theta").addEventListener("click", function() {
  lastClickedMathField.cmd("θ");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_lambda").addEventListener("click", function() {
  lastClickedMathField.cmd("λ");
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

document.getElementById("calc_button_3sf").addEventListener("click", function() {
  lastClickedMathField.cmd("(3s.f.)");
  lastClickedMathField.focus()
});

document.getElementById("calc_button_1dp").addEventListener("click", function() {
  lastClickedMathField.cmd("(1d.p.)");
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

document.getElementById("calc_button_static").addEventListener("click", function() {
  lastClickedMathField.cmd('【')
  lastClickedMathField.cmd('】')
});
