import pytest
from instruction_parser import InstructionParser

class TestInstructionParser:
    
    def test_init(self):
        """Test InstructionParser initialisation"""
        parser = InstructionParser()
        assert isinstance(parser, InstructionParser)
        assert "goto" in parser.action_styles
        assert "extract" in parser.action_styles
        assert "summarise" in parser.action_styles
        assert "Return" in parser.action_styles
    
    def test_parse_text_basic(self, sample_instructions_text):
        """Test parsing a basic set of instructions"""
        parser = InstructionParser()
        actions = parser.parse_text(sample_instructions_text)
        
        assert isinstance(actions, list)
        assert len(actions) == 4
        
        # Check goto action
        assert actions[0]["type"] == "goto"
        assert actions[0]["url"] == "https://arxiv.org/search/?query=grpo&searchtype=all&source=header"
        
        # Check extract action
        assert actions[1]["type"] == "extract"
        assert set(actions[1]["items"]) == set(["title", "authors", "links"])
        
        # Check summarise action
        assert actions[2]["type"] == "summarise"
        
        # Check Return action
        assert actions[3]["type"] == "Return"
    
    def test_parse_text_with_complex_extract(self):
        """Test parsing instructions with complex extract statements"""
        parser = InstructionParser()
        text = """
        - goto: https://example.com
        - extract title, authors, links and abstracts
        """
        
        actions = parser.parse_text(text)
        assert len(actions) == 2
        assert actions[1]["type"] == "extract"
        assert set(actions[1]["items"]) == set(["title", "authors", "links", "abstracts"])
    
    def test_parse_file(self, sample_instructions_file):
        """Test parsing instructions from a file"""
        parser = InstructionParser()
        actions = parser.parse_file(sample_instructions_file)
        
        assert isinstance(actions, list)
        assert len(actions) >= 3
        assert actions[0]["type"] == "goto"
        assert actions[1]["type"] == "extract"
    
    def test_parse_file_not_found(self):
        """Test parsing a file that doesn't exist"""
        parser = InstructionParser()
        with pytest.raises(ValueError) as excinfo:
            parser.parse_file("nonexistent_file.txt")
        assert "not found" in str(excinfo.value)
    
    def test_parse_text_with_spelling_variants(self):
        """Test parsing with different spelling variants (summarize vs summarise)"""
        parser = InstructionParser()
        text = """
        - goto: https://example.com
        - extract title
        - summarize abstracts
        """
        
        actions = parser.parse_text(text)
        assert len(actions) == 3
        assert actions[2]["type"] == "summarise"  # The type should be normalized
    
    def test_parse_text_with_empty_lines(self):
        """Test parsing text with empty lines"""
        parser = InstructionParser()
        text = """
        
        - goto: https://example.com
        
        - extract title
        
        """
        
        actions = parser.parse_text(text)
        assert len(actions) == 2