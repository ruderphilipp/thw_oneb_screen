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

    divera = os.getenv('DIVERA_ACCESS_KEY')
    logging.debug('Divera Access Key: %s' % divera)

    ordered_states = [
        states.Alarm(divera), # prio 1: show dashboard with alarm infos
        states.Service(),     # at regular service show internal infos etc.
        states.Event(),       # at a event with external guest show other stuff
        states.Update(),      # do not forget to keep the system up-to-date
        states.BlackScreen()  # otherwise screen off and waiting
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
