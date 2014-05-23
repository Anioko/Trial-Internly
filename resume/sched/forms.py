"""Forms to render HTML input & validate request data."""

from wtforms import Form, BooleanField, DateTimeField, PasswordField
from wtforms import TextAreaField, TextField
from wtforms.validators import Length, required


class AppointmentForm(Form):
    """Render HTML input for Appointment model & validate submissions.

    This matches the models.Appointment class very closely. Where
    models.Appointment represents the domain and its persistence, this class
    represents how to display a form in HTML & accept/reject the results.
    """
    title = TextField('Title', [Length(max=255)])
    start = DateTimeField('Start', [required()])
    end = DateTimeField('End')
    allday = BooleanField('All Day')
    location = TextField('Location', [Length(max=255)])
    description = TextAreaField('Description')

class ResumeForm(Form):
    """Render HTML input for Resume model & validate submissions.

    This matches the models.Resume class very closely. Where
    models.Resume represents the domain and its persistence, this class
    represents how to display a form in HTML & accept/reject the results.
    """
    name = TextField('Name', [Length(max=255)])
    email = TextField('Email', [Length(max=100)])
    phone = TextField('Phone', [Length(max=255)])
    city = TextField('City', [Length(max=100)])
    zip = TextField('Zip', [Length(max=50)])
    country = TextField('Country', [Length(max=255)])
    url = TextField('Url', [Length(max=255)])
    citizenship = TextField('Country of Birth', [Length(max=255)])

    summary_title = TextField('Summary Title', [Length(max=255)])
    summary_text = TextField('Summary Text', [Length(max=500)])

    company_name = TextField('Company Name', [Length(max=255)])
    company_summary = TextField('Company Summary', [Length(max=255)])
    role = TextField('Role', [Length(max=255)])
    role_description = TextAreaField('Role Description')
    
    
    start = TextField('Start')
    end = TextField('End')
    currently = BooleanField('Currently')
    location = TextField('Location', [Length(max=255)])


    company_name_two = TextField('Company Name', [Length(max=255)])
    company_summary_two = TextField('Company Summary', [Length(max=255)])
    role_two = TextField('Role', [Length(max=255)])
    role_description_two = TextAreaField('Role Description')
    
    
    start_date = TextField('Start')
    end_date = TextField('End')
    currently_two = BooleanField('Currently')
    location_two = TextField('Location', [Length(max=255)])


class LoginForm(Form):
    """Render HTML input for user login form.

    Authentication (i.e. password verification) happens in the view function.
    """
    username = TextField('Username', [required()])
    password = PasswordField('Password', [required()])
