from sqlalchemy import create_engine
from config import USER, PASSWORD
from sqlalchemy.orm import sessionmaker


DB = "epicevents"
DB_URL = "mysql+mysqlconnector://"+USER+":"+PASSWORD+"@localhost:3306/"+DB


engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
