// ==========================================================
// AI Loan Decision Support System
// Main JavaScript
// ==========================================================

document.addEventListener("DOMContentLoaded", () => {

    initializeAlerts();
    initializeForms();
    initializeProgressBar();
    initializeDeleteConfirmation();

});

// ==========================================================
// Auto Close Flash Messages
// ==========================================================

function initializeAlerts() {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach((alert) => {

        setTimeout(() => {

            if (bootstrap.Alert.getOrCreateInstance(alert)) {
                bootstrap.Alert.getOrCreateInstance(alert).close();
            }

        }, 4000);

    });

}

// ==========================================================
// Form Validation
// ==========================================================

function initializeForms() {

    const forms = document.querySelectorAll("form");

    forms.forEach((form) => {

        form.addEventListener("submit", (event) => {

            const inputs = form.querySelectorAll("input[required]");

            let valid = true;

            inputs.forEach((input) => {

                input.classList.remove("is-invalid");

                if (input.value.trim() === "") {

                    valid = false;

                    input.classList.add("is-invalid");

                }

            });

            if (!valid) {

                event.preventDefault();

                alert("Please fill all required fields.");

            }

        });

    });

}

// ==========================================================
// Animated Progress Bar
// ==========================================================

function initializeProgressBar() {

    const progressBar = document.querySelector(".progress-bar");

    if (!progressBar) return;

    const targetWidth = parseFloat(progressBar.innerText);

    progressBar.style.width = "0%";

    let width = 0;

    const animation = setInterval(() => {

        if (width >= targetWidth) {

            clearInterval(animation);

        } else {

            width++;

            progressBar.style.width = width + "%";
            progressBar.innerText = width + "%";

        }

    }, 15);

}

// ==========================================================
// Delete Confirmation
// ==========================================================

function initializeDeleteConfirmation() {

    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach((button) => {

        button.addEventListener("click", (event) => {

            const confirmDelete = confirm(
                "Are you sure you want to delete this record?"
            );

            if (!confirmDelete) {

                event.preventDefault();

            }

        });

    });

}

// ==========================================================
// Loading Button
// ==========================================================

function showLoading(button) {

    if (!button) return;

    button.disabled = true;

    button.dataset.originalText = button.innerHTML;

    button.innerHTML =
        '<span class="spinner-border spinner-border-sm"></span> Processing...';

}

// ==========================================================
// Restore Button
// ==========================================================

function hideLoading(button) {

    if (!button) return;

    button.disabled = false;

    if (button.dataset.originalText) {

        button.innerHTML = button.dataset.originalText;

    }

}

// ==========================================================
// Number Input Validation
// ==========================================================

document.querySelectorAll("input[type='number']").forEach((input) => {

    input.addEventListener("input", () => {

        if (Number(input.value) < 0) {

            input.value = "";

        }

    });

});