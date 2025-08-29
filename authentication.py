from typing import Any

from passlib.hash import argon2
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Collaborator, Credentials
import jwt


class PasswordTools:
    """
    Tool used to manage passwords and interact with DB
    """
    def __init__(self, db: Session):
        self.db = db

    def hash(self, password: str) -> str:
        """

        :param password:
        :return:
        """
        return argon2.hash(password)

    def get_by_name(self, username: str) -> dict[str, str] | None | Any:
        """
        Get the collaborator's name and return password hash associated if
        existing
        :param username: Collaborators.name
        :return: Credential.password_hash
        """
        if self.db.execute(
                select(Collaborator).filter_by(name=username)).scalar():
            sbq = select(Collaborator).where(
                Collaborator.name == username).subquery()
            stmt = select(Credentials).join(
                sbq,
                Credentials.collaborator_id == sbq.c.id)
            return self.db.execute(stmt).scalar()
        return {'message': "Wrong username"}

    def check(self, username: str, password: str) -> bool:
        user = self.get_by_name(username)
        if type(user) == dict:
            return False
        else:
            user_pw = user.password_hash
            return argon2.verify(password, user_pw)


class TokenTools:
    def __init__(self, username: str, password: str, team_id: int):
        self.username = username
        self.password = password
        self.team_id = team_id

    def get_token(self, username: str, password: str, team_id: int):
        # team_id = Collaborator.get_team_by_name(self.username)
        payload = {'user': username,
                   'password': password,
                   'team_id': team_id,
                   }
        return jwt.encode(payload, password, algorithm="HS256")

    def check_token(self):
        pass

    def store_token(self, token):
        pass


class AuthTools:
    def __init__(self, db: Session):
        self.db = db
