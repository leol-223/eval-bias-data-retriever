# Public Course Data Retriever
This repository contains a Python-based utility developed to extract and aggregate course evaluation data from a public university database into a structured CSV format. 

The tool was built specifically to support a research project investigating biases in student feedback. By analyzing historical evaluation trends, the resulting dataset helped identify specific discrepancies in student responses following the implementation of centralized, easier-to-access survey platforms.

### Implementation Details

The script is designed to handle high-volume data retrieval while maintaining a low footprint on the host's infrastructure.

*   **Extraction:** Selenium-driven automation for navigating authenticated or session-heavy web interfaces.
*   **Session Persistence:** Uses a human-in-the-loop approach where session cookies are manually captured from a browser and injected into the automated instance. This bypasses common bot-detection challenges associated with headful/headless Chromium.
*   **Throughput:** Implements rotating proxies to distribute requests across multiple IP addresses.
*   **Ethics and Rate Limiting:** To remain compliant with the institution's `robots.txt` and prevent server strain, the script enforces a strict 30-second delay between requests.

### Technical Stack

*   **Language:** Python 3.13
*   **Web Automation:** Selenium
*   **Parsing:** BeautifulSoup4 / Requests
*   **Data Processing:** Pandas
*   **Output:** CSV

### Usage and Ethics

Usage instructions and the target institution's identity have been intentionally omitted. This tool was built for a specific academic inquiry, and the code is provided here for transparency regarding the research methodology rather than for public redistribution or active scraping.
