import os
import pytest
from bs4 import BeautifulSoup

# Get the fixtures directory
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

@pytest.fixture
def sample_html():
    """Sample HTML content for testing extractors"""
    return """
    <html>
    <body>
        <div class="results">
            <p class="title is-5">GRPO: A New Approach to Reinforcement Learning</p>
            <p class="authors">Authors: John Smith, Emily Jones, Michael Brown</p>
            <p class="list-title"><a href="/abs/2401.12345">arXiv:2401.12345</a></p>
            <span class="abstract-short">
                This paper introduces GRPO (Generalized Reward Policy Optimization), a novel approach to 
                reinforcement learning. We demonstrate superior performance on benchmark tasks compared to 
                existing methods. Our algorithm leverages a unique reward formulation that better captures 
                long-term dependencies and improves sample efficiency.
            </span>
            
            <p class="title is-5">Multi-Agent GRPO for Collaborative Environments</p>
            <p class="authors">Authors: Jane Doe, Robert Johnson</p>
            <p class="list-title"><a href="/abs/2402.54321">arXiv:2402.54321</a></p>
            <span class="abstract-short">
                We extend GRPO to multi-agent settings and show how it can be adapted for collaborative 
                environments. Our approach maintains individual agent policies while optimizing for team 
                rewards. Experiments show significant improvements in coordination and overall performance.
            </span>
        </div>
    </body>
    </html>
    """

@pytest.fixture
def sample_soup(sample_html):
    """BeautifulSoup parsed sample HTML"""
    return BeautifulSoup(sample_html, 'html.parser')

@pytest.fixture
def sample_instructions_text():
    """Sample instructions text for testing parser"""
    return """
    - goto: https://arxiv.org/search/?query=grpo&searchtype=all&source=header
    - extract title, authors, and links
    - summarise abstracts
    - Return the data in a structured format: ```{"papers": {"title": <title>, "authors: <>, "link": <link>, "summary": <summary>}}```
    """

@pytest.fixture
def sample_parsed_actions():
    """Sample parsed actions output"""
    return [
        {
            "type": "goto",
            "url": "https://arxiv.org/search/?query=grpo&searchtype=all&source=header"
        },
        {
            "type": "extract",
            "items": ["title", "authors", "links"]
        },
        {
            "type": "summarise",
            "abstract": "abstracts"
        },
        {
            "type": "Return",
            "structured_output": """{"papers": {"title": <title>, "authors: <>, "link": <link>, "summary": <summary>}}"""
        }
    ]

@pytest.fixture
def sample_extracted_data():
    """Sample data extracted from HTML"""
    return {
        "title": ["GRPO: A New Approach to Reinforcement Learning", 
                 "Multi-Agent GRPO for Collaborative Environments"],
        "authors": [
            ["John Smith", "Emily Jones", "Michael Brown"],
            ["Jane Doe", "Robert Johnson"]
        ],
        "link": ["https://arxiv.org/abs/2401.12345", "https://arxiv.org/abs/2402.54321"],
        "abstract": [
            "This paper introduces GRPO (Generalized Reward Policy Optimization), a novel approach to reinforcement learning. We demonstrate superior performance on benchmark tasks compared to existing methods. Our algorithm leverages a unique reward formulation that better captures long-term dependencies and improves sample efficiency.",
            "We extend GRPO to multi-agent settings and show how it can be adapted for collaborative environments. Our approach maintains individual agent policies while optimizing for team rewards. Experiments show significant improvements in coordination and overall performance."
        ]
    }

@pytest.fixture
def sample_summarised_abstracts():
    """Sample summarised abstracts"""
    return [
        "GRPO introduces a novel reinforcement learning approach with superior benchmark performance. The algorithm uses a unique reward formulation to capture long-term dependencies and improve sample efficiency.",
        "This paper extends GRPO to multi-agent collaborative environments. It maintains individual agent policies while optimizing team rewards, showing significant improvements in coordination and performance."
    ]

@pytest.fixture
def sample_state_data(sample_extracted_data, sample_summarised_abstracts):
    """Sample controller state after executing actions"""
    state = {
        "current_url": "https://arxiv.org/search/?query=grpo&searchtype=all&source=header",
        **sample_extracted_data,
        "summary": sample_summarised_abstracts
    }
    return state

@pytest.fixture
def sample_structured_output():
    """Expected structured output"""
    return {
        "papers": [
            {
                "title": "GRPO: A New Approach to Reinforcement Learning",
                "authors": ["John Smith", "Emily Jones", "Michael Brown"],
                "link": "https://arxiv.org/abs/2401.12345",
                "summary": "GRPO introduces a novel reinforcement learning approach with superior benchmark performance. The algorithm uses a unique reward formulation to capture long-term dependencies and improve sample efficiency."
            },
            {
                "title": "Multi-Agent GRPO for Collaborative Environments",
                "authors": ["Jane Doe", "Robert Johnson"],
                "link": "https://arxiv.org/abs/2402.54321",
                "summary": "This paper extends GRPO to multi-agent collaborative environments. It maintains individual agent policies while optimizing team rewards, showing significant improvements in coordination and performance."
            }
        ]
    }

@pytest.fixture
def sample_instructions_file(tmp_path):
    """Create a temporary file with sample instructions"""
    file_path = tmp_path / "test_instructions.txt"
    with open(file_path, 'w') as f:
        f.write("""
        - goto: https://arxiv.org/search/?query=grpo&searchtype=all&source=header
        - extract title, authors, and links
        - summarise abstracts
        - Return the data in a structured format: ```{"papers": {"title": <title>, "authors: <>, "link": <link>, "summary": <summary>}}```
        """)
    return file_path