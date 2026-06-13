from flask import Flask , render_template , request , flash , redirect , url_for , session , send_file , jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , date
from werkzeug.security import generate_password_hash , check_password_hash
import os

app = Flask(__name__)
app.secret_key = "g6fd58734hj]5gkh53489dsf87324.jhg234jh!!kg39081098374#"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)  # not the database , but the controller of it    

# =========================
# MODELS
# =========================

class UserAuth(db.Model):
        __tablename__ = "user_auth"
        id = db.Column(db.Integer , primary_key = True)
        username = db.Column(db.String(80) , unique = True , nullable = False)
        password = db.Column(db.String(200) , nullable = False)
        email = db.Column(db.String(200) , nullable = False)
        active = db.Column(db.Boolean , nullable = False)
        update_date = db.Column(db.Date)

        patient = db.relationship(
                "PatientInfo" ,
                back_populates ="user" ,
                uselist=False
        )

        doctor = db.relationship(
                "DoctorInfo" ,
                back_populates ="user" ,
                uselist=False
        )


class PatientInfo(db.Model):
       __tablename__ = "patient_info"
       id = db.Column(db.Integer , primary_key = True)
       user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id"))
       first_name = db.Column(db.String(50) , nullable = False )
       last_name = db.Column(db.String(50) , nullable = False )
       birth_date = db.Column(db.Date , nullable = False)
       gender = db.Column(db.String(20), nullable = False)
       contact_email = db.Column(db.String(100), nullable = False)
       phone_number = db.Column(db.String(20))
       adress = db.Column(db.String(100))
       update_date = db.Column(db.Date)

       consultations = db.relationship(
                "ConsultationInfo" ,
                back_populates = "patient" ,
                order_by="ConsultationInfo.consultation_date.asc()" ,
       )

       user = db.relationship(
                "UserAuth" ,
                back_populates = "patient" ,
        )

class DoctorInfo(db.Model):
        __tablename__ = "doctor_info"
        id = db.Column(db.Integer , primary_key = True)
        user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id"))
        first_name = db.Column(db.String(50) , nullable = False )
        last_name = db.Column(db.String(50) , nullable = False )
        birth_date = db.Column(db.Date , nullable = False)
        gender = db.Column(db.String(20), nullable = False)
        contact_email = db.Column(db.String(100), nullable = False)
        phone_number = db.Column(db.String(20))
        adress = db.Column(db.String(100))
        specialisation = db.Column(db.String(100))
        update_date = db.Column(db.Date)

        consultations = db.relationship(
                "ConsultationInfo" ,
                back_populates = "doctor" ,
                order_by="ConsultationInfo.consultation_date.asc()" ,
        )

        user = db.relationship(
                "UserAuth" ,
                back_populates = "doctor" ,
        )


class ConsultationInfo(db.Model):
        __tablename__ = "consult_info"
        id = db.Column(db.Integer , primary_key = True)
        doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_info.id"))
        patient_id = db.Column(db.Integer, db.ForeignKey("patient_info.id"))
        diagnostic = db.Column(db.String(50) , nullable = False )
        weight = db.Column(db.Integer)
        health_state = db.Column(db.Integer)
        blood_pressure_systolic = db.Column(db.Integer) 
        blood_pressure_diastolic = db.Column(db.Integer)
        blood_oxygen_saturation = db.Column(db.Integer)  
        heart_rate = db.Column(db.Integer)
        consultation_date = db.Column(db.Date , nullable = False )
        upload_file_path = db.Column(db.String(200))
        update_date = db.Column(db.Date)

        patient = db.relationship(
        "PatientInfo",
        back_populates="consultations" ,
        )

        doctor = db.relationship(
        "DoctorInfo",
        back_populates="consultations" ,
        )

# =========================
# HELPERS
# =========================

def create_string_date( day , month , year):
        return f"{day}-{month}-{year}"

# =========================
# LOADING PAGES 
# =========================

@app.route('/')
def load_main_page():
        return render_template("index.html")

