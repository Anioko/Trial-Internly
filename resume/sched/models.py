"""Domain models for an appointment scheduler, using pure SQLAlchemy."""

from datetime import datetime

from flask.ext.security import UserMixin, RoleMixin

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship, synonym, backref
from sqlalchemy.sql import select

from werkzeug import check_password_hash, generate_password_hash

from common import db

ROLE_ADMIN = 0
ROLE_USER = 1
ROLE_COMPANY_SILVER = 2
ROLE_COMPANY_FREE = 3
ROLE_COMPANY_PREMIUM = 4
ROLE_COMPANY_PREMIUM_PRO = 5
ROLE_SCHOOL = 6
ROLE_CANDIDATE = 7

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

postions_users = db.Table('positions_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('position_id', db.Integer(), db.ForeignKey('Positions.id')))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    """A user login, with credentials and authentication."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column('password', String(255))

    # Falsk-Security
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    role_id = Column(Integer, ForeignKey('role.id'), )
    roles = relationship('Role', secondary=roles_users,
                            backref=backref('user', lazy='dynamic'))


    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    name = Column('name', String(200))
    company = Column(Boolean(), default=False)

    def __unicode__(self):
        return u"{0} uID:<{1}>".format(self.name, self.id)

class Resume(db.Model):
    """CV's."""
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)
    
    name = Column(String(255), default="")
    email = Column(String(100), default="")
    phone = Column(String(255), default="")
    title = Column(String(255), default="")
    city = Column(String(100), default="")
    zip = Column(String(50), default="")
    country = Column(String(255), default="")
    url = Column(String(255), default="")
    citizenship = Column(String(255), default="")

    summary_title = Column(String(255), default="")
    summary_text = Column(String(500), default="")
    
    company_name = Column(String(255), default="")
    company_summary = Column(String(255), default="")
    role = Column(String(255), default="")
    role_description = Column(Text)
    start = Column(String(255), default="")
    end = Column(String(255), default="")
    currently = Column(Boolean, default=False)
    location = Column(String(255), default="")


    summary_title_two = Column(String(255), default="")
    summary_text_two = Column(String(500), default="")
    
    company_name_two = Column(String(255), default="")
    company_summary_two = Column(String(255), default="")
    role_two = Column(String(255), default="")
    role_description_two = Column(Text)
    start_date = Column(String(255), default="")
    end_date = Column(String(255), default="")
    currently_two = Column(Boolean, default=False)
    location_two = Column(String(255), default="")

    school_name_one = Column(String(255), default="")
    degree_description = Column(String(255), default="")
    grading = Column(String(255), default="")
    start_date_school = Column(String(255), default="")
    end_date_graduation = Column(String(255), default="")
    currently_three = Column(Boolean, default=False)
    location_school = Column(String(255), default="")
    city_school = Column(String(255), default="")
    country_school = Column(String(255), default="")

    school_name_two = Column(String(255), default="")
    degree_description_two = Column(String(255), default="")
    grading_two = Column(String(255), default="")
    start_date_one = Column(String(255), default="")
    end_date_two = Column(String(255), default="")
    currently_four = Column(Boolean, default=False)
    location_school_two = Column(String(255), default="")
    city_school_two = Column(String(255), default="")
    country_school_two = Column(String(255), default="")

    skills_one = Column(String(255), default="")
    skills_two = Column(String(255), default="")
    skills_three = Column(String(255), default="")
    skills_four = Column(String(255), default="")
    skills_five = Column(String(255), default="")
    skills_six = Column(String(255), default="")
    skills_seven = Column(String(255), default="")
    skills_eight = Column(String(255), default="")
    skills_nine = Column(String(255), default="")
    skills_ten = Column(String(255), default="")

    # NEW FIELDS with new resume tempate
    company_summary1 = Column(String(255), default="")
    company_summary2 = Column(String(255), default="")

    role1 = Column(String(255), default="")
    role2 = Column(String(255), default="")

    role_description1 = Column(Text)
    role_description2 = Column(Text)


    company_name1 = Column(Text)
    company_name2 = Column(Text)

    core_compitencies = Column(Text)
    core_compitencies1 = Column(Text)
    core_compitencies2 = Column(Text)
    core_compitencies3 = Column(Text)
    core_compitencies4 = Column(Text)

    degree_description1 = Column(Text)
    degree_description2 = Column(Text)

    school_name = Column(Text)
    school_name1 = Column(Text)
    school_name2 = Column(Text)

    location_school1  = Column(Text)
    location_school2  = Column(Text)

    start_date_school = Column(Text)
    start_date_school1 = Column(Text)
    start_date_school2 = Column(Text)

    end_date_school = Column(Text)
    end_date_school1 = Column(Text)
    end_date_school2 = Column(Text)

    company_name1 = Column(Text)
    company_name2 = Column(Text)

    location_company = Column(Text)
    location_company1 = Column(Text)
    location_company2 = Column(Text)

    start_date_company = Column(Text)
    start_date_company1 = Column(Text)
    start_date_company2 = Column(Text)

    end_date_company = Column(Text)
    end_date_company1 = Column(Text)
    end_date_company2 = Column(Text)

    work_currently = Column(Boolean, default=False)
    work_currently1 = Column(Boolean, default=False)
    work_currently2 = Column(Boolean, default=False)

    school_currently = Column(Boolean, default=False)
    school_currently1 = Column(Boolean, default=False)
    school_currently2 = Column(Boolean, default=False)

    role1 = Column(Text)
    role2 = Column(Text)

    work1_achievement = Column(Text)
    work1_achievement1 = Column(Text)
    work1_achievement2 = Column(Text)

    work2_achievement = Column(Text)
    work2_achievement1 = Column(Text)
    work2_achievement2 = Column(Text)

    work3_achievement = Column(Text)
    work3_achievement1 = Column(Text)
    work3_achievement2 = Column(Text)

    other_skills = Column(Text)
    other_skills1 = Column(Text)
    other_skills2 = Column(Text)
    other_skills3 = Column(Text)
    other_skills4 = Column(Text)
    other_skills5 = Column(Text)

    duties = Column(Text)
    duties1 = Column(Text)
    duties2 = Column(Text)




    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)





