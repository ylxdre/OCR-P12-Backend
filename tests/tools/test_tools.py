import pytest
from sqlalchemy.util import monkeypatch_proxied_specials

from models import Customer
from tools import CustomerTools, CollaboratorTools

class TestCustomerTools:

    def test_db_should_be_populated(self, seed, session):
        test = session.query(Customer).all()
        # print(test)

    def test_list_should_return_all_customers(self, seed, session):
        tools = CustomerTools(session)
        users = tools.list()
        assert len(users) == 2

    def test_should_create_customer(self, seed, session, monkeypatch):
        CustomerTools(session).create(1)
        pass

    def test_delete_user_should_remove_from_db(self, seed, session):
        pass


class TestCollaboratorTools:

    def test_should_reply_id_by_name(self, seed, session):
        tool = CollaboratorTools(session)
        reply = tool.get_id_by_name("Col1")
        assert reply == 1

    def test_should_reply_id_by_team_id(self, seed, session):
        pass

class TestPasswordTools:

    def test_should_retrieve_hashed_password_by_username(self, seed, session):
        pass

    def test_right_user_could_connect(self, seed, session):
        pass

    def test_wrong_password_should_fail(self, seed, session):
        pass

    def test_unknown_user_should_fail(self, seed, session):
        pass
