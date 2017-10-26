from modules.scheduler import Scheduler
import logging.config

logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger("notify_domain")
if __name__ == '__main__':
	
    scheduler = Scheduler()
    scheduler.handle('_3494.txt')    

    print('main thread exit')
