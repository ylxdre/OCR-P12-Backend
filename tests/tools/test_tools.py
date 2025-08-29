import pytest
from sqlalchemy.util import monkeypatch_proxied_specials

from models import Customer
from tools import CustomerTools, CollaboratorTools


class TestCustomerTools:

    def test_db_should_be_populated(self, seed, session):
        test = session.query(Customer).all()
        assert test != None

    def test_list_should_return_all_customers(self, seed, session):
        tools = CustomerTools(session)
        users = tools.list()
        assert len(users) == 2

    # def test_should_create_customer(self, seed, session, monkeypatch):
    #     CustomerTools(session).create(1)
    #     pass

    def test_delete_user_should_remove_from_db(self, seed, session):
        pass


class TestCollaboratorTools:

    def test_should_reply_id_by_name(self, seed, session):
        tool = CollaboratorTools(session)
        reply = tool.get_id_by_name("Col1")
        assert reply == 1

    def test_should_reply_id_by_team_id(self, seed, session):
        tool = CollaboratorTools(session)
        reply = tool.get_by_team_id(1)
        assert len(reply) == 1
        reply = tool.get_by_team_id(2)
        assert len(reply) == 2

    def test_should_reply_team_id_by_name(self, seed, session):
        tool = CollaboratorTools(session)
        reply = tool.get_team_by_name("Col1")
        reply2 = tool.get_team_by_name("Col2")
        assert reply == 1
        assert reply2 == 2

    def test_should_reply_list(self, seed, session):
        tool = CollaboratorTools(session)
        reply = tool.list()
        len(reply) == 4