@app.route('/patient_stats_page')
def load_patient_stats_page():

        if "user_id" not in session or session.get("role") != "patient": # can only be accessed from patient account 
               return redirect(url_for("load_main_page"))
        
        user = db.session.get( UserAuth , session.get("user_id") )

        print(user.id)
        return render_template("patient_stats_page.html" ,
                               consultations = [{
                                        "diagnostic" : c.diagnostic ,
                                        "weight" : c.weight ,
                                        "health_state" : c.health_state ,
                                        "blood_pressure_systolic" : c.blood_pressure_systolic ,
                                        "blood_pressure_diastolic" : c.blood_pressure_diastolic ,
                                        "blood_oxygen_saturation" : c.blood_oxygen_saturation ,
                                        "heart_rate" : c.heart_rate ,
                                        "consultation_date" : c.consultation_date.strftime("%Y-%m-%d") ,
                               } for c in user.patient.consultations]
                               ) 

@app.route('/edit_account')
def load_edit_account_page(): # loads the edit account menu

        if "user_id" not in session : # only doctor can access this
               return redirect(url_for("load_main_page"))
        
        auth_entry = UserAuth.query.filter_by(id=session.get("user_id")).first()
        specialisation = ""
        
        if session.get("role") == "doctor":
                user_entry = DoctorInfo.query.filter_by(user_id=session.get("user_id")).first()
                specialisation = user_entry.specialisation
        else:
                user_entry = PatientInfo.query.filter_by(user_id=session.get("user_id")).first()
                
        
        
        return render_template(
                 "account_edit_page.html",
                   old_email=auth_entry.email,
                   old_username=auth_entry.username,
                   old_first_name=user_entry.first_name.title(),
                   old_last_name=user_entry.last_name.title(),
                   old_specialisation=specialisation , # null if user is a patient , checked anyway in jinja
                   old_adress =user_entry.adress ,
                   old_phone_number=user_entry.phone_number,
                   old_day=user_entry.birth_date.day ,
                   old_month=user_entry.birth_date.month ,
                   old_year=user_entry.birth_date.year ,
                   gender=user_entry.gender
        )

@app.route('/load_edit_consultation_page/<consultation_id>')
def load_edit_consultation_page(consultation_id):

        if "user_id" not in session or session.get("role") != "doctor": # only doctor can access this
               return redirect(url_for("load_main_page"))
        
        return render_template("edit_consultation_page.html",
                               c = ConsultationInfo.query.filter_by(id = consultation_id).first()
                               )

@app.route('/patient_info') # loads page for a patient user
def load_patient_page():

        if "user_id" not in session or session.get("role") != "patient": # only patient can access this
               return redirect(url_for("load_main_page"))
        
        user = PatientInfo.query.filter_by(user_id = session.get("user_id")).first()

        return render_template(
                "patient_page.html",
                first_name = user.first_name.title(),
                last_name = user.last_name.title(),
                patient = user ,
                consultations = [{
                "id": c.id ,
                "diagnostic": c.diagnostic,
                "consultation_date": c.consultation_date,
                "health_state": c.health_state ,
                "upload_file_path" : c.upload_file_path ,
                "doctor_first_name": c.doctor.first_name ,
                "doctor_last_name": c.doctor.last_name ,
                "doctor_specialisation": c.doctor.specialisation 
                } for c in user.consultations[:3] ]
        )


@app.route('/doctor_page') # loads page for a doctor user
def load_doctor_page():

        if "user_id" not in session or session.get("role") != "doctor": # only doctor can access this
               return redirect(url_for("load_main_page"))
        
        session["patient_id"] = 0

        user = DoctorInfo.query.filter_by(user_id = session.get("user_id")).first()

        return render_template(
            "doctor_page.html",
            first_name = user.first_name.title(),
            last_name = user.last_name.title() ,
            doctor = user
        )

@app.route('/register') # loads register menu
def load_register_page():
        return render_template("register.html")

