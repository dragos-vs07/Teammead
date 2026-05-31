from flask import Flask , render_template , request , flash , redirect , url_for , session , send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

CURRENT_DATE = datetime.now().strftime("%d/%m/%Y")
app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) # not the database , but the controller of it    

class UserAuth(db.Model):   # database user model , a.k.a. how an entry should look like
                                # in the table that contains user login info
        __tablename__ = "user_auth"
        id = db.Column(db.Integer , primary_key = True)
        username = db.Column(db.String(80) , unique = True , nullable = False) # prevents two users having the same username automatically
        password = db.Column(db.String(200) , nullable = False)
        email = db.Column(db.String(200) , nullable = False)
        update_date = db.Column(db.String(20))  # last update of the entry date

class PatientInfo(db.Model):
       __tablename__ = "patient_info"
       id = db.Column(db.Integer , primary_key = True)
       user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id")) # linked to UserAuth by the name
       first_name = db.Column(db.String(50) , nullable = False )
       last_name = db.Column(db.String(50) , nullable = False ) # family name
       birth_date = db.Column(db.String, nullable = False)
       gender = db.Column(db.String(20), nullable = False)
       email = db.Column(db.String(100), nullable = False)
       phone_number = db.Column(db.String(20))
       home_adress = db.Column(db.String(100))
       update_date = db.Column(db.String(20))  # last update of the entry date

class DoctorInfo(db.Model):
        __tablename__ = "doctor_info"
        id = db.Column(db.Integer , primary_key = True)
        user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id"))
        first_name = db.Column(db.String(50) , nullable = False )
        last_name = db.Column(db.String(50) , nullable = False ) # family name
        birth_date = db.Column(db.String(20), nullable = False)
        gender = db.Column(db.String(20), nullable = False)
        email = db.Column(db.String(100), nullable = False)
        phone_number = db.Column(db.String(20))
        workplace_adress = db.Column(db.String(100))
        update_date = db.Column(db.String(20))  # last update of the entry date

class ConsultationInfo(db.Model):  # defining an entry that contains user medical info
                                # registered after a consultation
        __tablename__ = "consult_info"
        id = db.Column(db.Integer , primary_key = True)
        doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_info.id"))
        patient_id = db.Column(db.Integer, db.ForeignKey("patient_info.id"))
        weight = db.Column(db.Integer)
        diagnostic = db.Column(db.String(50) , nullable = False ) # Healthy or disease name
        health_state = db.Column(db.Integer)    # rating from 1 to 10 health state
        consultation_date = db.Column(db.String(20) , nullable = False ) # consultation date
        upload_file_path = db.Column(db.String(200)) # if there is an atteched file to this consultation , the path to it is stored here
       # the doctor to which this patient is registered / that takes care of the patient
        update_date = db.Column(db.String(20))  # last update of the entry date

def create_birth_date( day , month , year):
        return f"{day}/{month}/{year}"

@app.route('/') # main url
def load_main_page():       # sends to the browser the main page
        return render_template("index.html")

@app.route('/register') # register page url
def load_register_page():    # sends to the browser the register page
        return render_template("register.html")

