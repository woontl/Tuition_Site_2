let mathFields = document.querySelectorAll("[id^='MQ-field-']");
let lastClickedMathField;

mathFields.forEach(function(mathField) {
  let mathFieldInstance = MQ.StaticMath(mathField);
  mathField.addEventListener("click", function(event) {
    let innerField = event.target;
    console.log(innerField)
    if (innerField.classList.contains("mq-root-block")) {
      innerField = innerField
    } else {
      innerField = innerField.parentNode
    }
    let innerField_id = innerField.getAttribute('mathquill-block-id')
    let index = mathFieldInstance.innerFields.findIndex(obj => obj.id == innerField_id);
    lastClickedMathField = mathFieldInstance.innerFields[index];
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