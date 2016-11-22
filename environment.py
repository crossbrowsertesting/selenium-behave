from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import requests
import subprocess

username = "you@yourdomain.com"
authkey  = "yourauthkey"
def before_feature(context, feature):
    caps = {}
    caps['name'] = 'Behave Example'
    caps['build'] = '1.0'
    caps['browser_api_name'] = "Chrome53"
    caps['os_api_name'] = "Win10"
    caps['screen_resolution'] = '1024x768'
    caps['record_video'] = 'true'
    caps['record_network'] = 'true'
    caps['take_snapshot'] = 'true'


    context.api_session = requests.Session()
    context.api_session.auth = (username, authkey)

    # cmd = "cbt_tunnels --username " + username + " --authkey " + authkey + " --ready tunnel_ready asadmin" 
    
    # context.tunnel_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)



    context.driver = webdriver.Remote(
        desired_capabilities=caps,
        command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub"%(username, authkey)
    )
    
def after_feature(context, feature):
    context.driver.quit() 
    # subprocess.Popen.terminate(context.tunnel_proc)
    
