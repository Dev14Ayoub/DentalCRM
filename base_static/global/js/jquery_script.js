$(document).ready(function() {
    console.log('Document ready: initializing scripts');

    // Debug: log when Record Payment button is clicked
    $('button[data-bs-target="#newPaymentModal"]').click(function() {
        console.log('Record Payment button clicked');
    });

    // Debug: log when payment modal is shown or hidden
    $('#newPaymentModal').on('show.bs.modal', function () {
        console.log('Payment modal is about to be shown');
    });
    $('#newPaymentModal').on('shown.bs.modal', function () {
        console.log('Payment modal is fully shown');
    });
    $('#newPaymentModal').on('hide.bs.modal', function () {
        console.log('Payment modal is about to be hidden');
    });
    $('#newPaymentModal').on('hidden.bs.modal', function () {
        console.log('Payment modal is fully hidden');
    });

    // Handle toggle confirm button click
    $('#toggleConfirmBtn').click(function() {
        var button = $(this);
        var appointmentId = button.data('appointment-id');
        $.ajax({
            url: '/patient/appointment/' + appointmentId + '/toggle-confirmation/',
            type: 'POST',
            headers: {
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    if (response.is_confirmed) {
                        button.text('Unconfirm Appointment');
                        button.removeClass('btn-success').addClass('btn-warning');
                    } else {
                        button.text('Confirm Appointment');
                        button.removeClass('btn-warning').addClass('btn-success');
                    }
                } else {
                    alert('Failed to update confirmation status.');
                }
            },
            error: function() {
                alert('Error occurred while updating confirmation status.');
            }
        });
    });

    // AJAX form submission for payment modal
    $('#paymentForm').submit(function(event) {
        event.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        var submitBtn = $('#submitPaymentBtn');
        submitBtn.prop('disabled', true);

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            headers: {
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                console.log('Payment AJAX success:', response);
                if (response.success) {
                    // Close modal and reload page
                    $('#newPaymentModal').modal('hide');
                    location.reload();
                } else {
                    alert('Failed to record payment: ' + (response.error || 'Unknown error'));
                    submitBtn.prop('disabled', false);
                }
            },
            error: function(xhr, status, error) {
                console.error('Payment AJAX error:', xhr.responseText);
                alert('Failed to record payment: ' + xhr.responseText);
                submitBtn.prop('disabled', false);
            }
        });
    });
});