class Position(db.Model):
    """An appointment on the calendar."""
    __tablename__ = 'Positions'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)

    company_website = Column(String(255))
    company_name = Column(String(255))
    location = Column(String(255))
    pub_date = Column(DateTime, default=datetime.now, nullable=False)

    position_title = Column(String(255))
    required_skill_one = Column(String(255))
    required_skill_two = Column(String(255))
    required_skill_three = Column(String(255))
    required_skill_four = Column(String(255))
    required_skill_five = Column(String(255))
    required_skill_six = Column(String(255))
    required_skill_seven = Column(String(255))
    required_skill_eight = Column(String(255))
    required_skill_nine = Column(String(255))
    required_skill_ten = Column(String(255))
    description = Column(Text)

    users = relationship('User', secondary=postions_users,
                            backref=backref('User', lazy='dynamic'))

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)

class Oauth(db.Model):
    __tablename__ = 'oauth'
    id = Column(Integer, primary_key=True)
    provider = Column(String(255))
    provider_id = Column(String(255))
    email = Column(String(255))
    profile = Column(String(),nullable=True)

    additional_data1 = Column(String(),nullable=True)
    additional_data2 = Column(String(),nullable=True)
    additional_data3 = Column(String(),nullable=True)
    additional_data4 = Column(String(),nullable=True)
    additional_data5 = Column(String(),nullable=True)

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')

class CompanyUserData(db.Model):
    __tablename__ = 'company_user_data'
    id = Column(Integer, primary_key=True,)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    website = Column(String(255))
    company_name = Column(String(255))
    company_adress = Column(String(),nullable=True)
    phone_number = Column(String(255))

    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')

    additional_data1 = Column(String(),nullable=True)
    additional_data2 = Column(String(),nullable=True)
    additional_data3 = Column(String(),nullable=True)
    additional_data4 = Column(String(),nullable=True)
    additional_data5 = Column(String(),nullable=True)

class ResumeView(db.Model):
    __tablename__ = 'resume_view'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)

    user_id = Column(Integer, ForeignKey(User.id))
    resume_id = Column(Integer, ForeignKey(Resume.id))

    user = relationship('User', foreign_keys='ResumeView.user_id')
    resume = relationship('Resume', foreign_keys='ResumeView.resume_id')

    def __init__(self, user=None, resume=None):
        print "init", user, resume
        self.timestamp = datetime.now()
        self.user = user
        self.resume = resume


if __name__ == '__main__':
    from datetime import timedelta

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # This uses a SQLite database in-memory.
    #
    # That is, this uses a database which only exists for the duration of
    # Python's process execution, and will not persist across calls to Python.
    engine = create_engine('sqlite://', echo=True)

    # Create the database tables if they do not exist, and prepare a session.
    #
    # The engine connects to the database & executes queries. The session
    # represents an on-going conversation with the database and is the primary
    # entry point for applications to use a relational database in SQLAlchemy.
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add a sample user.
    user = User(name='Ron DuPlain',
                email='ron.duplain@gmail.com',
                password='secret')
    session.add(user)
    session.commit()

    now = datetime.now()

    # Add some sample appointments.
    session.add(Appointment(
        user_id=user.id,
        title='Important Meeting',
        start=now + timedelta(days=3),
        end=now + timedelta(days=3, seconds=3600),
        allday=False,
        location='The Office'))
    session.commit()

    session.add(Appointment(
        user_id=user.id,
        title='Past Meeting',
        start=now - timedelta(days=3, seconds=3600),
        end=now - timedelta(days=3),
        allday=False,
        location='The Office'))
    session.commit()

    session.add(Appointment(
        user_id=user.id,
        title='Follow Up',
        start=now + timedelta(days=4),
        end=now + timedelta(days=4, seconds=3600),
        allday=False,
        location='The Office'))
    session.commit()

    session.add(Appointment(
        user_id=user.id,
        title='Day Off',
        start=now + timedelta(days=5),
        end=now + timedelta(days=5),
        allday=True))
    session.commit()

    # Create, update, delete.
    appt = Appointment(
        user_id=user.id,
        title='My Appointment',
        start=now,
        end=now + timedelta(seconds=1800),
        allday=False)

    # Create.
    session.add(appt)
    session.commit()

    # Update.
    appt.title = 'Your Appointment'
    session.commit()

    # Delete.
    session.delete(appt)
    session.commit()

    # Demonstration Queries

    # Each `appt` example is a Python object of type Appointment.
    # Each `appts` example is a Python list of Appointment objects.

    # Get an appointment by ID.
    appt = session.query(Appointment).get(1)

    # Get all appointments.
    appts = session.query(Appointment).all()

    # Get all appointments before right now, after right now.
    appts = session.query(Appointment).filter(Appointment.start < datetime.now()).all()
    appts = session.query(Appointment).filter(Appointment.start >= datetime.now()).all()

    # Get all appointments before a certain date.
    appts = session.query(Appointment).filter(Appointment.start <= datetime(2013, 5, 1)).all()

    # Get the first appointment matching the filter query.
    appt = session.query(Appointment).filter(Appointment.start <= datetime(2013, 5, 1)).first()

