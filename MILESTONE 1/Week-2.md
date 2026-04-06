# Documentation 


## Week 2 – Target Scanning Module Implementation

### Objective of Week 2

The primary objective of Week 2 was to develop an automated crawling mechanism capable of discovering the attack surface of the target web application.

This involved:

- Automatically exploring internal pages
- Extracting HTML forms
- Identifying input parameters
- Structuring discovered metadata
- Saving results for future vulnerability testing modules

### 1. Crawler Module Development (crawler.py)

During Week 2, a recursive crawler was implemented inside the scanner module.
The crawler performs the following tasks:
- Sends authenticated HTTP requests using session object
- Parses HTML content using BeautifulSoup
- Extracts <form> elements
- Identifies <input> fields within each form
- Extracts form action URL
- Identifies HTTP method (GET or POST)
- Recursively visits internal links
- Avoids duplicate crawling using a visited set
  
This ensures complete internal attack surface mapping.

<img width="658" height="585" alt="image" src="https://github.com/user-attachments/assets/35c0afaa-83d9-4091-9d87-9a571031a4cb" />

### 2. Attack Surface Discovery
After successful authentication, the crawler explored the DVWA application and discovered multiple vulnerability modules including:

- SQL Injection
- XSS (Reflected, Stored, DOM)
- Command Injection
- File Upload
- CSRF
- Brute Force
- File Inclusion
- Authentication modules
  
The crawler identified all form-based input points across these modules.

<img width="705" height="554" alt="image" src="https://github.com/user-attachments/assets/4c208072-b6eb-428a-9eea-97e4ea0ebae2" />

### 3. Results Obtained

The crawler successfully discovered:

- Target URL: http://localhost:8081
- Total Forms Identified: 22
  
Each discovered form includes:

- Action endpoint
- HTTP request method
- Input parameter names
- Input types
  
This confirms successful attack surface mapping.


### 4. Structured Metadata Storage (JSON Output)

The extracted data was saved into:

reports/results.json

The JSON structure contains:
- target → Base application URL
- total_forms → Total discovered forms
- forms → List of structured form objects

This structured format allows seamless integration with SQL Injection and XSS testing modules in the next milestone.

<img width="545" height="637" alt="image" src="https://github.com/user-attachments/assets/7c5e027e-a4ba-4d93-aad5-e9b6bffbc990" />

### 5. Technical Significance of Week 2

Week 2 established the foundational layer of the scanner by:

- Automating page discovery
- Identifying injection points
- Structuring attack surface data
- Enabling modular vulnerability testing
- Without this stage, automated vulnerability detection would not be possible.

### 6. Outcome of Week 2

By the end of Week 2, the system was capable of:

- Authenticating with the application
- Recursively crawling internal endpoints
- Extracting form-based input parameters
- Persisting structured metadata
- Preparing input data for SQL Injection and XSS modules
This successfully completed the Target Scanning Module as defined in Milestone 1.

