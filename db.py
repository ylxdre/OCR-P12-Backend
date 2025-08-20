from sqlalchemy import create_engine
from config import user1, pass1
from sqlalchemy.orm import sessionmaker


DB_URL = "mysql+mysqlconnector://"+user1+":"+pass1+"@localhost:3306/prout"


engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
