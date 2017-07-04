#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/6/12 0012 21:19
# @project  Python
# @file     FtpUtils
import ftplib
import os
import logging
logger = logging.getLogger("kakou.utils")


class FtpUtils(object):
    _connParams = None
    _connMgr = None

    @staticmethod
    def init_conn(params):
        FtpUtils._connParams = params

    @staticmethod
    def get_ftp_conn():
        try:
            if FtpUtils._connMgr:
                return FtpUtils._connMgr
            else:
                FtpUtils._connMgr = ftplib.FTP()
                FtpUtils._connMgr.set_debuglevel(2)
                FtpUtils._connMgr.encoding = 'utf-8'
                FtpUtils._connMgr.connect(FtpUtils._connParams['Ftp']['url'], FtpUtils._connParams['Ftp']['port'])
                FtpUtils._connMgr.login(FtpUtils._connParams['Ftp']['username'], FtpUtils._connParams['Ftp']['password'])
                return FtpUtils._connMgr
        except Exception, e:
            logger('ftp login failed: %s' % e.message)
            return None

    @staticmethod
    def upload_file(filename, upload_path):
        try:
            bufsize = 4096
            file_handle = open(filename, 'rb')
            ftp = FtpUtils.get_ftp_conn()
            ftp.set_debuglevel(2)
            if ftp:
                dirs = upload_path.split('/')
                parent_dir = ''
                for dir in dirs:
                    if len(dir) > 0:
                        parent_dir = parent_dir + '/' + dir
                        try:
                            ftp.mkd(parent_dir)
                        except:
                            print 'dir is exist!'
                #ftp.cwd(upload_path)
                ftp.storbinary('STOR %s' % (upload_path + os.path.basename(filename)), file_handle, bufsize)
            ftp.set_debuglevel(0)
            file_handle.close()
        except Exception, e:
            logger('upload file failed: %s, filename = %s' % (e.message, filename))

    @staticmethod
    def download_file(filename, download_path):
        try:
            bufsize = 4096
            file_handle = open(filename, 'rb')
            ftp = FtpUtils.get_ftp_conn()
            ftp.set_debuglevel(2)
            if ftp:
                ftp.cwd(download_path)
                ftp.retrbinary('RETR %s' % os.path.basename(filename), file_handle, bufsize)
            ftp.set_debuglevel(0)
            file_handle.close()
        except Exception, e:
            logger('download file failed: %s, filename = %s' % (e.message, filename))

    @staticmethod
    def close():
        if FtpUtils._connMgr:
            FtpUtils._connMgr.quite()