@app.route('/find_patient' , methods=["POST","GET"]) # displays results for a sought patient
def load_patient_result_page():

        if "user_id" not in session or session.get("role") != "doctor": # only doctor can access this
               return redirect(url_for("load_main_page"))
        
        patient_first_name = request.form.get("first_name")
        patient_last_name = request.form.get("last_name")

        if not patient_first_name or not patient_last_name :
                flash("Must complete full name")
                return redirect(url_for('load_doctor_page'))
        
        query_patient = PatientInfo.query.filter_by(
                first_name=patient_first_name.lower(),
                last_name=patient_last_name.lower()
                ).first()

        if not query_patient :
                flash("Patient doesnt exist")
                return redirect(url_for('load_doctor_page'))

        session["patient_id"] = query_patient.id

        return render_template(
            "patient_result.html",
            first_name=patient_first_name.title(),
            last_name=patient_last_name.title(),
            birth_date=query_patient.birth_date,
            gender=query_patient.gender,
            email=query_patient.contact_email,
            phone_number=query_patient.phone_number,
            consultations=[{ # making the consultations dictionaries so we can convert them to json for the javascript part
                "id": c.id ,
                "diagnostic": c.diagnostic,
                "consultation_date": c.consultation_date,
                "health_state": c.health_state ,
                "weight": c.weight ,
                "blood_pressure_systolic" : c.blood_pressure_systolic ,
                "blood_pressure_diastolic" : c.blood_pressure_diastolic ,
                "heart_rate" : c.heart_rate ,
                "blood_oxygen_saturation" : c.blood_oxygen_saturation ,
                "upload_file_path" : c.upload_file_path ,
                "doctor_user_id" : c.doctor.user_id
            }
            for c in query_patient.consultations
            ] , 
            update_date=date.today() ,
        )
@app.route('/find_doctor/<int:doctor_id>' )
def load_doctor_result_page(doctor_id):

        if "user_id" not in session or session.get("role") != "patient": # only doctor can access this
               return redirect(url_for("load_main_page"))
        
        doctor = DoctorInfo.query.filter_by(id = doctor_id ).first()

        if not doctor :
                flash("doctor not found")
                return redirect(url_for("load_patient_page"))
        
        return render_template( 
                "doctor_result.html" , 
                first_name = doctor.first_name ,
                last_name = doctor.last_name ,
                specialisation = doctor.specialisation ,
                contact_email = doctor.contact_email ,
                phone_number = doctor.phone_number ,
                adress = doctor.adress             
        )
# =========================
# REGISTER
# =========================

@app.route('/submit_register' , methods=["POST"]) # addsa new user to database
def submit_register_data():

        username = request.form.get("username")
        password = request.form.get("password")
        is_doctor = request.form.get("is_doctor")
        email = request.form.get("email")

        if not username:
                flash("Username required")
                return redirect(url_for("load_register_page"))
        if not password:
                flash("Password required")
                return redirect(url_for("load_register_page"))
        if not email:
                flash("Email required")
                return redirect(url_for("load_register_page"))

        existing_user_username = UserAuth.query.filter_by(username=username).first()
        existing_user_email = UserAuth.query.filter_by(email=email).first()

        if existing_user_username:
            flash("An account with this username already exists")
            return redirect(url_for("load_register_page"))

        if existing_user_email:
            flash("An account with this email already exists")
            return redirect(url_for("load_register_page"))

        new_user = UserAuth(
            username=username,
            password=generate_password_hash(password),
            email=email,
            active = True ,
            update_date=date.today()
        )

        db.session.add(new_user)
        db.session.commit()

        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")

        if not day or not month or not year :
                flash("Birthday date must be completed")
                return redirect( url_for("load_register_page") )

        StringBday = create_string_date( #birthday as a string
            day ,
            month ,
            year
        )

        if is_doctor == "on":
                new_doctor = DoctorInfo(
                      user_id = new_user.id,
                      first_name = request.form.get("first_name").lower(),
                      last_name = request.form.get("last_name").lower(),
                      birth_date = datetime.strptime(StringBday,"%d-%m-%Y").date() ,
                      gender = request.form.get("gender"),
                      contact_email = request.form.get("contact_email"), 
                      phone_number = request.form.get("phone_number"),
                      update_date = date.today()
               )
                db.session.add(new_doctor)

        else:
                new_patient = PatientInfo(
                      user_id = new_user.id,
                      first_name = request.form.get("first_name").lower(),
                      last_name = request.form.get("last_name").lower(),
                      birth_date = datetime.strptime(StringBday,"%d-%m-%Y").date() ,
                      gender = request.form.get("gender"),
                      contact_email = request.form.get("contact_email"),
                      phone_number = request.form.get("phone_number"),
                      update_date = date.today()
               )
                db.session.add(new_patient)

        db.session.commit()

        flash("Account created succesfully")
        return redirect(url_for("load_register_page"))


# =========================
# LOGIN
# =========================

