document.addEventListener('DOMContentLoaded', function() {
    // Detailed debugging for quick action buttons and modals

    // Log clicks on quick action buttons
    const quickActionButtons = document.querySelectorAll('.card .btn-outline-primary, .card .btn-outline-success, .card .btn-outline-info');
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            console.log('Quick action button clicked:', event.target);
        });
    });

    // Log modal show and hide events with timestamps
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            console.log(`[${new Date().toISOString()}] Modal shown:`, modal.id);
        });
        modal.addEventListener('shown.bs.modal', function() {
            console.log(`[${new Date().toISOString()}] Modal fully shown:`, modal.id);
        });
        modal.addEventListener('hide.bs.modal', function() {
            console.log(`[${new Date().toISOString()}] Modal hide started:`, modal.id);
        });
        modal.addEventListener('hidden.bs.modal', function() {
            console.log(`[${new Date().toISOString()}] Modal fully hidden:`, modal.id);
        });
    });

    // Log form submissions inside modals
    const modalForms = document.querySelectorAll('.modal form');
    modalForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            console.log(`[${new Date().toISOString()}] Form submitted in modal:`, form.closest('.modal').id);
        });
    });

    // Monitor AJAX requests triggered by form submissions or buttons
    (function(open) {
        XMLHttpRequest.prototype.open = function(method, url) {
            this.addEventListener('loadstart', function() {
                console.log(`[${new Date().toISOString()}] AJAX request started: ${method} ${url}`);
            });
            this.addEventListener('loadend', function() {
                console.log(`[${new Date().toISOString()}] AJAX request ended: ${method} ${url} - Status: ${this.status}`);
            });
            open.apply(this, arguments);
        };
    })(XMLHttpRequest.prototype.open);

    // Catch unhandled promise rejections to log errors
    window.addEventListener('unhandledrejection', function(event) {
        console.error(`[${new Date().toISOString()}] Unhandled promise rejection:`, event.reason);
    });

    // Catch global errors
    window.addEventListener('error', function(event) {
        console.error(`[${new Date().toISOString()}] Global error:`, event.message, 'at', event.filename + ':' + event.lineno + ':' + event.colno);
    });
});
