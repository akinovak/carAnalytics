import os
import time
from conf import ctx
while True:
    os.system('python3 crawler_process.py ' + 'polovni_scrap')
    os.system('python3 sold_scrip.py')
    ctx.log.info('loop finished')
    time.sleep(ctx.server_timeout)
