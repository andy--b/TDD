# FT

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
	
	def tearDown(self):
		self.browser.quit()
	
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])		

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Bob wants to go to that cool to-do app. So he goes to the homepage
		self.browser.get(self.live_server_url)

		# He notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)

		# He is invited to enter a to-do item right away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
				inputbox.get_attribute('placeholder'),
				'Enter a to-do item'
		)
		
		# He types "Cook bacon" into a text box
		inputbox.send_keys('Cook bacon')

		# When he hits enter, he is taken to a new URL,
		# and now the page lists
		# "1: Cook bacon" as an item in a to-do list
		inputbox.send_keys(Keys.ENTER)
		bob_list_url = self.browser.current_url
		self.assertRegex(bob_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Cook bacon')

		# There is still a text box inviting her to add another item. 
		# He adds "Eat the bacon"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Eat the bacon')	
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and shows him both items in the list
		self.check_for_row_in_list_table('1: Cook bacon')
		self.check_for_row_in_list_table('2: Eat the bacon')

		# Now a new user, Francis, comes along to the site.
		
		## We use a new browser session to make sure that no information
		## of Bob's is coming through from cookies etc
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		# Francis visits the homepage. There is no sign of Bob's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Cook bacon', page_text)
		self.assertNotIn('Eat the bacon', page_text)
		
		# Francis starts a new list by entering a new item.
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		
		# Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, bob_list_url)
		
		# Again, there is no trace of Bob's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Cook bacon', page_text)
		self.assertIn('Buy milk', page_text)
		
		# Satisfied, they both go back to sleep
		
	def test_layout_and_styling(self):
		# Bob goes to the homepage
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024,768)
		
		# He notices the input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width']/2,
			512,
			delta = 10
		)
	