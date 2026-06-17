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

     if (previous_button) // if a previous button remained press on another day
     {
          previous_button.style.backgroundColor = "";
          previous_button = null;
          selected_date = null;
     }

     info.dayEl.style.border = '2px solid #000000'  ;
     const current_day = ( info.date.getDay() - 1 + 7 ) % 7;

     document.getElementById("appointment_panel").style.display = "block";
     document.getElementById("main_text").textContent = "Book an appointment for " + info.dateStr ;
     document.getElementById( current_day+"_segments").style.display = "flex"
     // need to fetch the appointments this doctor has in this day and display them in the time segments menu

     previous_cell = info.dayEl;
     previous_day = current_day;

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

// APPOINTMENTS

let selected_date = null;
let previous_button = null;

function selectTimeSegment(this_button)
{
     selected_date = this_button.textContent;

     document.getElementById("make_appointment_button").style.display = "block";
     document.getElementById("make_appointment_button").style.display = "block";

     if (previous_button)
     {
          previous_button.style.backgroundColor = "";
     }

     this_button.style.backgroundColor = '#2BA5D9';
     previous_button = this_button;
}
function showConfirmBox()
{
     document.getElementById("modal_box").style.display = "flex";
}
function submitAppointment()
{

 fetch(   '/enquire_appointment' , 
     
     {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(
               {
                    doctor_id: doctorId, // already set as variable in html when page loads
                    date : selected_date , 
                    // when user clicks a time segment the date is already stuck to it too and is stored here
               }
          )
     }
)
}
function closeModal()
{
     document.getElementById("modal_box").style.display = "none";
}