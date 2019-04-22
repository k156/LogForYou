from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from keys import mysql_url

# Declare connection
mysql = mysql_url
engine = create_engine(mysql, echo=True, convert_unicode=True)

# Declare & create Session
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine) )

# Create SqlAlchemy Base Instance
Base = declarative_base()
Base.query = db_session.query_property()


def init_database():
    Base.metadata.create_all(bind=engine)