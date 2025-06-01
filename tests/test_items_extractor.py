import pytest
from bs4 import BeautifulSoup
from items_extractor import ItemsExtractor

class TestItemsExtractor:
    
    def test_init(self):
        """Test ItemsExtractor initialisation"""
        extractor = ItemsExtractor()
        assert isinstance(extractor, ItemsExtractor)
    
    def test_extract_titles(self, sample_soup):
        """Test extracting titles from HTML"""
        extractor = ItemsExtractor()
        titles = extractor._extract_titles(sample_soup)
        
        assert isinstance(titles, list)
        assert len(titles) == 2
        assert titles[0] == "GRPO: A New Approach to Reinforcement Learning"
        assert titles[1] == "Multi-Agent GRPO for Collaborative Environments"
    
    def test_extract_authors(self, sample_soup):
        """Test extracting authors from HTML"""
        extractor = ItemsExtractor()
        authors = extractor._extract_authors(sample_soup)
        
        assert isinstance(authors, list)
        assert len(authors) == 2
        assert authors[0] == ["John Smith", "Emily Jones", "Michael Brown"]
        assert authors[1] == ["Jane Doe", "Robert Johnson"]
    
    def test_extract_links(self, sample_soup):
        """Test extracting links from HTML"""
        extractor = ItemsExtractor()
        links = extractor._extract_links(sample_soup)
        
        assert isinstance(links, list)
        assert len(links) == 2
        assert links[0] == "https://arxiv.org/abs/2401.12345"
        assert links[1] == "https://arxiv.org/abs/2402.54321"
    
    def test_extract_abstracts(self, sample_soup):
        """Test extracting abstracts from HTML"""
        extractor = ItemsExtractor()
        abstracts = extractor._extract_abstracts(sample_soup)
        
        assert isinstance(abstracts, list)
        assert len(abstracts) == 2
        assert "This paper introduces GRPO" in abstracts[0]
        assert "We extend GRPO to multi-agent settings" in abstracts[1]
    
    def test_extract_multiple_items(self, sample_soup):
        """Test extracting multiple items at once"""
        extractor = ItemsExtractor()
        items_to_extract = ["title", "authors", "links"]
        extracted = extractor.extract(sample_soup, items_to_extract)
        
        assert "title" in extracted
        assert "authors" in extracted
        assert "link" in extracted
        assert len(extracted["title"]) == 2
        assert len(extracted["authors"]) == 2
        assert len(extracted["link"]) == 2
    
    def test_extract_with_empty_soup(self):
        """Test extracting from empty soup"""
        extractor = ItemsExtractor()
        empty_soup = BeautifulSoup("", "html.parser")
        
        titles = extractor._extract_titles(empty_soup)
        authors = extractor._extract_authors(empty_soup)
        links = extractor._extract_links(empty_soup)
        abstracts = extractor._extract_abstracts(empty_soup)
        
        assert titles == []
        assert authors == []
        assert links == []
        assert abstracts == []
    
    def test_extract_with_case_insensitivity(self, sample_soup):
        """Test case insensitivity in item names"""
        extractor = ItemsExtractor()
        items_to_extract = ["Title", "Authors", "Abstract"]
        extracted = extractor.extract(sample_soup, items_to_extract)
        
        assert "title" in extracted
        assert "authors" in extracted
        assert "abstract" in extracted
    
    def test_extract_nonexistent_item(self, sample_soup):
        """Test extracting a nonexistent item"""
        extractor = ItemsExtractor()
        items_to_extract = ["nonexistent"]
        extracted = extractor.extract(sample_soup, items_to_extract)
        
        assert len(extracted) == 0