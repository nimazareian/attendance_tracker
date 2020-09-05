from datetime import datetime
import pytz

# Current PST time
def get_current_time():
    pst = pytz.timezone('America/Los_Angeles')
    return datetime.now(pst)

# Current month 
# @return String
def get_current_month():
    return get_current_time().strftime('%B')

# current calendar day
def get_current_day():
    current_time = get_current_time()
    return str(current_time.day)

# current hour:min:sec
def get_current_hour():
    current_time = get_current_time()
    return str(current_time.time()) 