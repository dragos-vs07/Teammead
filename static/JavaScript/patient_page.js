function logout_user()
{
     window.location.href ="/logout";
}
function redirect_to_doctor_page( doctor_id )
{
     window.location.href ="/find_doctor/" + doctor_id;
}