
function add_topic() {
  var topic_rows = document.querySelectorAll('[id^=topic_row]')
  for (var i=1; i<topic_rows.length; i++){
    if (topic_rows[i].style.display=='none'){
      topic_rows[i].style.display=''
      break;
    }
  }
  }

function del_topic() {
  var topic_rows = document.querySelectorAll('[id^=topic_row]')
  for (var i=topic_rows.length-1; i>=1; i--){
    if (topic_rows[i].style.display==''){
      var topic_field = document.getElementById('topic_field_'+(i+1))
      topic_field.value=''
      topic_rows[i].style.display='none'
      break;
    }
  }
}

function topics_merged() {
  var topics = document.querySelectorAll("[id^='topic_field_']")
  topics_arr = []
  for (var i=0; i<topics.length; i++) {
    if (topics[i].value == "") { 
      continue
    } else {
    topics_arr.push(topics[i].value)
    }
  }
  var topics_check = document.querySelectorAll("[id^='checkbox_']")
  topics_check_arr = []
  for (var i=0; i<topics_check.length; i++) {
    if (topics_check[i].checked == true) { 
      topics_check_arr.push(1)
    } else {
    topics_check_arr.push(0)
    }
  }
  document.getElementById('ans').value = topics_arr + ';' + topics_check_arr;
}