# Agent: Frontier-Agent-TakeHome
## Mohammed AbuSadeh - Submission for the Frontier Health Take Home Test (Applied AI Engineer)

This project implements an Agentic workflow by executing a user-provided sequential list of tasks. 


# Overview
The Agent workflow follows a user-provided text input asking to perform 4 actions ("goto", "extract", "summarise", "Return"). The system uses a modular design pattern that utilises dependency injection to make components replaceable and testable which splits into the following tasks: 

1. Parse instructions from a text file
2. Navigate to web pages
3. Extract specific information (titles, authors, links, abstracts)
4. Summarise content using AI models (Google's Gemini or local Llama model)
5. Return structured JSON output

## System Design
┌─────────────────────┐  
│ Instruction Parser  │   
└─────────┬───────────┘  
          │  
          ▼  
┌─────────────────────┐      ┌─────────────────────┐  
│     Controller      │<─────│   Action Executor   │  
└─────────┬───────────┘      │                     │  
          │                  │ - Web Scraper       │  
          ▼                  │ - Data Extractor    │  
┌─────────────────────┐      │ - AI Summariser     │  
│  Output Formatter   │      └─────────────────────┘  
└─────────────────────┘  
  
## Main Project Structure
Frontier-Agent-TakeHome/  
├── agent.py                 # Main entry point for the agent workflow  
├── instruction_parser.py    # Parses user-provided instructions into structured actions  
├── Controller.py            # Orchestrates the execution of parsed instructions  
├── web_scraper.py           # Handles web scraping tasks (fetching and parsing web pages)  
├── items_extractor.py       # Extracts specific data (titles, authors, links, abstracts) from web pages  
├── abstract_summariser.py   # Summarises abstracts using AI models (Google Gemini or Llama)  
├── Output_Structurer.py     # Formats and structures the extracted data into JSON  
├── README.md                # Project documentation and usage instructions  
├── requirements.txt         # List of Python dependencies required for the project  
├── agent.log                # Log file for debugging and tracking the agent's execution  
└── test_instructions.txt           # Sample input file for testing the agent  


## Installation
### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup
1. Clone the repository from GitHub:
```bash
git clone git@github.com:Mo-abusadeh/Frontier-Agent-TakeHome.git
```

2. Navigate to the cloned repository:
```bash
cd Frontier-Agent-TakeHome
```

3. Install required dependencies
```bash
pip install -r requirements.txt
```

4. Set Google Gemini's API Key as an environment variable (alternatively pass the key explicity when instantiating the class)
```bash
set GEMINI_API_KEY="your_key_here" # windows
export GEMINI_API_KEY="your_key_here" # linux/mac
```

### Test Environment Setup
1. Install Testing Dependencies:
```bash
pip install -r requirements-test.txt
```

2. Run Unit Tests:
```bash
pytest tests/
```

## Test Directory Structure
tests/
├── __init__.py            # Makes tests directory a package
├── conftest.py            # Shared fixtures and setup
├── test_agent.py          # Tests for Agent class
├── test_controller.py     # Tests for Controller class
├── test_instruction_parser.py  # Tests for InstructionParser class
├── test_items_extractor.py     # Tests for ItemsExtractor class
├── test_abstract_summariser.py # Tests for AbstractSummariser class
├── test_output_structurer.py   # Tests for OutputStructurer class
└── test_web_scraper.py    # Tests for WebScraper class


### Usage
To run the Agent, run the following command: 
```bash
python agent.py test_instructions.txt
```

### Sample Instructions File
Create a text file with instructions in the following format:
```
- goto: https://arxiv.org/search/?query=grpo&searchtype=all&source=header
- extract title, authors, and links
- summarise abstracts
- Return the data in a structured format: ```{"papers": {"title": <title>, "authors: <>, "link": <link>, "summary": <summary>}}```
```

### Output
The agent will return structured JSON data containing the extracted and summarised information:

```
{
  "papers": [
    {
      "title": "Paper Title 1",
      "authors": ["Author 1", "Author 2"],
      "link": "https://arxiv.org/abs/xxxx.xxxxx",
      "summary": "Summarised content of the paper..."
    },
    {
      "title": "Paper Title 2",
      "authors": ["Author 3", "Author 4"],
      "link": "https://arxiv.org/abs/yyyy.yyyyy",
      "summary": "Summarised content of the paper..."
    }
  ]
}
```

## Technical Choices

### Web scraping
The python libraries **Requests** and **BeautifulSoup** were used for the web scraping module for the HTTP request and the access to the different items in the HTML file.  

### Model Choice
In this system, the default model inference is done on Google's Gemini via API calls, but the implementation provides two fallback alternatives in the case that the Gemini API method fails to work. The variant "gemini-2.0-flash-lite" is used since it is mainly used for simple and easy tasks that dont introduce a lot of complexity such as summarising the abstracts. 

The fallback alternative to Gemini is the use of **llama-cpp-python** locally on the machine by downloading a quantised small Llama model from the HuggingFace Hub. The model llama-2-7b-chat.gguf is used for its smaller size (7 billion parameters) and its robustness at handling a simple task such as summarising the abstracts of the papers on the webiste. One third and last fallback mechanism is also implemented just in case neither models work properly, and this method would just retrieve the first couple of sentences from the abstract instead of its summary.

1. Google's Gemini API (Default if API key is provided)
- Uses the Gemini-
- Requires an API key from Google AI Studio
- Much Faster inference time
- Higher quality summarisations
- Internet connection required


2. Local Llama Model (Fallback option)
- Downloads a quantized Llama 2 model (7B parameters)
- Works offline
- Requires more computational resources
- Lower quality but still functional summarisations


3. Simple Extraction (Last fallback)
- Uses the first few sentences if neither model works
- No AI summarization


### Error Handling
The system includes comprehensive error handling with logging at multiple levels to track execution and identify issues.

### Fallback Mechanisms
Multiple fallback options ensure the agent can still function if:

- No Gemini API key is provided
- The local model fails to load
- Web requests fail or page structure changes

## Technical Assumptions: 
- **Standard input format:** The input text follows the same layout as the provided text.
- **HTML Structure:** (in items_extractor.py) The HTML structure matches the selectors used in the code (e.g., p.title.is-5, p.authors, abstract-short). If the structure was changed, the selectors will need to be updated.
- **Environment Variable for API Key:** GEMINI_API_KEY is saved as an environment variable or else the user must change the input of the instantiation of the file.
- **External Module Compatibility:** The project supports the use of external modules as long as the arguments and the return types are the same.
- **Dependencies:** The project relies on installing the required dependency libraries to be able to use all the necessary tools. 
- **Local Llama Model:** The local Llama model is downloaded from HuggingFace and requires sufficient computational resources to run.
- **Error Handling:** The system assumes that the errors coming from one module will not stop the entire workflow, placeholders are used instead in the output (e.g., "Summary unavailable due to processing error."). 


## Potential Improvements with more time

### Practical Improvements
1. **Better Data Extraction**
    - Provide support for different types of data (tables, images, PDFs). 
2. **Expand Types of Preformable Actions**
    - Provide support for more complex instructional patterns such as using natural language understanding for less structured data to perform more ambiguous tasks. 
3. **Support for Web Interactions**
    - support for JavaScript-rendered content (Playwright and Selenium).
4. **Improved Model Selection**
    - Dynamically select the most appriopriate model to the specific use case or the complexity of the task.
5. **Parallel Processing**
    - Processing different sources (e.g. papers) at the same time for more efficient output generation. 
6. **User Interface**
    - Implement a user interface to query the model in a search portal and generate better visualisation of the structured data such as in a table format. 

### AI Engineering Feature Improvements
1. **Retrieval Augmented Generation (RAG)** Applications for any of the following features: 
    - Retrieve scientific background information about the topic and generate more comprehensive summaries.
    - Answer follow up questions about the retrieved data by using it as the context to the LLM.
    - Categorising papers into different research domains and discussed topics form the extracted data to form a knowledge graph.
2. **Dynamic Tool Use**
    - Allow the agent to call functions and specific tools appropriate to the task from a registry of functions, for domain-specific tasks. like in managing filing frameworks for medical files. 
3. **Chain-of-Thought Paradigm**
    - Have the agent plan steps before execution.
    - Provide the ability for the agent to evaluate and "self-reflect" it own outputs, by using "think-act-observe" cycles.



## Uses of LLM (Claude 3.7 Sonnet by Anthropic): 
- Instructions on how to use the **requests** and the **BeautifulSoup** libraries.
- I gave detailed instructions of the design decisions I have taken for my project, and the different modules that I need to implement, and asked it to describe the methods I should be implementing in each corresponding class. 
- I asked it to help me figure out the optimal workflow sequence to have a robust and error tolerant integration of the modules.
- Asked the LLM for optimal places in the code where I would implement error handling.
- Gave the LLM the different variations/parameters of tests I want to implement in my Unit Tests, and generated the majority of the testing code from the LLM, then did some minor fixes to the generated testing code. 


### Uses of online Resources: 
- https://beautiful-soup-4.readthedocs.io/en/latest/
- https://www.geeksforgeeks.org/python-requests-tutorial/
- https://ai.google.dev/gemini-api/docs/structured-output?lang=python 
- https://huggingface.co/docs/hub/en/index
- https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF


## NOTE: If want to explicitly use the local Llama Model
Go to the "abstract_summariser.py" file and comment out the following line:
```python
self.api_key = api_key or os.environ.get("GEMINI_API_KEY") # COMMENT OUT TO USE Llama
``` 
Then uncomment the following line: 
```python
#self.api_key = api_key # UNCOMMENT TO USE Llama
```

Then run the program as usual using: 
```bash
python agent.py test_instructions.txt
```
