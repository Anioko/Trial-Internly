
# -*- coding: utf-8 -*
import os
import logging


from flask import Flask
from flask import abort, jsonify, redirect, render_template, request, url_for , flash, session
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy


from flask.ext.admin import Admin, BaseView, expose


import os.path as op


from Intern_reg import config, filters
from Intern_reg.forms import LoginForm, EventForm, BlogForm, UnpaidForm, PaidForm, ThesisForm, CompanyForm, InterestForm
from Intern_reg.models import Base, User, Event, Blog, Unpaid, Paid, Thesis, Company, Interest

#from functools import wraps



app = Flask(__name__)
app.config.from_object(config)

admin = Admin(app, name='Internly')
# Add administrative views here



# Use Flask-SQLAlchemy for its engine and session configuration. Load the
# extension, giving it the app object, and override its default Model class
# with the pure SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base



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



#############Any admin panel here########
#@app.route('/admin/')
# @login_required
#def admin():
    #return render_template('admin/index.html')
	



######Test template designs###delete after

@app.route('/land')
@login_required
def land():
	return render_template('company/land.html')
    
@app.route('/base')
@login_required
def base():
	return render_template('company/base.html')

@app.route('/premium')
def test():
    return render_template('company/premium.html')


@app.route('/pro')
def pro():
    return render_template('company/pro.html')


@app.route('/public')
def public():
    return render_template('public/base.html')

@app.route('/intern/cv')
def cv():
    return render_template('intern/cv.html')

@app.route('/intern/sample')
def cv_sample():
    return render_template('intern/cv_sample.html')

@app.route('/intern/sample/cv')
def sample():
    return render_template('intern/sample.html')

@app.route('/company/interest')
def interest_added():
    return render_template('interest/interest.html')

####### Public Views  start  #################


@app.route('/home')
@login_required
def home():
	return render_template('home/base.html')

@app.route('/')
def landing_page():
	return render_template('layout.html')
    

@app.route('/company/')
@app.route('/company')
def company_land():
    return render_template('company/land.html')

@app.route('/intern')
def intern_land():
    return render_template('intern/land.html')



############ Event Views  Start  #################

@app.route('/events/')
@login_required
def event_list():
    """Provide HTML page listing all appointments in the database."""
    # Query: Get all Appointment objects, sorted by the appointment date.
    appts = (db.session.query(Event)
             .filter_by(user_id=current_user.id)
             .order_by(Event.start.asc()).all())
    return render_template('event/index.html', appts=appts)


@app.route('/events/<int:event_id>/')
@login_required
def event_detail(event_id):
    """Provide HTML page with all details on a given appointment."""
    # Query: get Appointment object by ID.
    appt = db.session.query(Event).get(event_id)
    if appt is None or appt.user_id != current_user.id:
        # Abort with Not Found.
        abort(404)
    return render_template('event/detail.html', appt=appt)


@app.route('/events/create/', methods=['GET', 'POST'])
@login_required
def event_create():
    """Provide HTML form to create a new appointment record."""
    form = EventForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Event(user_id=current_user.id)
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send the user back to the full appointment list.
        return redirect(url_for('event_list'))
    # Either first load or validation error at this point.
    return render_template('event/edit.html', form=form)


@app.route('/events/<int:event_id>/edit/', methods=['GET', 'POST'])
@login_required
def event_edit(event_id):
    """Provide HTML form to edit a given appointment."""
    appt = db.session.query(Event).get(event_id)
    if appt is None:
        abort(404)
    if appt.user_id != current_user.id:
        abort(403)
    form = EventForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view of that appointment.
        return redirect(url_for('event_detail', event_id=appt.id))
    return render_template('event/edit.html', form=form)


@app.route('/events/<int:event_id>/delete/', methods=['DELETE'])
@login_required
def event_delete(event_id):
    """Delete a record using HTTP DELETE, respond with JSON for JavaScript."""
    appt = db.session.query(Event).get(event_id)
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
	
	
############ Blog Views  Start  #################
	
