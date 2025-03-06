document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.querySelector('.file-input');
    const fileDropArea = document.querySelector('.file-drop-area');
    const fileNameDisplay = document.querySelector('.file-name');

    // Handle file input change
    fileInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            fileNameDisplay.textContent = file.name;
        }
    });

    // Handle drag-and-drop
    fileDropArea.addEventListener('dragover', function (e) {
        e.preventDefault();
        fileDropArea.classList.add('dragover');
    });

    fileDropArea.addEventListener('dragleave', function () {
        fileDropArea.classList.remove('dragover');
    });

    fileDropArea.addEventListener('drop', function (e) {
        e.preventDefault();
        fileDropArea.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file) {
            fileInput.files = e.dataTransfer.files;
            fileNameDisplay.textContent = file.name;
        }
    });

    // Trigger file input when clicking the drop area
    fileDropArea.addEventListener('click', function () {
        fileInput.click();
    });
});