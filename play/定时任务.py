from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


# 输出时间
# def job():
#     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# # BlockingScheduler
# scheduler = BlockingScheduler()
# scheduler.add_job(job, 'cron', day_of_week='1-5', hour=6, minute=30)
# scheduler.start()


def my_job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


sched = BlockingScheduler()
sched.add_job(my_job, 'interval', seconds=5)
sched.start()
