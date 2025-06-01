import pytest
from unittest.mock import Mock, patch, MagicMock
import os
from abstract_summariser import AbstractSummariser

class TestAbstractSummariser:
    
    def test_init_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict(os.environ, {}, clear=True):  # Ensure no environment variables
            summariser = AbstractSummariser()
            assert summariser.api_key is None
            assert summariser.genai is None
    
    def test_init_with_explicit_api_key(self):
        """Test initialization with explicitly provided API key"""
        with patch('google.generativeai.configure') as mock_configure:
            summariser = AbstractSummariser(api_key="test_api_key")
            assert summariser.api_key == "test_api_key"
            mock_configure.assert_called_once_with(api_key="test_api_key")
    
    def test_init_with_env_api_key(self):
        """Test initialization with API key from environment variable"""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "env_api_key"}):
            with patch('google.generativeai.configure') as mock_configure:
                summariser = AbstractSummariser()
                assert summariser.api_key == "env_api_key"
                mock_configure.assert_called_once_with(api_key="env_api_key")
    
    def test_init_with_custom_model_path(self):
        """Test initialization with custom model path"""
        with patch('llama_cpp.Llama') as mock_llama:
            mock_llama_instance = Mock()
            mock_llama.return_value = mock_llama_instance
            
            summariser = AbstractSummariser(model_path="custom/model/path")
            
            assert summariser.llm == mock_llama_instance
            mock_llama.assert_called_once_with(model_path="custom/model/path")
    
    @patch('abstract_summariser.AbstractSummariser.__init__', return_value=None)
    @patch('google.generativeai.GenerativeModel')
    def test_summarise_with_gemini(self, mock_generative_model, mock_init):
        """Test summarizing with Gemini API"""
        # Setup mock response
        mock_model_instance = Mock()
        mock_response = Mock()
        mock_response.text = "This is a summarised abstract."
        mock_model_instance.generate_content.return_value = mock_response
        mock_generative_model.return_value = mock_model_instance
        
        # Create summariser instance and configure it
        summariser = AbstractSummariser()
        summariser.api_key = "test_api_key"
        summariser.genai = MagicMock()
        summariser.genai.GenerativeModel = mock_generative_model
        summariser.llm = None
        
        # Test summarise method
        result = summariser.summarise("This is a test abstract.")
        
        # Verify results
        assert result == "This is a summarised abstract."
        mock_generative_model.assert_called_once_with('gemini-2.0-flash-lite')
        mock_model_instance.generate_content.assert_called_once()
    
    @patch('abstract_summariser.AbstractSummariser.__init__', return_value=None)
    def test_summarise_with_llama(self, mock_init):
        """Test summarizing with Llama model"""
        # Create mock Llama model
        mock_llama = Mock()
        mock_llama.return_value = {
            "choices": [{"text": "This is a summarised abstract with Llama."}]
        }
        
        # Create summariser instance and configure it
        summariser = AbstractSummariser()
        summariser.api_key = None
        summariser.genai = None
        summariser.llm = mock_llama
        
        # Test summarise method
        result = summariser.summarise("This is a test abstract.")
        
        # Verify results
        assert result == "This is a summarised abstract with Llama."
        mock_llama.assert_called_once()
    
    @patch('abstract_summariser.AbstractSummariser.__init__', return_value=None)
    def test_summarise_fallback(self, mock_init):
        """Test fallback to simple extraction when both models fail"""
        # Create summariser instance with no working models
        summariser = AbstractSummariser()
        summariser.api_key = None
        summariser.genai = None
        summariser.llm = None
        
        # Test with a multi-sentence abstract
        abstract = "First sentence. Second sentence. Third sentence. Fourth sentence. Fifth sentence."
        result = summariser.summarise(abstract)
        
        # Should return first 4 sentences
        assert result == "First sentence. Second sentence. Third sentence. Fourth sentence."
    
    @patch('abstract_summariser.AbstractSummariser.summarise')
    def test_summarise_abstracts(self, mock_summarise):
        """Test batch summarization of multiple abstracts"""
        # Setup mock
        mock_summarise.side_effect = ["Summary 1", "Summary 2", "Summary 3"]
        
        # Create summariser and test
        summariser = AbstractSummariser()
        abstracts = ["Abstract 1", "Abstract 2", "Abstract 3"]
        summaries = summariser.Summarise_abstracts(abstracts)
        
        # Verify results
        assert len(summaries) == 3
        assert summaries == ["Summary 1", "Summary 2", "Summary 3"]
        assert mock_summarise.call_count == 3
    
    @patch('abstract_summariser.AbstractSummariser.summarise')
    def test_summarise_abstracts_with_errors(self, mock_summarise):
        """Test handling of errors during batch summarization"""
        # Setup mock to raise an exception on the second abstract
        def side_effect(text):
            if text == "Abstract 2":
                raise Exception("Test error")
            return f"Summary of {text}"
        
        mock_summarise.side_effect = side_effect
        
        # Create summariser and test
        summariser = AbstractSummariser()
        abstracts = ["Abstract 1", "Abstract 2", "Abstract 3"]
        summaries = summariser.Summarise_abstracts(abstracts)
        
        # Verify results
        assert len(summaries) == 3
        assert summaries[0] == "Summary of Abstract 1"
        assert "Error" in summaries[1]
        assert summaries[2] == "Summary of Abstract 3"