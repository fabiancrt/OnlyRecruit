document.addEventListener('DOMContentLoaded', function() {

});

let activeField = null;

function toggleInput(field) {
    const displayElement = document.getElementById(`${field}-display`);
    const inputElement = document.getElementById(`${field}-input`);

    const errorMessages = document.querySelectorAll('.alert.alert-danger');
    errorMessages.forEach(function(error) {
        error.style.display = 'none';
    });

    const successMessages = document.querySelectorAll('.alert.alert-success');
    successMessages.forEach(function(success) {
        success.style.display = 'none';
    });

    if (activeField && activeField !== field) {
        const activeDisplayElement = document.getElementById(`${activeField}-display`);
        const activeInputElement = document.getElementById(`${activeField}-input`);
        activeDisplayElement.classList.remove('d-none');
        activeInputElement.classList.add('d-none');
    }


    if (displayElement.classList.contains('d-none')) {
        displayElement.classList.remove('d-none');
        inputElement.classList.add('d-none');
        activeField = null;
    } else {
        displayElement.classList.add('d-none');
        inputElement.classList.remove('d-none');
        activeField = field;
    }
}