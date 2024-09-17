// For "I'm Feeling Lucky" button clicked
function feelingLucky() {
    var query = document.querySelector('.query').value;
    var url = 'https://www.google.com/search?q=' + encodeURIComponent(query) + '&btnI';
    window.location.href = url;
}