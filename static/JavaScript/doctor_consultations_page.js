
searchBar = document.getElementById("patient_search");
searchBar.addEventListener("input" , function(){

    document.querySelectorAll(".patient_button").forEach( p =>{

        if( p.textContent.toLowerCase().includes(searchBar.value.toLowerCase()))
            p.style.display = "inline-block";
        else
            p.style.display = "none";
    });

});