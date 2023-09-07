from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.LegalOne.Actions.LegalOneActions import LegalOneActions

from Library_v1.LegalOne.env import get_env

def login(driver: DriverInterface):
    LegalOneActions(driver).login(get_env("office"), get_env("login"), get_env("password"))