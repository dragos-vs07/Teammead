
const calendar = new FullCalendar.Calendar(
    document.getElementById('calendar'),
    {
        initialView: 'dayGridMonth',
        events: '/api/get_patient_appointments'
    }
);

calendar.render();

function logout_user()
{
     window.location.href ="/logout";
}