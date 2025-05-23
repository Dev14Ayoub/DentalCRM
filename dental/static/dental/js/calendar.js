// dental/static/dental/js/calendar.js
document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: '/api/appointments/',
        eventDidMount: function(info) {
            info.el.style.backgroundColor = getStatusColor(info.event.extendedProps.status);
            info.el.style.borderColor = info.event.backgroundColor;
        },
        eventClick: function(info) {
            window.location.href = info.event.url;
        }
    });
    calendar.render();

    function getStatusColor(status) {
        const colors = {
            'SCH': '#0dcaf0',  // Bootstrap info
            'COM': '#198754',   // Bootstrap success
            'CAN': '#dc3545',   // Bootstrap danger
            'RES': '#ffc107'    // Bootstrap warning
        };
        return colors[status] || '#6c757d';
    }
});