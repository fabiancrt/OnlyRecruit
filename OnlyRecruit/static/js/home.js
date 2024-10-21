let folderToDelete = null;

function removeFolder(button) {
    const folderCard = button.closest('.folder-card');
    if (!folderCard) {
        console.error('Folder card not found');
        return;
    }

    console.log('Folder card found:', folderCard);

    const folderNameElement = folderCard.querySelector('.card-title');
    if (!folderNameElement) {
        console.error('Folder name element not found within:', folderCard);
        return;
    }

    console.log('Folder name element found:', folderNameElement);

    const folderName = folderNameElement.innerText;
    folderToDelete = folderCard;

    document.getElementById('folderPopupMessage').innerText = `Are you sure you want to delete the folder "${folderName}"?`;
    document.getElementById('deleteFolderPopup').style.display = 'flex';
}

function closeFolderPopup() {
    document.getElementById('deleteFolderPopup').style.display = 'none';
    folderToDelete = null;
}

function confirmFolderDelete() {
    if (folderToDelete) {
        const folderId = folderToDelete.getAttribute('data-folder-id');
        console.log('Folder ID:', folderId);

        if (!folderId) {
            console.error('Folder ID is null or undefined');
            alert('Failed to delete the folder.');
            return;
        }

        document.getElementById('folderPopupMessage').innerText = 'Loading';
        document.querySelector('.cyber-button-red').style.display = 'none';
        document.querySelector('.cyber-button-blue').style.display = 'none';

        const loadingDots = document.createElement('span');
        loadingDots.className = 'loading-dots';
        document.getElementById('folderPopupMessage').appendChild(loadingDots);

        const loadingBarContainer = document.createElement('div');
        loadingBarContainer.className = 'loading-bar-container';
        const loadingBar = document.createElement('div');
        loadingBar.className = 'loading-bar';
        loadingBarContainer.appendChild(loadingBar);
        document.querySelector('.popup-content').appendChild(loadingBarContainer);


        loadingBar.addEventListener('animationend', () => {
            document.getElementById('folderPopupMessage').innerText = 'Almost there';
            document.getElementById('folderPopupMessage').appendChild(loadingDots);

            setTimeout(() => {
                document.getElementById('folderPopupMessage').innerText = 'Complete!';
                document.getElementById('folderPopupMessage').className = 'complete-text';
                loadingBarContainer.style.display = 'none';


                setTimeout(() => {

                    fetch(`/folder/${folderId}/delete/`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken') 
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            console.log('Folder deleted successfully');
                            folderToDelete.remove();
                            location.reload();
                        } else {
                            console.error('Failed to delete the folder. Status:', response.status);
                            alert('Failed to delete the folder.');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Failed to delete the folder.');
                    });
                }, 200); 
            }, 1000); 
        });
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