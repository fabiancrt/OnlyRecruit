function validateSearch() {
    const searchInput = document.getElementById('navbar-search').value.trim();
    if (searchInput === "") {
        alert("Please enter a username to search.");
        return false;
    }
    return true;
}