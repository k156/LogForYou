from helloflask.templates.init_db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Doctor(Base):
    __tablename__ = 'Doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    departmentId = Column(Integer)
    # department = relationship('Departments')
    
    def __init__(self, email=None, passwd=None, name='의사', makeSha=False):
        self.email = email
        if makeSha:
            self.passwd = func.sha2(passwd, 256)
        else:
            self.passwd = passwd
        self.name = name

    def __repr__(self):
        return 'User %s, %r, %r' % (self.id, self.email, self.name)

class Patient(Base):
    __tablename__ = 'Patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    # doc_pat = relationship('Doc_Pat')
    
    ## log, col-patients relationship 필요.
    
    def __init__(self, email=None, passwd=None, name='환자', makeSha=False):
        self.email = email
        if makeSha:
            self.password = func.sha2(passwd, 256)
        else:
            self.password = passwd
        self.name = name

    def __repr__(self):
        return 'User %s, %r, %r' % (self.id, self.email, self.name)