@app.route('/submit_register' , methods=["POST"])       #activates when clicking submit button
def submit_register_data():                                  #on the register form
                                                        #sends the form data here
        username = request.form.get("username")         # getting the username sent
        password = request.form.get("password")         # getting the password sent
        is_doctor = request.form.get("is_doctor")
        email = request.form.get("email")
        if not username or not password:        # if one is missing => invalid input
            flash("All fields must be completed")       # display error message
            return redirect(url_for("load_register_page"))   # redirect to same page
        
        existing_user =  UserAuth.query.filter_by(username=username).first() 
        # checks whether or not the user with the given username exists

        if existing_user :      # if the user already exists
            flash("Username already exists")    # display error message
            return redirect(url_for("load_register_page"))   # redirect to the same page
        
        # if all went well , we arrive here 
        if not username:
                flash("Username required")
                return redirect(url_for("load_register_page"))
        if not password:
                flash("Password required")
                return redirect(url_for("load_register_page"))
        
        if not email:
                flash("Email required")
                return redirect(url_for("load_register_page"))
        
        new_user = UserAuth(username = username , password = password , email = email , update_date = CURRENT_DATE )   #create a new user doctor
       
        # and add the entry to the database    
        db.session.add(new_user)
        db.session.commit()

        if is_doctor == "on":
                new_doctor = DoctorInfo(
                      user_id = new_user.id,
                      first_name = request.form.get("first_name").lower() ,
                      last_name = request.form.get("last_name").lower() ,
                      birth_date =  create_birth_date( request.form.get("day") , request.form.get("month") , request.form.get("year") ) ,
                      gender = request.form.get("gender") ,
                      email = new_user.email ,
                      phone_number = request.form.get("phone_number") ,
                      update_date = CURRENT_DATE
               )
                db.session.add(new_doctor)
        else :
                new_patient = PatientInfo(
                      user_id = new_user.id,
                      first_name = request.form.get("first_name").lower() ,
                      last_name = request.form.get("last_name").lower() ,
                      birth_date =  create_birth_date( request.form.get("day") , request.form.get("month") , request.form.get("year") ) ,
                      gender = request.form.get("gender") ,
                      email = new_user.email ,
                      phone_number = request.form.get("phone_number") ,
                      update_date = CURRENT_DATE
               )
                db.session.add(new_patient)
                
        db.session.commit()

        flash("Account created succesfully")    #display success message
        return redirect(url_for("load_register_page"))       #return the same page
        
@app.route('/patient_info')
def load_patient_page():

        if "user_id" not in session:
               return redirect(url_for("load_main_page"))
        
        user = PatientInfo.query.filter_by(user_id = session["user_id"]).first()
        return render_template(
                "patient_page.html",
                first_name = user.first_name.title() ,
                last_name = user.last_name.title() ,
                consultations = ConsultationInfo.query.filter_by( patient_id = session["user_id"])
                )

@app.route('/doctor_page')
def load_doctor_page():

        if "user_id" not in session:
               return redirect(url_for("load_main_page"))
        
        user = DoctorInfo.query.filter_by(user_id = session["user_id"]).first()
        return render_template("doctor_page.html", first_name = user.first_name.title() , last_name = user.last_name.title())

@app.route('/reg_consultation' , methods = ["POST"])
def submit_consultation():
       
        first_name_form = request.form.get("first_name").lower()
        last_name_form = request.form.get("last_name").lower()

        doc = DoctorInfo.query.filter_by(user_id = session["user_id"]).first()
        pat = PatientInfo.query.filter_by(first_name = first_name_form , last_name = last_name_form ).first()

        if pat is None :
                flash("No patient found")
                return redirect(url_for("load_doctor_page"))

        base = fr"C:\Users\Dragos\Desktop\Teammed\uploaded_consultation_files" # base folder path
        folder_path = fr"{base}\{first_name_form}_{last_name_form}" # patient folder path

        print(folder_path)
        os.makedirs(folder_path, exist_ok = True)   # if patient doesnt have a folder , create it

        file = request.files["file"]    # file from the browser
        file_path = fr"{folder_path}\{file.filename}" # final file path
        print(file_path)

        file.save(file_path)

        new_consultation = ConsultationInfo(
                weight = request.form.get("weight") ,
                diagnostic = request.form.get("diagnostic") ,
                consultation_date = request.form.get("date") ,
                doctor_id = doc.user_id ,
                patient_id = pat.user_id,
                health_state = request.form.get("health_state") ,
                upload_file_path = file_path
       )
        
        db.session.add(new_consultation)
        db.session.commit()

        return redirect(url_for("load_doctor_page"))

@app.route('/find_patient' , methods = ["POST"])
def display_patient_info():
        patient_first_name = request.form.get("first_name")
        patient_last_name = request.form.get("last_name")

        query_patient = PatientInfo.query.filter_by(first_name = patient_first_name.lower() , last_name = patient_last_name.lower()).first()
        if query_patient is None:
                flash("Patient doesnt exist")
                return redirect(url_for('load_doctor_page'))
        else:
                consultations = ConsultationInfo.query.filter_by(patient_id = query_patient.user_id).all()                                            
                return render_template( "patient_result.html" ,
                      first_name = patient_first_name.title(),
                      last_name = patient_last_name.title(),
                      birth_date = query_patient.birth_date,
                      gender = query_patient.gender ,
                      email = query_patient.email ,
                      phone_number = query_patient.phone_number ,
                      consultations = consultations ,
                      update_date = CURRENT_DATE
                )
        
