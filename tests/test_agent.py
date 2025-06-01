import pytest
from unittest.mock import Mock, patch
import json
from agent import Agent

class TestAgent:
    
    def test_init(self):
        """Test Agent initialization"""
        agent = Agent()
        assert isinstance(agent, Agent)
        
        # Test with custom parser
        mock_parser = Mock()
        agent = Agent(parser=mock_parser)
        assert agent.parser == mock_parser
    
    @patch('instruction_parser.InstructionParser.parse_file')
    @patch('Controller.Controller.execute_actions')
    def test_run_success(self, mock_execute_actions, mock_parse_file, sample_parsed_actions, sample_structured_output):
        """Test successful execution of the agent"""
        # Setup mocks
        mock_parse_file.return_value = sample_parsed_actions
        mock_execute_actions.return_value = json.dumps(sample_structured_output)
        
        # Create agent and run
        agent = Agent()
        result = agent.run("test_instructions.txt")
        
        # Verify results
        mock_parse_file.assert_called_once_with("test_instructions.txt")
        mock_execute_actions.assert_called_once_with(sample_parsed_actions)
        
        # Result should be a JSON string representing the sample_structured_output
        output = json.loads(result)
        assert "papers" in output
        assert len(output["papers"]) == 2
    
    @patch('instruction_parser.InstructionParser.parse_file')
    def test_run_parser_error(self, mock_parse_file):
        """Test handling of parser errors"""
        # Setup mock to raise an exception
        mock_parse_file.side_effect = ValueError("Invalid instructions file")
        
        # Create agent and run
        agent = Agent()
        result = agent.run("invalid_file.txt")
        
        # Result should be a JSON string with an error message
        output = json.loads(result)
        assert "error" in output
        assert "Invalid instructions file" in output["error"]
    
    @patch('instruction_parser.InstructionParser.parse_file')
    @patch('Controller.Controller.execute_actions')
    def test_run_execution_error(self, mock_execute_actions, mock_parse_file, sample_parsed_actions):
        """Test handling of execution errors"""
        # Setup mocks
        mock_parse_file.return_value = sample_parsed_actions
        mock_execute_actions.side_effect = Exception("Failed to execute actions")
        
        # Create agent and run
        agent = Agent()
        result = agent.run("test_instructions.txt")
        
        # Result should be a JSON string with an error message
        output = json.loads(result)
        assert "error" in output
        assert "Failed to execute actions" in output["error"]
    
    @patch('agent.Agent.run')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function(self, mock_parse_args, mock_run, capsys):
        """Test the main function"""
        # Setup mocks
        mock_args = Mock()
        mock_args.instructions_file = "test_instructions.txt"
        mock_parse_args.return_value = mock_args
        
        mock_run.return_value = json.dumps({"result": "success"})
        
        # Import main function and run it
        from agent import main
        exit_code = main()
        
        # Verify results
        mock_run.assert_called_once_with("test_instructions.txt")
        assert exit_code == 0
        
        # Check stdout
        captured = capsys.readouterr()
        assert '{"result": "success"}' in captured.out