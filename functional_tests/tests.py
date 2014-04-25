from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# A user opens up the home page
		self.browser.get(self.live_server_url)

		# User reads the header and sees that it mentions to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# User is invited to enter a to-do item
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item')

		# User types 'Buy peacock feathers' into a text box
		inputbox.send_keys('Buy peacock feathers')

		# User hits enter, the page updates and the page lists the user's item
		inputbox.send_keys(Keys.ENTER)
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

		# User is asked to enter another item
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		# Page updates again, and now shows both items on the user's list
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
		self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])

		# The page updates again, showing both items on the user's list
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		# A new user enters the site and begins to use it

		## Use a new browser session to ensure that no information from the previous user is left behind ##
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# The new user opens the page and sees there is a new, blank list available
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		# The new user creates a new list by entering a new item
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		# A new, unique URL is generated for the new user
		francis_list_url = self.browser.current_url
		selt.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		# Once again, there is no evidence of the previous user
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		# Placeholder for future test development
		self.fail('Finish the test!')