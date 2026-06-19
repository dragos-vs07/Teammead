

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

searchBar = document.getElementById('doctor_search')
searchBar.addEventListener("input" , function(){ // fires on any change to input
    document.querySelectorAll(".doctor_button").forEach( b =>{
                
            if( b.textContent.toLowerCase().includes(searchBar.value.toLowerCase()))
                b.style.display = "inline-block";
            else
                b.style.display ="none";
    });
})

//auto styling
