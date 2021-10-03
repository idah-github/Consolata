from main_app import db,login_manager,app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User (UserMixin,db.Model):
    __tablename__ ="employees"
    id = db.Column(db.Integer,primary_key = True)
    employee_id = db.Column(db.Integer)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)
    profile_picture = db.Column(db.String(40),default="default.png")
    first_name =db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    phone_number = db.Column(db.Integer)
    department = db.Column(db.String(20))
    role = db.Column(db.String(20))
    kra_pin = db.Column(db.Integer)
    id_no = db.Column(db.Integer)
    dob = db.Column(db.DateTime)

    def get_reset_token(self,expires_sec = 1800):
            s=  Serializer(app.config['SECRET_KEY'],expires_sec)
            return s.dumps({'user_id': self.id}).decode('utf-8')

    def check_password(self,password):
            return check_password_hash(self.password_hash,password )
   
    @staticmethod
    def verify_reset_token(token):
            s= Serializer(app.config['SECRET_KEY'])
            try:
                user_id = s.loads(token)['user_id']
            except:
                return None
            return User.query.get(user_id)
     ### REPRESENTATION METHOD CODE GOES HERE ###
     
    def __repr__(self):
            return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer,primary_key = True)
    posted_by = db.Column(db.String(64), nullable=False)
    post_title = db.Column(db.String(100))
    employee_id = db.Column(db.Integer)
    posted_on = db.Column(db.DateTime, default = datetime.utcnow())
    post_category = db.Column(db.String(40))
    post_description =db.Column(db.String(400))
    post_image_filename = db.Column(db.String(80))
    comments = db.Column(db.Integer, default = 0)
    sender_image = db.Column(db.String(30))


class LeaveApplication(db.Model):
    __tablename = "leave"
    id = db.Column(db.Integer, primary_key= True)
    employee_id = db.Column(db.Integer)
    employee_name = db.Column(db.String(30))
    employee_dep = db.Column( db.String(30))
    job_desc = db.Column(db.String(30))
    leave_category = db.Column(db.String(30))
    reason  = db.Column(db.String(200))
    days = db.Column(db.Integer)
    start_date  = db.Column( db.DateTime, default= datetime.utcnow())
    status = db.Column(db.Boolean, default = False)

class Comments(db.Model):
    __tablename = "Comments"
    id = db.Column(db.Integer, primary_key = True)
    posted_by = db.Column(db.Integer)
    comment = db.Column(db.String(300))
    posted_on  = db.Column(db.DateTime, default = datetime.utcnow())
    post_id = db.Column(db.Integer)
    sender_profile = db.Column(db.String)


class LoanApplication(db.Model):
    __tablename = "Loanapp"
    id =db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer)
    address = db.Column(db.String(60))
    email_address = db.Column(db.String(40))
    maritual_status = db.Column(db.String(20))
    application_reason = db.Column(db.String(200))
    monthly_income = db.Column(db.Integer)
    loan_amount = db.Column(db.Integer)
    guarantor_name = db.Column(db.String(20))
    g_address = db.Column(db.String(30))
    g_email = db.Column(db.String(30))

class Events(db.Model):
    __tablename= "Events"
    id = db.Column(db.Integer, primary_key = True)
    event_target = db.Column(db.String(40))
    event_type = db.Column(db.String(30))
    descript = db.Column(db.String(20))
    date = db.Column(db.DateTime, default = datetime.utcnow())