@app.route('/blog/')
#@login_required
def blog_list():
    """Provide HTML page listing all appointments in the database."""
    # Query: Get all Appointment objects, sorted by the appointment date.
    blogs = (db.session.query(Blog)
             .filter_by(user_id=current_user.id)
             .order_by(Blog.pub_date.asc()).all())
    return render_template('blog/index.html', blogs=blogs)



@app.route('/blog/<int:blog_id>/')
@login_required
def blog_detail(blog_id): 
    """Provide HTML page with all details on a given appointment."""
    # Query: get Appointment object by ID.
    blog = db.session.query(Blog).get(blog_id)
    if blog is None or blog.user_id != current_user.id:
        # Abort with Not Found.
        abort(404)
    return render_template('blog/detail.html', blog=blog)


@app.route('/blog/create/', methods=['GET', 'POST'])
@login_required
def blog_create():
    """Provide HTML form to create a new appointment record."""
    form = BlogForm(request.form)
    if request.method == 'POST' and form.validate():
        blog = Blog(user_id=current_user.id)
        form.populate_obj(blog)
        db.session.add(blog)
        db.session.commit()
        # Success. Send the user back to the full appointment list.
        return redirect(url_for('blog_list'))
    # Either first load or validation error at this point.
    return render_template('blog/edit.html', form=form)


@app.route('/blog/<int:blog_id>/edit/', methods=['GET', 'POST'])
@login_required
def blog_edit(blog_id):
    """Provide HTML form to edit a given appointment."""
    blog = db.session.query(Blog).get(blog_id)
    if blog is None:
        abort(404)
    if blog.user_id != current_user.id:
        abort(403)
    form = BlogForm(request.form, blog)
    if request.method == 'POST' and form.validate():
        form.populate_obj(blog)
        db.session.commit()
        # Success. Send the user back to the detail view of that appointment.
        return redirect(url_for('blog_detail', blog_id=blog.id))
    return render_template('blog/edit.html', form=form)


@app.route('/blog/<int:blog_id>/delete/', methods=['DELETE'])
@login_required
def blog_delete(blog_id):
    """Delete a record using HTTP DELETE, respond with JSON for JavaScript."""
    blog = db.session.query(Blog).get(blog_id)
    if blog is None:
        # Abort with simple response indicating appointment not found.
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    if blog.user_id != current_user.id:
        # Abort with simple response indicating forbidden.
        response = jsonify({'status': 'Forbidden'})
        response.status_code = 403
        return response
    db.session.delete(blog)
    db.session.commit()
    return jsonify({'status': 'OK'})
	
	






############ Paid Views  Start  #################

@app.route('/paid/')
#@login_required
def paid_list():
    """Provide HTML page listing all appointments in the database."""
    # Query: Get all Appointment objects, sorted by the appointment date.
    appts = (db.session.query(Paid)
             .filter_by(user_id=current_user.id)
             .order_by(Paid.pub_date.asc()).all())
    return render_template('paid/index.html', appts=appts)


@app.route('/paid/<int:paid_id>/')
@login_required
def paid_detail(paid_id):
    """Provide HTML page with all details."""
    # Query: get object by ID.
    appt = db.session.query(Paid).get(paid_id)
    if appt is None or appt.user_id != current_user.id:
        # Abort with Not Found.
        abort(404)
    return render_template('paid/detail.html', appt=appt)


@app.route('/paids/')
#@login_required
def paid_details():
    """Provide HTML page with all details."""
    # Query: get object by ID.
    appt = Paid.query.all()
    #appt = Paid.query.order_by(Paid.id)
    return render_template('paid/detail.html', appt=appt)

@app.route('/paid/create/', methods=['GET', 'POST'])
@login_required
def paid_create():
    """Provide HTML form to create a new record."""
    form = PaidForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Paid(user_id=current_user.id)
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send the user back to the full appointment list.
        return redirect(url_for('paid_list'))
    # Either first load or validation error at this point.
    return render_template('paid/edit.html', form=form)


