function add_course() {
    var course_arr = document.querySelectorAll("[id^='blank-topic-']")
    for (var i=0; i<course_arr.length; i++) {
        if (course_arr[i].style.display == 'none'){
            course_arr[i].style.display = ''
            break
        }
    }
}

function del_course(topic) {
    var course = document.getElementById(topic)
    course.remove()
    // course.style.display = 'none'
    // var input = document.getElementById('input-'+topic)
    // input.value = ''
}

function course_arr() {
    var inputTags = document.querySelectorAll('.topic-input');
    var values = [];

    inputTags.forEach(function(input) {
        values.push(input.value);
    });
    
    var checkboxes = document.querySelectorAll('.checkbox');
    var check_values = [];

    checkboxes.forEach(function(checkbox) {
    var value = checkbox.checked ? 1 : 0;
    check_values.push(value);
    });

    var jsonData = JSON.stringify({ 'topics': values,'checked': check_values});
    document.getElementById('save_course').value = jsonData
}