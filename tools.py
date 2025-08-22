from menu import return_menu
from models import Collaborator, Customer, Contract, Event, Credentials
from authentication import PasswordTools
from views import View
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert, delete


class Tools:
    """
    Generic tools with object as an arg
    """
    def __init__(self, db: Session):
        self.db = db
        self.view = View()

    def list(self, object):
        """
        Select all objects from DB and return the list
        :param object: object in Collaborator, Customer, Contract, Event
        :return: list of object
        """
        while self.db:
            return self.db.execute(select(object)).all()

    def filter(self, object, filter):
        """
        Select objects from DB where filter and return the list
        :param object: object in Collaborator, Customer, Contract, Event
        :param filter: (attribute, value):tuple
        :return: list of selected object matching filter
        """
        item, value = filter
        stmt = (select(object).where(**{item: value}))
        while self.db:
            result = self.db.execute(
                select(object).where(**{item: value})).all()
            if not result:
                self.view.display_error()
            self.view.display_results(result)


class CollaboratorTools:
    """
    Interface to manage Collaborator object in DB
    """
    def __init__(self, db: Session):
        self.db = db
        self.view = View()
        self.pw_tools = PasswordTools(self.db)

    def get_id_by_name(self, username):
        collaborator = self.db.execute(
            select(Collaborator).where(Collaborator.name == username)).scalar()
        if not collaborator:
            return None
        return collaborator.id

    def get_by_team_id(self, team_id):
        collaborator = self.db.execute(
            select(Collaborator).where(Collaborator.team_id == team_id)).all()
        return collaborator

    def list(self):
        result = self.db.execute(select(Collaborator)).all()
        self.view.display_results(result)

    def create(self) -> None:
        """
        Create a new collaborator with minimum information
        :return: None; creates object in DB
        """
        pwd_tools = PasswordTools(self.db)
        collaborator = self.view.prompt_for_collaborator()
        print(collaborator)
        new_collab = Collaborator(
                                name=collaborator['name'],
                                email=collaborator['email'],
                                phone=collaborator['phone'],
                                team_id=collaborator['team_id']
                                )
        self.db.add(new_collab)
        self.db.commit()
        new_collab_pwd = Credentials(collaborator_id=new_collab.id,
                                     password_hash=pwd_tools.hash("123456"))
        self.db.add(new_collab_pwd)
        self.db.commit()
        self.view.display_confirm("collaborator", new_collab.id)

    def update(self, my_id) -> None:
        """
        Update a collaborator; asks for field to change and value
        :param my_id: id of the collaborator to modify
        :return: None; Update entry in DB
        """
        pwd_tools = PasswordTools(self.db)
        collab = self.db.get(Collaborator, my_id)
        item, value = self.view.prompt_for_collaborator_update()
        stmt = (update(Collaborator).where(Collaborator.id == my_id).values(
            **{item: value}))
        if item == 'password':
            if not self.db.execute(select(Credentials).where(
                    Credentials.collaborator_id == my_id)).all():
                stmt = (insert(Credentials).values(
                    collaborator_id=my_id,
                    password_hash=pwd_tools.hash(value)))
            else:
                stmt = (update(Credentials).where(
                    Credentials.collaborator_id == my_id).values(
                    password_hash=pwd_tools.hash(value)))
        self.db.execute(stmt)
        self.db.commit()
        self.view.display_change(collab.name, item, value)

    def delete(self, my_id) -> None:
        """
        Delete a collaborator
        :param my_id: id of the collaborator to delete
        :return: None; deletes entry in DB
        """
        stmt = delete(Collaborator).where(Collaborator.id == my_id)
        self.db.execute(stmt)
        self.db.commit()

    def get_team_by_name(self, username: str) -> int | None:
        """
        Check if username exists, returns team_id to check permission further
        :param username: string, Collaborator.username
        :return: None|team_id:int
        """
        ret = self.db.execute(
            select(Collaborator).where(Collaborator.name == username)).scalar()
        if ret is None:
            self.view.display_error()
            return ret
        else:
            return ret.team_id

    def list_by_team_id(self, my_id):
        pass

    def list_by_contract_id(self, my_id):
        pass

    def list_by_event_id(self, my_id):
        pass


class CustomerTools:
    """
    Interface to manage Customer object in DB
    """
    def __init__(self, db: Session):
        self.db = db
        self.view = View()

    def list(self):
        result = self.db.execute(select(Customer)).all()
        self.view.display_results(result)
        return result

    def create(self) -> None:
        """
        Create a new customer with minimum information
        :return: None; creates object in DB
        """
        customer = self.view.prompt_for_customer()
        new_customer = Customer(
                                name=customer['name'],
                                email=customer['email'],
                                phone=customer['phone'],
                                company=customer['company'],
                                )
        self.db.add(new_customer)
        self.db.commit()
        self.view.display_confirm("customer", new_customer.id)

    def update(self, my_id):
        """
        Update a customer; asks for field to change and value
        :param my_id: id of the collaborator to modify
        :return: None; Update entry in DB
        """
        cust = self.db.get(Customer, my_id)
        item, value = self.view.prompt_for_customer_update()
        stmt = (update(Customer).where(Customer.id == my_id).values(
            **{item: value}))
        self.db.execute(stmt)
        self.db.commit()
        self.view.display_change(cust.name, item, value)


    def delete(self, my_id) -> None:
        """
        Delete a customer
        :param my_id: id of the customer to delete
        :return: None; deletes entry in DB
        """
        stmt = delete(Customer).where(Customer.id == my_id)
        self.db.execute(stmt)
        self.db.commit()

    def get_by_commercial_id(self, my_id):
        """
        Check if commercial exists, then returns a list
        :param my_id: a commercial id
        :return: a list of Customer
        """
        if self.db.get(Collaborator, my_id):
            ret = self.db.execute(
                select(Customer).where(Customer.commercial_id == my_id)).all()
            if ret is None:
                # print({'message': "No customer found"})
                self.view.display_error()
            return ret
        else:
            # print({'message': "No commercial with this id"})
            self.view.display_error()
            return None


