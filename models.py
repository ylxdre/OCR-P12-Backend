from datetime import datetime, date
from sqlalchemy import ForeignKey, String, Integer, DateTime, Boolean, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import (DeclarativeBase, Mapped,
                            mapped_column, relationship)
from typing import Optional


class Base(DeclarativeBase):
    pass


class Collaborator(Base):
    __tablename__ = "collaborator"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(30))
    phone: Mapped[int] = mapped_column(Integer)
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("team.id"))
    team: Mapped["Team"] = relationship(back_populates="collaborator")
    customers: Mapped[Optional[list["Customer"]]] = relationship()
    contracts: Mapped[Optional[list["Contract"]]] = relationship()
    events: Mapped[Optional[list["Event"]]] = relationship()

    def __repr__(self):
        return (f"Collaborator: (id={self.id!r}, "
                f"name={self.name!r}, "
                f"email={self.email!r}, "
                f"phone={self.phone!r}, "
                f"team_id={self.team_id!r}, "
                f"customers={self.customers!r}, "
                f"contracts={self.contracts!r}, "
                f"events={self.events!r})"
                )


class Credentials(Base):
    __tablename__ = "credentials"

    id: Mapped[int] = mapped_column(primary_key=True)
    collaborator_id: Mapped[int] = mapped_column(ForeignKey("collaborator.id"))
    password_hash: Mapped[str] = mapped_column(String(200))


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))
    collaborator: Mapped[list["Collaborator"]] = relationship(
        back_populates="team")


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(20))
    phone: Mapped[int] = mapped_column(Integer)
    company: Mapped[str] = mapped_column(String(40))
    creation_date: Mapped[date] = mapped_column(Date,
                                                server_default=func.now())
    last_update: Mapped[Optional[datetime]] = mapped_column(DateTime)
    commercial_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("collaborator.id"))

    def __repr__(self):
        return (f"Customer: (id={self.id!r}, "
                f"name={self.name!r}, "
                f"email={self.email!r}, "
                f"phone={self.phone!r}, "
                f"company={self.company!r}, "
                f"creation_date={self.creation_date!r}, "
                f"last_update={self.last_update!r}, "
                f"commercial_id={self.commercial_id!r})"
                )


class Contract(Base):
    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(primary_key=True)
    signed: Mapped[bool] = mapped_column(Boolean, default=False)
    creation_date: Mapped[date] = mapped_column(Date,
                                                server_default=func.now())
    amount: Mapped[int] = mapped_column(Integer)
    customer_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("customer.id"))
    commercial_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("collaborator.id"))
    event_id: Mapped[Optional[int]] = mapped_column(ForeignKey("event.id"))

    def __repr__(self):
        return (f"Contract: (id={self.id!r}, "
                f"creation_date={self.creation_date!r}, "
                f"amount={self.amount!r}, "
                f"customer_id={self.customer_id!r}, "
                f"commercial_id={self.commercial_id!r}, "
                f"event_id={self.event_id!r}, "
                f"signed={self.signed!r}, "
                )


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    contract_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("contract.id"))
    customer_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("customer.id"))
    customer_contact: Mapped[str] = mapped_column(String(30))
    date_start: Mapped[str] = mapped_column(String(30))
    date_end: Mapped[Optional[str]] = mapped_column(String(30))
    location: Mapped[Optional[str]] = mapped_column(String(100))
    attendees: Mapped[Optional[set["Attendee"]]] = relationship(
        back_populates="event")
    support_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("collaborator.id"))

    def __repr__(self):
        return (f"Event: (id={self.id!r}, "
                f"name={self.name!r}, "
                f"contract_id={self.contract_id!r}, "
                f"customer_id={self.customer_id!r}, "
                f"customer_contact={self.customer_contact!r}, "
                f"support_id={self.support_id!r}, "
                f"date_start={self.date_start!r}, "
                f"date_end={self.date_end!r}, "
                f"location={self.location!r}, "
                f"attendees={self.attendees!r}"
                )


class Attendee(Base):
    __tablename__ = "attendee"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    event_id: Mapped[Optional[int]] = mapped_column(ForeignKey("event.id"))
    event: Mapped[Optional[set["Event"]]] = relationship(
        back_populates="attendees")
