// Main function to open the appointment modal and set up event listeners
function openCreateAppointmentModal() {
    fetch('/appointment/add')
        .then(response => response.text())
        .then(data => {
            setupModal(data);
        })
        .catch(error => {
            console.error('Error loading modal:', error);
        });
}

// Function to set up the modal content and attach event listeners
function setupModal(data) {
    document.getElementById("createAppointmentModal").innerHTML = data;
    document.getElementById("myModal").classList.add("active");

    // Add event listener for closing the modal
    document.getElementById("closeModalBtn").onclick = function () {
        document.getElementById("myModal").classList.remove("active");
    };

    // Add event listener to close the modal when clicking outside of it
    window.onclick = function (event) {
        if (event.target == document.getElementById("myModal")) {
            document.getElementById("myModal").classList.remove("active");
        }
    };

    // Add event listener for form submission validation
    let form = document.getElementById("appointmentForm");
    if (form) {
        form.addEventListener("submit", handleFormSubmission);
    } else {
        console.error("Form not found");
    }
}

// Function to handle form submission and validate the date field
function handleFormSubmission(event) {
    let dateField = document.getElementById("form-date");
    if (dateField) {
        let today = new Date().toISOString().split('T')[0];
        if (dateField.value < today) {
            event.preventDefault(); // Prevent form submission
            dateField.setCustomValidity('Randevu tarihi geçmişte olamaz.');
            dateField.reportValidity();
        } else {
            dateField.setCustomValidity(''); // Clear the custom validation message if the date is valid
        }
    } else {
        console.error("Date field not found");
    }
}

// Attach the main function to the click event of the button
document.getElementById("openCreateAppointmentModal").onclick = openCreateAppointmentModal;
