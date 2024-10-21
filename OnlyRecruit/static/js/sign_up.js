
    document.addEventListener('DOMContentLoaded', function() {
        const passwordInput = document.getElementById('id_password1');
        const confirmPasswordInput = document.getElementById('id_password2');
        const usernameInput = document.getElementById('id_username');
        const emailInput = document.getElementById('id_email');
        const passwordCriteria = document.getElementById('password-criteria');
        const passwordRequirements = document.getElementById('password-requirements');
        const passwordMatchError = document.getElementById('password-match-error');
        const signUpForm = document.getElementById('sign-up-form');
        const errorMessages = document.querySelectorAll('.alert.alert-danger');
        const requirements = {
            length: document.getElementById('length'),
            uppercase: document.getElementById('uppercase'),
            lowercase: document.getElementById('lowercase'),
            digit: document.getElementById('digit'),
            special: document.getElementById('special'),
            similar: document.getElementById('similar')
        };

        function validatePassword() {
            const password = passwordInput.value;
            const username = usernameInput.value;

            requirements.length.classList.toggle('valid', password.length >= 8);
            requirements.length.classList.toggle('invalid', password.length < 8);

            requirements.uppercase.classList.toggle('valid', /[A-Z]/.test(password));
            requirements.uppercase.classList.toggle('invalid', !/[A-Z]/.test(password));

            requirements.lowercase.classList.toggle('valid', /[a-z]/.test(password));
            requirements.lowercase.classList.toggle('invalid', !/[a-z]/.test(password));

            requirements.digit.classList.toggle('valid', /[0-9]/.test(password));
            requirements.digit.classList.toggle('invalid', !/[0-9]/.test(password));

            requirements.special.classList.toggle('valid', /[\W_]/.test(password));
            requirements.special.classList.toggle('invalid', !/[\W_]/.test(password));

            requirements.similar.classList.toggle('valid', username && !password.toLowerCase().includes(username.toLowerCase()));
            requirements.similar.classList.toggle('invalid', username && password.toLowerCase().includes(username.toLowerCase()));
        }

        function validatePasswordMatch() {
            const password = passwordInput.value;
            const confirmPassword = confirmPasswordInput.value;

            if (password !== confirmPassword) {
                passwordMatchError.style.display = 'block';
            } else {
                passwordMatchError.style.display = 'none';
            }
        }

        function hideErrors() {
            errorMessages.forEach(function(error) {
                error.style.display = 'none';
            });
        }

        passwordInput.addEventListener('focus', function() {
            passwordCriteria.style.display = 'block';
            passwordRequirements.style.display = 'block';
            hideErrors(); 
        });

        confirmPasswordInput.addEventListener('focus', function() {
            hideErrors(); 
        });

        usernameInput.addEventListener('focus', function() {
            hideErrors(); 
        });

        emailInput.addEventListener('focus', function() {
            hideErrors(); 
        });

        passwordInput.addEventListener('blur', function() {
            if (!passwordInput.value) {
                passwordCriteria.style.display = 'none';
                passwordRequirements.style.display = 'none';
            }
        });

        passwordInput.addEventListener('input', function() {
            validatePassword();
        });

        signUpForm.addEventListener('submit', function(event) {
            validatePasswordMatch();
            if (passwordMatchError.style.display === 'block') {
                event.preventDefault();
            }
        });
    });
