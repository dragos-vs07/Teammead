function open_confirm_window()
{
    document.getElementById("confirm_window").style.display = "block";
}
function close_confirm_window()
{
    document.getElementById("confirm_window").style.display = "none";
}
function logout_user()
{
     window.location.href ="/logout";
}
function submit_deactivation()
{
    const input_password = document.getElementById("confirm_password").value;

    fetch(  "/deactivate_account" , {
            method: "POST" ,
            headers: {
                "Content-Type" : "application/json" 
            } ,
            body : JSON.stringify({ input_password : input_password })
        }
    ).then( res => res.json() ).then( data => {
            if( !data.success )
                alert("Wrong password");
            else
                window.location.href ="/"
    })
}
function open_password_change_window()
{
    document.getElementById("old_password_required_window").style.display = "block";
}
function close_password_change_window()
{
    document.getElementById("old_password_required_window").style.display = "none";
}
function submit_password_change()
{
    const input_password = document.getElementById("old_password").value;

    fetch("/submit_changes_auth" , {
        method : "POST" ,
        headers : {
            "Content-Type" : "application/json"
        } ,
        body : JSON.stringify({ old_password : input_password ,
                                new_password :  document.querySelector("input[name='new_password']").value ,
                                new_email : document.querySelector("input[name='new_email']").value 
         })
    }).then( res => res.json() ).then( data => {
            if( data.success ){
               close_password_change_window()
               alert("Changes applied successfully")
            }
            else
                alert("Wrong password");
    })
}
