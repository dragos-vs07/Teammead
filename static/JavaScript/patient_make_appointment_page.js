let exceptions_list = [];

// load exceptions once when page loads
fetch(`/api/get_exceptions/${doctorId}`)
    .then(r => r.json())
    .then(data => { exceptions_list = data; });


// CALENDAR

let previous_cell = null;
let previous_day = null;

let selected_date = null;


function blocked(dateStr, timeStr) {
     
     console.log(exceptions_list);

    for (const e of exceptions_list) {

          if (e.start_date < e.end_date) //if the blockage spans multiple days
          {
               if ( e.start_date < dateStr && dateStr < e.end_date) //if it s simply between the days
                    return true;
               else if(e.start_date == dateStr && e.start_time <= timeStr) //if it s on the first day and after starting time
                    return true;
                else if(e.end_date == dateStr &&  timeStr < e.end_time ) //if it s on the last day and before ending time
                    return true;     
          }
          else if(e.start_date == dateStr) //if the blockage is single day and the day matches
          {
                    if(e.start_time <= timeStr && timeStr < e.end_time) //if between the closing times
                         return true;
          }
    }
    return false;
}

function ClickCell(info) {
    const events = calendar.getEvents().filter(e =>
        e.startStr.startsWith(info.dateStr)
    );
    const isUnavailable = events.some(e => e.title === 'Unavailable');
    if (isUnavailable) return;

    if (previous_cell) {
        previous_cell.style.border = '';
        document.getElementById(previous_day + "_segments").style.display = "none";
    }

    if (previous_button) {
        previous_button.style.backgroundColor = "";
        previous_button = null;
        selected_date = null;
    }

    info.dayEl.style.border = '2px solid #000000';

    const current_day = (info.date.getDay() - 1 + 7) % 7;
    const segDiv = document.getElementById(current_day + "_segments");

    segDiv.querySelectorAll('.time_segment_button').forEach(btn => {
        btn.style.display = blocked(info.dateStr, btn.textContent.trim()) ? "none" : "block";
    });

    document.getElementById("appointment_panel").style.display = "block";
    document.getElementById("main_text").textContent = "Book an appointment for " + info.dateStr;
    segDiv.style.display = "flex";

    previous_cell = info.dayEl;
    previous_day = current_day;
    selected_date = info.dateStr;
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

let selected_time = null;
let previous_button = null;

function selectTimeSegment(this_button)
{
     selected_time = this_button.textContent;

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
function closeModal()
{
     document.getElementById("modal_box").style.display = "none";
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
                    date : selected_date +' '+selected_time , 
                    // when user clicks a time segment the date is already stuck to it too and is stored here
               }
          )
     }
)
closeModal();
}