@app.route('/submit_login' , methods=["POST"]) # checks login with database 
def submit_login_data():

        session.clear();

        username = request.form.get("username")
        input_password = request.form.get("password")

        if not username:
                flash("Must input username or email")
                return redirect(url_for("load_main_page"))
        
        if not input_password:
                flash("Must input password")
                return redirect(url_for("load_main_page"))
        
        found_user_by_username = UserAuth.query.filter_by(username=username , active = True).first()
        found_user_by_email = UserAuth.query.filter_by(email=username , active = True).first()

        if not found_user_by_username  and not found_user_by_email :
               flash("Wrong authentification data")
               return redirect(url_for("load_main_page"))

        if not found_user_by_username :
                found_user = found_user_by_email
        else:
                found_user = found_user_by_username

        
        
        if not check_password_hash(found_user.password, input_password):
                flash("Wrong authentification data")
                return redirect(url_for("load_main_page"))

        session["user_id"] = found_user.id

        if PatientInfo.query.filter_by(user_id=found_user.id).first():
                session["role"] = "patient"
                return redirect(url_for("load_patient_page"))
        else:
                session["role"] = "doctor"
                return redirect(url_for("load_doctor_page"))


# =========================
# PATIENT + DOCTOR FEATURES
# =========================

@app.route('/reg_consultation' , methods=["POST"])  # adds new consultation to database
def submit_consultation():

        if "user_id" not in session or session.get("role") != "doctor": # only doctor can access this
               return redirect(url_for("load_main_page"))
         
        doc = DoctorInfo.query.filter_by(user_id=session.get("user_id")).first()
        pat = PatientInfo.query.filter_by(id=session.get("patient_id")).first()

        if not pat :
                flash("No patient found")
                return redirect(url_for("load_patient_result_page"))

        first_name = pat.first_name.lower()
        last_name = pat.last_name.lower()

        file = request.files.get("file")
        file_path = None

        if file and file.filename:
                base = os.path.join( os.path.dirname( __file__ ) , "uploaded_consultation_files" )
                folder_path = os.path.join( base , f"{first_name}_{last_name}" )
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join( folder_path , file.filename )
                file.save(file_path)

        ConsultationDateString = create_string_date( #birthday as a string
            request.form.get("day"),
            request.form.get("month"),
            request.form.get("year")
        )

        new_consultation = ConsultationInfo(
                diagnostic=request.form.get("diagnostic"),
                weight=request.form.get("weight"),
                health_state=request.form.get("health_state"),
                heart_rate = request.form.get("heart_rate") ,
                blood_pressure_systolic = request.form.get("blood_pressure_systolic") ,
                blood_pressure_diastolic = request.form.get("blood_pressure_diastolic") ,
                blood_oxygen_saturation = request.form.get("blood_oxygen_saturation")  ,
                consultation_date=datetime.strptime(ConsultationDateString,"%d-%m-%Y").date() ,
                doctor_id=doc.id,
                patient_id=pat.id,
                upload_file_path=file_path,
        )

        if not new_consultation.diagnostic :
                flash("Must confirm a diagnostic")
                return redirect(url_for("load_patient_result_page"))
        
        if not new_consultation.consultation_date :
                flash("Must specify the date of the consultation")
                return redirect(url_for("load_patient_result_page"))
        
        db.session.add(new_consultation)
        db.session.commit()

        return redirect(url_for("load_patient_result_page"))


@app.route('/change_consultation/<consultation_id>' , methods=["POST"])
def apply_changes(consultation_id):

        if "user_id" not in session:
                return redirect(url_for("load_main_page"))
        
        consultation = ConsultationInfo.query.get_or_404(consultation_id)

        consultation.weight = request.form.get("weight")
        consultation.diagnostic = request.form.get("diagnostic")
        consultation.health_state = request.form.get("health_state")
        consultation.blood_pressure_systolic = request.form.get("blood_pressure_systolic") 
        consultation.blood_pressure_diastolic = request.form.get("blood_pressure_diastolic") 
        consultation.blood_oxygen_saturation = request.form.get("blood_oxygen_saturation")  
        consultation.heart_rate = request.form.get("heart_rate") 
        
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")

        if not day or not month or not year :
                flash("Consultation date must be completed")
                return redirect(url_for("load_edit_consultation_page", consultation_id=consultation_id))

        ConsultationDateString = create_string_date( #birthday as a string
            day ,
            month ,
            year
        )

        consultation.consultation_date = datetime.strptime(ConsultationDateString,"%d-%m-%Y").date() 

        if not consultation.diagnostic :
                flash("Diagnostic must be completed")
                return redirect(url_for("load_edit_consultation_page", consultation_id=consultation_id))

        db.session.commit()

        return redirect(url_for("load_doctor_page") )


