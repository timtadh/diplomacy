import sys
sys.stderr = sys.stdout
import cgitb; cgitb.enable()
import config_db_con
import warnings
warnings.simplefilter('ignore', UserWarning)

