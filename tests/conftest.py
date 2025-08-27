import pytest
from models import Base, Credentials, Collaborator, Customer, Contract, Event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.hash import argon2


DB_URL = "sqlite:///:memory:"
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

cust1 = ("Cust1", "aa", 11, "Cust1CO")
cust2 = ("Cust2", "bb", 22, "Cust2CO")

@pytest.fixture
def session():
    if not engine.url.get_backend_name() == "sqlite":
        raise RuntimeError("Use SQLite backend to run tests\n"
                           "with command :\n"
                           "DB_URL=sqlite:///:memory: pytest -s -v .")

    Base.metadata.create_all(engine)
    try:
        with SessionLocal() as session:
            yield session
    finally:
        Base.metadata.drop_all(engine)


@pytest.fixture
def seed(session):
    session.add_all(
        [
            Customer(name="Cust1", email="aa", phone=11, company="Cust1CO"),
            Customer(name="Cust2", email="bb", phone=22, company="Cust2CO"),
        ]
    )
    session.commit()

    session.add_all(
        [
            Collaborator(name="Col1", email="aa", phone=1, team_id=1),
            Collaborator(name="Col2", email="bb", phone=2, team_id=2),
            Collaborator(name="Col3", email="cc", phone=3, team_id=3),
            Collaborator(name="Col4", email="dd", phone=4, team_id=2),
        ]
    )
    # session.add_all(
    #     [
    #         Collaborator(name="Com", email="a", phone=1, team_id=1),
    #         Collaborator(name="Man", email="b", phone=2, team_id=2),
    #         Collaborator(name="Sup", email="c", phone=3, team_id=3),
    #         Customer(name="Cust1", email="aa", phone=11, company="Cust1CO"),
    #         Customer(name="Cust2", email="bb", phone=22, company="Cust2CO"),
    #     ]
    # )
    # session.commit()
    # session.add_all(
    #     [
    #         Credentials(collaborator_id=1,
    #                     password_hash=argon2.hash("test")),
    #         Credentials(collaborator_id=2,
    #                     password_hash=argon2.hash("test")),
    #         Credentials(collaborator_id=3,
    #                     password_hash=argon2.hash("test")),
    #         Contract(signed=0, amount=200000, customer_id=1, commercial_id=1),
    #     ]
    # )
    # session.commit()
    # session.add_all(
    #     [
    #         Event(name="Event1", customer_contact="Test",
    #               date_start="01.01.01", date_end="02.01.01",
    #               location=".",contract_id=1, customer_id=1),
    #     ]
    # )
    # session.commit()