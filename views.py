from getpass import getpass
from menu import return_menu


class View:
    def __init__(self):
        pass

    def prompt_connect(self):
        print("Please connect")
        collaborator = input("Username : ")
        password = getpass("Password : ")
        return collaborator, password

    def prompt_for_id(self):
        id = input("What id ? ")
        return id

    def prompt_for_update(self, options):
        print("What do you want to update ?")
        ids = ("support_id", "commercial_id", "customer_id", "event_id")
        item = return_menu(options)
        if item == 'password':
            data = getpass("New password : ")
        elif item == 'team_id':
            data = self.prompt_for_collaborator_team()
        elif item in ids:
            data = ""
        else:
            data = input(f"New {item}'s value : ")
        return item, data


    def prompt_for_collaborator_team(self):
        options = {"Commercial": 1,
                   "Management": 2,
                   "Support": 3,
                   }
        return return_menu(options)

    def prompt_for_collaborator(self):
        collaborator = {}
        options = {"Commercial": 1,
                   "Management": 2,
                   "Support": 3,
                   }
        print("Please enter collaborator's information")
        collaborator['name'] = input("Name ? : ")
        collaborator['email'] = input("Email ? : ")
        collaborator['phone'] = input("Phone ? : ")
        item = return_menu(options)
        collaborator['team_id'] = item
        return collaborator

    def prompt_for_collaborator_update(self) -> tuple:
        options = {"password": "password",
                   "name": "name",
                   "email": "email",
                   "phone": "phone",
                   "team": "team_id",
                   }
        return self.prompt_for_update(options)

    def prompt_for_customer(self) -> dict:
        customer = {}
        print("** New customer **")
        customer['name'] = input("Name ? : ")
        customer['email'] = input("Email ? : ")
        customer['phone'] = input("Phone ? : ")
        customer['company'] = input("Company name ? : ")
        return customer

    def prompt_for_customer_update(self) -> tuple:
        options = {"name": "name",
                   "email": "email",
                   "phone": "phone",
                   "company": "company",
                   }
        return self.prompt_for_update(options)

    def prompt_for_contract(self) -> dict:
        contract = {}
        print("** New contract **")
        contract['customer'] = input("Customer (id) ? : ")
        contract['commercial'] = input("Commercial (id) ")
        contract['amount'] = input("Budget ? : ")
        return contract

    def prompt_for_contract_update(self) -> tuple:
        options = {"customer": "customer_id",
                   "commercial": "commercial_id",
                   "event": "event_id",
                   "amount": "amount",
                   "signed": "signed",
                   }
        return self.prompt_for_update(options)

    def prompt_for_event(self) -> dict:
        event = {}
        print("** New Event **")
        event['name'] = input("Event's name ? : ")
        event['contract_id'] = input("Contract (id) ? : ")
        event['customer_id'] = input("Customer (id) ? : ")
        event['customer_contact'] = input("Customer's contact ? : ")
        event['date_start'] = input("Start date ? : ")
        event['date_end'] = input("End date ? : ")
        event['location'] = input("Location ? : ")
        # event['attendee'] = input("Attendees ? : ")
        return event

    def prompt_for_event_update(self, support_options) -> tuple:
        options = {"name": "name",
                   "contract": "contract_id",
                   "customer": "customer_id",
                   "date_start": "date_start",
                   "date_end": "date_end",
                   "location": "location",
                   "Support Member": "support_id"
                   }
        return self.prompt_for_update(options)

    def display_quit(self):
        print("Bye")

    def display_confirm(self, object, id):
        print(f"New {object} with id:{id} created !")

    def display_change(self, object, item, value):
        print(f"{item} for {object} updated, set to {value} !")

    def display_results(self, result):
        for item in result:
            print(item)

    def display_error(self):
        print("No object matches this query")

    def display_items(self):
        print()
