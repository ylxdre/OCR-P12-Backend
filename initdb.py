from types import resolve_bases

import models
from db import engine
from sqlalchemy import MetaData

from passlib.hash import argon2


def write_db(db, model):
    db.add(model)
    db.commit()

def clean_db():
    models.Base.metadata.drop_all(bind=engine)


def init_test_db(db):
    # clean up everything before starting
    # models.Attendee.__table__.drop(engine)

    teams = ["commercial", "management", "support"]
    for item in teams:
        team = models.Team(name=item)
        write_db(db, team)
    
    # create a manager
    man = models.Collaborator(name="admin",
                                    email="a",
                                    phone=1,
                                    team_id=2,
                                    )
    write_db(db, man)
    man_password = models.Credentials(
            collaborator_id = man.id,
            password_hash = argon2.hash("password"))
    write_db(db, man_password)

    # create an attendee
    attendee = models.Attendee(name="Guest")
    write_db(db, attendee)
    # data = [com1, commercial_password, attendee]


