document.addEventListener('DOMContentLoaded', function() {
    const usernameInput = document.getElementById('username');
    const errorMessages = document.querySelectorAll('.alert.alert-danger');

    function hideErrors() {
        errorMessages.forEach(function(error) {
            error.style.display = 'none';
        });
    }

    usernameInput.addEventListener('focus', function() {
        hideErrors();
    });
});