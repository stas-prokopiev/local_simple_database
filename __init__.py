
# Standard library imports
# Third party imports

# Local imports
from local_simple_database.class_local_simple_database import \
    class_local_simple_database
from local_simple_database.class_local_dict_database import \
    class_local_dict_database


__all__ = [
    "class_local_simple_database",
    "class_local_dict_database"

]


#####
# Prepare basic logger in case user is not setting it itself.
#####
import logging
#STR_LOG_STDOUT_FORMAT = '[%(levelname)s]:  %(message)s'
# DEBUG=10   INFO=20   WARNING=30   ERROR=40   CRITICAL=50
#logging.basicConfig(format=STR_LOG_STDOUT_FORMAT, level=20)

LOGGER = logging.getLogger("local_simple_database")
LOGGER.addHandler(logging.NullHandler())
