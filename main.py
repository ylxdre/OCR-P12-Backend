import models
import tools
from db import engine, session
from controllers import App
from views import View
from authentication import PasswordTools
from initdb import init_test_db

import sentry_sdk
import config



def main():
    sentry_sdk.init(
        dsn=config.sentry_url,
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
    )

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
    models.Base.metadata.create_all(bind=engine)
    init_test_db(session)
    main()
