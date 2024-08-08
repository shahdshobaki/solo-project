// static/js/alerts.js

function likeMe(element) {
    alert("Your complaint was added successfully. We will get back to you within 72 working hours.");
    // Submit the form after showing the alert
    element.closest('form').submit();
}
