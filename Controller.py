from web_scraper import WebScraper
from items_extractor import ItemsExtractor
from abstract_summariser import AbstractSummariser
from Output_Structurer import OutputStructurer
import logging

class Controller: 

    def __init__(self, scraper=None, extractor=None, summariser=None, structurer=None): 
        """
        Initialising all the system components

        Args: 
            scraper: (func)
            extractor: (func)
            summeriser: (func)
            structurer: (func)
        """
        # This implementation supports the use of independent/external components rather than the ones in this project
        
        self.state = {} # state between executing actions
        self.scraper = scraper if scraper is not None else WebScraper()
        self.extractor = extractor if extractor is not None else ItemsExtractor()
        self.summariser = summariser if summariser is not None else AbstractSummariser() # include model path if want to use local Llama model
        self.structurer = structurer if structurer is not None else OutputStructurer()


    def execute_actions(self, actions):
        """
        Executing sequential actions

        Args:
            actions: (list)

        Returns: 
            (json)
        """

        logging.info(f"Executing {len(actions)} actions")
        
        # Store actions for reference between steps
        self.actions = actions

        # Executing one action at a time (Sequentially)
        for i, action in enumerate(actions):
            # Pass the remaining actions so we can look ahead
            next_actions = actions[i+1:] if i+1 < len(actions) else []
            self._execute_one_action(action, next_actions)

        # structure the output
        return self.structurer.structure_output(self.state)

    def _execute_one_action(self, action, next_actions): 
        """
        Execute a single action with awareness of upcoming actions
        
        Args:
            action: (list)
            next_actions: (list)
        """

        type_of_action = action.get('type')
        logging.info(f"Executing action of type: {type_of_action}")

        if type_of_action == "goto":
            # save url
            url = action.get("url")
            _, soup = self.scraper.fetch_n_parse(url)
            self.state['current_soup'] = soup
            self.state['current_url'] = url

        elif type_of_action == "extract":
            # In case goto action is missing
            if "current_soup" not in self.state: 
                raise ValueError("Have to execute goto before extract.\n No content found for extraction.")

            items = action.get("items", [])
            
            # Check if the next action is "summarise" and add abstracts to extract if needed
            if any(a.get("type") == "summarise" for a in next_actions) and "abstract" not in items and "abstracts" not in items:
                items.append("abstracts")

            items_data = self.extractor.extract(self.state["current_soup"], items)
            self.state.update(items_data)
        
        elif type_of_action == "summarise":
            if "abstract" in self.state:
                self.state["summary"] = self.summariser.Summarise_abstracts(self.state["abstract"])
            else:
                logging.error("No abstracts found to summarise")