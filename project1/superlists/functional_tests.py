from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
	
	def tearDown(self):
		self.browser.quit()
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		# Bob wants to go to that cool to-do app. So he goes to the homepage
		self.browser.get('http://localhost:8000')

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

		# When he hits enter, the page updates, and now the page lists
		# "1: Cook bacon" as an item in a to-do list
		inputbox.send_keys(Keys.ENTER)
		
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Cook bacon', [row.text for row in rows])

		# There is still a text box inviting her to add another item. 
		# He adds "Eat the bacon"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Eat the bacon')	
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and shows him both items in the list
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Cook bacon', [row.text for row in rows])
		self.assertIn('2: Eat the bacon', [row.text for row in rows])

		# Bob wonders whether the site will remember the list. Then he sees
		# that the site has generated a unique URL for him -- there is some
		# explanatory text to that effect
		self.fail('Finish the test!')
		# Bob visits that URL - his to-do list is still there

		# Satisfied, Bob closes his browser, full of bacon
		
if __name__ == '__main__':
	unittest.main()

	