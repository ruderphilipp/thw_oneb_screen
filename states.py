from abc import ABC, abstractmethod
import datetime
import logging
import requests
import subprocess

#region generic base classes
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

class AbstractBrowserState(BaseState):
        """ Base class for any browser based state. """
        def activate(self):
            # starts chromium in in kiosk mode
            command = 'chromium-browser --noerrdialogs --kiosk --disable-sync --incognito --start-fullscreen --hide-scrollbars %s &>/dev/null &' % self.URL
            self.proc = subprocess.Popen(command.split(' '))

        def deactivate(self):
            self.proc.terminate()
            # just kill every chromium process
            #command = 'pkill chromium >/dev/null'
            #subprocess.run(command.split(' '))
#endregion

class Alarm(AbstractBrowserState):
        """
            Alarm state

            This state shows the Divera dashboard in case that there is an alarm.
        """
        def __init__(self, api_key, dashboard_url) -> None:
            super().__init__()
            self.API_URL="https://www.divera247.com/api/last-alarm?accesskey=" + api_key
            self.URL = dashboard_url

        def should_be_active(self):
            alarm_active = False
            # code block from https://github.com/Dustin1358/Raspberry-Pi-Divera-Monitor
            try:
                result = requests.get(self.API_URL).content.decode()
                alarm_active = "\"success\":true" in result and "Probealarm" not in result
            except Exception as e:
                #if not internet connection avaible show
                #screen that people recognize that somethong is wrong
                logging.warn('%s' % e)
            return alarm_active

class Service(AbstractBrowserState):
        """
            Service state

            Shows a given URL during weekly service hours.
        """
        def __init__(self, url) -> None:
            super().__init__()
            self.URL = url

        def should_be_active(self) -> bool:
            duty_time=False

            now=datetime.datetime.now()
            day_of_week=now.isoweekday()
            hour=now.hour
            # helper
            MON, TUE, WED, THU, FRI, SAT, SUN = range(1,8)

            ##################################
            # define your service times here #
            ##################################

            # Thursday 19:00 - Friday 01:00 in the morning
            if((day_of_week==THU and hour >= 19) or (day_of_week==FRI and hour < 1)):
                duty_time=True
            # Saturday 07:00 - 19:00
            if(day_of_week==SAT and hour >= 7 and hour <= 19):
                duty_time=True

            return duty_time

class Event(NoOp):
        pass

class Update(NoOp):
        pass

class BlackScreen(NoOp):
        pass