class ContractTools:
    """
    Interface to manage Contract object in DB
    """
    def __init__(self, db: Session):
        self.db = db
        self.view = View()

    def list(self):
        """
        List all contracts from DB
        :return: a list of Contract objects
        """
        result = self.db.execute(select(Contract)).all()
        self.view.display_results(result)

    def signed(self):
        """
        List only Contract where signed is True (or 1)
        :return: a list of Contract objects
        """
        result = self.db.execute(
            select(Contract).where(Contract.signed == 1))
        self.view.display_results(result)

    def not_signed(self):
        """
        List only Contract where signed is False (or 0)
        :return: a list of Contract objects
        """
        result = self.db.execute(
            select(Contract).where(Contract.signed == 0))
        self.view.display_results(result)

    def create(self) -> None:
        """
        Create a new contracts with minimum information
        :return: None; creates object in DB
        """
        contract = self.view.prompt_for_contract()
        new_contract = Contract(
            customer=contract['customer'],
            commercial=contract['commercial'],
            amount=contract['amount'],
        )
        self.db.add(new_contract)
        self.db.commit()
        self.view.display_confirm("contract", new_contract.id)

    def update(self, my_id,
               customer_options,
               commercial_options,
               event_options):
        """
        Update a contract; asks for field to change and value
        :param my_id: id of the contract to modify
        :return: None; Update entry in DB
        """
        item, value = self.view.prompt_for_contract_update()
        if item == 'signed':
            if value.lower() == "yes":
                value = 1
            else:
                value = 0
            # stmt = (update(Contract).where(Contract.id == my_id).values(
            #     signed=is_signed))
        if item == 'customer_id':
            value = return_menu(customer_options)
        if item == 'commercial_id':
            value = return_menu(commercial_options)
        if item == 'event_id':
            value = return_menu(event_options)
        stmt = (update(Contract).where(Contract.id == my_id).values(
            **{item: value}))
        self.db.execute(stmt)
        self.db.commit()
        self.view.display_change("Contract"+str(my_id), item, value)

    def delete(self, my_id) -> None:
        """
        Delete a contract
        :param my_id: id of the contract to delete
        :return: None; deletes entry in DB
        """
        stmt = delete(Contract).where(Contract.id == my_id)
        self.db.execute(stmt)
        self.db.commit()


class EventTools:
    """
    Interface to manage Event object in DB
    """
    def __init__(self, db: Session):
        self.db = db
        self.view = View()

    def list(self):
        """
        List all events from DB
        :return: list of Event objects
        """
        result = self.db.execute(select(Event)).all()
        self.view.display_results(result)

    def filter(self, field, value):
        """
        Retrieve only event with specified field
        :param field: Event.field
        :return: display a list of Event
        """
        result = self.db.execute(
            select(Event).filter_by(**{field: value})).all()
        if not result:
            self.view.display_error()
        else:
            self.view.display_results(result)

    def filter_owned(self, user_id):
        """
        List only events where support_id is the id of the user logged in
        :param user_id: the connected user id
        :return: list of Event objects
        """
        result = self.db.execute(
            select(Event).where(Event.support_id == user_id)).all()
        if not result:
            self.view.display_error()
            return None
        self.view.display_results(result)
        return result

    def create(self) -> None:
        """
        Create a new event with minimum information
        :return: None; creates object in DB
        """
        event = self.view.prompt_for_event()
        new_event = Event(
            name=event['name'],
            contract_id=event['contract_id'],
            customer_id=event['customer_id'],
            customer_contact=event['customer_contact'],
            date_start=event['date_start'],
            date_end=event['date_end'],
            location=event['location'],
        )
        self.db.add(new_event)
        self.db.commit()
        self.view.display_confirm("event", new_event.id)

    def update(self, my_id, support_options):
        """
        Update an event in DB; asks for field to change and value
        :param my_id: id of the event to modify
        :return: None; Update entry in DB
        """
        event = self.db.get(Event, my_id)
        item, value = self.view.prompt_for_event_update(support_options)
        if item == 'support_id':
            value = return_menu(support_options)
        stmt = (update(Event).where(Event.id == my_id).values(
            **{item: value}))
        self.db.execute(stmt)
        self.db.commit()
        self.view.display_change(event.name, item, value)

    def delete(self, my_id) -> None:
        """
        Delete an event
        :param my_id: id of the event to delete
        :return: None; deletes entry in DB
        """
        stmt = delete(Event).where(Event.id == my_id)
        self.db.execute(stmt)
        self.db.commit()
