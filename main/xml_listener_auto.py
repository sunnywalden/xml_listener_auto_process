#!/usr/bin/python
#-- coding:utf-8 --

import ConfigParser

import sys
import codecs

import re

sys.path.append('/opt/xml_transfer/xml_listener_auto_process/')


import check_vedio_status
import os

def get_config():
    cp = ConfigParser.SafeConfigParser()

    with codecs.open('config/files.config', 'r', encoding='utf-8') as f:  
        cp.readfp(f)

        log_file = cp.get('log_files','log_today').strip()
        #log_file = cp.get('log_files','log_yesrtoday').strip()
        #log_file = cp.get('log_files','log_history').strip()
        work_dir = cp.get('searchid_files','wk_dir').strip()
        searchid_file_pre_offline = work_dir + cp.get('searchid_files','pre_offline').strip()
        searchid_file_offline = work_dir + cp.get('searchid_files','offline').strip()
        searchid_file_online = work_dir + cp.get('searchid_files','online').strip()
    print(log_file,searchid_file_pre_offline,searchid_file_offline,searchid_file_online)
    return log_file,searchid_file_pre_offline,searchid_file_offline,searchid_file_online

def searchid_generater(log_file,file_pre_offline,file_online):
    with open(log_file,'r') as f:
        l = f.readline().strip()
        
        err_online_msg = 'ERROR Build'
        err_offline_msg = 'ERROR Delete'
#err_msg = 'failed with timed out'
        include_msg = 'server'
        exclude_msg = 'format requires'

        open(file_online,'w').close()

        open(file_pre_offline,'w').close()
        file_todo = ''
        while l:
            global file_todo
            if re.search(err_online_msg,l) and re.search(include_msg,l) and not re.search(exclude_msg,l):
                print('debug all that match online err:',l)
                id = l.split(' ')[5].strip()
                file_todo = file_online
                f2 = open(file_todo,'a')
                f2.write(id + '\n')
                f2.close()
            elif re.search(err_offline_msg,l) and re.search(include_msg,l) and not re.search(exclude_msg,l):
                print('debug all that match offline err:',l)
                id = l.split(' ')[5].strip()
                file_todo = file_pre_offline
                f3 = open(file_todo,'a')
                f3.write(id + '\n')
                f3.close()
            else:
                pass
            l = f.readline().strip()


        f5 = open(file_online,'r')
        print('online ids todo with:',f5.readlines())
        f5.close()

        f6 = open(file_pre_offline,'r')
        print('offline ids todo with:',f6.readlines())
        f6.close()


def main():
    log_file,file_pre_offline,file_offline,file_online = get_config()
    searchid_generater(log_file,file_pre_offline,file_online)

    check_vedio_status.check_status(file_pre_offline,file_offline,file_online)

if __name__  == '__main__':
    main()
