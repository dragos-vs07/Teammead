

function logout_user()
{
     window.location.href ="/logout";
}

// CALENDAR 

const calendar = new FullCalendar.Calendar(
    document.getElementById('calendar'),
    {
        initialView: 'dayGridMonth',
        events: '/api/get_patient_appointments'
    }
);

calendar.render();

// DOCTOR SEARCH

const doc_buttons = document.querySelectorAll(".doctor_button") // get all doctors shown

searchbar = document.getElementById('doctor_search')
searchbar.addEventListener("input" , function(){ // fires on any change to input
    doc_buttons.forEach( b =>{
                
            if( b.textContent.toLowerCase().includes(searchbar.value.toLowerCase()))
                b.style.display = "inline-block";
            else
                b.style.display ="none";
    });
})