import os
import time
from conf import ctx
from datetime import datetime
while True:
    start_time = datetime.now()
    os.system('python3 crawler_process.py ' + 'polovni_scrap')
    os.system('python3 crawler_process.py ' + 'sold_spider')
    ctx.log.info('loop finished')
    end_time = datetime.now()
    diff = int((start_time-end_time).total_seconds())
    sleep_time = 24*60*60 - diff
    time.sleep(sleep_time)