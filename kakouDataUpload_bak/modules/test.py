import sys
import pyinotify
import re
import logging
import os

def mirror(command):
    logger=logging.getLogger('mirror')
    try:
        logger.debug(command)
    except OSError as ose:
        logger.debug('Execution failed:')
        logger.debug(  ose )

class PTmp(pyinotify.ProcessEvent):    
    def process_IN_MOVED_FROM(self, event):
        logger=logging.getLogger('PTmp')
        if not EXCLUDE_PAT.match(event.pathname):
            if os.path.isdir(event.pathname):
                logger.debug('event name:'+event.maskname+',action of dir ' + event.pathname + ' is delete')
                S3_COMMAND = S3_PATH + ' delete dir ' + event.pathname
                mirror(S3_COMMAND)
            else:
                logger.debug('event name:'+event.maskname+',action of file ' + event.pathname + ' is delete')
                S3_COMMAND = S3_PATH + ' delete file ' + event.pathname
                mirror(S3_COMMAND)

    def process_IN_MOVED_TO(self, event):
        logger=logging.getLogger('PTmp')
        if not EXCLUDE_PAT.match(event.pathname):
            if os.path.isdir(event.pathname):
                logger.debug('event name:'+event.maskname+',action of dir ' + event.pathname + ' is edit')
                S3_COMMAND = S3_PATH + ' edit dir ' + event.pathname
                mirror(S3_COMMAND)
            else:
                logger.debug('event name:'+event.maskname+',action of file ' + event.pathname + ' is edit')
                S3_COMMAND = S3_PATH + ' edit file ' + event.pathname
                mirror(S3_COMMAND)
        else:
            logger.debug('event name:'+event.maskname+',file '+ event.pathname +' match exclude pattens.')

    def process_IN_DELETE(self, event):
        logger=logging.getLogger('PTmp')
        if not EXCLUDE_PAT.match(event.pathname):
            if os.path.isdir(event.pathname):
                logger.debug('event name:'+event.maskname+',action of dir ' + event.pathname + ' is delete')
            else:
                logger.debug('event name:'+event.maskname+',action of file ' + event.pathname + ' is delete')
                S3_COMMAND = S3_PATH + ' delete file ' + event.pathname
                mirror(S3_COMMAND)

    def process_IN_DELETE_SELF(self, event):
        logger=logging.getLogger('PTmp')
        if not EXCLUDE_PAT.match(event.pathname):
            if os.path.isdir(event.pathname):
                logger.debug('event name:'+event.maskname+',action of dir ' + event.pathname + ' is delete')
            else:
                logger.debug('event name:'+event.maskname+',action of file ' + event.pathname + ' is delete')
                S3_COMMAND = S3_PATH + ' delete file ' + event.pathname
                mirror(S3_COMMAND)

    def process_IN_CLOSE_WRITE(self, event):
        logger=logging.getLogger('PTmp')
        if not EXCLUDE_PAT.match(event.pathname):
            logger.debug('event name:'+event.maskname+',action of ' + event.pathname + ' is edit')
            S3_COMMAND = S3_PATH + ' edit file ' + event.pathname
            mirror(S3_COMMAND)
        else:
            logger.debug('event name:'+event.maskname+',file '+ event.pathname +' match exclude pattens.')

    def process_IN_CREATE(self, event):
        logger=logging.getLogger('PTmp')
        if not EXCLUDE_PAT.match(event.pathname):
            if os.path.isdir(event.pathname):
                logger.debug('event name:'+event.maskname+',dir ' + event.pathname + ' is created.')
            else:
                logger.debug('event name:'+event.maskname+',file ' + event.pathname + ' is created.')
        else:
            logger.debug('event name:'+event.maskname+',file '+ event.pathname +' match exclude pattens.')

def main():
    global EXCLUDE_PAT,S3_PATH
    S3_PATH='s3sync'
    EXCLUDE_PAT=re.compile('.*\/\..*\.sw|.*\/.*~')
    logger = logging.getLogger('s3sync')
    log_level = logging.DEBUG
    logging.basicConfig(level=log_level,)
    PIDFILE='./pidfile'
    FREQ=0
    wmg = pyinotify.WatchManager()
    mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE | \
           pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM | \
           pyinotify.IN_DELETE_SELF | pyinotify.IN_CREATE  |  \
           pyinotify.IN_MODIFY
    ptm = PTmp()
    notifier = pyinotify.Notifier(wmg, ptm, read_freq=FREQ)
    try:
        wmg.add_watch(sys.argv[1], mask, rec=True, auto_add=True)
    except pyinotify.WatchManagerError as err:
        logger.warn(err)
        logger.warn(err.wmd)
    print('daemon...')
    notifier.loop(pid_file=PIDFILE)

if __name__ == "__main__":
    main()