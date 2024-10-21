document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const usernameInput = document.getElementById('id_username');
    const passwordInput = document.getElementById('id_password');
    const usernameError = document.getElementById('username-error');
    const passwordError = document.getElementById('password-error');

    function hideErrors() {
        if (usernameError) {
            usernameError.style.display = 'none';
        }
        if (passwordError) {
            passwordError.style.display = 'none';
        }
    }

    usernameInput.addEventListener('focus', hideErrors);
    passwordInput.addEventListener('focus', hideErrors);

    loginForm.addEventListener('submit', function(event) {
        let hasErrors = false;

        if (usernameInput.value.trim() === '') {
            if (usernameError) {
                usernameError.style.display = 'block';
            }
            hasErrors = true;
        }

        if (passwordInput.value.trim() === '') {
            if (passwordError) {
                passwordError.style.display = 'block';
            }
            hasErrors = true;
        }

        if (hasErrors) {
            event.preventDefault();
        }
    });

    if (usernameError && usernameError.querySelector('p')) {
        usernameError.style.display = 'block';
    }
    if (passwordError && passwordError.querySelector('p')) {
        passwordError.style.display = 'block';
    }
});