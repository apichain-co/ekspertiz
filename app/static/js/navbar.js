document.getElementById("openCreateAppointmentModal").onclick = function () {
    fetch('/appointment/add')
        .then(response => response.text())
        .then(data => {
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
        })
        .catch(error => {
            console.error('Error loading modal:', error);
        });
};
