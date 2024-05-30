// Example JavaScript for interactive elements
document.addEventListener('DOMContentLoaded', function() {
    // New script for handling form submissions
    const workoutForm = document.querySelector('#log-section form');
    workoutForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(workoutForm);
        fetch(workoutForm.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert('Workout logged successfully!');
            // Optionally update the UI here
        })
        .catch(error => {
            alert('Failed to log workout');
        });
    });
});

