from abc import ABC, abstractmethod
import requests

class BaseState(ABC):
        """ Defines the API for all states """

        @abstractmethod
        def should_be_active(self) -> bool:
            """ check the conditions if this state should become active """
            pass

        @abstractmethod
        def activate(self) -> None:
            """ set this state active and do the magic """
            pass

        @abstractmethod
        def deactivate(self) -> None:
            """ clean up if necessary """
            pass

class NoOp(BaseState):
        """ State with no operation (Dummy) """
        def should_be_active(self):
            pass
        def activate(self):
            pass
        def deactivate(self):
            pass

class Alarm(NoOp):
        def __init__(self, divera_key) -> None:
              super().__init__()
              self.API_URL="https://www.divera247.com/api/last-alarm?accesskey="+divera_key

class Service(NoOp):
        pass

class Event(NoOp):
        pass

class Update(NoOp):
        pass

class BlackScreen(NoOp):
        pass