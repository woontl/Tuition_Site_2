
function add_topic() {
  var topic_fields = document.getElementById('topic_fields')
  var field_num = document.querySelectorAll("[id^='topic_row_']").length+1
  topic_fields.innerHTML += "<div class=\"row my-2\" id=\"topic_row_" + field_num + "\">\
                              <div class=\"col-2 mx-0\">\
                                  <p class=\"form-control-label mt-1\">Topic "+ field_num + ":</p>\
                              </div>\
                              <div class=\"d-flex col-10 mx-0\">\
                                  <input class=\"mr-4 form-control\" id=\"topic_field_"+ field_num + "\" name=\"topics\" required type=\"text\">\
                                  <input id=\"checkbox_" + field_num + "\" type=\"checkbox\">\
                              </div>\
                            </div>"
  }

function del_topic() {
  var field_num = document.querySelectorAll("[id^='topic_row_']").length
  if (field_num == 1) {
    return
  }
  document.getElementById('topic_row_'+String(field_num)).remove();
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