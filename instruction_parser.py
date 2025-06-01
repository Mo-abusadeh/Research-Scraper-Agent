from typing import List, Dict, Any
import re

class InstructionParser:
    """Parses instructions from a text file and then executes the defined actions."""
    
    def __init__(self): 
        # Accounting for different variations of each item
        self.action_styles = {
            "goto": r"goto:\s*(https?://\S+)",
            "extract": r"extract\s+(.+?)(?=$|\n|-\s)",
            "summarise": r"summari[sz]e\s+(.+?)(?=$|\n|-\s)",
            "Return": r"Return the data in a structured format:\s*```(.+?)```"
        }


    def parse_text(self, text):
        """
        Function for parsing text lines into instructions and actions
        
        Args: 
            text: (str)
        
        Returns: 
            actions: (list)
        """
        
        # Convert multiple new lines to single new line
        cleaned_text = re.sub(r"\n+", "\n", text)
        
        # Take every line starting with - as a new instruction        
        instructions = []
        for line in cleaned_text.split("\n"):
            line = line.strip()  # Remove leading and trailing whitespaces
            if line.startswith("-"):
                instructions.append(line)

        # Associate every line with an action
        actions = []
        output = None

        for line in instructions:
            line = line[1:].strip()  # Remove the leading -

            for action_type, input_style in self.action_styles.items():
                match = re.search(input_style, line, re.IGNORECASE)
                
                # Parse instructions under every respective action
                if match: 
                    # Parsing "goto"
                    if action_type == "goto": 
                        action = {
                            "type": "goto",
                            "url": match.group(1)
                        }
                    
                    # Parsing "extract"
                    elif action_type == "extract":
                        extracted_items = []
                        for item in match.group(1).split(","): 
                            extracted_items.append(item.strip())

                        # Handling the case for when there is "and" before the last item in executing "extract"
                        if len(extracted_items) > 1 and "and" in extracted_items[-1]:
                            # Remove last item from list and split "and"
                            last_item = extracted_items.pop().split("and")
                            # Extend the extract_items list with cleaned items from last_items
                            for item in last_item:
                                cleaned_item = item.strip()  # Remove leading and trailing whitespaces
                                if cleaned_item: # Add only non-empty items
                                    extracted_items.append(cleaned_item)  # Add the cleaned item to extract_items
                        
                        action = {
                            "type": "extract",
                            "items": extracted_items
                        }
                    
                    # Parsing "summarise"
                    elif action_type == "summarise": 
                        action = {
                            "type": "summarise",
                            "abstract": match.group(1) 
                        }

                    # Parsing "Return"
                    elif action_type == "Return": 
                        action = {
                            "type": "Return", 
                            "structured_format": match.group(1)
                        }
                    
                    else: 
                        action = None

                
            if action:
                if action["type"] == "Return":
                    output = action["structured_format"]
                else: 
                    actions.append(action)

        # Assign the action to the structured output
        if output is not None: 
            actions.append({
                "type": "Return",
                "structured_output": output
            })
        
        return actions


    def parse_file(self, file_path):
        """
        Function for parsing the text content in the prompt file

        Args: 
            file_path: (str)

        Returns: (list)


        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            return self.parse_text(content)
        except FileNotFoundError:
            raise ValueError(f"Prompt text file is not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error in reading the prompt text file: {str(e)}")