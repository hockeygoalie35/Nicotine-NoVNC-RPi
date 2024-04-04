# python3
# This script runs on startup of the container and ensures that nicotine's config has "header_bar" set to False
# For whatever reason, the header bar doesn't show up while using noVNC, so this will move the search bar
# and other actions into the app.
import logging
from sys import stdout
from colorama import Fore, init
import os
import time
import configparser

CONFIGPATH = "/data/.config/nicotine/config"
VERSION = '1.0.0'

# Logging Setup
logging.basicConfig(
    format=f'%(asctime)s :: ConfigSet :: {VERSION} :: %(levelname)s :: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO, handlers=[logging.StreamHandler(stdout)])
logger = logging.getLogger('configset')

# Initialize colorama
init(autoreset=True)
# Init STDOUT MSG
logger.info(Fore.GREEN + 'Logger initialized'+Fore.LIGHTWHITE_EX)

first_time = False
if os.path.isfile(CONFIGPATH) is False:
    first_time = True

logger.info(Fore.YELLOW +"Waiting for Config"+ Fore.LIGHTWHITE_EX)
retries = 0
while os.path.isfile(CONFIGPATH) is False and retries < 100:
    time.sleep(0.1)
    retries += 1
    pass
if retries >= 100:  # If it retries a bunch and config file is never found, exit.
    logger.error(Fore.RED+"Config File Not Found, Are You sure Docker Compose is mapped properly? Exiting..."
                 + Fore.LIGHTWHITE_EX)
    exit(68)

# Nicotine is quick to make a config file, but slow to populate
logger.info(Fore.GREEN + "Config found, waiting for ui section to populate" + Fore.LIGHTWHITE_EX)


parser = configparser.ConfigParser()  # Init configparser
parser.read(CONFIGPATH)
while 'ui' not in parser.sections():
    parser = configparser.ConfigParser()
    parser.read(CONFIGPATH)
logger.info(Fore.GREEN+"UI Section found, continuing..." + Fore.LIGHTWHITE_EX)

try:
    if parser.get('ui', 'header_bar') == 'True':
        logger.info(Fore.YELLOW + f'header_bar = {parser.get("ui","header_bar")}' + Fore.LIGHTWHITE_EX)
        parser.set('ui', 'header_bar', 'False')
        with open(CONFIGPATH, 'w') as configfile:
            parser.write(configfile)
            configfile.close()
        with open(CONFIGPATH+'.old', 'w') as configfile:
            parser.write(configfile)
            configfile.close()
        logger.info(Fore.YELLOW+"header_bar set to False, config saved"+Fore.LIGHTWHITE_EX)
        if first_time is True:
            logger.info(Fore.GREEN+"Initial settings written to config. Please restart the container to continue!"
                        + Fore.LIGHTWHITE_EX)
            exit(0)
    time.sleep(5)
    logger.info(Fore.GREEN+"Config properly set, Enjoy!"+Fore.LIGHTWHITE_EX)
    exit(0)

except Exception as e:
    logger.error(Fore.RED+str(e)+Fore.LIGHTWHITE_EX)
