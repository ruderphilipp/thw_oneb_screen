#!/usr/bin/python3

import logging
import os
import time
from dotenv import load_dotenv

import states

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    load_dotenv()

    divera_api_key = os.getenv('DIVERA_ACCESS_KEY')
    logging.debug('Divera Access Key: %s' % divera_api_key)
    divera_dashboard = os.getenv('DIVERA_DASHBOARD_URL')
    logging.debug('Divera Dashboard: %s' % divera_dashboard)
    service_webpage = os.getenv('SERVICE_URL')
    logging.debug('Homepage (Service): %s' % service_webpage)


    ordered_states = [
        # prio 1: show dashboard with alarm infos
        states.Alarm(divera_api_key, divera_dashboard),
        # at regular service show internal infos etc.
        states.Service(service_webpage),
        # at a event with external guest show other stuff
        states.Event(),
        # do not forget to keep the system up-to-date
        states.Update(),
        # otherwise screen off and waiting
        states.BlackScreen()
    ]

    active_state = states.NoOp()
    while True:
        for state in ordered_states:
            logging.info(state.__class__.__name__)
            if state.should_be_active():
                if state != active_state:
                    logging.info('deactivating %s' % active_state.__class__.__name__)
                    active_state.deactivate()
                    logging.info('activating %s' % state.__class__.__name__)
                    state.activate()
                    active_state = state
                break

        # sleep x seconds and start evaluation cycle again
        time.sleep(30)