@app.route('/paid/<int:paid_id>/edit/', methods=['GET', 'POST'])
@login_required
def paid_edit(paid_id):
    """Provide HTML form to edit a given appointment."""
    appt = db.session.query(Paid).get(paid_id)
    if appt is None:
        abort(404)
    if appt.user_id != current_user.id:
        abort(403)
    form = PaidForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view of that appointment.
        return redirect(url_for('paid_detail', paid_id=appt.id))
    return render_template('paid/edit.html', form=form)


@app.route('/paid/<int:paid_id>/delete/', methods=['DELETE'])
@login_required
def paid_delete(paid_id):
    """Delete a record using HTTP DELETE, respond with JSON for JavaScript."""
    appt = db.session.query(Paid).get(paid_id)
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



############ thesis Views  Start  #################

@app.route('/thesis/')
#@login_required
def thesis_list():
    """Provide HTML page listing all appointments in the database."""
    # Query: Get all Appointment objects, sorted by the appointment date.
    appts = (db.session.query(Thesis)
             .filter_by(user_id=current_user.id)
             .order_by(Thesis.pub_date.asc()).all())
    return render_template('thesis/index.html', appts=appts)


@app.route('/thesis/<int:thesis_id>/')
@login_required
def thesis_detail(thesis_id):
    """Provide HTML page with all details."""
    # Query: get object by ID.
    appt = db.session.query(Thesis).get(thesis_id)
    if appt is None or appt.user_id != current_user.id:
        # Abort with Not Found.
        abort(404)
    return render_template('thesis/detail.html', appt=appt)


@app.route('/thesis/')
#@login_required
def thesis_details():
    """Provide HTML page with all details."""
    # Query: get object by ID.
    appt = Thesis.select()
    return render_template('thesis/detail.html', appt=appt)

@app.route('/thesis/create/', methods=['GET', 'POST'])
@login_required
def thesis_create():
    """Provide HTML form to create a new record."""
    form = ThesisForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Thesis(user_id=current_user.id)
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send the user back to the full appointment list.
        return redirect(url_for('thesis_list'))
    # Either first load or validation error at this point.
    return render_template('thesis/edit.html', form=form)


@app.route('/thesis/<int:thesis_id>/edit/', methods=['GET', 'POST'])
@login_required
def thesis_edit(thesis_id):
    """Provide HTML form to edit a given appointment."""
    appt = db.session.query(Thesis).get(thesis_id)
    if appt is None:
        abort(404)
    if appt.user_id != current_user.id:
        abort(403)
    form = ThesisForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view of that appointment.
        return redirect(url_for('thesis_detail', thesis_id=appt.id))
    return render_template('thesis/edit.html', form=form)


@app.route('/thesis/<int:thesis_id>/delete/', methods=['DELETE'])
@login_required
def thesis_delete(thesis_id):
    """Delete a record using HTTP DELETE, respond with JSON for JavaScript."""
    appt = db.session.query(Thesis).get(thesis_id)
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




############ unpaid Views  Start  #################

@app.route('/unpaid/')
#@login_required
def unpaid_list():
    appts = (db.session.query(Unpaid)
             .filter_by(user_id=current_user.id)
             .order_by(Unpaid.pub_date.asc()).all())
    return render_template('unpaid/index.html', appts=appts)


@app.route('/unpaid/<int:unpaid_id>/')
@login_required
def unpaid_detail(unpaid_id):
    """Provide HTML page with all details."""
    # Query: get object by ID.
    appt = db.session.query(Unpaid).get(unpaid_id)
    if appt is None or appt.user_id != current_user.id:
        # Abort with Not Found.
        abort(404)
    return render_template('unpaid/detail.html', appt=appt)


@app.route('/unpaid/')
#@login_required
def unpaid_details():
    """Provide HTML page with all details."""
    # Query: get object by ID.
    appt = Unpaid.select()
    return render_template('unpaid/detail.html', appt=appt)

