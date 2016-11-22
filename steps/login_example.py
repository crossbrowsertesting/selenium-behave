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





