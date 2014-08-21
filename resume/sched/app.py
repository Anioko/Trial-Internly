"""The Flask app, with initialization and view functions."""

import logging
import base64
import datetime
from functools import wraps
from unicodedata import normalize
from sqlalchemy import func

from flask import send_from_directory
from flask import abort, jsonify, redirect, render_template, request, url_for, flash, session, make_response
from flask.ext.login import LoginManager, current_user, login_user
from flask.ext.login import login_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.security.signals import user_registered
from flask.ext.security.utils import url_for_security
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.misaka import Misaka
from flask_oauthlib.client import OAuth , OAuthException
from flask_mail import Mail, Message


from werkzeug import secure_filename
from wtforms.ext.appengine import db

from sched.config import DefaultConfig
from sched import filters
from sched.forms import ResumeForm, PositionForm, ExtendedRegisterForm, RegisteCompanyForm, ContactForm
from sched.models import User, Resume, Position, Role, Oauth, CompanyUserData, ResumeView
from sched.common import app, db, security
from sched.pdfs import create_pdf

from sched.utils.linkedin_resume import create_linkedin_resume
from sched.utils.base62 import dehydrate, saturate


def slug(text, encoding=None,permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):
    if isinstance(text, str):
        text = text.decode(encoding or 'ascii')
    clean_text = text.strip().replace(' ', '-').lower()
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)
    return ''.join(strict_text)

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

def company_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.has_role('ROLE_COMPANY_FREE') is False:
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
admin.add_view(AdminView(Position, db.session))
admin.add_view(AdminView(CompanyUserData, db.session))


@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role("ROLE_CANDIDATE")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()

# Load custom Jinja filters from the `filters` module.
filters.init_app(app)

def date_from_string(date):
    if date:
      return date if len(date)>0 else '-'
    else:
      return '-'

def base64_encode(value):
    return base64.b64encode(str(value))

app.jinja_env.filters['datefromstring'] = date_from_string
app.jinja_env.filters['b64'] = base64_encode
app.jinja_env.filters['b62'] = dehydrate
app.jinja_env.filters['slug'] = slug

Misaka(app)
mail = Mail(app)

# Setup logging for production.
if not app.debug:
    app.logger.setHandler(logging.StreamHandler()) # Log to stderr.
    app.logger.setLevel(logging.INFO)


@app.errorhandler(404)
def error_not_found(error):
    """Render a custom template when responding with 404 Not Found."""
    return render_template('error/not_found.html'), 404


########################OAUTH#################################################
oauth = OAuth(app)

facebook = oauth.remote_app(
    'facebook',
    consumer_key=app.config['FACEBOOK_LOGIN_APP_ID'],
    consumer_secret=app.config['FACEBOOK_LOGIN_APP_SECRET'],
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    access_token_method='POST',
)

linkedin = oauth.remote_app(
    'linkedin',
    consumer_key=app.config['LINKEDIN_LOGIN_API_KEY'],
    consumer_secret=app.config['LINKEDIN_LOGIN_SECRET_KEY'],
    request_token_params={
        'scope': ['r_basicprofile', 'r_emailaddress'],
        'state': 'RandomString',
    },
    base_url='https://api.linkedin.com/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
    authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
)

linkedin_resume = oauth.remote_app(
    'linkedin_resume',
    consumer_key=app.config['LINKEDIN_FULL_PROFILE_API_KEY'],
    consumer_secret=app.config['LINKEDIN_FULL_PROFILE_SECRET_KEY'],
    request_token_params={
        'scope': ['r_basicprofile','r_fullprofile', 'r_contactinfo'],
        'state': 'RandomString',
    },
    base_url='https://api.linkedin.com/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
    authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
)


@app.route('/login/fb')
def login_fb():
    callback = url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return facebook.authorize(callback=callback)

@app.route('/login/ln')
def login_ln():
    return linkedin.authorize(callback=url_for('authorized', _external=True))

@app.route('/resumes/create/linkedin')
def create_resume_ln():
    #session.pop('linkedin_token')
    #session.pop('access_token')
    return linkedin_resume.authorize(callback=url_for('linkedin_resume_authorized', _external=True))

