document.addEventListener('DOMContentLoaded', function() {
    // Ensure Bootstrap modals work properly for quick action buttons

    // Fix for modal focus and backdrop issues
    var modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        modal.addEventListener('shown.bs.modal', function () {
            // Focus the first input element inside the modal when shown
            var firstInput = modal.querySelector('input, select, textarea, button');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });

    // Prevent multiple modals from causing backdrop issues
    var openModals = 0;
    modals.forEach(function(modal) {
        modal.addEventListener('show.bs.modal', function () {
            openModals++;
            document.body.classList.add('modal-open');
        });
        modal.addEventListener('hidden.bs.modal', function () {
            openModals--;
            if (openModals <= 0) {
                document.body.classList.remove('modal-open');
                openModals = 0;
            }
        });
    });

    // AJAX form submission for quick action modals: appointment, payment, prescription
    function ajaxFormSubmit(formSelector, modalSelector) {
        const form = document.querySelector(formSelector);
        const modal = document.querySelector(modalSelector);
        if (!form || !modal) return;

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const submitButton = form.querySelector('button[type="submit"]');
            if (!submitButton) return;

            // Disable submit button and show loading spinner
            submitButton.disabled = true;
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...';

            const formData = new FormData(form);

            fetch(form.action, {
                method: form.method,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json().catch(() => null);
            })
            .then(data => {
                // If server returns JSON with success key
                if (data && data.success) {
                    // Close modal
                    const bsModal = bootstrap.Modal.getInstance(modal);
                    if (bsModal) {
                        bsModal.hide();
                    }
                    // Optionally show success message (using alert for simplicity)
                    alert('Action completed successfully.');
                    // Optionally reload or update parts of the page here
                } else if (data && data.error) {
                    alert('Error: ' + data.error);
                } else {
                    // If no JSON or unexpected response, fallback to full page reload
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('AJAX form submission error:', error);
                alert('An error occurred. Please try again.');
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.innerHTML = originalText;
            });
        });
    }

    // Initialize AJAX form submissions for quick action modals
    ajaxFormSubmit('#newAppointmentModal form', '#newAppointmentModal');
    ajaxFormSubmit('#newPaymentModal form', '#newPaymentModal');
    ajaxFormSubmit('#newPrescriptionModal form', '#newPrescriptionModal');
});
