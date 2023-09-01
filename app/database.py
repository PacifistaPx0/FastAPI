from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database>"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:thinkthank2016@localhost/fastapi"

#The engine is responsible for establishing connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

#Session responsible for talking to database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Dependency. Session responsible for talking with database. 
#function allows us get a session and close it after requests
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()