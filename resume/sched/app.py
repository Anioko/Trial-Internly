"""The Flask app, with initialization and view functions."""

import logging

from flask import Flask
from flask import abort, jsonify, redirect, render_template, request, url_for, flash, session
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy


from sched import config, filters
from sched.forms import LoginForm, ResumeForm, SignupForm, PositionForm
from sched.models import Base, User, Resume, Position


from flask import send_from_directory
from werkzeug import secure_filename


from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView







app = Flask(__name__)
app.config.from_object(config)




# Use Flask-SQLAlchemy for its engine and session configuration. Load the
# extension, giving it the app object, and override its default Model class
# with the pure SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base

admin = Admin(app, name='Internly')
# Add administrative views here
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Resume, db.session))


# Use Flask-Login to track the current user in Flask's session.
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in .'


@login_manager.user_loader
def load_user(user_id):
    """Hook for Flask-Login to load a User instance from a user ID."""
    return db.session.query(User).get(user_id)


# Load custom Jinja filters from the `filters` module.
filters.init_app(app)


# Setup logging for production.
if not app.debug:
    app.logger.setHandler(logging.StreamHandler()) # Log to stderr.
    app.logger.setLevel(logging.INFO)


@app.errorhandler(404)
def error_not_found(error):
    """Render a custom template when responding with 404 Not Found."""
    return render_template('error/not_found.html'), 404






#########Views for Resume#######

@app.route('/find/')
@login_required
def all_resumes():
    """Provide HTML page listing all resumes in the database."""
    # Query: Get all Resume objects, sorted by the resume date.
    appts = db.session.query(Resume).all()
    return render_template('resume/all.html', appts=appts)

@app.route('/resume/<int:resume_id>/')
@login_required
def resume_details(resume_id):
    """Provide HTML page with all details on a given resume."""
    # Query: get Resume object by ID.
    appt = db.session.query(Resume).get(resume_id)
    return render_template('resume/details.html', appt=appt)


@app.route('/dashboard/')
@login_required
def resumes_list():
    """Provide HTML page listing all resumes in the database."""
    # Query: Get all Resume objects, sorted by the resume date.
    appts = (db.session.query(Resume)
             .filter_by(user_id=current_user.id)
             .order_by(Resume.start.asc()).all())

    return render_template('resume/test.html', appts=appts)


@app.route('/resumes/<int:resume_id>/')
@login_required
def resume_detail(resume_id):
    """Provide HTML page with all details on a given resume."""
    # Query: get Resume object by ID.
    appt = db.session.query(Resume).get(resume_id)
    if appt is None or appt.user_id != current_user.id:
        # Abort with Not Found.
        abort(404)
    return render_template('resume/detail.html', appt=appt)






@app.route('/resumes/create/', methods=['GET', 'POST'])
@login_required
def resume_create():
    """Provide HTML form to create a new resume record."""
    form = ResumeForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Resume(user_id=current_user.id)
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send the user back to the full resumes list.
        return redirect(url_for('resumes_list'))
    # Either first load or validation error at this point.
    return render_template('resume/edit.html', form=form)


@app.route('/resumes/<int:resume_id>/edit/', methods=['GET', 'POST'])
@login_required
def resume_edit(resume_id):
    """Provide HTML form to edit a given appointment."""
    appt = db.session.query(Resume).get(resume_id)
    if appt is None:
        abort(404)
    if appt.user_id != current_user.id:
        abort(403)
    form = ResumeForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view of that resume.
        return redirect(url_for('resume_detail', resume_id=appt.id))
    return render_template('resume/edit.html', form=form)


@app.route('/resumes/<int:resume_id>/delete/', methods=['DELETE'])
@login_required
def resume_delete(resume_id):
    """Delete a record using HTTP DELETE, respond with JSON for JavaScript."""
    appt = db.session.query(Resume).get(resume_id)
    if appt is None:
        # Abort with simple response indicating appointment not found.
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    if appt.user_id != current_user.id:
        # Abort with simple response indicating forbidden.
        response = jsonify({'status': 'Forbidden'})
        response.status_code = 403
        return response
    db.session.delete(appt)
    db.session.commit()
    return jsonify({'status': 'OK'})


#########Views for Positions#######

@app.route('/positions/')
@login_required
def all_positions():
    """Provide HTML page listing all positions in the database."""
    # Query: Get all Position objects.
    appts = db.session.query(Position).all()
    return render_template('position/all.html', appts=appts)

