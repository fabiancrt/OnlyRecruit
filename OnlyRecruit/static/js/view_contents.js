
    let projectToDelete = null;

    function removeProject(button) {
        const projectCard = button.closest('.project-card');
        if (!projectCard) {
            console.error('Project card not found');
            return;
        }
    
        console.log('Project card found:', projectCard);
    
        const projectNameElement = projectCard.querySelector('.card-title.broken-light');
        if (!projectNameElement) {
            console.error('Project name element not found within:', projectCard);
            return;
        }
    
        console.log('Project name element found:', projectNameElement);
    
        const projectName = projectNameElement.innerText;
        projectToDelete = projectCard;
    
        document.getElementById('popupMessage').innerText = `Are you sure you want to delete "${projectName}"?`;
        document.getElementById('deletePopup').style.display = 'flex';
    }
    
    function closePopup() {
        document.getElementById('deletePopup').style.display = 'none';
    }
    
    function confirmDelete() {
        if (projectToDelete) {
            const projectId = projectToDelete.getAttribute('data-project-id');
            console.log('Project ID:', projectId);
    
            if (!projectId) {
                console.error('Project ID is null or undefined');
                alert('Failed to delete the project.');
                return;
            }


            closePopup();


            projectToDelete.style.opacity = '0';


            setTimeout(() => {
                fetch(`/delete_project/${projectId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {

                        setTimeout(() => {
                            location.reload();
                        }, 100);
                    } else {
                        alert('Failed to delete the project.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Failed to delete the project.');
                });
            }, 2000);
        }
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }