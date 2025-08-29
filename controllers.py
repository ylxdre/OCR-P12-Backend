from menu import CommercialMenu, ManagementMenu, SupportMenu
from sqlalchemy.orm import Session


class App:
    """
    Entry point of the application. Instantiate Tools which are meant to be
    like kind of repository pattern to interact with data, and Menus then route
    depending on team... sort of permission management using simple_term_menu
    """
    def __init__(self,
                 db: Session,
                 view,
                 collaborator_tools,
                 customer_tools,
                 contract_tools,
                 event_tools,
                 passwd_tools,
                 tools):
        self.db = db
        self.view = view
        self.passwd_tools = passwd_tools
        self.collaborator_tools = collaborator_tools
        self.customer_tools = customer_tools
        self.contract_tools = contract_tools
        self.event_tools = event_tools
        self.tools = tools

    def connect(self) -> tuple | None:
        """
        Check if provided password exists in table credentials and verify
        if matches with stored hash
        :return: tuple(team_id:int, user_id:int) | None and print if no match
        """
        username, password = self.view.prompt_connect()
        if not self.collaborator_tools.get_id_by_name(username):
            self.view.display_no_user()
            quit()
        else:
            if self.passwd_tools.check(username, password):
                perm = self.collaborator_tools.get_team_by_name(username)
                user_id = self.collaborator_tools.get_id_by_name(username)
                return perm, user_id
            else:
                self.view.display_co_failed()
                quit()

    def start(self):
        team, user_id = self.connect()
        if team == 1:
            CommercialMenu(self.customer_tools,
                           self.contract_tools,
                           self.event_tools,
                           self.tools,
                           user_id).launch()

        if team == 2:
            ManagementMenu(self.collaborator_tools,
                           self.customer_tools,
                           self.contract_tools,
                           self.event_tools,
                           self.tools,
                           user_id).launch()

        if team == 3:
            SupportMenu(self.customer_tools,
                        self.contract_tools,
                        self.event_tools,
                        self.tools,
                        user_id).launch()
