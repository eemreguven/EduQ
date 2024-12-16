document.addEventListener('DOMContentLoaded', function () {
    const questionInputs = document.querySelectorAll('.question-input');
    const totalWarning = document.getElementById('totalWarning');
    const submitButton = document.getElementById('submitButton');
    const processingSection = document.getElementById('processingSection');
    const questionTable = document.getElementById('questionTable');
    const processingMessage = document.getElementById('processingMessage');
    const form = document.getElementById('questionForm');
    let progressInterval;

    // Reset form inputs and state
    function resetFormState() {
        questionInputs.forEach(input => input.value = '0');
        totalWarning.style.visibility = 'visible';
        totalWarning.textContent = 'Total must be between 1 and 10.';
        submitButton.disabled = true; 
        processingSection.style.display = 'none';
        questionTable.style.display = 'block';
        validateTotals(); // Validate totals on reset
    }

    // Validate totals and enable/disable the submit button
    function validateTotals() {
        let total = 0;
        questionInputs.forEach(input => total += parseInt(input.value, 10) || 0);

        if (total < 1 || total > 10) {
            totalWarning.style.visibility = 'visible';
            totalWarning.textContent = 'Total must be between 1 and 10.';
            submitButton.disabled = true;
        } else {
            totalWarning.style.visibility = 'hidden';
            submitButton.disabled = false;
        }
    }

    // Attach event listeners to question inputs for validation
    questionInputs.forEach(input => input.addEventListener('input', validateTotals));

    // Fetch progress updates during form processing
    async function fetchProgress() {
        try {
            const response = await fetch('/progress');
            const data = await response.json();
            processingMessage.textContent = data.status;
        } catch (error) {
            console.error('Error fetching progress:', error);
        }
    }

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        submitButton.disabled = true;
        submitButton.style.display = 'none'; 
    
        // Hide question table and show processing section
        questionTable.style.display = 'none';
        totalWarning.style.display = 'none'
        processingSection.style.display = 'block';
        processingMessage.textContent = 'Generating questions...';
    
        const formData = new FormData(form);
        progressInterval = setInterval(fetchProgress, 500);
    
        try {
            const response = await fetch(form.action, { method: 'POST', body: formData });
            const result = await response.json();
    
            if (result.success && result.redirect_url) {
                clearInterval(progressInterval);
                processingMessage.textContent = 'Questions generated successfully!';
                setTimeout(() => window.location.href = result.redirect_url, 500);
            } else {
                throw new Error(result.error || 'An unknown error occurred.');
            }
        } catch (err) {
            clearInterval(progressInterval);
            processingMessage.textContent = 'An error occurred. Please try again.';
            totalWarning.style.visibility = 'visible';
            totalWarning.textContent = err.message;
    
            // Show the question table and submit button again
            submitButton.style.display = 'block';
            submitButton.disabled = false;
            questionTable.style.display = 'block';
        }
    });
    

    window.addEventListener('pageshow', resetFormState);
    resetFormState();
});
