import datetime
from telegram.ext import JobQueue, Application
import callbacks
import logger
import filehandler
import json

TZ_OFFSET = datetime.timezone(datetime.timedelta(0, 60*60*2))
LOTTERY_TIME = datetime.time(10, 0, tzinfo=TZ_OFFSET)
start_day: int = 1
result_day: int = 8
is_scheduled: bool = False
    
#set lottery scheduled
def schedule(set_scheduled: bool, app: Application):
    global is_scheduled
    is_scheduled = set_scheduled
    save_lottery()
    if is_scheduled: 
        #remove old jobs
        for job in app.job_queue.jobs(): job.schedule_removal()
        #schedule notification, reminder and result according to lottery schedule
        app.job_queue.run_monthly(callbacks.lottery_notification, when=LOTTERY_TIME, day=start_day)
        app.job_queue.run_monthly(callbacks.lottery_reminder, when=LOTTERY_TIME, day=result_day-1)
        app.job_queue.run_monthly(callbacks.lottery_result, when=LOTTERY_TIME, day=result_day)
        log_txt = f"monthly lottery has been scheduled with {start_day}. as start day and {result_day}. as result day"
    else: 
        for job in app.job_queue.jobs(): job.schedule_removal()
        log_txt = "monthly lottery is paused"
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
        save_lottery()
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

#save lottery schedule
def save_lottery():
    data = {"start_day" : start_day,
            "result_day" : result_day,
            "is_scheduled" : is_scheduled}
    open(filehandler.LOTTERY_FP, "w").write(json.dumps(data, indent=2))

#load lottery schedule
def load_lottery(app: Application):
    global start_day, result_day, is_scheduled
    try:
        data = json.load(open(filehandler.LOTTERY_FP, "r"))
        start_day = data["start_day"]
        result_day = data["result_day"]
        is_scheduled = data["is_scheduled"]
        schedule(is_scheduled, app)
    except KeyError:
        logger.error("KeyError: Lottery data is corrupted")
    except json.decoder.JSONDecodeError:
        logger.error(f"JSONDecodeError: Tried to load lottery schedule from '{filehandler.LOTTERY_FP}' but the file was empty")