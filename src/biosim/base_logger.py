import logging

# Gir modeulen hvor loggingen kommer fra
logger = logging.getLogger(__name__)

# Loglevel som logges. Lovlige verdier er DEBUG, INFO, WARNING, ERROR og CRITICAL.
# Må bytte level for å endre outputen fra loggingen. Normal står den til INFO.
# For å finne feil kan man skru på DEBUG. FOr at dette skal fungere må det være satt DEBUG statements i koden.
logger.setLevel(logging.INFO)

# Standardoppsett for loggeren med filnavn, format
file_handler = logging.FileHandler('logfile.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)