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
ROLE_COMPANY_FREE = 2
ROLE_COMPANY_PREMIUM = 3
ROLE_COMPANY_PREMIUM_PRO = 4
#ROLE_SCHOOL = 5
#ROLE_INTERN= 6




class User(Base):
    """A user login, with credentials and authentication."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    name = Column('name', String(200))
    email = Column(String(100), unique=True, nullable=False)
    active = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    role = Column(Integer, default=ROLE_COMPANY_FREE)

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

class Appointment(Base):
    """."""
    __tablename__ = 'Appointment'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)

    title = Column(String(255))
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    allday = Column(Boolean, default=False)
    location = Column(String(255))
    description = Column(Text)

    @property
    def duration(self):
        # If the datetime type were supported natively on all database
        # management systems (is not on SQLite), then this could be a
        # hybrid_property, where filtering clauses could compare
        # Appointment.duration. Without that support, we leave duration as an
        # instance property, where appt.duration is calculated for us.
        delta = self.end - self.start
        return delta.days * 24 * 60 * 60 + delta.seconds

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


class Event(Base):
    """."""
    __tablename__ = 'Event'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)

    title = Column(String(255))
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    allday = Column(Boolean, default=False)
    location = Column(String(255))
    description = Column(Text)

    @property
    def duration(self):
        # If the datetime type were supported natively on all database
        # management systems (is not on SQLite), then this could be a
        # hybrid_property, where filtering clauses could compare
        # Appointment.duration. Without that support, we leave duration as an
        # instance property, where appt.duration is calculated for us.
        delta = self.end - self.start
        return delta.days * 24 * 60 * 60 + delta.seconds

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
		
	
class Blog(Base):
    """."""
    __tablename__ = 'Blog'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)

    title = Column(String(255))
    pub_date = Column(DateTime, nullable=False)
    author = Column(String(255))
    description = Column(Text)

	
    @property
    def duration(self):
        # If the datetime type were supported natively on all database
        # management systems (is not on SQLite), then this could be a
        # hybrid_property, where filtering clauses could compare
        # Appointment.duration. Without that support, we leave duration as an
        # instance property, where appt.duration is calculated for us.
        delta = self.pud_date
        return delta.days * 24 * 60 * 60 + delta.seconds

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
		
		
class Deal(Base):
    """ ."""
    __tablename__ = 'Deal'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)

    title = Column(String(255))
    elevator = Column(Text)
    description = Column(Text)
    links = Column(String(255))
    pub_date = Column(DateTime, nullable=False)

	
    @property
    def duration(self):
        # If the datetime type were supported natively on all database
        # management systems (is not on SQLite), then this could be a
        # hybrid_property, where filtering clauses could compare
        # Appointment.duration. Without that support, we leave duration as an
        # instance property, where appt.duration is calculated for us.
        delta = self.pud_date
        return delta.days * 24 * 60 * 60 + delta.seconds

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


class Unpaid(Base):
    """."""
    __tablename__ = 'Unpaid'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)

    title = Column(String(255))
    company = Column(Text)
    description = Column(Text)
    website = Column(String(255))
    pub_date = Column(DateTime, nullable=False)

	
    @property
    def duration(self):
        # If the datetime type were supported natively on all database
        # management systems (is not on SQLite), then this could be a
        # hybrid_property, where filtering clauses could compare
        # Appointment.duration. Without that support, we leave duration as an
        # instance property, where appt.duration is calculated for us.
        delta = self.pud_date
        return delta.days * 24 * 60 * 60 + delta.seconds

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)



class Paid(Base):
    """."""
    __tablename__ = 'Paid'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)

    title = Column(String(255))
    company = Column(Text)
    description = Column(Text)
    location = Column(String(255))
    website = Column(String(255))
    skills_needed_one = Column(String(255))
    skills_needed_two = Column(String(255))
    skills_needed_three = Column(String(255))
    skills_needed_four = Column(String(255))
    pub_date = Column(DateTime, nullable=False)

	
    @property
    def duration(self):
        # If the datetime type were supported natively on all database
        # management systems (is not on SQLite), then this could be a
        # hybrid_property, where filtering clauses could compare
        # Appointment.duration. Without that support, we leave duration as an
        # instance property, where appt.duration is calculated for us.
        delta = self.pud_date
        return delta.days * 24 * 60 * 60 + delta.seconds

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


class Thesis(Base):
   
    __tablename__ = 'Thesis'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)

    title = Column(String(255))
    research_topic = Column(String(255))
    company = Column(Text)
    description = Column(Text)
    location = Column(String(255))
    website = Column(String(255))
    academic_level = Column(String(255))
    pub_date = Column(DateTime, nullable=False)

	
    @property
    def duration(self):
        # If the datetime type were supported natively on all database
        # management systems (is not on SQLite), then this could be a
        # hybrid_property, where filtering clauses could compare
        # Appointment.duration. Without that support, we leave duration as an
        # instance property, where appt.duration is calculated for us.
        delta = self.pud_date
        return delta.days * 24 * 60 * 60 + delta.seconds

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


class Company(Base):
    """An appointment on the calendar."""
    __tablename__ = 'Company'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)

    company_name = Column(String(255))
    company_location = Column(String(255))
    company_website = Column(String(255))
    industry = Column(String(255))
    company_description = Column(Text)

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)

class Interest(Base):

    __tablename__ = 'Interest'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1, viewonly=True)
    looking_for_title = Column(String(255))
    looking_for = Column(Text)

    joining_startup = Column(Boolean, default=False)
    unpaid_internships = Column(Boolean, default=False)
    paid_internships = Column(Boolean, default=False)
    volunteer_work = Column(Boolean, default=False)
    thesis_work_unpaid = Column(Boolean, default=False)
    thesis_work_paid = Column(Boolean, default=False)
    research_work_unpaid = Column(Boolean, default=False)
    research_work_paid = Column(Boolean, default=False)
    contact_details = Column(Text)
    interest_location = Column(String(255))
    interest_location_two = Column(String(255))
    interest_location_three = Column(String(255))


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
