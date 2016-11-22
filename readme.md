# Selenium Testing with CrossBrowserTesting and Behave

[Behavior Driver Development](https://en.wikipedia.org/wiki/Behavior-driven_development) is growing in popularity, and performing BDD with Python is no exception. [Behave](http://pythonhosted.org/behave/) is a popular BDD framework for performing tests, and, because Behave is built on Python's [Selenium](http://docs.seleniumhq.org) language bindings, performing Behavioural Driven testing on CBT is easy. We'll walk your through getting started here.

To get started, we'll need to ensure that Behave is installed. The easiest means of doing so is with Pip:

```
pip install Behave
```

Alternatively you can read [installation documenation](http://pythonhosted.org/behave/install.html) on the Behave website. We also need to install [Requests](http://docs.python-requests.org/en/master/) so we can perform interactions with our API like taking a snapshot and setting the score:

'''
pip install requests
'''

Lastly, we'll need to install Selenium:

'''
pip install selenium
'''

Once that's complete, we're ready to start writing our first test with Behave. Tests start with writing "Feature" files that use plain english to describe the steps of your test. Features use keywords to form the actual steps being taken in the test:

* **Given** we put the system in a known state before the user (or external system) starts interacting with the system (in the When steps). Avoid talking about user interaction in givens.

* **When** we take key actions the user (or external system) performs. This is the interaction with your system which should (or perhaps should not) cause some state to change.

* **Then** we observe outcomes.

Create a new directory with a single file we'll call 'Example.feature'. You can then copy the following feature into your feature file:

'''
Feature: Test a login form

Scenario: Test Login
  Given I go to my login form
  Then the title should be "Login Form - CrossBrowserTesting.com"
  When I enter my credentials
  When I click login
  Then I should see the login message
'''

Next, we'll need to modify the environment we're testing on so we can perform our test in the cloud. Add another file to your directory called environment.py, and copy the following script into it:

'''
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import requests
import subprocess

username = "you@yourdomain.com"							# change this to the username associated with your account
authkey  = "yourauthkey"								# change this the authkey found on the 'Manage Account' section of our site
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
'''

As you can see from our example, we're creating a Remote WebDriver that points to our hub. You can alternatively start a local connection so you can access locally hosted content. Just ensure that you've installed [cbt_tunnels](https://github.com/crossbrowsertesting/cbt-tunnel-nodejs).