@app.route('/download_attachment/<int:consultation_id>')
def download_attachment(consultation_id):
        consultation = ConsultationInfo.query.get_or_404(consultation_id)

        file_path = consultation.upload_file_path

        return send_file(file_path, as_attachment=True)

@app.route('/submit_login' , methods=["POST"])  #activates when clicking on submit login
def submit_login_data():

        username = request.form.get("username")
        password = request.form.get("password")

        found_user_by_username =  UserAuth.query.filter_by(username = username , password = password).first()
        found_user_by_email = UserAuth.query.filter_by( email = username , password = password ).first()

        #if a user with the given username and password exists within the database
        if found_user_by_username is None and found_user_by_email is None: # if not
               flash("Account not registered") # error message
               return redirect(url_for("load_main_page"))
        
        if found_user_by_username is None:
                found_user = found_user_by_email
        else:
                found_user = found_user_by_username

        session["user_id"] = found_user.id
        
        if PatientInfo.query.filter_by(user_id = found_user.id).first()  :
                session["role"] = "patient"
                return redirect(url_for("load_patient_page"))
        else:
                session["role"] = "doctor"
                return redirect(url_for("load_doctor_page"))

@app.route('/edit_account') # access password change , email change or delete account 
def load_edit_account_page():

        auth_entry = UserAuth.query.filter_by(id = session["user_id"]).first()

        if session['role'] == "doctor":
                user_entry = DoctorInfo.query.filter_by(user_id = session["user_id"]).first()
        else:
                user_entry = PatientInfo.query.filter_by(user_id = session["user_id"]).first()

        birth_date_split = user_entry.birth_date.split('/')

        return render_template(
                 "account_edit_page.html" ,
                   old_email = auth_entry.email ,
                   old_username = auth_entry.username,
                   old_first_name = user_entry.first_name.title(),
                   old_last_name = user_entry.last_name.title(),
                   old_phone_number = user_entry.phone_number,
                   old_day = birth_date_split[0],
                   old_month = birth_date_split[1],
                   old_year = birth_date_split[2] ,
                   gender = user_entry.gender
                   )

@app.route('/submit_changes_profile' , methods = ["POST"])
def update_profile_data():

        auth_entry = UserAuth.query.filter_by(id = session["user_id"]).first()

        if session['role'] == "doctor":
                user_entry = DoctorInfo.query.filter_by(id = session["user_id"]).first()
        else:
                user_entry = PatientInfo.query.filter_by(id = session["user_id"]).first()

        auth_entry.username = request.form.get("username")
        user_entry.first_name = request.form.get("first_name") 
        user_entry.last_name = request.form.get("last_name") 
        user_entry.gender =  request.form.get("gender") 
        user_entry.phone_number= request.form.get("phone_number") 
        user_entry.birth_date = create_birth_date(request.form.get("day") , request.form.get("month") , request.form.get("year"))
        user_entry.update_date = CURRENT_DATE
        
        db.session.commit()

        flash("Changes applied successfully")
        return redirect(url_for("load_edit_account_page"))

@app.route('/submit_changes_auth' , methods = ["POST"])
def update_authentification_data():

        auth_entry = UserAuth.query.filter_by(id = session["user_id"]).first()

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        new_email =  request.form.get("new_email")

        if auth_entry.password != old_password :        # for any changes to take place the user must input at least the old password
                flash("Old password is wrong")
                return redirect(url_for("load_edit_account_page"))
        
        if not new_password : # if the user input no new password , we leave the old one in place 
                new_password = old_password     # we do this since the user might only want to edit their email

        if new_email is None:   # since we prefill the email , if the user deletes it and inputs nothing new we give an error
                flash("Must input a valid email")
                return redirect(url_for("load_edit_account_page"))
        
        # if the user only wishes to edit their password they simply leave the old email in place already prefilled

        auth_entry.password = new_password
        auth_entry.email = new_email    
        auth_entry.update_date = CURRENT_DATE

        db.session.commit()

        flash("Authentification data updated successfully")
        return redirect(url_for("load_edit_account_page"))
        
with app.app_context():
        db.create_all()

if __name__ == "__main__":
        app.run()