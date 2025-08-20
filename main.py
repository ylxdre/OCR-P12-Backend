import models
import tools
from db import engine, session
from controllers import App
from views import View
from authentication import PasswordTools


models.Base.metadata.create_all(bind=engine)


def main():
    view = View()
    collaborator_tools = tools.CollaboratorTools(session)
    customer_tools = tools.CustomerTools(session)
    contract_tools = tools.ContractTools(session)
    event_tools = tools.EventTools(session)
    passwd_tools = PasswordTools(session)
    common_tools = tools.Tools(session)
    with session:
        App(session,
            view,
            collaborator_tools,
            customer_tools,
            contract_tools,
            event_tools,
            passwd_tools,
            common_tools).start()


if __name__ == "__main__":
    main()
