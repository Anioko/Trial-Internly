"""The Flask app, with initialization and view functions."""

import logging
from functools import wraps

from flask import send_from_directory
from flask import abort, jsonify, redirect, render_template, request, url_for, flash, session, make_response
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.security.signals import user_registered
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView

from werkzeug import secure_filename

from sched.config import DefaultConfig
from sched import filters
from sched.forms import ResumeForm, PositionForm, ExtendedRegisterForm
from sched.models import User, Resume, Position, Role
from sched.common import app, db, security
from sched.pdfs import create_pdf



app.config.from_object(DefaultConfig)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security.init_app(app, user_datastore, register_form=ExtendedRegisterForm)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.has_role('ROLE_ADMIN') is False:
            abort(404)
        return f(*args, **kwargs)
    return decorated_function

class MyAdminIndexView(AdminIndexView):
    @login_required
    @admin_required
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('ROLE_ADMIN')

# Flask-Admin
admin = Admin(app, name='Internly', index_view=MyAdminIndexView())

admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Resume, db.session))


@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role("ROLE_CANDIDATE")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()

# Load custom Jinja filters from the `filters` module.
filters.init_app(app)

def date_from_string(date):
    return date if len(date)>0 else '-'

app.jinja_env.filters['datefromstring'] = date_from_string


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

    return render_template('resume/dashboard.html', appts=appts)


@app.route('/resumes/<int:resume_id>/')
@login_required
def resume_detail(resume_id):
    """Provide HTML page with all details on a given resume."""
    # Query: get Resume object by ID.
    appt = db.session.query(Resume).get(resume_id)
    if appt is None or appt.user_id != current_user.id:
        # Abort with Not Found.
        abort(404)
    return render_template('resume/resume_detail.html', appt=appt)


@app.route('/resumes_pdf/<int:resume_id>/')
@login_required
def resume_detail_pdf(resume_id):
    """Provide HTML page with all details on a given resume."""
    # Query: get Resume object by ID.
    appt = db.session.query(Resume).get(resume_id)
    if appt is None or appt.user_id != current_user.id:
        # Abort with Not Found.
        abort(404)

    pdf = create_pdf(render_template('resume/resume_detail_pdf.html', appt=appt))

    response = make_response(pdf.getvalue())
    response.headers['Content-Disposition'] = "attachment; filename=resume.pdf"
    response.mimetype = 'application/pdf'
    return response





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
    
    if current_user.is_authenticated():
        
        return redirect(url_for('resumes_list'))
    else:
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