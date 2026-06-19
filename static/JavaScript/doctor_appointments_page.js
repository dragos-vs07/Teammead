

const start_date_input = document.getElementById("start_date_input")
const end_date_input = document.getElementById("end_date_input")

start_date_input.addEventListener("change" , function(){
     end_date_input.min = start_date_input.value;
})
