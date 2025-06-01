import logging

class ItemsExtractor: 

    """This class includes the methods that will be used to extract 
    the required items in the webpage (titles, authors, links and abstracts)"""


    def extract(self, soup, items_to_extract):
        """Extract items from the BeautifulSoup object
        
        Args:
            soup: (BeautifulSoup object)
            items_to_extract: (list)
            
        Returns:
            extracted data: (dict)
        """
        extracted = {}
        logging.info(f"Extracting items: {items_to_extract}")
        
        for item in items_to_extract:
            if item.lower() == "title":
                extracted["title"] = self._extract_titles(soup)
            elif item.lower() == "authors":
                extracted["authors"] = self._extract_authors(soup)
            elif item.lower() == "links":
                extracted["link"] = self._extract_links(soup)
            elif item.lower() in ["abstract", "abstracts"]:
                extracted["abstract"] = self._extract_abstracts(soup)
            
        return extracted
    


    def _extract_titles(self, soup):
        """
        Extracting the titles of the papers on the web page

        Args:
            soup: (BeautifulSoup Object)

        Returns:
            titles: (list)
        """
        titles = []
        title_elements = soup.select("p.title.is-5")
        # extract each title and remove spaces from start and end
        for element in title_elements: 
             titles.append(element.text.strip())

        if titles:
            logging.info(f"Successfully Exctracted {len(titles)} titles")
        
        return titles
    
    def _extract_authors(self, soup): 
        
        """
        Extracting the list of authors for papers on the web page

        Args:
            soup: (BeautifulSoup Object)

        Returns:
            titles: (list)
        """
        authors = []
        author_elements = soup.select("p.authors")

         # Extract the group of author names for every paper
        for element in author_elements: 
             
            # Isolate the element content and take out the Authors: prefix
            raw_authors_text = element.text.replace("Authors:", "")

            # Get each author's name
            raw_authors_names = raw_authors_text.split(",")

            # Remove spaces from start and end of each author's name
            clean_authors = []
            for author in raw_authors_names: 
                clean_authors.append(author.strip())
        
            authors.append(clean_authors)

        if authors: 
            logging.info(f"Successfully extracted authors names for {len(authors)} papers")

        return authors


    def _extract_links(self, soup):
        """
        Extracting the links for each paper on the web page

        Args:
            soup: (BeautifulSoup Object)

        Returns:
            titles: (list)
        """
        links = []
        link_elements = soup.select("p.list-title a[href*='/abs/']")

        for element in link_elements: 
            
            # Extract the Hypertext Reference for the link
            href = element.get("href")
            if href:
                # Convert relative URLs to absolutes
                if href.startswith("/"):
                    href = f"https://arxiv.org{href}"
                links.append(href)

        if links:
            logging.info(f"Successfully extracted {len(links)} links")

        return links
    
    def _extract_abstracts(self, soup):
        """
        Extracting the links for each paper on the web page

        Args:
            soup: (BeautifulSoup Object)

        Returns:
            titles: (list)
        """
        abstracts = []
        abstract_elements = soup.select("span.abstract-short")

        for element in abstract_elements: 
            # Append and clean spaces at the beginning and end of abstract
            abstracts.append(element.text.strip())
        
        if abstracts: 
            logging.info(f"Successfully extracted {len(abstracts)} abstracts")
        
        return abstracts