import datetime
import logger

TZ_OFFSET = datetime.timezone(datetime.timedelta(0, 60*60*2))
LOTTERY_TIME = datetime.time(10, 0, tzinfo=TZ_OFFSET)
start_day: int = 1
result_day: int = 8
is_scheduled: bool = False

#set lottery scheduled
def set_scheduled(set_running: bool):
    global is_scheduled
    is_scheduled = set_running
    if is_scheduled: log_txt = f"monthly lottery has been scheduled with {start_day}. as start day and {result_day}. as result day"
    else: log_txt = "monthly lottery has been paused"
    logger.info(None, log_txt)

#change start and result days
def change_days(days: "tuple[int, int]") -> bool:
    new_start = days[0]
    new_result = days[1]
    def valid_day(day: int) -> bool:
        return (day >= 1) & (day <= 28)
    if valid_day(new_start) & valid_day(new_result) & (new_start < new_result):
        global start_day
        global result_day
        start_day = new_start
        result_day = new_result
        return True
    return False

#is lottery currently active
def is_active() -> bool:
    datetime_now = datetime.datetime.now(tz=TZ_OFFSET)
    day_now = datetime_now.day
    #check if today is between start and end day
    if (day_now > start_day) & (day_now < result_day):
        return True
    #check if it is start day 
    elif (day_now == start_day):
        #return true if start time precedes time now
        return (datetime_now.timetz() > LOTTERY_TIME)
    #check if it is end day
    elif (day_now == result_day):
        #return true if time now precedes result time
        return (datetime_now.timetz() < LOTTERY_TIME)
    else:
        return False

#return days, hours and minutes until lottery start or lottery result
def time_until_event() -> "tuple[int, int, int]":
    now = datetime.datetime.now(tz=TZ_OFFSET)
    day = result_day if is_active() else start_day
    event = now.replace(day=day, hour=LOTTERY_TIME.hour, minute=LOTTERY_TIME.minute)
    #if event day has already been, next event day is in following month
    if (event - now).days < 0: 
        event = event.replace(month=now.month + 1)
    time = event - now
    return (time.days, int(time.seconds / 3600), int((time.seconds / 60) % 60))