document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileElem');
    const fileInfo = document.getElementById('file-info');
    const filenameDisplay = document.getElementById('filename');
    const processBtn = document.getElementById('process-btn');
    const loadingState = document.getElementById('loading');
    const resultState = document.getElementById('result');
    const errorState = document.getElementById('error');
    const errorMessage = document.getElementById('error-message');
    const recordsCount = document.getElementById('records-count');
    const downloadBtn = document.getElementById('download-btn');
    const resetBtn = document.getElementById('reset-btn');
    const retryBtn = document.getElementById('retry-btn');

    let currentFile = null;

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropArea.classList.add('highlight');
    }

    function unhighlight(e) {
        dropArea.classList.remove('highlight');
    }

    // Handle dropped files
    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    // Handle click to upload
    dropArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type !== 'application/pdf') {
                showError('Por favor, selecciona un archivo PDF válido.');
                return;
            }
            
            currentFile = file;
            filenameDisplay.textContent = file.name;
            
            // UI State change
            dropArea.classList.add('hidden');
            errorState.classList.add('hidden');
            fileInfo.classList.remove('hidden');
        }
    }

    processBtn.addEventListener('click', uploadFile);

    function uploadFile() {
        if (!currentFile) return;

        const formData = new FormData();
        formData.append('file', currentFile);

        // UI State change
        fileInfo.classList.add('hidden');
        loadingState.classList.remove('hidden');

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Error en el servidor') });
            }
            return response.json();
        })
        .then(data => {
            // UI State change
            loadingState.classList.add('hidden');
            resultState.classList.remove('hidden');
            
            const timeMsg = data.processing_time ? ` en ${data.processing_time}s` : '';
            recordsCount.textContent = `Se encontraron ${data.records_found} registros exitosamente${timeMsg}.`;
            downloadBtn.href = data.excel_url;
        })
        .catch(error => {
            showError(error.message);
        });
    }

    function showError(msg) {
        loadingState.classList.add('hidden');
        fileInfo.classList.add('hidden');
        dropArea.classList.add('hidden');
        
        errorMessage.textContent = msg;
        errorState.classList.remove('hidden');
    }

    function resetApp() {
        currentFile = null;
        fileInput.value = '';
        
        resultState.classList.add('hidden');
        errorState.classList.add('hidden');
        fileInfo.classList.add('hidden');
        
        dropArea.classList.remove('hidden');
    }

    resetBtn.addEventListener('click', resetApp);
    retryBtn.addEventListener('click', resetApp);
});
