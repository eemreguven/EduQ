document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('.question-input'); // Select all input boxes
    const totalWarning = document.getElementById('totalWarning'); // Total warning message
    const submitButton = document.getElementById('submitButton'); // Submit button

    function validateTotals() {
        let total = 0;

        // Calculate the total value of all input boxes
        inputs.forEach((input) => {
            const value = parseInt(input.value, 10) || 0;
            total += value;
        });

        // Validate total and update UI
        if (total < 1 || total > 10) {
            totalWarning.style.visibility = 'visible'; // Show warning if invalid
            totalWarning.textContent = 'Total must be between 1 and 10.';
            submitButton.disabled = true; // Disable the submit button
        } else {
            totalWarning.style.visibility = 'hidden'; // Hide the warning
            submitButton.disabled = false; // Enable the submit button
        }
    }



    // Add event listeners for all input boxes to validate on input
    inputs.forEach((input) => {
        input.addEventListener('input', validateTotals);
    });


    // Initial validation on page load
    validateTotals();
});
