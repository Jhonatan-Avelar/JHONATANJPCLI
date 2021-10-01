import requests
import json
import time
import sys
import time
from relacao_site import relacao_site

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

protocol = "http://"
port = ":3000"
url_info = "/api/v1.0/system/info"
url_post = "/api/v1.0/sysconf/compose"
url_docker = "/api/v1.0/app/pullimage"
url_reset = "/api/v1.0/app/restart"

log_file = open('./error_logs.txt', 'w+')

hostname_arrays = []
dict_tokens = {}
defective_name_array = []

class jpcli_script_python(relacao_site):
    
    def __init__(self, *args, **kwargs):
        self.hostname_array = self.get_all()
        self.initiate()

    def initiate(self):
        start_time_overall = time.time()
        
        # # compose file upload loop
        # for hostname in content[:]:
        #     print("----------------uploading compose----------------")
        #     print(hostname)
        #     self.start_loop(hostname, 1)
    
        # # image pull loop
        # for hostname in content[:]:
        #     print("----------------pulling----------------")
        #     print(hostname)
        #     self.start_loop(hostname, 2)
    
        # sleep time for images to finish pulling
        # print("----------------sleeping 60s----------------")
        # time.sleep(60)
    
        # reset AIO container loop
        # for hostname in content[:]:
        #     print("----------------reseting----------------")
        #     print(hostname)
        #     self.start_loop(hostname, 3)
    
        # get system info (for testing only)
        for hostname in self.hostname_array:
            print("----------------sys info----------------")
            print(hostname)
            self.start_loop(hostname, 777)
        
        # list all the defective units (units that could not authenticate in the jpcli endpoint)
        print("----------------defective units----------------")
        for name in defective_name_array:
            print("defective: " + name)
    
        # elapsed time of the whole process
        end_time_overall = time.time()
        total_time_overall = end_time_overall - start_time_overall
        print("elapsed time - overall: ", total_time_overall)
    
    
    def start_loop(self, hostname, option):
    
        try:
            token = dict_tokens[hostname]
            if option == 1:
                self.upload_compose(token, hostname)
            if option == 2:
                self.docker_pull(token, hostname)
            if option == 3:
                self.app_reset(token, hostname)
            if option == 777:
                self.get_sysinfo(token, hostname)
    
        except:
            try:
                # get authentication token
                url_token = "https://pi-login.docker.corp.*****.org/api/v1.0/auth/hostname?value=" + hostname
                body={}
                headers={"username": "100059527",
                        "password": "Sdesenha2018*",
                        "Content-Type": "application/json"}

                request = requests.post(url_token, data=body, headers=headers, verify = False)
                response = json.loads(request.content)
                token = response['token']
                print(token)
    
                dict_tokens[hostname] = token
    
                if option == 1:
                    upload_compose(token, hostname)
                if option == 2:
                    docker_pull(token, hostname)
                if option == 3:
                    app_reset(token, hostname)
                if option == 777:
                    self.get_sysinfo(token, hostname)
    
            except Exception as e:
                print(e)
                print("########################error########################")
                defective_name_array.append(hostname)
                log_file.writelines(hostname + "\n")
                self.hostname_array.remove(hostname)
    
    def upload_compose(self, token, hostname):
        file_name = open('./compose.yml','rb')
        url = protocol + hostname + port + url_post
        headers={'Authorization': 'Bearer ' + token}
        body={}
        upload_file = {'document' : file_name}
    
        request = requests.post(url, data=body, files=upload_file, headers=headers, verify = False)
        print(request)
    
    def docker_pull(self, token, hostname):
        url = protocol + hostname + port + url_docker
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json" }
        # body={"image_name": "aio:latest"}
    
        request = requests.post(url, headers=headers, verify = False)
        print(request)
    
    def app_reset(self, token, hostname):
        url = protocol + hostname + port + url_reset
        body = {}
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json" }
    
        request = requests.post(url, headers=headers, data=json.dumps(body), verify = False)
        print(request)
    
    def get_sysinfo(self, token, hostname):
        url = protocol + hostname + port + url_info
        headers={'Authorization': 'Bearer ' + token}
    
        request = requests.get(url, headers=headers, verify = False)
        response = json.loads(request.content)
        print(response)

jpcli_script_python()