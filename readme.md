# Selenium Testing with CrossBrowserTesting and Behave

[Behavior Driver Development](https://en.wikipedia.org/wiki/Behavior-driven_development) is growing in popularity, and performing BDD with Python is no exception. [Behave](http://pythonhosted.org/behave/) is a popular BDD framework for performing tests, and, because Behave is built on Python's [Selenium](http://docs.seleniumhq.org) language bindings, performing Behavioural Driven testing on CBT is easy. We'll walk your through getting started here.

To get started, we'll need to ensure that Behave is installed. The easiest means of doing so is with Pip:

```
pip install Behave
```

Alternatively you can read [installation documenation](http://pythonhosted.org/behave/install.html) on the Behave website. We also need to install [Requests](http://docs.python-requests.org/en/master/) so we can perform interactions with our API like taking a snapshot and setting the score:

```
pip install requests
```

Lastly, we'll need to install Selenium:

```
pip install selenium
```

Once that's complete, we're ready to start writing our first test with Behave. Tests start with writing "Feature" files that use plain english to describe the steps of your test. Features use keywords to form the actual steps being taken in the test:

* **Given** we put the system in a known state before the user (or external system) starts interacting with the system (in the When steps). Avoid talking about user interaction in givens.

* **When** we take key actions the user (or external system) performs. This is the interaction with your system which should (or perhaps should not) cause some state to change.

* **Then** we observe outcomes.

Create a new directory with a single file we'll call 'Example.feature'. You can then copy the following feature into your feature file:

```
Feature: Test a login form

Scenario: Test Login
  Given I go to my login form
  Then the title should be "Login Form - CrossBrowserTesting.com"
  When I enter my credentials
  When I click login
  Then I should see the login message
```

Next, we'll need to modify the environment we're testing on so we can perform our test in the cloud. Add another file to your directory called environment.py, and copy the following script into it:

```
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
    caps['browserName'] = "Chrome"      # pulls the latest version of Chrome by default
    caps['platform'] = "Windows 10"     # to specify a version, add caps['version'] = "desired version"
    caps['screen_resolution'] = '1366x768'
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
```

As you can see from our example, we're creating a Remote WebDriver that points to our hub. You can alternatively start a local connection so you can access locally hosted content. Just ensure that you've installed [cbt_tunnels](https://github.com/crossbrowsertesting/cbt-tunnel-nodejs) and then uncomment out the lines of code necessary for running the subprocess.

Now its time to actually define the steps from our Example.feature file in code. Create a new directory within your current one called 'Steps'. This is where Behave will initially look for the code for your tests. Within that directory, create a file called 'login_example.py', and copy to following code into that file:


```

@given('I go to my login form')
def go_to_login_form(context):
	context.driver.get('http://crossbrowsertesting.github.io/login-form.html')

@then('the title should be {text}')
def verify_title(context, text):
	title = context.driver.title
	try:
		assert "Login Form - CrossBrowserTesting.com" == title
	except AssertionError as e:
		set_score(context, 'fail')

@when('I enter my credentials')
def enter_credentials(context):
	context.driver.find_element_by_id('username').send_keys('tester@crossbrowsertesting.com')
	context.driver.find_element_by_id('password').send_keys('test123')

@when('I click login')
def click_login(context):
	context.driver.find_element_by_xpath('/html/body/div/div/div/div/form/div[3]/button').click()

@then('I should see the login message')
def see_login_message(context):
	context.driver.implicitly_wait(10)
	elem = context.driver.find_element_by_xpath('//*[@id=\"logged-in-message\"]/h2')
	welcomeText = elem.text
	try:
		assert "Welcome tester@crossbrowsertesting.com" == welcomeText
		set_score(context, 'pass')
	except AssertionError as e:
		set_score(context, 'fail')

def set_score(context, test_result):
	context.api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + context.driver.session_id,
        	data={'action':'set_score', 'score': test_result})

```

You should note that we use, the Given-When-Then prefixes before every corresponding function. Steps are narrowed down to individual functions and the whole feature acts as a single unit test. At the end we set the score to the final value of our score variable, and our test is complete. 

This is just the beginning of what you can do with Behave and Selenium! There's really no limits to what's possible with Selenium, and Behave makes it much easier, especially if you're working with QA's that aren't programmers. If you have trouble running your tests with our service, feel free to [get in touch](mailto: info@crossbrowsertesting.com).
