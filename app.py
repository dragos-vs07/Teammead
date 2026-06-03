from flask import Flask , render_template , request , flash , redirect , url_for , session , send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , date
from werkzeug.security import generate_password_hash , check_password_hash
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

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
        update_date = db.Column(db.Date)


class PatientInfo(db.Model):
       __tablename__ = "patient_info"
       id = db.Column(db.Integer , primary_key = True)
       user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id"))
       first_name = db.Column(db.String(50) , nullable = False )
       last_name = db.Column(db.String(50) , nullable = False )
       birth_date = db.Column(db.Date , nullable = False)
       gender = db.Column(db.String(20), nullable = False)
       email = db.Column(db.String(100), nullable = False)
       phone_number = db.Column(db.String(20))
       home_adress = db.Column(db.String(100))
       update_date = db.Column(db.Date)


class DoctorInfo(db.Model):
        __tablename__ = "doctor_info"
        id = db.Column(db.Integer , primary_key = True)
        user_id = db.Column(db.Integer, db.ForeignKey("user_auth.id"))
        first_name = db.Column(db.String(50) , nullable = False )
        last_name = db.Column(db.String(50) , nullable = False )
        birth_date = db.Column(db.Date , nullable = False)
        gender = db.Column(db.String(20), nullable = False)
        email = db.Column(db.String(100), nullable = False)
        phone_number = db.Column(db.String(20))
        workplace_adress = db.Column(db.String(100))
        update_date = db.Column(db.Date)


class ConsultationInfo(db.Model):
        __tablename__ = "consult_info"
        id = db.Column(db.Integer , primary_key = True)
        doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_info.id"))
        patient_id = db.Column(db.Integer, db.ForeignKey("patient_info.id"))
        weight = db.Column(db.Integer)
        diagnostic = db.Column(db.String(50) , nullable = False )
        health_state = db.Column(db.Integer)
        consultation_date = db.Column(db.Date , nullable = False )
        upload_file_path = db.Column(db.String(200))
        update_date = db.Column(db.Date)


# =========================
# HELPERS
# =========================

def create_string_date( day , month , year):
        return f"{day}-{month}-{year}"


# =========================
# MAIN PAGES
# =========================

@app.route('/')
def load_main_page():
        return render_template("index.html")

@app.route('/load_edit_consultation_page/<consultation_id>')
def load_edit_consultation_page(consultation_id):
        return render_template("edit_consultation_page.html",
                               c = ConsultationInfo.query.filter_by(id = consultation_id).first()
                               )
@app.route('/patient_info') # loads page for a patient user
def load_patient_page():

        if "user_id" not in session:
               return redirect(url_for("load_main_page"))
        
        user = PatientInfo.query.filter_by(user_id = session["user_id"]).first()

        return render_template(
                "patient_page.html",
                first_name = user.first_name.title(),
                last_name = user.last_name.title(),
                consultations = ConsultationInfo.query.filter_by(patient_id = session["user_id"])
        )


@app.route('/doctor_page') # loads page for a doctor user
def load_doctor_page():

        if "user_id" not in session:
               return redirect(url_for("load_main_page"))
        
        session["patient_id"] = 0

        user = DoctorInfo.query.filter_by(user_id = session["user_id"]).first()

        return render_template(
            "doctor_page.html",
            first_name = user.first_name.title(),
            last_name = user.last_name.title()
        )


# =========================
# REGISTER
# =========================

