from helloflask.init_db import Base, db_session
from sqlalchemy import Column, Integer, String, func, ForeignKey, DATE, MetaData, Table, DATETIME
from sqlalchemy.orm import relationship, joinedload

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
    birth = Column(String)
    gender = Column(Integer)
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

    def get_json(self):
        return {'id' : self.id, 'name' : self.name, 'email' : self.email}

class Pat_Usercol(Base):
    __tablename__ = 'Pat_Usercol'
    id = Column(Integer, primary_key = True)
    pat_id = Column(Integer, ForeignKey('Patients.id'))
    usercol_id = Column(Integer, ForeignKey('UsercolMaster.id'))
    pat = relationship('Patient')
    usercol = relationship('UsercolMaster')


    def __init__(self, pat_id, usercol_id):
        self.pat_id = pat_id
        self.usercol_id = usercol_id
    
    def get_json(self):
        return {"id":self.id, "pat_id" : self.pat_id, "usercol_id" : self.usercol_id}

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
    
    def get_json(self):
        return {"id":self.id, "col_name" : self.col_name, "col_desc" : self.col_desc, "col_type" : self.col_type}

class Log(Base):
    __tablename__ = 'Log'
    id = Column(Integer, primary_key = True)
    pat_id = Column(Integer)
    # date = Column(String)
    date = Column(DATETIME)
    usercol_id = Column(Integer)
    value = Column(String)
    # pat_usercol = relationship('Pat_Usercol')

    def __init__(self, pat_id, usercol_id, value):
        self.pat_id = pat_id
        self.usercol_id = usercol_id 
        self.value = value
        self.metadata = MetaData()
    
    def __repr__(self):
        return 'Log %s, %s, %s, %s' % (self.pat_id, self.date, self.usercol_id, self.value)
    
    def get_json(self):
        return {"pat_id" : self.pat_id, "usercol_id" : self.usercol_id, "value" : self.value}


class Discode(Base):
    __tablename__ = 'DisCode'
    id = Column(Integer, primary_key = True)
    code = Column(String) 
    disease = Column(String)
    sci_name = Column(String)


    def __init__(self, code, disease, sci_name):
        self.code = code
        self.disease = disease
        self.sci_name = sci_name

    def __repr__(self):
        return 'Discode %s, %s, %s' % (self.code, self.disease, self.sci_name)
    
    def get_json(self):
        return {"code" : self.code, "disease" : self.disease, "sci_name" : self.sci_name}

class DisCode_Usercol(Base):
    __tablename__ = 'DisCode_Usercol'
    id = Column(Integer, primary_key = True)
    discode_id = Column(Integer)
    usercol_id = Column(Integer)

    def __init__(self, discode_id, usercol_id):
        self.discode_id = discode_id
        self.usercol_id = usercol_id
    
    def __repr__(self):
        return 'DisCode_Usercol %s, %s' % (self.discode_id, self.usercol_id)

    def get_json(self):
        return {"discode_id" : self.discode_id, "usercol_id" : self.usercol_id}