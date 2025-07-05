document.addEventListener('DOMContentLoaded', function() {
    // Debug event listeners on quick action buttons and modals

    // Log clicks on quick action buttons
    const quickActionButtons = document.querySelectorAll('.card .btn-outline-primary, .card .btn-outline-success, .card .btn-outline-info');
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            console.log('Quick action button clicked:', event.target);
        });
    });

    // Log modal show and hide events
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            console.log('Modal shown:', modal.id);
        });
        modal.addEventListener('hide.bs.modal', function() {
            console.log('Modal hidden:', modal.id);
        });
    });

    // Catch unhandled promise rejections to log errors
    window.addEventListener('unhandledrejection', function(event) {
        console.error('Unhandled promise rejection:', event.reason);
    });
});