@app.route('/unpaid/create/', methods=['GET', 'POST'])
@login_required
def unpaid_create():
    """Provide HTML form to create a new record."""
    form = UnpaidForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Unpaid(user_id=current_user.id)
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send the user back to the full appointment list.
        return redirect(url_for('unpaid_list'))
    # Either first load or validation error at this point.
    return render_template('unpaid/edit.html', form=form)


@app.route('/unpaid/<int:unpaid_id>/edit/', methods=['GET', 'POST'])
@login_required
def unpaid_edit(unpaid_id):
    """Provide HTML form to edit a given appointment."""
    appt = db.session.query(Unpaid).get(unpaid_id)
    if appt is None:
        abort(404)
    if appt.user_id != current_user.id:
        abort(403)
    form = UnpaidForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view of that appointment.
        return redirect(url_for('unpaid_detail', unpaid_id=appt.id))
    return render_template('unpaid/edit.html', form=form)


@app.route('/unpaid/<int:unpaid_id>/delete/', methods=['DELETE'])
@login_required
def unpaid_delete(unpaid_id):
    """Delete a record using HTTP DELETE, respond with JSON for JavaScript."""
    appt = db.session.query(Unpaid).get(unpaid_id)
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



############ Company Views  Start  #################





@app.route('/company/login/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def company_login():
    if current_user.is_authenticated():
        return redirect(url_for('company_dashboard'))
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        email = form.username.data.lower().strip()
        password = form.password.data.lower().strip()
        user, authenticated = \
            User.authenticate(db.session.query, email, password)
        login_user(user)
        flash("Logged in successfully.")
        return redirect(url_for('company_dashboard'))
    else:
        error = 'Incorrect username or password. Try again.'
        
    return render_template('company/login.html', form=form, error=error)





@app.route('/signup' , methods=['GET','POST'])
@app.route('/company/signup' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    user = User(name=request.form['name'],
                email=request.form['email'],
                password=request.form['password'],
                role=2)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('company_login'))

##
##@app.route('/index')
##def index():
##    blogs = (db.session.query(Blog)
##
##             .order_by(Blog.pub_date.asc()).all())
##    
##    return render_template('blog/index.html', blogs=blogs)
##




@app.route('/company/dashboard/')
def company_dashboard():
    appt = Interest.select()
    appta = Unpaid.select()
    apptb = Paid.select()
    apptc = Thesis.select()
    return render_template('company/dashboard.html', appt=appt,appta=appta, apptb=apptb, apptc=apptc)

@app.route('/login/')
def login():
    return redirect(url_for('company_login'))


@app.route('/logout/')
@app.route('/company/logout/')
def company_logout():
    logout_user()
    return redirect(url_for('company_login'))

@app.route('/companies/')
#@login_required
def company_list():
    """Provide HTML page listing all appointments in the database."""
    # Query: Get all Appointment objects, sorted by the appointment date.
    appts = (db.session.query(Company)
             .filter_by(user_id=current_user.id)
             .order_by(Company.created.asc()).all())
    return render_template('company/index.html', appts=appts)


@app.route('/companies/<int:company_id>/')
@login_required
def company_detail(company_id):
    """Provide HTML page with all details."""
    # Query: get object by ID.
    appt = db.session.query(Company).get(company_id)
    if appt is None or appt.user_id != current_user.id:
        # Abort with Not Found.
        abort(404)
    return render_template('company/detail.html', appt=appt)


@app.route('/companies/')
#@login_required
def company_details():
    """Provide HTML page with all details."""
    # Query: get object by ID.
    appt = Company.select()
    return render_template('company/detail.html', appt=appt)

@app.route('/company/create/', methods=['GET', 'POST'])
@app.route('/companies/create/', methods=['GET', 'POST'])
@login_required
def company_create():
    """Provide HTML form to create a new record."""
    form = CompanyForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Company(user_id=current_user.id)
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send the user back to the full appointment list.
        return redirect(url_for('company_list'))
    # Either first load or validation error at this point.
    return render_template('company/edit.html', form=form)


@app.route('/companies/<int:company_id>/edit/', methods=['GET', 'POST'])
@login_required
def company_edit(company_id):
    """Provide HTML form to edit a given appointment."""
    appt = db.session.query(Company).get(company_id)
    if appt is None:
        abort(404)
    if appt.user_id != current_user.id:
        abort(403)
    form = CompanyForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view of that appointment.
        return redirect(url_for('company_detail', company_id=appt.id))
    return render_template('company/edit.html', form=form)


@app.route('/companies/<int:company_id>/delete/', methods=['DELETE'])
@login_required
def company_delete(company_id):
    """Delete a record using HTTP DELETE, respond with JSON for JavaScript."""
    appt = db.session.query(Company).get(company_id)
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

@app.route('/company/index')
def company_index():
    appt = Company.select()
    return render_template('company/index.html', appt=appt)



############ Intern Views  Start  #################



##
##
##@app.route('/intern/login/', methods=['GET', 'POST'])
##def intern_login():
##    if current_user.is_authenticated():
##        return redirect(url_for('company_results'))
##    form = LoginForm(request.form)
##    error = None
##    if request.method == 'POST' and form.validate():
##        email = form.username.data.lower().strip()
##        password = form.password.data.lower().strip()
##        user, authenticated = \
##            User.authenticate(db.session.query, email, password)
##        login_user(user)
##        flash("Logged in successfully.")
##        return redirect(url_for('intern_index'))
##    else:
##        error = 'Incorrect username or password. Try again.'
##        
##    return render_template('intern/login.html', form=form, error=error)

#@app.route('/intern/')
#@app.route('/intern/index')
def intern_index():
    appt = Interest.select()
    return render_template('intern/index.html', appt=appt)

@app.route('/intern/')
@app.route('/intern/index')
def company_results():
    appt = Interest.select()
    return render_template('intern/index.html', appt=appt)


##@app.route('/intern/logout/')
##def intern_logout():
##    logout_user()
##    return redirect(url_for('intern_login'))


@app.route('/interest/')
#@login_required
def interest_list():
    """Provide HTML page listing all appointments in the database."""
    # Query: Get all Appointment objects, sorted by the appointment date.
    appts = (db.session.query(Interest)
             .filter_by(user_id=current_user.id)
             .order_by(Interest.created.asc()).all())
    return render_template('interest/index.html', appts=appts)


@app.route('/interest/<int:interest_id>/')
#@login_required
def interest_detail(interest_id):
    """Provide HTML page with all details."""
    # Query: get object by ID.
    appt = db.session.query(Interest).get(interest_id)
    if appt is None or appt.user_id != current_user.id:
        # Abort with Not Found.
        abort(404)
    return render_template('interest/detail.html', appt=appt)


@app.route('/interests/')
#@login_required
def interest_details():
    """Provide HTML page with all details."""
    # Query: get object by ID.
    appt = Interest.select()
    return render_template('interest/detail.html', appt=appt)

@app.route('/interest/create/', methods=['GET', 'POST'])
#@login_required
def interest_create():
    """Provide HTML form to create a new record."""
    form = InterestForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Interest(user_id=current_user.id)
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send the user back to the full interest list.
        return redirect(url_for('interest_list'))
    # Either first load or validation error at this point.
    return render_template('interest/edit.html', form=form)


@app.route('/interest/<int:interest_id>/edit/', methods=['GET', 'POST'])
#@login_required
def interest_edit(Interest_id):
    """Provide HTML form to edit ."""
    appt = db.session.query(Interest).get(interest_id)
    if appt is None:
        abort(404)
    if appt.user_id != current_user.id:
        abort(403)
    form = InterestForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view of that interest.
        return redirect(url_for('interest_detail', interest_id=appt.id))
    return render_template('interest/edit.html', form=form)


@app.route('/interest/<int:interest_id>/delete/', methods=['DELETE'])
#@login_required
def interest_delete(Interest_id):
    """Delete a record using HTTP DELETE, respond with JSON for JavaScript."""
    appt = db.session.query(Interest).get(interest_id)
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
