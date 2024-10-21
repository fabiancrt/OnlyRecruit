document.getElementById('try-again-button').addEventListener('click', function(event) {
    event.preventDefault();
    const searchInput = document.getElementById('navbar-search');
    searchInput.focus();
    searchInput.classList.add('short-input-hover');
    setTimeout(() => {
        if (!searchInput.matches(':hover')) {
            searchInput.classList.remove('short-input-hover');
        }
    }, 1000);
});