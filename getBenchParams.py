import os
import copy
import time
import requests
import json
import psutil
import io
import datetime

# defining the api-endpoint
API_ENDPOINT = "https://telemetry-benchmark-automation.apps.cac.preview.pcf.manulife.com/api/metrics"
#API_ENDPOINT = "http://ptsv2.com/t/976df-1566575145/post"
#API_ENDPOINT = "http://localhost:8080/yourpath"

def sendStats(hostName):
    cpuPercent = psutil.cpu_percent()
    memUsage = psutil.virtual_memory().percent
    cmd='syslog-ng-ctl stats | awk --field-separator=\",\" \'{print $6}\''
    var=os.popen(cmd).read()
    final_list=[]
    final_dict={'topics': [{'topic': 'cec-logtrail'}, {'topic': 'INFRA_LOGS_DEV'}, {'topic': 'eb-con-syslog-dev'}, {'topic': 'cec-logtrail3'}, {'topic': 'ULS_LOGS_IDENTITY_PREV'}, {'topic': 'cec-logtrail2'}, {'topic': 'cec-logtrail1'}]}
    new_dict = copy.deepcopy(final_dict)
    for line in var.splitlines():
        if line is not '':
            final_list.append(line.split(';'))
    for i in final_list:
        index=final_dict['topics'].index({"topic":i[0]})
        new_dict['topics'][index].update({i[2]:i[3]})
    currTime = datetime.datetime.utcnow()
    curr = str(currTime)
    new_dict.update({'metrics_date': curr})
    new_dict.update({'vm':hostName})
    new_dict.update({'cpu':cpuPercent})
    new_dict.update({'ram':memUsage})
    jsondata = json.dumps(new_dict)
    print(jsondata)
#    with open('data.json', 'w') as f:
#        json.dump(new_dict, f)
    r = requests.post(url = API_ENDPOINT, data = jsondata, headers={'content-type':'application/json'})
    # extracting response text
    pastebin_url = r
    print("The pastebin URL is:%s"%pastebin_url)
    time.sleep(30)

if __name__ == "__main__":
#    cmd='hostname'
#    hostName=os.popen(cmd).read()
#    hostName = os.getenv('HOSTNAME')
    hostName = os.uname()[1]
    while True:
        sendStats(hostName)
