from authentication import PasswordTools
from tests.conftest import HASH


class TestPasswordTool:
    def test_check_wrong_user(self, seed, session):
        tool = PasswordTools(session)
        user = "WrongUser"
        password = "test"
        reply = tool.check(user, password)
        assert reply == False

    def test_check_right_password(self, seed, session):
        tool = PasswordTools(session)
        user = "Col1"
        password = "test"
        reply = tool.check(user, password)
        assert reply == True

    def test_check_wrong_pwd(self, seed, session):
        tool = PasswordTools(session)
        user = "Col1"
        password = "not_test"
        reply = tool.check(user, password)
        assert reply == False

    def test_get_by_name_should_reply_right_hash(self, seed, session):
        tool = PasswordTools(session)
        result = tool.get_by_name("Col1")
        hash = HASH
        assert result.password_hash == hash