@app.route('/register') # loads register menu
def load_register_page():
        return render_template("register.html")


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
            update_date=date.today()
        )

        db.session.add(new_user)
        db.session.commit()

        StringBday = create_string_date( #birthday as a string
            request.form.get("day"),
            request.form.get("month"),
            request.form.get("year")
        )

        if is_doctor == "on":
                new_doctor = DoctorInfo(
                      user_id = new_user.id,
                      first_name = request.form.get("first_name").lower(),
                      last_name = request.form.get("last_name").lower(),
                      birth_date = datetime.strptime(StringBday,"%d-%m-%Y").date() ,
                      gender = request.form.get("gender"),
                      email = new_user.email,
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
                      email = new_user.email,
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

        username = request.form.get("username")
        input_password = request.form.get("password")

        found_user_by_username = UserAuth.query.filter_by(username=username).first()
        found_user_by_email = UserAuth.query.filter_by(email=username).first()

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
        session["patient_id"] = 0

        if PatientInfo.query.filter_by(user_id=found_user.id).first():
                session["role"] = "patient"
                return redirect(url_for("load_patient_page"))
        else:
                session["role"] = "doctor"
                return redirect(url_for("load_doctor_page"))


# =========================
# PATIENT + DOCTOR FEATURES
# =========================

@app.route('/find_patient' , methods=["POST","GET"]) # displays results for a sought patient
def display_patient_info():

        if not session["patient_id"] :
                patient_first_name = request.form.get("first_name")
                patient_last_name = request.form.get("last_name")

                query_patient = PatientInfo.query.filter_by(
                    first_name=patient_first_name.lower(),
                    last_name=patient_last_name.lower()
                ).first()

                if not query_patient :
                        flash("Patient doesnt exist")
                        return redirect(url_for('load_doctor_page'))

                session["patient_id"] = query_patient.user_id

        else:
                query_patient = PatientInfo.query.filter_by(
                    user_id=session["patient_id"]
                ).first()

                patient_first_name = query_patient.first_name
                patient_last_name = query_patient.last_name

        if not query_patient :
                flash("Patient doesnt exist")
                return redirect(url_for('load_doctor_page'))

        consultations_data = ConsultationInfo.query.filter_by(
            patient_id=query_patient.user_id
        ).all()

        return render_template(
            "patient_result.html",
            first_name=patient_first_name.title(),
            last_name=patient_last_name.title(),
            birth_date=query_patient.birth_date,
            gender=query_patient.gender,
            email=query_patient.email,
            phone_number=query_patient.phone_number,
            consultations=[{ # making the consultations dictionaries so we can convert them to json for the javascript part
                "id": c.id ,
                "weight": c.weight,
                "diagnostic": c.diagnostic,
                "consultation_date": c.consultation_date,
                "health_state": c.health_state ,
                "upload_file_path" : c.upload_file_path
            }
            for c in consultations_data
            ] ,
            update_date=date.today() ,
        )

@app.route('/reg_consultation' , methods=["POST"])  # adds new consultation to database
def submit_consultation():

        doc = DoctorInfo.query.filter_by(user_id=session["user_id"]).first()
        pat = PatientInfo.query.filter_by(user_id=session["patient_id"]).first()

        if not pat :
                flash("No patient found")
                return redirect(url_for("display_patient_info"))

        first_name = pat.first_name.lower()
        last_name = pat.last_name.lower()

        file = request.files.get("file")
        file_path = None

        if file and file.filename:
                base = fr"C:\Users\Dragos\Desktop\Teammed\uploaded_consultation_files"
                folder_path = fr"{base}\{first_name}_{last_name}"
                os.makedirs(folder_path, exist_ok=True)
                file_path = fr"{folder_path}\{file.filename}"
                file.save(file_path)

        ConsultationDateString = create_string_date( #birthday as a string
            request.form.get("day"),
            request.form.get("month"),
            request.form.get("year")
        )

        new_consultation = ConsultationInfo(
                weight=request.form.get("weight"),
                diagnostic=request.form.get("diagnostic"),
                consultation_date=datetime.strptime(ConsultationDateString,"%d-%m-%Y").date() ,
                doctor_id=doc.user_id,
                patient_id=pat.user_id,
                health_state=request.form.get("health_state"),
                upload_file_path=file_path,
        )

        if not new_consultation.diagnostic :
                flash("Must confirm a diagnostic")
                return redirect(url_for("display_patient_info"))
        
        if not new_consultation.consultation_date :
                flash("Must specify the date of the consultation")
                return redirect(url_for("display_patient_info"))
        
        db.session.add(new_consultation)
        db.session.commit()

        return redirect(url_for("display_patient_info"))


@app.route('/change_consultation/<consultation_id>' , methods=["POST"])
def apply_changes(consultation_id):

        consultation = ConsultationInfo.query.get_or_404(consultation_id)

        consultation.weight = request.form.get("weight")
        consultation.diagnostic = request.form.get("diagnostic")
        consultation.health_state = request.form.get("health_state")

        ConsultationDateString = create_string_date( #birthday as a string
            request.form.get("day"),
            request.form.get("month"),
            request.form.get("year")
        )

        consultation.consultation_date = datetime.strptime(ConsultationDateString,"%d-%m-%Y").date() 

        if not consultation.consultation_date :
                flash("Consultation date must be completed")
                return redirect(url_for("load_edit_consultation_page", consultation_id=consultation_id))

        if not consultation.diagnostic :
                flash("Diagnostic must be completed")
                return redirect(url_for("load_edit_consultation_page", consultation_id=consultation_id))

        db.session.commit()

        return redirect(url_for("display_patient_info") )


@app.route('/download_attachment/<int:consultation_id>')  # downloads attachement to consultation
def download_attachment(consultation_id):

        consultation = ConsultationInfo.query.get_or_404(consultation_id)
        return send_file(consultation.upload_file_path, as_attachment=True)


# =========================
# EDIT ACCOUNT
# =========================

@app.route('/edit_account')
def load_edit_account_page(): # loads the edit account menu

        auth_entry = UserAuth.query.filter_by(id=session["user_id"]).first()

        if session['role'] == "doctor":
                user_entry = DoctorInfo.query.filter_by(user_id=session["user_id"]).first()
        else:
                user_entry = PatientInfo.query.filter_by(user_id=session["user_id"]).first()

        return render_template(
                 "account_edit_page.html",
                   old_email=auth_entry.email,
                   old_username=auth_entry.username,
                   old_first_name=user_entry.first_name.title(),
                   old_last_name=user_entry.last_name.title(),
                   old_phone_number=user_entry.phone_number,
                   old_day=user_entry.birth_date.day ,
                   old_month=user_entry.birth_date.month ,
                   old_year=user_entry.birth_date.year ,
                   gender=user_entry.gender
        )


@app.route('/submit_changes_profile' , methods=["POST"]) # applies changes of profile data to database
def update_profile_data():

        auth_entry = UserAuth.query.filter_by(id=session["user_id"]).first()

        if session['role'] == "doctor":
                user_entry = DoctorInfo.query.filter_by(user_id=session["user_id"]).first()
        else:
                user_entry = PatientInfo.query.filter_by(user_id=session["user_id"]).first()

        StringBday = create_string_date( #birthday as a string
            request.form.get("day"),
            request.form.get("month"),
            request.form.get("year")
        )

        auth_entry.username = request.form.get("username")
        user_entry.first_name = request.form.get("first_name").lower()
        user_entry.last_name = request.form.get("last_name").lower()
        user_entry.gender = request.form.get("gender")
        user_entry.phone_number = request.form.get("phone_number")
        user_entry.birth_date = datetime.strptime(StringBday,"%d-%m-%Y").date()
        user_entry.update_date = date.today()

        db.session.commit()

        flash("Changes applied successfully")
        return redirect(url_for("load_edit_account_page"))


@app.route('/submit_changes_auth' , methods=["POST"]) # applies changes of authentification data to database
def update_authentification_data():

        auth_entry = UserAuth.query.filter_by(id=session["user_id"]).first()

        old_password_input = request.form.get("old_password")
        new_password = request.form.get("new_password")
        new_email = request.form.get("new_email")

        if not check_password_hash(auth_entry.password, old_password_input):
                flash("Old password is wrong")
                return redirect(url_for("load_edit_account_page"))

        if not new_password:
                new_password = old_password_input

        if not new_email:
                flash("Must input a valid email")
                return redirect(url_for("load_edit_account_page"))

        auth_entry.password = generate_password_hash(new_password)
        auth_entry.email = new_email
        auth_entry.update_date = date.today()

        db.session.commit()

        flash("Authentification data updated successfully")
        return redirect(url_for("load_edit_account_page"))


# =========================
# APP INIT
# =========================

with app.app_context():
        db.create_all()

if __name__ == "__main__":
        app.run()