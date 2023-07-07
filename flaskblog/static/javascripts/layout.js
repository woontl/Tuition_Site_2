// link white div when hover
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.nav-white-hover');

    links.forEach(link => {
      if (link.href === window.location.href) {
        link.classList.add('active');
      }
    });
});

var readTagBtn = document.getElementById('read_tag_btn');
var readTagSpans = document.querySelectorAll('span.read-tag');

readTagBtn.addEventListener('click', function() {
  // Hide the read tag span element
  readTagSpans.forEach(function(span) {
    span.classList.add('d-none');
  });
});