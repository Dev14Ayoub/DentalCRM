$(document).ready(function() {
    // Hide all tab panes except the active one on page load
    $('.tab-pane').not('.show.active').hide();

    // On tab shown event, show the active tab pane and hide others
    $('#patientTabs button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        var target = e.target.getAttribute('data-bs-target');
        $('.tab-pane').hide();
        $(target).show();
    });
});
