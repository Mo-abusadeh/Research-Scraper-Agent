import logging
from bs4 import BeautifulSoup
import requests


class WebScraper: 

    def __init__(self, session=None): 
        # Initialise the optional session for connection reuse
        self.session = session or requests.Session()


    def fetch_n_parse(self, url): 
        """
        Fetch and parse the content on the web page

        Args: 
            url: (str)

        Returns: 
            tuple: (Raw Text HTML, BeautifulSoup Object)

        """
        try: 
            logging.info("Fetching and Parsing content from the url: {url}")
            
            response = self.session.get(url)
            response.raise_for_status() # Raises HTTP Error if request fails
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            return response.text, soup
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Request Failed to fetch the url: {url} Error Message: {str(e)}")
            raise