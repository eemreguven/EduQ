document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('uploadForm');
    const fileRadio = document.getElementById('fileRadio');
    const youtubeRadio = document.getElementById('youtubeRadio');
    const fileCard = document.getElementById('fileCard');
    const youtubeInputContainer = document.getElementById('youtubeInputContainer');
    const youtubeUrlInput = document.getElementById('youtubeUrl');
    const fileInput = document.getElementById('fileInput');
    const selectedFileName = document.getElementById('selectedFileName');
    const chooseFileText = document.getElementById('chooseFileText');
    const submitButton = form.querySelector('button[type="submit"]');
    const processingSection = document.getElementById('processingSection');
    const processingMessage = document.getElementById('processingMessage');
    const errorModal = document.getElementById('errorModal');
    const errorMessage = document.getElementById('errorMessage');
    const closeModal = document.getElementById('closeModal');

    function resetFormState() {
        fileInput.value = '';
        youtubeUrlInput.value = '';
        selectedFileName.textContent = '';
        chooseFileText.textContent = 'Upload a file';
        submitButton.disabled = true;
    
        fileRadio.checked = true;
        youtubeRadio.checked = false;
    
        fileCard.style.display = 'block';
        youtubeInputContainer.style.display = 'none';
        youtubeUrlInput.removeAttribute('required');
    
        form.style.display = 'block';
        processingSection.style.display = 'none';
        processingMessage.textContent = '';
    }    

    function toggleResourceInput() {
        if (fileRadio.checked) {
            fileCard.style.display = 'block';
            youtubeInputContainer.style.display = 'none';
            youtubeUrlInput.removeAttribute('required');
            fileInput.setAttribute('required', 'required');
        } else {
            fileCard.style.display = 'none';
            youtubeInputContainer.style.display = 'block';
            youtubeUrlInput.setAttribute('required', 'required');
            fileInput.removeAttribute('required');
        }
        validateInputs();
    }

    function validateInputs() {
        if (fileRadio.checked) {
            submitButton.disabled = !fileInput.files.length;
        } else if (youtubeRadio.checked) {
            submitButton.disabled = !youtubeUrlInput.value.trim();
        }
    }

    function fetchStatus() {
        fetch('/progress')
            .then(response => response.json())
            .then(data => {
                processingMessage.textContent = data.status;
            })
            .catch(err => console.error('Error fetching progress:', err));
    }

    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            selectedFileName.textContent = file.name;
            selectedFileName.style.display = 'block';
            chooseFileText.textContent = 'Tap to change file';
        } else {
            selectedFileName.textContent = '';
            selectedFileName.style.display = 'none';
            chooseFileText.textContent = 'Upload a file';
        }
        validateInputs();
    });

    youtubeUrlInput.addEventListener('input', validateInputs);

    closeModal.addEventListener('click', () => {
        errorModal.style.display = 'none';
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);

        form.style.display = 'none';
        processingSection.style.display = 'block';
        processingMessage.textContent = 'Processing...';

        const intervalId = setInterval(fetchStatus, 500);

        try {
            const response = await fetch(form.action, { method: 'POST', body: formData });
            const result = await response.json();

            clearInterval(intervalId);

            if (response.ok && result.success) {
                processingMessage.textContent = 'Processing completed successfully!';
                setTimeout(() => window.location.href = result.redirect_url, 500);
            } else {
                throw new Error(result.error || 'An unknown error occurred.');
            }
        } catch (err) {
            clearInterval(intervalId);
            form.style.display = 'block';
            processingSection.style.display = 'none';
            errorMessage.textContent = err.message;
            errorModal.style.display = 'block';
        }
    });

    window.addEventListener('pageshow', resetFormState);
    fileRadio.addEventListener('change', toggleResourceInput);
    youtubeRadio.addEventListener('change', toggleResourceInput);

    resetFormState();
});
