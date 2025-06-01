import logging 
import json

class OutputStructurer:
    def structure_output(self, info):
        """
        Structured Output Generator

        Args: 
            info: (str)

        Returns: 
            (json)

        """

        logging.info("Starting Output Structuring...")

        # Initialise info sructs
        output = {"papers": []}
        lengths = []

        # Lengths of lists: 'title', 'authors', 'link', and 'summary'
        for key in ['title', 'authors', 'link', 'summary']:
            # default an empty list for missing key
            length = len(info.get(key, []))
            lengths.append(length)

        # When no lengths appended this returns the default JSON
        if not lengths:
            return json.dumps(output, indent=2)

        # Iterate through the lengths to find the minimum nonzero value
        num_papers = None

        for length in lengths:
            if length > 0:
                if num_papers is None or length < num_papers:
                    num_papers = length

        if num_papers is None:
            return json.dumps(output, indent=2)  # Return empty papers array

        # collect paper objects
        for i in range(num_papers):
            paper = {
                "title": info.get('title', [])[i] if i < len(info.get('title', [])) else "",
                "authors": info.get('authors', [])[i] if i < len(info.get('authors', [])) else [],
                "link": info.get('link', [])[i] if i < len(info.get('link', [])) else "",
                "summary": info.get('summary', [])[i] if i < len(info.get('summary', [])) else ""
            }
            output['papers'].append(paper)
        
        return json.dumps(output, indent=2)