@app.route('/login/ln/authorized')
@linkedin.authorized_handler
def authorized(resp):
    if resp is None: # Authentication failure...
        flash("There was a problem with log in using LinkedIn: {0}".format(request.args['error_description']), 'danger')
        return render_template('layout.html')

    # Get LinkedIn token
    session['linkedin_token'] = (resp['access_token'], '')
    # Load profile fields from linkedin
    profile = linkedin.get("people/~:(id,site-standard-profile-request,email-address,first-name,last-name)")

    # Try to find user and his Oauth record in db
    user = db.session.query(User).filter(User.email==profile.data['emailAddress']).first()
    oauth = db.session.query(Oauth).filter(Oauth.provider_id==profile.data['id']).\
        filter(Oauth.provider=='linkedin').first()

    # User not exist? So we need to 'register' him on the site
    if user is None:
        user = User()
        user.email = profile.data['emailAddress']
        user.name = profile.data['firstName'] + u" " + profile.data['lastName']
        user.password = unicode(u"ln-id|"+profile.data['id'])   # User from OAuth have no password (we save id)
        user.active = True
        user.confirmed_at = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        default_role = user_datastore.find_role("ROLE_CANDIDATE")
        user_datastore.add_role_to_user(user, default_role)
        db.session.commit()

    # Save some data from OAuth service that might be useful sometime later
    # This is also used when user was registered by e-mail and now he
    # logs in using social account for the same e-mail
    if oauth is None:
        oauth = Oauth()
        oauth.provider='linkedin'
        oauth.provider_id=profile.data['id']
        oauth.email=profile.data['emailAddress']
        oauth.profile=profile.data['siteStandardProfileRequest']['url']
        oauth.user=user     # Connect with user
        # There are few fields empty...
        db.session.add(oauth)
        db.session.commit()

    # Try to login new user
    lok = login_user(user)
    if lok:
        # Show green mesaage that all went fine
        flash("You have been successfully signed in using LinkedIn.", 'success')
        return redirect(url_for('resumes_list'))
    else:
        flash("There was a problem with your logining-in", 'warning')
        return render_template('layout.html')



