from instruction_parser import InstructionParser
from Controller import Controller
import sys
import json 
import argparse
import logging

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('agent.log')
    ]
)

logger = logging.getLogger('agent')
logger.setLevel(logging.INFO)
logger.propagate = False  # This prevents propagation to the root logger

class Agent: 
    """
    Main class to run the Agent
    """

    def __init__(self, parser=None):
        """
        Initialise the parser method and the agent controller

        Args:
            parser: (func)
        """

        self.parser = parser if parser is not None else InstructionParser()
        self.controller = Controller() # supports call for custom components/modules as an arg


    def run(self, instructions_file_path):
        """
        Run the AI Agent to follow the instructions sequentially

        Args: 
            Instructions file path: (str)

        Returns: 
            workflow output: (json)

        """
        try: 

            logging.info(f"Running Agent to follow {instructions_file_path}")

            # running the instruction parser
            actions = self.parser.parse_file(instructions_file_path)
            logging.info(f"Agent: Parsed the instructions file successfully")

            # Execute actions
            workflow_output = self.controller.execute_actions(actions)
            logging.info("Agent: Executed actions successfully")

            return workflow_output
        
        except Exception as e:
            logging.error(f"Agent workflow failed: {str(e)}")
            return json.dumps({"error": str(e)})


def main():
    """Main entry point for command-line execution."""

    parser = argparse.ArgumentParser(description="AI Agent that follows instructions")
    parser.add_argument("instructions_file", help="Path to the instructions file")
    
    args = parser.parse_args()
    
    agent = Agent()
    result = agent.run(args.instructions_file)
    
    # Print result
    print(result)
    return 0

if __name__ == "__main__":
    sys.exit(main())