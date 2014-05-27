"""Domain models for an appointment scheduler, using pure SQLAlchemy."""

from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.declarative import declarative_base
from werkzeug import check_password_hash, generate_password_hash


Base = declarative_base()


#ROLE_USER = 0
#ROLE_COMPANY_SILVER = 1
#ROLE_COMPANY_FREE = 2
#ROLE_COMPANY_PREMIUM = 3
#ROLE_COMPANY_PREMIUM_PRO = 4
#ROLE_SCHOOL = 5
ROLE_CANDIDATE = 6



class User(Base):
    """A user login, with credentials and authentication."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    name = Column('name', String(200))
    email = Column(String(100), unique=True, nullable=False)
    active = Column(Boolean, default=True)
    role = Column(Integer, default=ROLE_CANDIDATE)

    _password = Column('password', String(100))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        if self.password is None:
            return False
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        email = email.strip().lower()
        user = query(cls).filter(cls.email==email).first()
        if user is None:
            return None, False
        if not user.active:
            return user, False
        return user, user.check_password(password)

    # Hooks for Flask-Login.
    #
    # As methods, these are only valid for User instances, so the
    # authentication will have already happened in the view functions.
    #
    # If you prefer, you can use Flask-Login's UserMixin to get these methods.

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


class Resume(Base):
    """CV's."""
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)
    
    name = Column(String(255))
    email = Column(String(100))
    phone = Column(String(255))
    title = Column(String(255))
    city = Column(String(100))
    zip = Column(String(50))
    country = Column(String(255))
    url = Column(String(255))
    citizenship = Column(String(255))

    summary_title = Column(String(255))
    summary_text = Column(String(500))
    
    company_name = Column(String(255))
    company_summary = Column(String(255))
    role = Column(String(255))
    role_description = Column(Text)
    start = Column(String(255))
    end = Column(String(255))
    currently = Column(Boolean, default=False)
    location = Column(String(255))


    summary_title_two = Column(String(255))
    summary_text_two = Column(String(500))
    
    company_name_two = Column(String(255))
    company_summary_two = Column(String(255))
    role_two = Column(String(255))
    role_description_two = Column(Text)
    start_date = Column(String(255))
    end_date = Column(String(255))
    currently_two = Column(Boolean, default=False)
    location_two = Column(String(255))

    school_name_one = Column(String(255))
    degree_description = Column(String(255))
    grading = Column(String(255))
    start_date_school = Column(String(255))
    end_date_graduation = Column(String(255))
    currently_three = Column(Boolean, default=False)
    location_school = Column(String(255))
    city_school = Column(String(255))
    country_school = Column(String(255))

    school_name_two = Column(String(255))
    degree_description_two = Column(String(255))
    grading_two = Column(String(255))
    start_date_one = Column(String(255))
    end_date_two = Column(String(255))
    currently_four = Column(Boolean, default=False)
    location_school_two = Column(String(255))
    city_school_two = Column(String(255))
    country_school_two = Column(String(255))

    skills_one = Column(String(255))
    skills_two = Column(String(255))
    skills_three = Column(String(255))
    skills_four = Column(String(255))
    skills_five = Column(String(255))
    skills_six = Column(String(255))
    skills_seven = Column(String(255))
    skills_eight = Column(String(255))
    skills_nine = Column(String(255))
    skills_ten = Column(String(255))


    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)





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
