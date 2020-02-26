import datetime
from sqlalchemy import (Column, VARCHAR, INTEGER, TEXT, 
                        create_engine, ForeignKey)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash


engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(20), unique=True, nullable=False)
    password = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(30), unique=True, nullable=False)
    created_on = Column(TEXT, default=datetime.date.today().isoformat())

    user_tasks = relationship('Task', cascade="all, delete-orphan")

    def __str__(self):
        return f'''id: {self.id}
        name: {self.name}
        password: {self.password}
        email: {self.email}
        created_on: {self.created_on}
        '''

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(VARCHAR(20), nullable=False)
    content = Column(TEXT)
    created_on = Column(TEXT, default=datetime.date.today().isoformat())
    deadline_on = Column(TEXT)

    author = relationship('User')

    def __str__(self):
        return f'''id: {self.id}
        user_id: {self.user_id}
        title: {self.title}
        content: {self.content}
        created_on: {self.created_on}
        deadline_on: {self.deadline_on}
        '''

Base.metadata.create_all(bind=engine)


def add_user(username, email, password):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    password = generate_password_hash(password)
    session.add(User(name=username, password=password, email=email))
    session.commit()
    session.close()

def login_user(email, password):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)

    user = session.query(User).filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session.close()
        return user
    return False

def get_user_id(name):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user_id = session.query(User).filter_by(name=name).first().id
    session.close()
    return user_id


def add_task(user_id, title, content, deadline_on):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    session.add(Task(user_id=user_id, 
                    title=title, 
                    content=content, 
                    deadline_on=deadline_on))
    session.commit()
    session.close()


def get_user_tasks(user_id):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user_tasks = session.query(Task).filter_by(user_id=user_id).all()
    session.close()
    return user_tasks

def delete_task(username, task_id):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(name=username).first()
    user_tasks = user.user_tasks
    task_to_delete = user_tasks[int(task_id)-1].title
    del user_tasks[int(task_id)-1]
    session.commit()
    session.close()
    return task_to_delete