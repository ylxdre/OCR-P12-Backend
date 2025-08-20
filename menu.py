from simple_term_menu import TerminalMenu
from models import Customer, Contract, Collaborator, Event


class Prompt:

    def menu(self, options):
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        selection = options[menu_entry_index]
        return selection

    def exec_menu(self, dict_options):
        selection = self.menu(list(dict_options.keys()))
        selected_function = dict_options.get(selection)
        selected_function()

    def return_menu(self, dict_options):
        selection = self.menu(list(dict_options.keys()))
        return dict_options.get(selection)



class CommercialMenu:
    """
    Main menu for commercial users displaying only specific submenus according
    to permissions :
        customers:  CRUD
        contracts:  RU
        events:     CR
    filter :
        contract: signed
    """
    def __init__(self, customer_tools, contract_tools, event_tools, tools):
        self.customer_tools = customer_tools
        self.contract_tools = contract_tools
        self.event_tools = event_tools
        self.tools = tools
        self.prompt = Prompt()

    def launch(self):
        """
        Menu entry point for commercial user; display objects then submenu
        :return: call submenus
        """
        base = {
            "Customer": self.customer_menu,
            "Contract": self.contract_menu,
            "Event": self.event_menu,
            "Quit": quit,
        }
        while True:
            self.prompt.exec_menu(base)

    def customers_for_update(self):
        """
        get all customers from db, create a dict options, call menu
        and get choice (Customer.id)
        :return: exec the update tool with the chosen id
        """
        options = {}
        for item in self.tools.list(Customer):
            options[item[0].name] = item[0].id
        choice = self.prompt.return_menu(options)
        self.customer_tools.update(choice)

    def customer_menu(self):
        """
        display the CRUD menu for customer and get choice
        :return: exec the function associated with chosen item
        """
        customer_options = {
            "List": self.customer_tools.list,
            "Create": self.customer_tools.create,
            "Update": self.customers_for_update,
            "Delete": self.customer_tools.delete,
        }
        self.prompt.exec_menu(customer_options)

    def contracts_for_update(self):
        """
        get all contracts from db, create a dict options, call menu
        and get choice (Contract.id)
        :return: exec the update tool with the chosen id
        """
        options = {}
        for item in self.tools.list(Contract):
            options["Contrat "+str(item[0].id)] = item[0].id
        choice = self.prompt.return_menu(options)
        self.contract_tools.update(choice)

    def contract_menu(self):
        """
        display the CRUD menu for contracts and get choice
        :return: exec the function associated with chosen item
        """
        contract_options = {
            "List": self.contract_list,
            "Update": self.contracts_for_update,
        }
        self.prompt.exec_menu(contract_options)

    def contract_list(self):
        """
        interface after CRUD menu : list meant to provide filter
        here on signed attribute
        :return: exec tool method which apply filter and call view to display
        """
        contract_list_options = {
            "Signed": self.contract_tools.signed,
            "Not signed": self.contract_tools.not_signed,
        }
        self.prompt.exec_menu(contract_list_options)

    def event_menu(self):
        """
        display the CRUD menu for event and get choice
        :return: exec the function associated with chosen item
        """
        event_options = {
            "List": self.event_tools.list,
            "Create": self.event_tools.create,
        }
        self.prompt.exec_menu(event_options)


