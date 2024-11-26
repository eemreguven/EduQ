document.addEventListener('DOMContentLoaded', function () {
    const questionCountSelect = document.getElementById('question_count');
    const easyInput = document.getElementById('easy');
    const mediumInput = document.getElementById('medium');
    const difficultInput = document.getElementById('difficult');
    const easyWarning = document.getElementById('easyWarning');
    const mediumWarning = document.getElementById('mediumWarning');
    const difficultWarning = document.getElementById('difficultWarning');
    const totalWarning = document.getElementById('totalWarning');

    // Validate individual input fields
    function validateInput(input, warning) {
        const value = parseInt(input.value, 10);
        if (isNaN(value) || value < 0 || value > 10) {
            warning.textContent = 'Value must be between 0 and 10.';
        } else {
            warning.textContent = '';
        }
    }

    // Validate the total count
    function validateTotal() {
        const questionCount = parseInt(questionCountSelect.value, 10);
        const easy = parseInt(easyInput.value, 10) || 0;
        const medium = parseInt(mediumInput.value, 10) || 0;
        const difficult = parseInt(difficultInput.value, 10) || 0;

        if (easy + medium + difficult !== questionCount) {
            totalWarning.textContent = `The sum of easy, medium, and difficult questions must equal ${questionCount}.`;
        } else {
            totalWarning.textContent = '';
        }
    }

    // Add event listeners for real-time validation
    easyInput.addEventListener('input', () => {
        validateInput(easyInput, easyWarning);
        validateTotal();
    });

    mediumInput.addEventListener('input', () => {
        validateInput(mediumInput, mediumWarning);
        validateTotal();
    });

    difficultInput.addEventListener('input', () => {
        validateInput(difficultInput, difficultWarning);
        validateTotal();
    });

    questionCountSelect.addEventListener('change', () => {
        validateTotal();
    });

    // Initial validation on page load
    validateTotal();
});