@app.route('/download_attachment/<int:consultation_id>')  # downloads attachement to consultation
def download_attachment(consultation_id):

        if "user_id" not in session:
                return redirect(url_for("load_main_page"))
        
        consultation = ConsultationInfo.query.get_or_404(consultation_id)
        return send_file(consultation.upload_file_path, as_attachment=True)


# =========================
# EDIT ACCOUNT
# =========================

@app.route('/submit_changes_profile' , methods=["POST"]) # applies changes of profile data to database
def update_profile_data():

        if "user_id" not in session : 
               return redirect(url_for("load_main_page"))
        
        auth_entry = UserAuth.query.filter_by(id=session.get("user_id")).first()

        if session.get("role") == "doctor":
                user_entry = DoctorInfo.query.filter_by(user_id=session.get("user_id")).first()
                user_entry.specialisation = request.form.get("specialisation")
        else:
                user_entry = PatientInfo.query.filter_by(user_id=session.get("user_id")).first()
                

        StringBday = create_string_date( #birthday as a string
            request.form.get("day"),
            request.form.get("month"),
            request.form.get("year")
        )

        username = request.form.get("username")
        input_first_name = request.form.get("first_name")
        input_last_name = request.form.get("last_name")

        if not username:
                flash("must fill in username")
                return redirect(url_for("load_edit_account_page"))
        
        if not input_first_name:
                flash("must fill in first name")
                return redirect(url_for("load_edit_account_page"))
        
        if not input_last_name:
                flash("must fill in last name")
                return redirect(url_for("load_edit_account_page"))
        
        auth_entry.username = username
        user_entry.first_name = input_first_name.lower()
        user_entry.last_name = input_last_name.lower()
        user_entry.gender = request.form.get("gender")
        user_entry.phone_number = request.form.get("phone_number")
        user_entry.birth_date = datetime.strptime(StringBday,"%d-%m-%Y").date()
        user_entry.update_date = date.today()
        user_entry.adress = request.form.get("adress")

        db.session.commit()

        flash("Changes applied successfully")
        return redirect(url_for("load_edit_account_page"))


@app.route('/submit_changes_auth' , methods=["POST"]) # applies changes of authentification data to database
def update_authentification_data():

        if "user_id" not in session : 
               return redirect(url_for("load_main_page"))
        
        auth_entry = UserAuth.query.filter_by(id=session.get("user_id")).first()

        data = request.get_json()
        old_password_input = data.get("old_password")
        new_password = data.get("new_password")
        new_email = data.get("new_email")

        if not old_password_input:
                return jsonify({
                        "success" : False ,
                        "message" : "Must input password"
                })
        
        if not check_password_hash(auth_entry.password, old_password_input):
                return jsonify({
                        "success" : False ,
                        "message" : "Wrong password"
                })

        if not new_password:
                new_password = old_password_input

        if not new_email:
                return jsonify({
                        "success" : False ,
                        "message" : "Must input valid Email"
                })

        auth_entry.password = generate_password_hash(new_password)
        auth_entry.email = new_email
        auth_entry.update_date = date.today()

        db.session.commit()

        return jsonify({"success" : True })

@app.route('/deactivate_account' , methods = ["POST"])
def deactivate_account():

        if "user_id" not in session : 
               return redirect(url_for("load_main_page"))
        
        data = request.get_json()
        input_password = data.get("input_password")
        auth_entry = UserAuth.query.filter_by(id = session.get("user_id")).first()
        
        if not input_password:
                return jsonify({"success": False})
        
        if check_password_hash( auth_entry.password , input_password ):
                auth_entry.active = False
                db.session.commit()
                session.clear()
                return redirect(url_for("load_main_page"))
        
@app.route('/logout')
def logout():
        session.clear();
        return redirect(url_for("load_main_page"))
# =========================
# APP INIT
# =========================

with app.app_context():
        db.create_all()

if __name__ == "__main__":
        app.run()
