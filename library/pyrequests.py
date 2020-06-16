from time import sleep

import requests

def httprequest_check_200(url):

    for i in range(10):

        try:
            r = requests.get(url, timeout=1)
            return True
        except:
            sleep(2)
            pass

    return False

# httprequest_check_200('http://ec2-18-216-92-205.us-east-2.compute.amazonaws.com:5000')