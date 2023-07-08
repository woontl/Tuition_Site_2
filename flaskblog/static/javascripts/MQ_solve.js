let mathFields = document.querySelectorAll("[id^='MQ-field-']");
let lastClickedMathField;

var temp_index = 0
mathFields.forEach(function(mathField) {
  let mathFieldInstance = MQ.StaticMath(mathField);
  mathField.addEventListener("click", function(event) {
    let innerField = event.target;
    if (innerField.classList.contains("mq-root-block")) {
      innerField = innerField
    } else {
      innerField = innerField.parentNode
    }
    let innerField_id = innerField.getAttribute('mathquill-block-id')
    let index = mathFieldInstance.innerFields.findIndex(obj => obj.id == innerField_id);
    temp_index = index
    lastClickedMathField = mathFieldInstance.innerFields[index];
  });
});


let mf_num = 0;
while (mf_num < mathFields.length && mathFields[mf_num].style.display === 'none' || MQ.StaticMath(mathFields[mf_num]).innerFields.length===0) {
  mf_num++;
}
if (mf_num < mathFields.length) {
  lastClickedMathField = MQ.StaticMath(mathFields[mf_num]).innerFields[0];
}
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

document.getElementById("calc_button_delete").addEventListener("click", function() {
  lastClickedMathField.keystroke('Backspace')
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

var mqFieldIds = document.querySelectorAll("[id^='MQ-field-']");
var mqFieldIds_list = []
for (var i = 0; i < mqFieldIds.length; i++) {
  mqFieldIds_list.push(mqFieldIds[i].id)
}

document.getElementById("calc_button_next").addEventListener("click", function() {
  MQ_div_id = lastClickedMathField.el().closest('div').getAttribute('id')
  var currentIndex = mqFieldIds_list.indexOf(MQ_div_id);

  if (temp_index < MQ.StaticMath(mathFields[currentIndex]).innerFields.length-1){
    next_tab_within_part(currentIndex)
  } else if (temp_index == MQ.StaticMath(mathFields[currentIndex]).innerFields.length-1){
    if (mathFields[currentIndex+1].style.display=='none'){
      next_tab_mainpart(currentIndex)
    } else {
      next_tab_subpart(currentIndex)
    }
  }
})

function next_tab_within_part(currentIndex){
  lastClickedMathField = MQ.StaticMath(mathFields[currentIndex]).innerFields[temp_index+1];
  lastClickedMathField.focus()
  temp_index++
}

function next_tab_mainpart(currentIndex){
  currentIndex++
  temp_index=0
  while (MQ.StaticMath(mathFields[currentIndex]).innerFields.length==0){
    currentIndex++
  }
  lastClickedMathField = MQ.StaticMath(mathFields[currentIndex]).innerFields[temp_index+1];
  lastClickedMathField.focus()
}

function next_tab_subpart(currentIndex){
  currentIndex++
  temp_index=0
  while (MQ.StaticMath(mathFields[currentIndex]).innerFields.length==0){
    currentIndex++
  }
  lastClickedMathField = MQ.StaticMath(mathFields[currentIndex]).innerFields[temp_index];
  lastClickedMathField.focus()
}

document.getElementById("calc_button_prev").addEventListener("click", function() {
  MQ_div_id = lastClickedMathField.el().closest('div').getAttribute('id')
  var currentIndex = mqFieldIds_list.indexOf(MQ_div_id);

  if (temp_index > 0){
    prev_tab_within_part(currentIndex)
  } else if (temp_index == 0){
    if (mathFields[currentIndex-1].style.display=='none'){
      prev_tab_mainpart(currentIndex)
    } else {
      prev_tab_subpart(currentIndex)
    }
  }
});

function prev_tab_within_part(currentIndex){
  lastClickedMathField = MQ.StaticMath(mathFields[currentIndex]).innerFields[temp_index-1];
  lastClickedMathField.focus()
  temp_index--
}

function prev_tab_mainpart(currentIndex){
  currentIndex-=2
  while (MQ.StaticMath(mathFields[currentIndex]).innerFields.length==0){
    currentIndex--
  }
  temp_index=MQ.StaticMath(mathFields[currentIndex]).innerFields.length-1
  lastClickedMathField = MQ.StaticMath(mathFields[currentIndex]).innerFields[temp_index];
  lastClickedMathField.focus()
}

function prev_tab_subpart(currentIndex){
  currentIndex--
  while (MQ.StaticMath(mathFields[currentIndex]).innerFields.length==0){
    currentIndex--
  }
  temp_index=MQ.StaticMath(mathFields[currentIndex]).innerFields.length-1
  lastClickedMathField = MQ.StaticMath(mathFields[currentIndex]).innerFields[temp_index];
  lastClickedMathField.focus()
}