function logout_user()
{
     window.location.href ="/logout";
}

// CALENDAR

let previous_cell = null;
let previous_day = null;

function ClickCell(info)
{
     // info.dayEl accesses the actual cell
     if (previous_cell)
     {
          previous_cell.style.border = '';
          document.getElementById(previous_day+"_segments").style.display = "none";
     }

     info.dayEl.style.border = '2px solid #000000'  ;

     document.getElementById("appointment_panel").style.display = "block";
     document.getElementById("main_text").textContent = "Book an appointment for " + info.dateStr ;
     document.getElementById( ( info.date.getDay() - 1 + 7 ) % 7+"_segments").style.display = "block"
     
     // need to fetch the appointments this doctor has in this day and display them in the time segments menu

     previous_cell = info.dayEl;
     previous_day = ( info.date.getDay() - 1 + 7 ) % 7;
}
const calendar = new FullCalendar.Calendar(
    document.getElementById('calendar'),
    {
        initialView: 'dayGridMonth',
        firstDay: 1,
        events: function(info, successCallback, failureCallback) { // fires every time the user changes the view
          //  info.startStr, info.endStr give the current time range the user sees
          // call successCallback with your events array when ready
               fetch('/api/get_doctor_schedule/' + doctorId + '/' + info.startStr + '/' + info.endStr)
               .then(r => r.json()) // parse response as JSON
               .then(data =>successCallback(data));
          } ,
        dateClick: ClickCell ,
          
    }
);

calendar.render();