class ManagementMenu:
    """
    Main menu for manager users displaying only specific submenus according
    to permissions :
        collaborators:  CRUD
        customers:      R
        contracts:      CRU
        events:         RU
    filter:
        event:  support_id
    """
    def __init__(self, collaborator_tools,
                 customer_tools,
                 contract_tools,
                 event_tools, tools):
        self.collaborator_tools = collaborator_tools
        self.customer_tools = customer_tools
        self.contract_tools = contract_tools
        self.event_tools = event_tools
        self.tools = tools
        self.prompt = Prompt()

    def launch(self):
        """
        Menu entry point for management user; display objects then submenu
        :return: call submenus
        """
        base = {
            "Collaborator": self.collaborator_menu,
            "Customer": self.customer_menu,
            "Contract": self.contract_menu,
            "Event": self.event_menu,
            "Quit": quit,
        }
        while True:
            self.prompt.exec_menu(base)

    def choose_collaborator(self):
        """
        gets all collaborators from db, creates a dict options, calls menu
        and returns choice (Collaborator.id)
        :return: chosen Collaborator.id:int
        """
        options = {}
        for item in self.tools.list(Collaborator):
            options[item[0].name] = item[0].id
        return self.prompt.return_menu(options)

    def collaborator_update(self):
        """
        exec choose_collaborator and call tool update with chosen id
        """
        choice = self.choose_collaborator()
        self.collaborator_tools.update(choice)

    def collaborator_delete(self):
        """
        exec choose_collaborator and call tool delete with chosen id
        """
        choice = self.choose_collaborator()
        self.collaborator_tools.delete(choice)

    def collaborator_menu(self):
        """
        display the CRUD menu for collaborator and get choice
        :return: exec the function associated with chosen item
        """
        collaborator_options = {
            "List": self.collaborator_tools.list,
            "Create": self.collaborator_tools.create,
            "Update": self.collaborator_update,
            "Delete": self.collaborator_delete,
        }
        self.prompt.exec_menu(collaborator_options)

    def customer_menu(self):
        """
        display the CRUD menu for customer and get choice
        :return: exec the function associated with chosen item
        """
        customer_options = {"List": self.customer_tools.list}
        self.prompt.exec_menu(customer_options)

    def contracts_for_update(self):
        (options,
         customer_options,
         commercial_options,
         event_options) = {},{},{},{}
        commercial = self.collaborator_tools.get_by_team_id(1)
        for customer in self.tools.list(Customer):
            customer_options[customer[0].name] = customer[0].id
        for user in commercial:
            commercial_options[user[0].name] = user[0].id
        for event in self.tools.list(Event):
            event_options[event[0].name] = event[0].id
        for item in self.tools.list(Contract):
            options["Contrat "+str(item[0].id)] = item[0].id
        choice = self.prompt.return_menu(options)
        self.contract_tools.update(choice, customer_options,
                                   commercial_options, event_options)

    def contract_menu(self):
        """
        display the CRUD menu for contract and get choice
        :return: exec the function associated with chosen item
        """
        contract_options = {"List": self.contract_tools.list,
                            "Create": self.contract_tools.create,
                            "Update": self.contracts_for_update,
                            }
        self.prompt.exec_menu(contract_options)

    def event_for_update(self):
        """
        get all events from db, create a dict options, call menu
        and get choice (Event.id)
        also gets all support collaborators and creates dict option given
        to tool update method
        :return: exec the update tool with the chosen id
        """
        options = {}
        support_options = {}
        support = self.collaborator_tools.get_by_team_id(3)
        for user in support:
            support_options[user[0].name] = user[0].id
        for item in self.tools.list(Event):
            options[item[0].name] = item[0].id
        choice = self.prompt.return_menu(options)
        self.event_tools.update(choice, support_options)

    def event_list(self):
        event_list_options = {
            "All": self.event_tools.list,
            "No Support yet": self.event_no_support,
        }
        self.prompt.exec_menu(event_list_options)

    def event_no_support(self):
        self.event_tools.filter("support_id", "NULL")

    def event_menu(self):
        event_options = {"List": self.event_list,
                         "Update": self.event_for_update,
                         }
        self.prompt.exec_menu(event_options)


class SupportMenu:
    """
    Main menu for support users displaying only specific submenus according
    to permissions :
        customers:      R
        contracts:      R
        events:         CRU
    filter:
        event:  owned
    """
    def __init__(self,
                 customer_tools,
                 contract_tools,
                 event_tools,
                 tools,
                 user_id):
        self.customer_tools = customer_tools
        self.contract_tools = contract_tools
        self.event_tools = event_tools
        self.tools = tools
        self.user_id = user_id
        self.prompt = Prompt()

    def launch(self):

        base = {
            "Customer": self.customer_menu,
            "Contract": self.contract_menu,
            "Event": self.event_menu,
            "Quit": quit,
        }
        while True:
            self.prompt.exec_menu(base)

    def customer_menu(self):
        customer_options = {"List": self.customer_tools.list}
        self.prompt.exec_menu(customer_options)

    def contract_menu(self):
        contract_options = {"List": self.contract_tools.list,
                            }
        self.prompt.exec_menu(contract_options)

    def event_menu(self):
        event_options = {"List": self.event_list,
                         "Create": self.event_tools.create,
                         "Update": self.event_for_update,
                         }
        self.prompt.exec_menu(event_options)

    def event_list(self):
        event_list_options = {
            "All": self.event_tools.list,
            "Owned only": self.event_owned,
        }
        self.prompt.exec_menu(event_list_options)

    def event_owned(self):
        self.event_tools.filter_owned(self.user_id)

    def event_for_update(self):
        options = {}
        for item in self.tools.list(Event):
            options[item[0].name] = item[0].id
        choice = self.prompt.return_menu(options)
        self.event_tools.update(choice)


def menu(options):
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    selection = options[menu_entry_index]
    return selection


def return_menu(dict_options):
    selection = menu(list(dict_options.keys()))
    return dict_options.get(selection)
