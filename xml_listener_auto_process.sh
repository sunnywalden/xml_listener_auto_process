#!/usr/bin/bash

#log_file='/var/log/db_doc_onoff.log.1'

#grep -i 'ERROR Build' ${log_file}| grep 'failed with timed out'|awk '{print $6}' > /opt/xml_transfer/id.txt.2.online
#grep -i 'ERROR Delete' ${log_file}|grep 'failed with timed out'|awk '{print $6}' > /opt/xml_transfer/id.txt.2.pre_offline

#echo 'searchids to parse'
#echo '*****************************************'

#cat /opt/xml_transfer/id.txt.2.online
#cat /opt/xml_transfer/id.txt.2.pre_offline

echo '*****************************************'
echo `date`
echo 'processing start'

cd /opt/xml_transfer/xml_listener_auto_process/
python main/xml_listener_auto.py
echo '*****************************************'
echo 'get uniq searchids'
sort -n /opt/xml_transfer/id.txt.2.online |uniq -u > /opt/xml_transfer/id.txt.2.online_tmp
sort -n /opt/xml_transfer/id.txt.2.offline |uniq -u > /opt/xml_transfer/id.txt.2.offline_tmp

cat /opt/xml_transfer/id.txt.2.online_tmp > /opt/xml_transfer/id.txt.2.online
cat /opt/xml_transfer/id.txt.2.offline_tmp > /opt/xml_transfer/id.txt.2.offline



echo '*****************************************'
cd /opt/xml_transfer/

if test -s /opt/xml_transfer/id.txt.2.online;then
    bash /opt/xml_transfer/doc_online_zhangbo.sh
else
    echo 'No vedio to go online'
fi
if test -s /opt/xml_transfer/id.txt.2.offline;then
    bash /opt/xml_transfer/doc_offline_zhangbo.sh
else
    echo 'No vedio to go offline'
fi
echo '***********All finished here*************'
echo '*****************************************'
