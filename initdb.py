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
    # models.Event.__table__.drop(engine)
    # models.Team.__table__.drop(engine)
    # models.Contract.__table__.drop(engine)
    # models.Customer.__table__.drop(engine)
    # models.Collaborator.__table__.drop(engine)
    # models.Credentials.__table__.drop(engine)

    # create teams
    teams = ["commercial", "management", "support"]
    for item in teams:
        team = models.Team(name=item)
        write_db(db, team)
 
    # create a commercial
    com1 = models.Collaborator(name="com1",
                                     email="com1@truc.fr",
                                     phone=1092837465,
                                     team_id=1,
                                     )
    write_db(db, com1)
    commercial_password = models.Credentials(
        collaborator_id=com1.id,
        password_hash=argon2.hash("testtest"))
    write_db(db, commercial_password)
    
    # create a manager
    man = models.Collaborator(name="admin",
                                    email="pp",
                                    phone=2,
                                    team_id=2,
                                    )
    write_db(db, man)
    man_password = models.Credentials(
            collaborator_id = man.id,
            password_hash = argon2.hash("testtest"))
    write_db(db, man_password)

    # create an attendee
    attendee = models.Attendee(name="Guest")
    write_db(db, attendee)
    # data = [com1, commercial_password, attendee]


