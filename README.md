# Evaluation Bias Data Retriever
This project extracts and aggregates public course evaluation data from a university's website into a comprehensive CSV file.

This script and data it produced is part of a research project investigating biases in student feedback. The resulting dataset helped reveal trends in student feedback and responses to surveys.

### Implementation Details

The script is designed to retrieve a high amount of data (thousands of entries) without spamming requests. This means it runs over a long period of time, with only minimal need for human intervention.

*   **Extraction:** Automatic extraction of data from webpages, using Selenium and BeautifulSoup.
*   **Testing:** Uses basic tests to determine the quality of the data.
*   **Ethics and Rate Limiting:** A minimum 30 second between requests delay is used, to abide by `robots.txt` rules

### Technical Stack

*   **Language:** Python 3.13
*   **Web Automation:** Selenium
*   **Parsing:** BeautifulSoup4 / Requests
*   **Data Processing:** Pandas
*   **Output:** CSV

### Usage and Ethics

Usage instructions and the institution's identity have been intentionally omitted. The code is provided here for transparency regarding the research methodology rather than for public redistribution or active scraping.
