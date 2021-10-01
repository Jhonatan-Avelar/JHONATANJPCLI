import requests
import json
import time
import sys
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class relacao_site():
    def get_all(self):
        array = {'fabrica': []}
        url = 'http://*****/eSt***on/API/a***pi/Rasp***ry?All***e=true'
        request = requests.get(url, verify = False)
        response = json.loads(request.content)

        for ArrayOfVmGetRaspberry in response:
            linha = ArrayOfVmGetRaspberry['LineDescription']
            hostname = ArrayOfVmGetRaspberry['Name']
            array.setdefault(linha, [])
            array[linha].append(hostname)
            array['fabrica'].append(hostname)
        
        return array[sys.argv[1]]

# Nome extenso linhas: