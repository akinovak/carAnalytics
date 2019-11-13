import os
import time
from conf import ctx
while True:
    os.system('python3 crawler_process.py ' + 'polovni_scrap')
    time.sleep(ctx.server_timeout)
