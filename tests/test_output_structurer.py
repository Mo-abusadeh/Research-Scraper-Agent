import pytest
import json
from Output_Structurer import OutputStructurer

class TestOutputStructurer:
    
    def test_init(self):
        """Test OutputStructurer initialization"""
        structurer = OutputStructurer()
        assert isinstance(structurer, OutputStructurer)
    
    def test_structure_output_complete_data(self, sample_state_data):
        """Test structuring output with complete data"""
        structurer = OutputStructurer()
        json_output = structurer.structure_output(sample_state_data)
        
        # Convert JSON string to dict for easier assertions
        output = json.loads(json_output)
        
        assert "papers" in output
        assert isinstance(output["papers"], list)
        assert len(output["papers"]) == 2
        
        # Check first paper
        paper1 = output["papers"][0]
        assert paper1["title"] == "GRPO: A New Approach to Reinforcement Learning"
        assert paper1["authors"] == ["John Smith", "Emily Jones", "Michael Brown"]
        assert paper1["link"] == "https://arxiv.org/abs/2401.12345"
        assert "GRPO introduces a novel reinforcement learning approach" in paper1["summary"]
        
        # Check second paper
        paper2 = output["papers"][1]
        assert paper2["title"] == "Multi-Agent GRPO for Collaborative Environments"
        assert paper2["authors"] == ["Jane Doe", "Robert Johnson"]
        assert paper2["link"] == "https://arxiv.org/abs/2402.54321"
        assert "extends GRPO to multi-agent collaborative environments" in paper2["summary"]
    
    def test_structure_output_missing_data(self):
        """Test structuring output with missing data"""
        structurer = OutputStructurer()
        
        # Test with empty info dictionary
        json_output = structurer.structure_output({})
        output = json.loads(json_output)
        assert "papers" in output
        assert output["papers"] == []
        
        # Test with only titles
        info = {"title": ["Paper 1", "Paper 2"]}
        json_output = structurer.structure_output(info)
        output = json.loads(json_output)
        
        assert len(output["papers"]) == 2
        assert output["papers"][0]["title"] == "Paper 1"
        assert output["papers"][0]["authors"] == []
        assert output["papers"][0]["link"] == ""
        assert output["papers"][0]["summary"] == ""
    
    def test_structure_output_mismatched_lengths(self):
        """Test structuring output with mismatched data lengths"""
        structurer = OutputStructurer()
        
        # More titles than other fields
        info = {
            "title": ["Paper 1", "Paper 2", "Paper 3"],
            "authors": [["Author 1"], ["Author 2"]],
            "link": ["Link 1", "Link 2"],
            "summary": ["Summary 1"]
        }
        
        json_output = structurer.structure_output(info)
        output = json.loads(json_output)
        
        # Should use the shortest non-zero length (summary has 1 item)
        assert len(output["papers"]) == 1
        assert output["papers"][0]["title"] == "Paper 1"
        assert output["papers"][0]["authors"] == ["Author 1"]
        assert output["papers"][0]["link"] == "Link 1"
        assert output["papers"][0]["summary"] == "Summary 1"
    
    def test_structure_output_empty_lists(self):
        """Test structuring output with empty lists"""
        structurer = OutputStructurer()
        
        info = {
            "title": [],
            "authors": [],
            "link": [],
            "summary": []
        }
        
        json_output = structurer.structure_output(info)
        output = json.loads(json_output)
        
        assert output["papers"] == []