@app.route('/positions/<int:position_id>/')
@login_required
def position_details(position_id):
    """Provide HTML page with all details on a given position."""
    # Query: get Position object by ID.
    appt = db.session.query(Position).get(position_id)
    return render_template('position/details.html', appt=appt)


@app.route('/position/')
@login_required
def position_list():
    """Provide HTML page listing all rpositions in the database."""
    # Query: Get all Position objects, sorted by the position date.
    appts = (db.session.query(Position)
             .filter_by(user_id=current_user.id)
             .order_by(Position.pub_date.asc()).all())

    return render_template('position/index.html', appts=appts)


@app.route('/positions/<int:position_id>/')
@login_required
def position_detail(position_id):
    """Provide HTML page with all details on a given positions."""
    # Query: get Position object by ID.
    appt = db.session.query(Position).get(position_id)
    if appt is None or appt.user_id != current_user.id:
        # Abort with Not Found.
        abort(404)
    return render_template('position/detail.html', appt=appt)






@app.route('/positions/create/', methods=['GET', 'POST'])
@login_required
def position_create():
    """Provide HTML form to create a new positions record."""
    form = PositionForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Position(user_id=current_user.id)
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send the user back to the full resumes list.
        return redirect(url_for('position_list'))
    # Either first load or validation error at this point.
    return render_template('position/edit.html', form=form)


@app.route('/positions/<int:position_id>/edit/', methods=['GET', 'POST'])
@login_required
def position_edit(position_id):
    """Provide HTML form to edit a given position."""
    appt = db.session.query(Position).get(position_id)
    if appt is None:
        abort(404)
    if appt.user_id != current_user.id:
        abort(403)
    form = PositionForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view of that resume.
        return redirect(url_for('position_detail', position_id=appt.id))
    return render_template('position/edit.html', form=form)


@app.route('/positions/<int:position_id>/delete/', methods=['DELETE'])
@login_required
def position_delete(position_id):
    """Delete a record using HTTP DELETE, respond with JSON for JavaScript."""
    appt = db.session.query(Position).get(position_id)
    if appt is None:
        # Abort with simple response indicating position not found.
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    if appt.user_id != current_user.id:
        # Abort with simple response indicating forbidden.
        response = jsonify({'status': 'Forbidden'})
        response.status_code = 403
        return response
    db.session.delete(appt)
    db.session.commit()
    return jsonify({'status': 'OK'})


###Public Views

@app.route('/')
def landing_page():
	return render_template('layout.html')

@app.route('/premium')
def premium():
    return render_template('public/premium.html')


@app.route('/pro')
def pro():
    return render_template('public/pro.html')

@app.route('/about')
def about_us():
    return render_template('public/about.html')

@app.route('/policy')
def data_policy():
    return render_template('public/policy.html')




##
##@app.route('/signup/' , methods=['GET','POST'])
##def register():
##    if request.method == 'GET':
##        return render_template('public/register.html')
##    user = User(name=request.form['name'],
##                email=request.form['email'],
##                password=request.form['password'],
##                role=6)
##    db.session.add(user)
##    db.session.commit()
##    flash('User successfully registered')
##    return redirect(url_for('login'))
##





@app.route('/signup/' , methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('public/signup.html')
    user = User(name=request.form['name'],
                email=request.form['email'],
                password=request.form['password'],
                role=6)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered. Please Login with your details')
    return redirect(url_for('login'))


#Views for Login ###########

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('resumes_list'))
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        email = form.username.data.lower().strip()
        password = form.password.data.strip()
        role = 3
        user, authenticated = \
            User.authenticate(db.session.query, email, password)
        if authenticated:
            login_user(user)
            return redirect(url_for('resumes_list'))
        else:
            error = 'Incorrect username or password. Try again.'
    return render_template('public/login.html', form=form, error=error)





##
##@app.route("/login", methods=["GET", "POST"])
##def login():
##    form = LoginForm(request.form)
##    if request.method == 'POST' and form.validate():
##        if role = 3
##        
##        user = User.select.filter_by(username = user, role = 3).first()
##        # login and validate the user...
##        
##        login_user(user)
##        flash("Logged in successfully.")
##        return redirect(request.args.get("next") or url_for("index"))
##    return render_template("user/login.html", form=form)

##
##@app.route('/login/', methods=['GET', 'POST'])
##def login():
##    
##    if current_user.is_authenticated():
##        
##        return redirect(url_for('resumes_list'))
##    
##    form = LoginForm()
##    if form.validate_on_submit():
##        user = User.query.filter_by(username = user, role = 3).first()
##        login_user(user)
##        
##        return redirect(url_for('resumes_list')
            

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))
