const numberButtons = document.querySelectorAll('[data-append]')
const powerButtons = document.querySelectorAll('[data-powers]')
const fractionButton = document.querySelector('[data-fraction]')
const equalsButton = document.querySelector('[data-equals]')
const deleteButton = document.querySelector('[data-delete]')
const allClearButton = document.querySelector('[data-all-clear]')
const current_content = document.querySelector('[data-current-content]')


// var ans_part = ""
// var position = ""

// function ans_sub_part(ans_sub_part_num) {
//   ans_part = ans_sub_part_num
//   var dest_all = document.querySelectorAll("[id^='answer-input']")
//   for (var i = 0; i<dest_all.length; i++) {
//     dest_all[i].style.backgroundColor=""
//   }
//   var dest=document.getElementById('answer-input'+ ans_part)
//   dest.style.backgroundColor="lightblue"
//   position = getCaretCharacterOffsetWithin(dest)
//   console.log(position)
// }

// function getCaretCharacterOffsetWithin(element) {
//   var caretOffset = 0;
//   var doc = element.ownerDocument || element.document;
//   var win = doc.defaultView || doc.parentWindow;
//   var sel;
//   if (typeof win.getSelection != "undefined") {
//       sel = win.getSelection();
//       if (sel.rangeCount > 0) {
//           var range = win.getSelection().getRangeAt(0);
//           var preCaretRange = range.cloneRange();
//           preCaretRange.selectNodeContents(element);
//           preCaretRange.setEnd(range.endContainer, range.endOffset);
//           caretOffset = preCaretRange.toString().length;
//       }
//   } else if ( (sel = doc.selection) && sel.type != "Control") {
//       var textRange = sel.createRange();
//       var preCaretTextRange = doc.body.createTextRange();
//       preCaretTextRange.moveToElementText(element);
//       preCaretTextRange.setEndPoint("EndToEnd", textRange);
//       caretOffset = preCaretTextRange.text.length;
//   }
//   return caretOffset;
// }

numberButtons.forEach(button => {
  button.addEventListener('click', () => {
    var dest=document.getElementById('answer-input'+ ans_part)
    if ((document.getElementById('super_script_button').style.backgroundColor != 'yellow') && (document.getElementById('super_script_button').style.backgroundColor != 'blue')) {
      dest.innerHTML += button.innerText
    }
    if (document.getElementById('super_script_button').style.backgroundColor == 'blue') {
      dest.innerHTML += "<sup><sup>" + button.innerText + "</sup></sup>"
    }
    if (document.getElementById('super_script_button').style.backgroundColor == 'yellow'){
      // console.log((dest.innerHTML.length-dest.innerText.length)/11)
      dest.innerHTML += "<sup>" + button.innerText + "</sup>"
    }
    dest.innerHTML = dest.innerHTML.replace(/\s+/g, '');
  })
});

powerButtons.forEach(button => {
  button.addEventListener("click", function(){
    if (this.style.backgroundColor == 'yellow') {
      this.style.backgroundColor = 'blue'
    }
    else if (this.style.backgroundColor == 'blue') {
      this.style.backgroundColor = 'white'
    } else if ((this.style.backgroundColor != 'yellow') && (this.style.backgroundColor != 'blue')) {
      this.style.backgroundColor = 'yellow'
    }
  })
});

allClearButton.addEventListener('click', () => {
  var dest=document.getElementById('answer-input' + ans_part)
  dest.innerHTML = ""
})

deleteButton.addEventListener('click', () => {
  var dest=document.getElementById('answer-input' + ans_part)
  if (String(dest.innerHTML).slice(-1) != ">"){
    dest.innerHTML = dest.innerHTML.toString().slice(0, -1)
  } else (
    dest.removeChild(dest.lastChild) 
  )
})

fractionButton.addEventListener('click', () => { 
  var dest=document.getElementById('answer-input' + ans_part) 
  dest.innerHTML += "<span class=\"fraction\">a<span class=\"fraction-denominator\">b</span></span>" 
})