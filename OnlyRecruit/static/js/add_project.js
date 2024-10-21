document.addEventListener('DOMContentLoaded', function() {
    const videoInput = document.getElementById('id_video');
    const videoFileName = document.getElementById('video-file-name');
    const imageInput = document.getElementById('id_image');
    const imageFileName = document.getElementById('image-file-name');

    videoInput.addEventListener('change', function() {
        if (videoInput.files.length > 0) {
            videoFileName.textContent = 'Chosen file: ' + videoInput.files[0].name;
        } else {
            videoFileName.textContent = 'Choose file.';
        }
    });

    imageInput.addEventListener('change', function() {
        if (imageInput.files.length > 0) {
            imageFileName.textContent = 'Chosen file: ' + imageInput.files[0].name;
        } else {
            imageFileName.textContent = 'Choose file.';
        }
    });
});