import pytest
from unittest.mock import Mock, patch
from Controller import Controller

class TestController:
    
    def test_init(self):
        """Test Controller initialization"""
        controller = Controller()
        assert isinstance(controller, Controller)
        assert controller.state == {}
        
        # Test with custom components
        mock_scraper = Mock()
        mock_extractor = Mock()
        mock_summariser = Mock()
        mock_structurer = Mock()
        
        controller = Controller(
            scraper=mock_scraper,
            extractor=mock_extractor,
            summariser=mock_summariser,
            structurer=mock_structurer
        )
        
        assert controller.scraper == mock_scraper
        assert controller.extractor == mock_extractor
        assert controller.summariser == mock_summariser
        assert controller.structurer == mock_structurer
    
    @patch('web_scraper.WebScraper.fetch_n_parse')
    def test_execute_goto_action(self, mock_fetch_n_parse, sample_soup):
        """Test execution of 'goto' action"""
        # Setup mock
        mock_fetch_n_parse.return_value = ("html content", sample_soup)
        
        # Create controller and execute action
        controller = Controller()
        action = {"type": "goto", "url": "https://example.com"}
        controller._execute_one_action(action, [])
        
        # Verify results
        mock_fetch_n_parse.assert_called_once_with("https://example.com")
        assert controller.state["current_url"] == "https://example.com"
        assert controller.state["current_soup"] == sample_soup
    
    @patch('items_extractor.ItemsExtractor.extract')
    def test_execute_extract_action(self, mock_extract, sample_soup, sample_extracted_data):
        """Test execution of 'extract' action"""
        # Setup mock
        mock_extract.return_value = {
            "title": sample_extracted_data["title"],
            "authors": sample_extracted_data["authors"],
            "link": sample_extracted_data["link"]
        }
        
        # Create controller and set initial state
        controller = Controller()
        controller.state["current_soup"] = sample_soup
        
        # Execute action
        action = {"type": "extract", "items": ["title", "authors", "links"]}
        controller._execute_one_action(action, [])
        
        # Verify results
        mock_extract.assert_called_once_with(sample_soup, ["title", "authors", "links"])
        assert "title" in controller.state
        assert "authors" in controller.state
        assert "link" in controller.state
    
    def test_execute_extract_action_no_soup(self):
        """Test extract action without prior goto action"""
        controller = Controller()
        action = {"type": "extract", "items": ["title"]}
        
        with pytest.raises(ValueError) as excinfo:
            controller._execute_one_action(action, [])
        
        assert "Have to execute goto before extract" in str(excinfo.value)
    
    @patch('items_extractor.ItemsExtractor.extract')
    def test_execute_extract_with_upcoming_summarise(self, mock_extract, sample_soup):
        """Test extract action when summarise is coming up next"""
        # Setup mock
        mock_extract.return_value = {"abstract": ["Sample abstract"]}
        
        # Create controller and set initial state
        controller = Controller()
        controller.state["current_soup"] = sample_soup
        
        # Execute action with upcoming summarise action
        current_action = {"type": "extract", "items": ["title"]}
        next_actions = [{"type": "summarise"}]
        controller._execute_one_action(current_action, next_actions)
        
        # Verify that abstracts were added to the items to extract
        mock_extract.assert_called_once_with(sample_soup, ["title", "abstracts"])
    
    @patch('abstract_summariser.AbstractSummariser.Summarise_abstracts')
    def test_execute_summarise_action(self, mock_summarise_abstracts, sample_extracted_data, sample_summarised_abstracts):
        """Test execution of 'summarise' action"""
        # Setup mock
        mock_summarise_abstracts.return_value = sample_summarised_abstracts
        
        # Create controller and set initial state
        controller = Controller()
        controller.state["abstract"] = sample_extracted_data["abstract"]
        
        # Execute action
        action = {"type": "summarise"}
        controller._execute_one_action(action, [])
        
        # Verify results
        mock_summarise_abstracts.assert_called_once_with(sample_extracted_data["abstract"])
        assert controller.state["summary"] == sample_summarised_abstracts
    
    def test_execute_summarise_action_no_abstracts(self):
        """Test summarise action without abstracts in state"""
        controller = Controller()
        action = {"type": "summarise"}
        
        # Should not raise an exception, just log an error
        controller._execute_one_action(action, [])
        assert "summary" not in controller.state
    
    @patch('Controller.Controller._execute_one_action')
    @patch('Output_Structurer.OutputStructurer.structure_output')
    def test_execute_actions(self, mock_structure_output, mock_execute_one_action, sample_state_data, sample_structured_output):
        """Test executing a sequence of actions"""
        # Setup mocks
        mock_structure_output.return_value = sample_structured_output
        
        # Create controller 
        controller = Controller()
        controller.state = sample_state_data
        
        # Create actions
        actions = [
            {"type": "goto", "url": "https://example.com"},
            {"type": "extract", "items": ["title", "authors", "links"]},
            {"type": "summarise"}
        ]
        
        # Execute actions
        result = controller.execute_actions(actions)
        
        # Verify results
        assert mock_execute_one_action.call_count == 3
        mock_structure_output.assert_called_once_with(sample_state_data)
        assert result == sample_structured_output