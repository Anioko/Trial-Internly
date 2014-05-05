"""Forms to render HTML input & validate request data."""

from wtforms import Form, BooleanField, DateTimeField, PasswordField
from wtforms import TextAreaField, TextField
from wtforms.validators import Length, required




##### Unpaid Internships Forms
    
class UnpaidForm(Form):
	
    title = TextField('Title', [Length(max=255)])
    company = TextAreaField('Company')
    description = TextAreaField('Description')
    website = TextField('website', [Length(max=255)])
    pub_date = DateTimeField('pub_date')

class PaidForm(Form):
    title = TextField('Title', [Length(max=255)])
    company = TextField('Company', [Length(max=255)])
    description = TextAreaField('Description')
    location = TextField('Location', [Length(max=255)])
    website = TextField('Website', [Length(max=255)])
    skills_needed_one = TextField('skills_needed_one', [Length(max=255)])
    skills_needed_two = TextField('skills_needed_two', [Length(max=255)])
    skills_needed_three = TextField('skills_needed_three', [Length(max=255)])
    skills_needed_four = TextField('skills_needed_four', [Length(max=255)])
    pub_date = DateTimeField('pub_date')


class ThesisForm(Form):
    title = TextField('Title', [Length(max=255)])
    research_topic = TextField('Research_topic', [Length(max=255)])
    company = TextField('Company', [Length(max=255)])
    description = TextAreaField('Description')
    location = TextField('Location', [Length(max=255)])
    website = TextField('Website', [Length(max=255)])
    academic_level = TextField('academic_level', [Length(max=255)])
    pub_date = DateTimeField('pub_date')
    
	
class EventForm(Form):

    title = TextField('Title', [Length(max=255)])
    start = DateTimeField('Start', [required()])
    end = DateTimeField('End')
    allday = BooleanField('All Day')
    location = TextField('Location', [Length(max=255)])
    description = TextAreaField('Description')


class CompanyForm(Form):
    company_name = TextField('Company Name', [Length(max=255)])
    company_location = TextField('Company Location', [Length(max=255)])
    company_website = TextField('Company Website', [Length(max=255)])
    industry = TextField('Industry', [Length(max=255)])
    company_description = TextAreaField('Description')

class InterestForm(Form):
    looking_for_title = TextField('Title of what you are looking for', [Length(max=255)])
    looking_for = TextAreaField('Describe yourself and what you are looking for')

    joining_startup = BooleanField('Joining a Startup')
    unpaid_internships = BooleanField('Unpaid Internships')
    paid_internships = BooleanField('Paid Internships')
    volunteer_work = BooleanField('Volunteer Work')
    thesis_work_unpaid = BooleanField('Unpaid Thesis Work ')
    thesis_work_paid = BooleanField('Paid Thesis Work ')
    research_work_unpaid = BooleanField(' Unpaid Research Work')
    research_work_paid = BooleanField(' Paid Research Work')
    contact_details = TextAreaField('Contact Details')
    interest_location = TextField('Interested Location', [Length(max=255)])
    interest_location_two = TextField('Interested Location', [Length(max=255)])
    interest_location_three = TextField('Interested Location', [Length(max=255)])
	

class BlogForm(Form):
    """Render HTML input for Blog model & validate submissions.

    This matches the models.Blog class very closely. Where
    models.Blog represents the domain and its persistence, this class
    represents how to display a form in HTML & accept/reject the results.
    """
    title = TextField('Title', [Length(max=255)])
    pub_date = DateTimeField('pub_date')
    author = TextField('author', [Length(max=255)])
    description = TextAreaField('Description')

	
class LoginForm(Form):
    """Render HTML input for user login form.

    Authentication (i.e. password verification) happens in the view function.
    """
    username = TextField('Email', [required()])
    password = PasswordField('Password', [required()])
