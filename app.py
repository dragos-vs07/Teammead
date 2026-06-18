from flask import Flask , render_template , request , flash , redirect , url_for , session , send_file , jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , date , time , timedelta
from dateutil.parser import parse
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

       appointments = db.relationship(
                "AppointmentInfo" ,
                back_populates = 'patient' ,
                order_by="AppointmentInfo.appointment_date.asc()" ,
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

        appointments = db.relationship(
                "AppointmentInfo" ,
                back_populates = 'doctor' ,
                order_by="AppointmentInfo.appointment_date.asc()" ,
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

class AppointmentInfo(db.Model):
        __tablename__ = "appointment_info"
        id = db.Column(db.Integer , primary_key = True)
        doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_info.id"))
        patient_id = db.Column(db.Integer, db.ForeignKey("patient_info.id"))
        appointment_date = db.Column(db.DateTime , nullable = False ) # stores date and time segment at which it starts ( time can only be xx:00 or xx:30 )
        confirmation = db.Column(db.Integer , nullable = False) # -1 rejected , 0 pending , 1 accepted ( doctor does this )
        status = db.Column(db.String(30) , nullable = False) # finished , cancelled , upcoming
        update_date = db.Column(db.Date)
        
        patient = db.relationship(
        "PatientInfo",
        back_populates="appointments" ,
        )

        doctor = db.relationship(
        "DoctorInfo",
        back_populates="appointments" ,
        )

class DoctorSchedule(db.Model): # stores the general schedule of each doctor 
        __tablename__ = "doctor_schedule"
        id = db.Column(db.Integer , primary_key = True)
        doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_info.id"))
        day = db.Column(db.Integer) # 1 2 3 4 5 6 7 for each day in order
        start_time = db.Column(db.Time) # starting hour of program
        end_time = db.Column(db.Time) # closing hour

# time slots are defined by their starting time , each consultation is assigned 30 mins
# doctors can block time ranges and then if a patient tries booking an appointment for a time slot
# that is contained by that blocked time range , he wont be allowed

class DoctorException(db.Model): # stores blocked time segments where patients cant book an appointment
        __tablename__ = "doctor_exception"
        id = db.Column(db.Integer , primary_key = True)
        doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_info.id"))
        start_date = db.Column(db.Date) # the starting date for the exception
        end_date = db.Column(db.Date) # the end date for the exception
        start_time = db.Column(db.Time) # starting time of the time range that is blocked
        end_time = db.Column(db.Time) # end time of the time range that is blocked
        source = db.Column(db.String(30)) # patient if it came from a patient ( an appointment ) , doctor if it was made by the doctor 

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

@app.route('/doctor_appointments_page')
def load_doctor_appointments_page():
         
        if "user_id" not in session or session.get("role") != "doctor": # can only be accessed from doctor account 
               return redirect(url_for("load_main_page"))
        
        user = UserAuth.query.filter_by(id = session["user_id"]).first()

        general_schedule = DoctorSchedule.query.filter_by(doctor_id = user.doctor.id).order_by(DoctorSchedule.day).all()

        return render_template(         "doctor_appointments_page.html" ,
                                        pending_appointments = AppointmentInfo.query.filter_by(
                                        doctor_id = user.doctor.id ,
                                        confirmation = 0 ).all() , # appointments not accepted / rejected yet
                                        
                                        upcoming_appointments = AppointmentInfo.query.filter_by(
                                        doctor_id = user.doctor.id ,
                                        confirmation = 1 ,
                                        status = "upcoming" ).all() , # appointments accepted and that are on the way

                                        submitted_exceptions = DoctorException.query.filter(
                                                DoctorException.doctor_id == user.doctor.id ,
                                                DoctorException.end_date >= datetime.today().date() ,
                                                DoctorException.source == "doctor"
                                        ).all() ,

                                        schedule = general_schedule
        )


@app.route('/patient_stats_page')
def load_patient_stats_page():

        if "user_id" not in session or session.get("role") != "patient":
               return redirect(url_for("load_main_page"))
        
        user = db.session.get(UserAuth, session.get("user_id"))

        weights = [float(c.weight) for c in user.patient.consultations if c.weight not in (None, '')]
        health_states = [float(c.health_state) for c in user.patient.consultations if c.health_state not in (None, '')]
        bps = [float(c.blood_pressure_systolic) for c in user.patient.consultations if c.blood_pressure_systolic not in (None, '')]
        bpd = [float(c.blood_pressure_diastolic) for c in user.patient.consultations if c.blood_pressure_diastolic not in (None, '')]
        spo2 = [float(c.blood_oxygen_saturation) for c in user.patient.consultations if c.blood_oxygen_saturation not in (None, '')]
        heart_rates = [float(c.heart_rate) for c in user.patient.consultations if c.heart_rate not in (None, '')]

        def s(lst):
                if not lst:
                        return {"max": "N/A", "min": "N/A", "mean": "N/A"}
                return {
                        "max": int(max(lst)),
                        "min": int(min(lst)),
                        "mean": round(sum(lst) / len(lst), 1)
                }

        return render_template("patient_stats_page.html",
                consultations=[{
                        "diagnostic": c.diagnostic,
                        "consultation_date": c.consultation_date.strftime("%Y-%m-%d"),
                        "weight": c.weight,
                        "health_state": c.health_state,
                        "blood_pressure_systolic": c.blood_pressure_systolic,
                        "blood_pressure_diastolic": c.blood_pressure_diastolic,
                        "blood_oxygen_saturation": c.blood_oxygen_saturation,
                        "heart_rate": c.heart_rate,
                } for c in user.patient.consultations],
                stats={
                        "weight": s(weights),
                        "health_state": s(health_states),
                        "blood_pressure_systolic": s(bps),
                        "blood_pressure_diastolic": s(bpd),
                        "blood_oxygen_saturation": s(spo2),
                        "heart_rate": s(heart_rates)
                }
        )
 
@app.route('/patient_consultations_page')
def load_patient_consultations_page():
         
        if "user_id" not in session or session.get("role") != "patient": # can only be accessed from patient account 
               return redirect(url_for("load_main_page"))
          
        user = db.session.get( UserAuth , session.get("user_id") )
        return render_template("patient_consultations_page.html" ,
                                user = user
                              )

@app.route('/patient_appointments_page')
def load_patient_appointments_page():

        if "user_id" not in session or session.get("role") != "patient": # can only be accessed from patient account 
               return redirect(url_for("load_main_page"))
        
        user = UserAuth.query.filter_by( id = session["user_id"] ).first()

        return render_template("patient_appointments_page.html" ,
                               doctor_list =  DoctorInfo.query.all() ,
                               appointments = AppointmentInfo.query.filter_by( patient_id = user.patient.id ,  ).all()
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
                } for c in user.consultations[-3:] ]
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
@app.route('/patient_make_appointment_page/<int:doctor_id>')
def load_patient_make_appointment_page(doctor_id):

        if "user_id" not in session or session.get("role") != "patient": # only doctor can access this
               return redirect(url_for("load_main_page"))
        
        # WE ONLY LOAD GENERAL SCHEDULE HERE , WE HANDLE EXCEPTIONS LATER BECAUSE THEY NEED TO BE TAKEN
        # DAY BY DAY

        segment_dict = {i: [] for i in range(0, 7)} # stores valid time segments for each day of the week

        schedule = DoctorSchedule.query.filter_by(doctor_id = doctor_id).all()

        for s in schedule: # for each of the 7 entries every doctor has that defines their schedule

                if s.start_time : # if the doctor input anything means he works today

                        current_date = datetime.combine( datetime.today() , s.start_time ) 
                        end_date = datetime.combine( datetime.today() , s.end_time )
                        # we combine to today date because timedelta cant be added to time element
                        # only to datetime

                        while current_date < end_date:
                                segment_dict[s.day].append(current_date.time())
                                current_date += timedelta( minutes = 30 )

        return render_template("patient_make_appointment_page.html" ,
                                doctor = DoctorInfo.query.filter_by(id = doctor_id).first() ,
                                time_segments = segment_dict ,
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

        if is_doctor == "on":

                for i in range(7):
                        new_schedule= DoctorSchedule(
                        doctor_id=new_doctor.id,
                        day=i,
                        start_time=None,
                        end_time=None
                        )
                        db.session.add(new_schedule)

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

@app.route('/submit_time_exception' , methods =["POST"])
def block_time_range():
        
        if "user_id" not in session or session.get("role") != "doctor": # only doctor can access this
               return redirect(url_for("load_main_page"))
        
        user = UserAuth.query.filter_by(id = session["user_id"]).first()

        day = request.form.get("start_day_exception")
        month = request.form.get("start_month_exception")
        year = request.form.get("start_year_exception")

        start_date = date(int(year), int(month), int(day))

        day = request.form.get("end_day_exception")
        month = request.form.get("end_month_exception")
        year = request.form.get("end_year_exception")

        end_date = date(int(year), int(month), int(day))


        hour = request.form.get("start_hour_exception")
        minute =  request.form.get("start_minute_exception")

        if not minute:
                minute = 0

        if not hour:
                hour = 0

        start_time = time( int(hour) , int(minute) )

        hour = request.form.get("end_hour_exception")
        minute =  request.form.get("end_minute_exception")

        if not minute:
                minute = 0

        if not hour:
                hour = 0

        end_time = time( int(hour) , int(minute) )

        new_time_range = DoctorException(
                doctor_id = user.doctor.id ,
                start_date = start_date ,
                end_date = end_date ,
                start_time = start_time ,
                end_time = end_time ,
                source = "doctor"
        )

        db.session.add(new_time_range)
        db.session.commit()

        return redirect(url_for("load_doctor_appointments_page"))

@app.route('/submit_general_schedule' , methods =["POST"])
def set_schedule():

        if "user_id" not in session or session.get("role") != "doctor": # only doctor can access this
               return redirect(url_for("load_main_page"))
        
        user = UserAuth.query.filter_by( id = session["user_id"] ).first()
        
        days_otw = [ "monday" , "tuesday" , "wednesday" , "thursday" , "friday" , "saturday" , "sunday" ]
        
        schedule_time_ranges = []

        for day in days_otw:

                start_hour = request.form.get(f"start_hour_{day}")
                start_minute = request.form.get(f"start_minute_{day}")

                end_hour = request.form.get(f"end_hour_{day}")
                end_minute = request.form.get(f"end_minute_{day}")

                if not start_hour:
                        start_hour = '0'

                if not start_minute:
                        start_minute = '0'

                if not end_hour:
                        end_hour = '0'

                if not end_minute:
                        end_minute = '0'
                
                schedule_time_ranges.append( 
                                ( 
                                        time( int(start_hour), int(start_minute) ) ,
                                        time( int(end_hour) , int(end_minute) ) 
                                )  
                        )

        schedule = DoctorSchedule.query.filter_by( doctor_id = user.doctor.id ).order_by(DoctorSchedule.day).all()
        # getting the schedule for each day of this doctor

        for i, s in enumerate(schedule):
                s.start_time = schedule_time_ranges[i][0]
                s.end_time = schedule_time_ranges[i][1]
        
        db.session.commit()

        return redirect(url_for('load_doctor_appointments_page'))

@app.route('/submit_appointments_response' , methods =["POST"])
def confirm_appointments():

        if "user_id" not in session or session.get("role") != "doctor": # only doctor can access this
               return redirect(url_for("load_main_page"))
        
        user = UserAuth.query.filter_by(id = session["user_id"]).first()

        pending_appointments = AppointmentInfo.query.filter_by(
        doctor_id = user.doctor.id ,
        confirmation = 0 ).all()  # appointments not accepted / rejected yet

        for ap in pending_appointments:
                appointment_response = request.form.get(f"confirmation_{ap.id}")

                if appointment_response : # if it isnt null then the user chose an option here and didnt ommit it
                        if appointment_response == '1':
                                ap.confirmation = 1
                                ap.status = "upcoming"
                                new_exception = DoctorException(
                                        doctor_id = user.doctor.id ,
                                        start_date = ap.appointment_date.date() ,
                                        start_time = ap.appointment_date.time() ,
                                        end_date = ap.appointment_date.date() ,
                                        end_time = ( ap.appointment_date + timedelta(minutes = 30) ).time() ,
                                        source = "patient"
                                        # start date and end date ar the same
                                        # lasts 30 minutes
                                        # this is how we distinguish it from an exception made by the doctor 
                                        # this blocks a time segmetn when an appointment is made
                                )
                                db.session.add(new_exception)
                        else:
                                ap.confirmation = -1
                                ap.status = "rejected"
        
        db.session.commit()
        return redirect(url_for('load_doctor_appointments_page'))

@app.route('/api/get_exceptions/<int:doctor_id>')
def get_exceptions(doctor_id):

        exceptions = DoctorException.query.filter_by(doctor_id = doctor_id).all()
        return jsonify([
        {
                "start_date": str(e.start_date),
                "start_time": str(e.start_time),
                "end_date":   str(e.end_date),
                "end_time":   str(e.end_time)
        } for e in exceptions
        ])


@app.route('/api/get_doctor_schedule/<int:doctor_id>/<start_view>/<end_view>')
def get_schedule( doctor_id , start_view , end_view ):

        if "user_id" not in session : 
               return jsonify({"status" : "failed"}) , 401
        
        schedule = DoctorSchedule.query.filter_by( doctor_id = doctor_id ).all()

        schedule_days = []

        for s in schedule:
                schedule_days.append( ( s.start_time , s.end_time ) )

        start_view_date = parse(start_view).date()
        end_view_date = parse(end_view).date()

        events = []

        current_day = start_view_date
        day_num = start_view_date.isoweekday()-1

        while current_day <= end_view_date:

                st = schedule_days[day_num][0]
                et = schedule_days[day_num][1]
                
                if st != time(0,0,0) and current_day >= date.today()  : # if the doctor input anything in start time means he has a program on this day
                        events.append({
                                "title" : f"{st}-{et}" ,
                                "start" : f"{current_day}" ,
                                "display" : "background" ,
                                "backgroundColor" : "rgba(43, 165, 217,0.75)"  ,
                                "extendedProps" : {
                                    "type" : 1
                                 }
                        })
                else :
                        events.append({
                                "title" : "Unavailable" ,
                                "start" : f"{current_day}" ,
                                "display" : "background" ,
                                "backgroundColor" : "rgba(245, 39, 39,0.75)" ,
                        })

                current_day += timedelta(days=1)
                day_num = ( day_num + 1 ) % 7


        return jsonify(events)


@app.route('/api/get_patient_appointments')
def get_appointments():

        if "user_id" not in session or session.get("role") != "patient": # only patient can access this
               return jsonify({"status" : "failed"}) , 401
        
        user = UserAuth.query.filter_by(id = session["user_id"]).first()
        valid_appointments = AppointmentInfo.query.filter_by( patient_id = user.patient.id , confirmation = 1)

        return jsonify([
                {
                        "title" : f"Dr. {ap.doctor.first_name.title()} {ap.doctor.last_name.title()}" ,
                        "start" : ap.appointment_date.isoformat() ,
                        "id" : ap.id
                }
                for ap in valid_appointments
        ])
        
@app.route( '/enquire_appointment' , methods = ["POST"] )
def register_appointment():

        if "user_id" not in session or session.get("role") != "patient": # only patient can access this
                return redirect(url_for('load_main_page'))
        
        data = request.get_json()
        
        PatientQuery = PatientInfo.query.filter_by( user_id = session["user_id"] ).first()

        print("HERE:" , data['date'])
        new_appointment = AppointmentInfo(
                doctor_id = data["doctor_id"] ,
                patient_id = PatientQuery.id ,
                appointment_date = datetime.strptime( f"{data['date']}" , "%Y-%m-%d %H:%M:%S") ,
                confirmation = 0 ,
                status = "upcoming" ,
                update_date = date.today()
        )

        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({
                "status" : "success"
        })
        

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

        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")

        new_consultation = ConsultationInfo(
                diagnostic=request.form.get("diagnostic"),
                weight=request.form.get("weight"),
                health_state=request.form.get("health_state"),
                heart_rate = request.form.get("heart_rate") ,
                blood_pressure_systolic = request.form.get("blood_pressure_systolic") ,
                blood_pressure_diastolic = request.form.get("blood_pressure_diastolic") ,
                blood_oxygen_saturation = request.form.get("blood_oxygen_saturation")  ,
                consultation_date=datetime( int(year) , int(month) , int(day) ) ,
                doctor_id=doc.id,
                patient_id=pat.id,
                upload_file_path=file_path,
                update_date = date.today()
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
        consultation.update_date = date.today()

        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")

        if not day or not month or not year :
                flash("Consultation date must be completed")
                return redirect(url_for("load_edit_consultation_page", consultation_id=consultation_id))

        consultation.consultation_date = datetime(day,month,year) 

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
                

        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")

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
        user_entry.birth_date = date(year,month,day)
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