@app.route('/login/fb/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None: # Authentication failure...
        flash("There was a problem with log in using Facebook: {0}".format(request.args['error_description']), 'danger')
        return render_template('layout.html')

    # Facebook session token
    session['oauth_token'] = (resp['access_token'], '')
    # Load facebook profile
    profile = facebook.get('/me')

    # Try to find user and his Oauth record in db
    user = db.session.query(User).filter(User.email==profile.data['email']).first()
    oauth = db.session.query(Oauth).filter(Oauth.provider_id==profile.data['id']).\
        filter(Oauth.provider=='facebook').first()

    # User not exist? So we need to 'register' him on the site
    if user is None:
        user = User()
        user.email = profile.data['email']
        user.name = profile.data['first_name'] + u" " + profile.data['last_name']
        user.password = unicode(u"fb-id|"+profile.data['id'])   # User from OAuth have no password (we save id)
        user.active = True
        user.confirmed_at = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        default_role = user_datastore.find_role("ROLE_CANDIDATE")
        user_datastore.add_role_to_user(user, default_role)
        db.session.commit()

    # Save some data from OAuth service that might be useful sometime later
    # This is also used when user was registered by e-mail and now he
    # logs in using social account for the same e-mail
    if oauth is None:
        oauth = Oauth()
        oauth.provider='facebook'
        oauth.provider_id=profile.data['id']
        oauth.email=profile.data['email']
        oauth.profile=profile.data['link']
        oauth.user=user     # Contect with user
        # There are few fields empty...
        db.session.add(oauth)
        db.session.commit()

    # Try to login new user
    lok = login_user(user)
    if lok:
        # Show green mesaage that all went fine
        flash("You have been successfully signed in using Facebook.", 'success')
        return redirect(url_for('resumes_list'))
    else:
        flash("There was a problem with your logining-in", 'warning')
        return render_template('layout.html')

@app.route('/resumes/create/linkedin/redirect')
@linkedin_resume.authorized_handler
def linkedin_resume_authorized(resp):
    if resp is None: # Authentication failure...
        flash("Oh! We can get your data from you Linkedin,", 'danger')
        return redirect(url_for('resumes_list'))

    # Get LinkedIn token
    session['linkedin_full_profile_token'] = (resp['access_token'], '')
    # Load resume fileds
    resume_fields = linkedin.get("people/~:(id,first-name,last-name,phone-numbers,location:(name,country),site-standard-profile-request,headline,positions,skills,educations,public-profile-url)",
                                 token=session.get('linkedin_full_profile_token'))

    if hasattr(resume_fields, 'data'):
        resume = create_linkedin_resume(resume_fields.data)
        if resume is not None:
            resume.user = current_user
            resume.user_id = current_user.id
            resume.email = current_user.email
            db.session.add(resume)
            db.session.commit()
            return redirect(url_for('resumes_list'))
        else:
            flash("Oh! There was a problem while generating your resume :(", 'warning')
            return redirect(url_for('resumes_list'))
    else:
        flash("Oh! We can get data from you Linkedin,", 'warning')
        return redirect(url_for('resumes_list'))

# Here goes special functions need by Flask-OAuthlib
@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@linkedin.tokengetter
def get_linkedin_oauth_token():
    return session.get('linkedin_token')

@linkedin_resume.tokengetter
def get_linkedin_full_profile_oauth_token():
    return session.get('linkedin_full_profile_token')

def change_linkedin_query(uri, headers, body):
    auth = headers.pop('Authorization')
    headers['x-li-format'] = 'json'
    if auth:
        auth = auth.replace('Bearer', '').strip()
        if '?' in uri:
            uri += '&oauth2_access_token=' + auth
        else:
            uri += '?oauth2_access_token=' + auth
    return uri, headers, body

linkedin.pre_request = change_linkedin_query
# linkedin_resume.pre_request = change_linkedin_query

########################OAUTH#################################################

#######View for site map############
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/BingSiteAuth.xml')
def static_from_root_bing():
    return send_from_directory(app.static_folder, request.path[1:])

#########Views for Resume#######

@app.route('/find/')
@admin_required
def all_resumes():
    """Provide HTML page listing all resumes in the database."""
    # Query: Get all Resume objects, sorted by the resume date.
    appts = db.session.query(Resume).all()
    return render_template('resume/all.html', appts=appts)

@app.route('/dashboard/')
def resumes_list():
    """Provide HTML page listing all resumes in the database."""
    # Query: Get all Resume objects, sorted by the resume date.
    appts = list()
    resumes = (db.session.query(Resume)
             .filter_by(user_id=current_user.id)
             .order_by(Resume.start.asc()).all())

    for resume in resumes:
        views_count_resume = db.session.query(ResumeView.id).filter(ResumeView.resume == resume).count()
        appts.append((resume, views_count_resume))

    positions = db.session.query(Position).filter(
                Position.users.contains(current_user)).all()

    return render_template('resume/dashboard.html', appts=appts, positions=positions)

@app.route('/company/resumes/preview/<resume_id>/')
@login_required
def resume_preview(resume_id):
    """Provide HTML page with all details on a given resume.
       The url is base64 encoded so no one will try to check other resumes.
    """
    resume_id = base64.b64decode(resume_id)
    appt = db.session.query(Resume).get(resume_id)
    if appt is None:
        # Abort with Not Found.
        abort(404)
    # Count the view to user resume views
    resume_view = ResumeView(current_user, appt)
    db.session.add(resume_view)
    db.session.commit()
    # Template without edit buttons
    return render_template('resume/resume_detail_preview.html', appt=appt)

@app.route('/company/resumes/preview/pdf/<resume_id>/')
@login_required
def resume_preview_pdf(resume_id):
    """Provide pdf preview of resume.
       The url is base64 encoded so no one will try to check other resumes.
    """
    resume_id = base64.b64decode(resume_id)
    appt = db.session.query(Resume).get(resume_id)
    if appt is None:
        # Abort with Not Found.
        abort(404)

    pdf = create_pdf(render_template('resume/resume_detail_pdf.html', appt=appt))

    response = make_response(pdf.getvalue())
    response.headers['Content-Disposition'] = "attachment; filename=resume.pdf"
    response.mimetype = 'application/pdf'
    return response

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


@app.route('/resumes/<int:resume_id>/delete/', methods=['GET', 'POST'])
@login_required
def resume_delete(resume_id):
    appt = db.session.query(Resume).get(resume_id)
    if appt is None:
        abort(404)
    if appt.user_id != current_user.id:
        abort(403)
    db.session.delete(appt)
    db.session.commit()
    return redirect(url_for('resumes_list'))

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

#########Views for Positions#######

@app.route('/positions/')
def all_positions():
    """Provide HTML page listing all positions in the database.

    THIS VIEW IS FOR APPLICANTS
    """
    # Query: Get all Position objects that don't exceed the deadline.

    if current_user and current_user.has_role('ROLE_ADMIN'):
        appts = db.session.query(Position).all()
    else:
        time_diff = datetime.datetime.today() - \
                datetime.timedelta(
                    days=app.config['POSITION_APPERANCE_TIME_IN_DAYS'])

        appts = db.session.query(Position).filter(Position.pub_date > time_diff).all()

    return render_template('position/all.html', appts=appts)

@app.route('/positions/<int:position_id>/apply/')
@login_required
def position_apply(position_id):
    """
    Applaying for positon by applicants.

    THIS VIEW IS FOR APPLICANTS
    :param position_id: id of position to apply
    :return: nothing
    """
    position = db.session.query(Position).get(position_id)
    if position is None:
        abort(404)
    elif current_user.id is None:
        abort(403)
    else:
        if current_user in position.users:
            flash("You have <strong>already applied</strong> for this position.", 'warning')
        else:
            position.users.append(current_user)
            db.session.add(position)
            db.session.commit()
            flash("You have <strong>successfully applied</strong> for a {0}.".format(position.position_title), 'success')
        return redirect(url_for('all_positions'))

@app.route('/positions/<int:position_id>/')
def position_details(position_id):
    """Provide HTML page with all details on a given position.

    THIS VIEW IS FOR APPLICANTS
    """
    # Query: get Position object by ID.
    appt = db.session.query(Position).get(position_id)
    if current_user.is_anonymous():
        resume_exists = False
        anonymous = True
    else:
        resume_exists = bool(db.session.query(Resume).filter(Resume.user_id==current_user.id).count()> 0)
        anonymous = False
    return render_template('position/details.html', appt=appt,
                           have_resume=resume_exists, anonym=anonymous)

@app.route('/apply-now/<b62id>/<title>')
def position_apply_now(b62id, title):
    position_id = saturate(b62id)
    return redirect(url_for('position_details', position_id=position_id))

# Company views

@app.route('/company/signup/', methods=['GET', 'POST'])
def security_company_register():
    return redirect(url_for_security('register', next=url_for('company_register')))

@app.route('/company/activate/', methods=['GET', 'POST'])
@login_required
def company_register():
    company_details = None
    try:
        company_details = db.session.query(CompanyUserData
                        ).filter_by(user_id=current_user.id).all()[0]
    except IndexError:
        pass

    if company_details:
        return redirect(url_for('position_list'))

    form = RegisteCompanyForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = CompanyUserData(user_id=current_user.id)
        if not appt.last_name:
            appt.last_name = ""
        form.populate_obj(appt)
        db.session.add(appt)

        company_role = user_datastore.find_role("ROLE_COMPANY_FREE")
        user_datastore.add_role_to_user(current_user, company_role)
        db.session.commit()

        # Success. Send to the postion list
        flash("Welcome in company dashboard.", 'succes')
        return redirect(url_for('position_list'))
    # Either first load or validation error at this point.
    return render_template('position/edit_company.html', form=form)

@app.route('/company/positions/')
@login_required
@company_required
def position_list():
    """Provide HTML page listing all rpositions in the database.

    THIS VIEW IS FOR COMPANIES
    """
    # Query: Get all Position objects, sorted by the position date.
    if current_user and current_user.has_role('ROLE_ADMIN'):
        appts = (db.session.query(Position).
                 order_by(Position.pub_date.asc()).all())
    else:
        appts = (db.session.query(Position)
             .filter_by(user_id=current_user.id)
             .order_by(Position.pub_date.asc()).all())

    return render_template('position/index.html', appts=appts)

@app.route('/company/positions/create/', methods=['GET', 'POST'])
@login_required
@company_required
def position_create():
    """Provide HTML form to create a new positions record.

    THIS VIEW IS FOR COMPANIES
    """
    try:
        company_details = db.session.query(CompanyUserData
                        ).filter_by(user_id=current_user.id).all()[0]
    except IndexError:
        return redirect(url_for('company_register'))

    if company_details is None:
        return redirect(url_for('company_register'))

    form = PositionForm(request.form)
    if company_details is not None:
        form.company_name.data = company_details.company_name
        form.company_website.data = company_details.website

    if request.method == 'POST' and form.validate():
        appt = Position(user_id=current_user.id)
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send the user back to the full resumes list.
        return redirect(url_for('position_list'))
    # Either first load or validation error at this point.
    return render_template('position/edit.html', form=form)

@app.route('/company/positions/<int:position_id>/edit/', methods=['GET', 'POST'])
@login_required
@company_required
def position_edit(position_id):
    """Provide HTML form to edit a given position.

    THIS VIEW IS FOR COMPANIES
    """
    appt = db.session.query(Position).get(position_id)
    if appt is None:
        abort(404)
    if appt.user_id != current_user.id and (not current_user.has_role('ROLE_ADMIN')):
        abort(403)
    form = PositionForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        del form.pub_date
        db.session.commit()
        # Success. Send the user back to the detail view of that resume.
        return redirect(url_for('position_details', position_id=appt.id))
    return render_template('position/edit.html', form=form)

@app.route('/company/positions/<int:position_id>/delete/', methods=['GET', 'POST'])
@login_required
@company_required
def position_delete(position_id):
    """Delete a record

    THIS VIEW IS FOR COMPANIES
    """
    appt = db.session.query(Position).get(position_id)

    if appt is None:
        # Abort with simple response indicating position not found.
        flash("Wrong postion id.", 'danger')
        return redirect(url_for('position_list'))
    if appt.user_id != current_user.id and (not current_user.has_role('ROLE_ADMIN')):
        # Abort with simple response indicating forbidden.
        flash("You can't remove this position.", 'danger')
        return redirect(url_for('position_list'))
    db.session.delete(appt)
    db.session.commit()
    flash("Postion was removed.", 'succes')
    return redirect(url_for('position_list'))
    # return jsonify({'status': 'OK'})

@app.route('/company/positions/<int:position_id>/applicants/')
@login_required
@company_required
def position_list_applicants(position_id):

    position = db.session.query(Position).get(position_id)
    if position is None:
        abort(404)
    elif current_user.id is None:
        abort(403)
    elif position.user_id != current_user.id and (not current_user.has_role('ROLE_ADMIN')):
        abort(403)
    else:
        applicants_resumes = {}
        applicants = position.users
        for applicant in applicants:
            resumes = db.session.query(Resume).filter(Resume.user_id==applicant.id).all()
            if len(resumes) > 0:
                # encoding each id of resume
                resumes = [base64.b64encode(str(resume.id)) for resume in resumes ]
                applicants_resumes[applicant.id] = resumes
            else:
                applicants_resumes[applicant.id] = None
        return render_template('position/applicants.html', position_id=position_id,
                               applicants=applicants, resumes=applicants_resumes)


@app.route('/company/positions/<int:position_id>/applicants/send-message/', methods=['GET', 'POST'])
@login_required
@admin_required
def position_applicants_send_email(position_id):
    """
     View for conntacitng all aplicants of postion by e-mail.

    :param position_id: id of postion that applicants will be contacted
    :return: None
    """
    if current_user.id is None:
        abort(403)
    else:
        form = ContactForm(request.form)
        if request.method == 'POST' and form.validate():
            position = db.session.query(Position).get(position_id)
            if position is None:
                abort(404)
            emails = [u.email for u in position.users]
            message = Message(subject=form.subject.data,
                            sender='info@intern.ly',
                           reply_to='info@intern.ly',
                           recipients=['info@intern.ly'],
                           bcc=emails,
                           body=form.text.data)
            mail.send(message)
            flash("Message was send.", 'succes')
            return redirect(url_for('position_list_applicants', position_id=position_id))
        return render_template('position/message_send_form.html', form=form)

###Public Views

@app.route('/')
def landing_page():
    if current_user.is_authenticated():
        if current_user.company:
            return redirect(url_for('company_register'))
        else:
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

@app.route('/contact', methods=['GET', 'POST'])
def contact_form():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        #SEND E-MAIL
        message = Message(subject=form.subject.data,
                        sender='support@intern.ly',
                       reply_to=current_user.email,
                       recipients=['support@intern.ly'],
                       body=form.text.data)
        mail.send(message)

        # Success. Send to the postion list
        flash("Your message was send.", 'succes')
        return redirect(url_for('resumes_list'))

    # Either first load or validation error at this point.
    return render_template('public/contact_form.html', form=form)


@app.route('/some-endpoint', methods=['POST'])
def share_email():
    share_text = "Your friend {0} on http://intern.ly want to recommend you this open position: {1}.\n"\
                  "Register, and view it here: {2}."\
                  "\n\n"\
                  "Regards,\n"\
                  "Intern.ly team"

    formated_text = share_text.format(current_user.name, request.form['title'], request.form['url'])
    message = Message(subject="Intern.ly - job offer recomendation!",
                       sender='info@intern.ly',
                       reply_to=current_user.email,
                       recipients=[request.form['email']],
                       body=formated_text)
    mail.send(message)




    print request.__dict__
    print request.form
    return jsonify(status='success')