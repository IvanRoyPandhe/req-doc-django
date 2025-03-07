document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const dropArea = document.querySelector('.file-drop-area');
    const fileInput = document.querySelector('.file-input');
    const fileName = document.querySelector('.file-name');
    const uploadIcon = document.querySelector('.file-drop-icon');
    const uploadText = document.querySelector('.file-drop-text');

    // Configuration
    const CONFIG = {
        maxFileSize: 10 * 1024 * 1024, // 10MB
        allowedTypes: [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'image/jpeg',
            'image/png',
            'image/gif'
        ],
        animations: {
            duration: 300,
            easing: 'ease'
        }
    };

    // State management
    let currentFile = null;
    let isDragging = false;
    let dragCounter = 0;

    // Event listeners for drag and drop
    const dragEvents = ['dragenter', 'dragover', 'dragleave', 'drop'];
    dragEvents.forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, handleDragEnter, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, handleDragLeave, false);
    });

    // Handle file drop and selection
    dropArea.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFileSelect, false);

    // Click handling for the entire drop area
    dropArea.addEventListener('click', () => fileInput.click());

    // Prevent default behaviors
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Handle drag enter
    function handleDragEnter(e) {
        preventDefaults(e);
        dragCounter++;
        
        if (dragCounter === 1) {
            dropArea.classList.add('dragover');
            animateDropArea(true);
        }
    }

    // Handle drag leave
    function handleDragLeave(e) {
        preventDefaults(e);
        dragCounter--;
        
        if (dragCounter === 0) {
            dropArea.classList.remove('dragover');
            animateDropArea(false);
        }
    }

    // Handle file drop
    function handleDrop(e) {
        preventDefaults(e);
        dragCounter = 0;
        dropArea.classList.remove('dragover');
        animateDropArea(false);

        const files = e.dataTransfer.files;
        handleFiles(files);
    }

    // Handle file selection
    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }

    // Process files
    function handleFiles(files) {
        if (files.length === 0) return;

        const file = files[0];
        
        // Validate file
        if (!validateFile(file)) return;

        currentFile = file;
        updateFileInfo(file);
        showSuccessAnimation();
    }

    // Validate file
    function validateFile(file) {
        // Check file size
        if (file.size > CONFIG.maxFileSize) {
            showError(`File is too large. Maximum size is ${formatFileSize(CONFIG.maxFileSize)}`);
            return false;
        }

        // Check file type
        if (!CONFIG.allowedTypes.includes(file.type)) {
            showError('Invalid file type. Please upload a PDF, Word document, or image file.');
            return false;
        }

        return true;
    }

    // Update file information display
    function updateFileInfo(file) {
        const icon = getFileIcon(file.type);
        const size = formatFileSize(file.size);
        const fileInfo = `
            <div class="file-info">
                <span class="file-icon">${icon}</span>
                <span class="file-name-text">${file.name}</span>
                <span class="file-size">(${size})</span>
            </div>
        `;
        
        fileName.innerHTML = fileInfo;
        fileName.classList.add('upload-success');
    }

    // Animate drop area
    function animateDropArea(isDragging) {
        const scale = isDragging ? 1.02 : 1;
        dropArea.style.transform = `scale(${scale})`;
        
        if (isDragging) {
            uploadIcon.classList.add('pulse');
            uploadText.textContent = 'Drop your file here';
        } else {
            uploadIcon.classList.remove('pulse');
            uploadText.textContent = 'Drag & drop your file or click to browse';
        }
    }

    // Show success animation
    function showSuccessAnimation() {
        dropArea.classList.add('success');
        
        // Create and show checkmark
        const checkmark = document.createElement('div');
        checkmark.className = 'checkmark';
        dropArea.appendChild(checkmark);

        setTimeout(() => {
            dropArea.classList.remove('success');
            checkmark.remove();
        }, 2000);
    }

    // Show error message
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'upload-error';
        errorDiv.textContent = message;

        // Remove existing error messages
        const existingError = dropArea.querySelector('.upload-error');
        if (existingError) existingError.remove();

        dropArea.appendChild(errorDiv);
        dropArea.classList.add('error');

        setTimeout(() => {
            errorDiv.remove();
            dropArea.classList.remove('error');
        }, 3000);
    }

    // Get appropriate icon for file type
    function getFileIcon(fileType) {
        const icons = {
            'application/pdf': '📄',
            'application/msword': '📝',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '📝',
            'image/jpeg': '🖼️',
            'image/png': '🖼️',
            'image/gif': '🖼️'
        };
        return icons[fileType] || '📎';
    }

    // Format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Add keyboard accessibility
    dropArea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });

    // Handle paste events
    document.addEventListener('paste', (e) => {
        const files = e.clipboardData.files;
        if (files.length > 0) {
            handleFiles(files);
        }
    });

    // Clean up function
    function cleanup() {
        currentFile = null;
        fileName.textContent = '';
        fileName.classList.remove('upload-success');
        dropArea.classList.remove('dragover', 'success', 'error');
        uploadIcon.classList.remove('pulse');
        uploadText.textContent = 'Drag & drop your file or click to browse';
    }

    // Reset button functionality (if needed)
    const resetButton = document.querySelector('.reset-button');
    if (resetButton) {
        resetButton.addEventListener('click', cleanup);
    }
});
