  
from main_app import app,db
from main_app.forms import RegistrationForm,LoginForm,PostForm,ImageUpload,ChangePassword
from flask import render_template,request, redirect, url_for,flash
# from app import RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import login_user,logout_user,login_required,UserMixin,current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from main_app.models import User,Post,LeaveApplication, Comments, LoanApplication, Events


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    posts = Post.query.order_by(Post.posted_on.desc()).all()
        

    return render_template("index.html", title='Homepage', posts= posts)


@app.route('/add_comment/<int:post_id>',methods =['GET','POST'])
def add_comment(post_id):
    if request.method == "POST":
        comment = Comments()
        comment.posted_by = current_user.first_name + " " + current_user.last_name
        comment.comment = request.form.get("comment")
        comment.posted_on = datetime.now()
        comment.post_id = post_id
        comment.sender_profile = current_user.profile_picture
        db.session.add(comment)
        db.session.commit()
        flash("Your comment was sent successfully", "success")
        post = Post.query.filter_by(post_id = comment.post_id).first()

        post.comments = post.comments +1 
        db.session.commit()

        return redirect( url_for('singlepost', post_id = post_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form= RegistrationForm()
    if  request.method == "POST":
        password = generate_password_hash(form.password.data)

        user = User(first_name=form.first_name.data,
                    last_name = form.last_name.data,
                    employee_id = form.employee_id.data,
                    phone_number = form.phone_number.data,
                    email=form.email.data,
                    password_hash=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration was successfully completed','success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form = form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(employee_id=form.employee_id.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Employee id or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
        next = request.args.get('next')

        if next == None or not next[0]== '/':
            next = url_for('index')
    return render_template('login.html', form=form, title="login")

@app.route('/account', methods=['GET', 'POST'])
@login_required 
def account():

    form = ImageUpload()
    event = Events()
    updatepassword  = ChangePassword()
    if request.method == "POST":
        if request.form['submit'] == "updateinfo":
            user = User.query.filter_by(employee_id = current_user.employee_id).first()
            user.first_name = request.form.get('first_name')
            user.last_name=request.form.get('last_name')
            user.department = request.form.get('department')
            user.role = request.form.get('role')
            dob= request.form.get('dob')
            y, m, d = dob.split('-')
            actual_date = datetime(int(y), int(m), int(d))
            user.dob = actual_date
            user.kra_pin = request.form.get('kra_pin')
            user.id_no = request.form.get('id_no')
            user.phone_number = request.form.get('phone_number')
            db.session.add(user)
            db.session.commit()
            flash("Your personal data has been updated successfully","success")
            return redirect(url_for('account'))

        if form.validate_on_submit() and request.files:
            user = User.query.filter_by(employee_id = current_user.employee_id).first()
            file = request.files['profile_upload']
            filename =secure_filename(file.filename)
            user.profile_picture = filename
            db.session.add(user)
            db.session.commit()
            file.save(os.path.join(app.config['IMAGE_UPLOAD_FOLDER'],filename))

            flash("Your profile picture has been updated successfully","success")
        if updatepassword.validate_on_submit():
            user = User.query.filter_by(employee_id=current_user.employee_id).first()
            password = updatepassword.old_password.data
            if user.check_password(password) :
                password = generate_password_hash(updatepassword.new_password.data)
                user.password_hash = password
                db.session.add(user)
                db.session.commit()
                flash("Your password has been updated successfully", "success")
            else:
                flash("Invalid current Password", "danger")
        if  request.form['submit'] == 'leave':
            leave_data = LeaveApplication()

            leave_data.employee_id = current_user.employee_id
            leave_data.employee_name = request.form.get('employee_name')
            leave_data.employee_dep = request.form.get('department')
            leave_data.job_desc = request.form.get('role')
            leave_data.leave_category = request.form.get('leave_type')
            leave_data.reason = request.form.get('reason')
            leave_data.days = request.form.get('days')
            start_date= request.form.get('start_date')
            y, m, d = start_date.split('-')
            actual_date = datetime(int(y), int(m), int(d))
            leave_data.start_date = actual_date
            db.session.add(leave_data)
            db.session.commit()
            flash("Your application was sent to the admin", "success")

            event.event_type = "Leave application Pending Approval"
            event.event_target = current_user.employee_id
            event.descript = " You just uploaded a post "
            event.date = datetime.utcnow()
            db.session.add(event)
            db.session.commit()
               
        flash("something went wrong try again", "warning")
        return redirect(url_for('activity'))
   
    return render_template('account.html', title="account/page" ,form=form , updatepassword=updatepassword)

@app.route('/activity', methods=['GET','POST'])
@login_required
def activity():
    form = PostForm()
    post = Post()
    event = Events()
    posts = Post.query.filter_by(employee_id = current_user.employee_id).all()
    loan = LoanApplication()
    if request.method =="POST" and request.files:
            post.post_title = request.form.get("title")
            post.posted_by = current_user.first_name + current_user.last_name
            post.employee_id = current_user.employee_id
            post.post_category = request.form.get('category')
            post.post_description = request.form.get('description')
            post.posted_on = datetime.now()
            post.comments = 0
            post.sender_image = current_user.profile_picture
            file = request.files['avatar']   
            filename =secure_filename(file.filename)
            post.post_image_filename = filename
            file.save(os.path.join(app.config['POST_UPLOAD_FOLDER'],filename))

            db.session.add(post)
            db.session.commit()

            event.event_type = "Post uploaded"
            event.event_target = current_user.employee_id
            event.descript = " You just uploaded a post "
            event.date = datetime.utcnow()
            db.session.add(event)
            db.session.commit()

            flash("Your post was uploaded successfully", "success")
            return redirect(url_for('index'))

    if request.method == "POST" and  request.form['submit']=="noimage":
        post.post_title = request.form.get("title")
        post.posted_by = current_user.first_name + " " + current_user.last_name
        post.post_category = request.form.get('category')
        post.post_description = request.form.get('description')
        post.sender_image = current_user.profile_picture
        post.employee_id = current_user.employee_id


        post.posted_on = datetime.now()
        post.comments = 0
        db.session.add(post)
        db.session.commit()
        event.event_type = "Post uploaded"
        event.event_target = current_user.employee_id
        event.descript = " You just uploaded a post "
        event.date = datetime.utcnow()
        db.session.add(event)
        db.session.commit()

        flash("Your post was uploaded successfully","success")
        return redirect(url_for('index'))

    if request.method == "POST" and request.form['submit'] == "loanform":
        loan.applicant_id = current_user.employee_id
        loan.address = request.form.get('address')
        loan.email_address = request.form.get('email')
        loan.maritual_status = request.form.get('maritual_status')
        loan.application_reason = request.form.get('reason')
        loan.monthly_income = request.form.get('monthly_income')
        loan.loan_amount = request.form.get('loan_amount')
        loan.guarantor_name = request.form.get('guarantor_name')
        loan.g_address = request.form.get('g_address')
        loan.g_email = request.form.get('g_email')
        db.session.add(loan)
        db.session.commit()
        event.event_type = "Pending loan application"
        event.event_target = current_user.employee_id
        event.descript = " Sumittion of loan application form waiting for approval"
        event.date = datetime.utcnow()
        db.session.add(event)
        db.session.commit()
        flash("You application has been sent ", "success")
        return redirect(url_for('activity'))

    return render_template('activity.html' , title="activity_page", form=form, posts=posts)

@app.template_test("none")
def is_none(obj):
    return obj is None

@app.route("/singlepost/<int:post_id>", methods=['GET','POST'])
def singlepost(post_id):
    post= Post.query.filter_by(post_id = post_id).first()
    comments = Comments.query.filter_by(post_id = post_id)

    return render_template("single_post.html",post=post, comments=comments)
    

    
@app.route('/delete_post/<int:post_id>', methods=['GET','POST'])
def delete_post(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
 
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('activity'))


@app.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("You are logged out successfully","Success")
    return redirect(url_for('login'))


    










