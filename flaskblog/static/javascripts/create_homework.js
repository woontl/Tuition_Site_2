function loadTopics() {
    var student = document.getElementById('student').value;
    var url = '/get_topics/' + student;
    document.getElementById('topics').value = ''
    // Send an AJAX request to the server
    fetch(url)
        .then(response => response.json())
        .then(data => {
            var topicsField = document.getElementById('topics');
            // Clear existing options
            topicsField.innerHTML = '';

            // Add new options based on the response
            data.topics.forEach(function(topic) {
                var option = document.createElement('option');
                option.text = topic;
                option.value = topic;
                topicsField.add(option);
            });

            // Check if the current topic matches the selectedTopic
            if (option.value == 'Algebra') {
                option.selected = true; // Set the selected attribute
            }
        });
    loadTitle()
}

function loadTitle() {
    if (topics) {
        topics = topics
    } else {
        var topics = document.getElementById('topics').value;
    }
    var titleField = document.getElementById('title');
    titleField.value = 'HW - ' + topics;
}



