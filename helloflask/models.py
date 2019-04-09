from helloflask.init_db import Base
from sqlalchemy import Column, Integer, String, func, ForeignKey
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
    pat_usercol = relationship('Pat_Usercol')

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

class Pat_Usercol(Base):
    __tablename__ = 'Pat_Usercol'
    id = Column(Integer, primary_key = True)
    pat_id = Column(Integer, ForeignKey('Patients.id'))
    usercol_id = Column(Integer, ForeignKey('UsercolMaster.id'))
    pat = relationship('Patient')
    usercol = relationship('UsercolMaster')

    # def __repr__(self):
    #     return 'Pat_Usercol %s, %s' % (self.pat, self.usercol)

class UsercolMaster(Base):
    __tablename__ = 'UsercolMaster'
    id = Column(Integer, primary_key = True)
    col_name = Column(String)
    min = Column(Integer)
    max = Column(Integer)
    col_desc = Column(String)
    dept_id = Column(Integer)
    col_type = Column(Integer)
    pat_usercol = relationship('Pat_Usercol')

    def __repr__(self):
        return 'Column %s, %s, %s, %s' % (self.id, self.col_name, self.col_desc, self.col_type)