"""
functional_tests.py
This file stores tests used to establish correct functioning of the web front
end of our application.
"""
from selenium import webdriver


browser = webdriver.Firefox()
browser.get('http://localhost:8765')

assert 'GenSci' in browser.title
