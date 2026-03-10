# WebScanPro - Comprehensive Documentation

## Table of Contents
- Project Overview
- System Architecture
- Component Documentation
- API Key Setup
- Installation & Setup
- Running the Application
- API Documentation
- Testing & Usage Examples
- Deployment Guide
- Hugging Face Deployment

---

## Project Overview

WebScanPro is an automated web application security scanner that detects SQL Injection Testing, Cross-Site Scripting (XSS), Testing Authentication, Session Testing Access Control, IDOR Testing vulnerabilities. It features an AI-powered adaptive testing engine using Google's Gemini AI to generate sophisticated attack payloads based on server responses.

### Key Features
- Automated web crawling and form detection
-  SQL Injection testing with multiple techniques
-  XSS vulnerability detection
-  AI-driven payload generation (Gemini 2.5 Flash)
-  Adaptive testing based on server responses
-  Session management for authenticated scanning
-  FastAPI-based REST API

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Application                    │
│                      (Browser / API Client)                  │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP Requests
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Server (app.py)                 │
│                         Port: 8000                           │
│                      CORS: All Origins                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                        Scanner Core                          │
│                      (scanner.py)                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Crawler   │  │   SQL       │  │   GeminiFeedback    │ │
│  │  (crawler.py)│◄─┤   Injector  │  │   Agent            │ │
│  └─────────────┘  │(sql_injection│  │(sql_generator.py)   │ │
│         │         │    .py)      │  └─────────────────────┘ │
│         ▼         └─────────────┘              ▲            │
│  ┌─────────────┐         │                     │            │
│  │  Form       │         │                     │            │
│  │  Detection  │         │                     │            │
│  └─────────────┘         │                     │            │
│         │                 ▼                     │            │
│         └──────────►┌─────────────┐            │            │
│                     │   XSS       │            │            │
│                     │  Injector   │────────────┘            │
│                     │  (xss.py)   │                         │
│                     └─────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Target Web Application                  │
│                    (e.g., DVWA, Test Site)                   │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
┌──────────┐   1. Scan Request    ┌──────────┐
│  Client  │──────────────────────►│  FastAPI │
└──────────┘                       └──────────┘
                                         │
                                         │ 2. Initialize Scanner
                                         ▼
                                   ┌─────────────┐
                                   │   Scanner   │
                                   └─────────────┘
                                         │
                      ┌──────────────────┼──────────────────┐
                      │ 3. Crawl         │ 4. For each form │
                      ▼                  ▼                   ▼
                ┌─────────────┐   ┌─────────────────┐ ┌─────────────┐
                │  Crawler    │──►│ Form Detection │ │ SQL Injector│
                └─────────────┘   └─────────────────┘ └─────────────┘
                                         │                   │
                                         │                   │ 5. Seed Payloads
                                         ▼                   ▼
                                   ┌─────────────────────────────────┐
                                   │     Payload Testing Loop        │
                                   └─────────────────────────────────┘
                                         │                   │
                                         │ 6. Results        │ 7. AI Refinement
                                         ▼                   ▼
                                   ┌─────────────┐   ┌─────────────┐
                                   │   History   │◄─►│    Gemini   │
                                   └─────────────┘   │     Agent   │
                                                     └─────────────┘
                                         │
                                         │ 8. Final Results
                                         ▼
                                   ┌─────────────┐
                                   │   JSON      │
                                   │  Response   │
                                   └─────────────┘
                                         │
                                         ▼
┌──────────┐   9. Scan Results   ┌──────────┐
│  Client  │◄─────────────────────│  FastAPI │
└──────────┘                      └──────────┘
```

---

## Component Documentation

### 1. **app.py** - FastAPI Server
**Purpose**: Main entry point for the application, exposing REST API endpoints.

**Key Functions**:
- `health()`: GET endpoint for server health check
- `get_web()`: POST endpoint to initiate security scan

**Dependencies**:
- FastAPI
- CORS middleware
- Pydantic models

### 2. **scanner.py** - Scanner Core
**Purpose**: Orchestrates the entire scanning process.

**Class: `Scaner`**
- `__init__(base_url)`: Initializes scanner with target URL
- `crawl()`: Main scanning workflow
  - Crawls target website
  - Detects forms
  - Tests SQL injection with seed payloads
  - Uses AI for adaptive testing

**Key Logic**:
- Maintains session across requests
- Integrates crawler, injector, and AI components
- Returns comprehensive attack results

### 3. **crawler.py** - Web Crawler
**Purpose**: Discovers and extracts forms from target website.

**Class: `WebCrawler`**
- `__init__(base_url, session)`: Initializes with base URL and session
- `scan(url)`: Recursively crawls URLs within same domain
- `get_inputs(soup, url)`: Extracts form details from HTML
- `run()`: Starts crawling from base URL

**Form Detection**:
- Extracts form action URLs
- Identifies input fields (text, textarea)
- Preserves baseline page length for comparison
- Handles relative/absolute URLs

### 4. **sql_injection.py** - SQL Injection Tester
**Purpose**: Tests for SQL injection vulnerabilities.

**Class: `SQLInjector`**
- `__init__(timeout)`: Sets up session with timeout
- `login()`: Handles DVWA authentication
- `send_payload(form, payload)`: Sends payload to target form
- `analyze_response(response, delay, baseline_len)`: Analyzes response for vulnerabilities

**Detection Methods**:
- Error-based SQL injection (database error messages)
- Time-based blind SQL injection (delay > 5 seconds)
- Boolean-based blind SQL injection (content length diff > 500)

### 5. **xss.py** - XSS Tester
**Purpose**: Tests for Cross-Site Scripting vulnerabilities.

**Class: `XSSInjector`**
- `__init__(session)`: Initializes with shared session
- `send_payload(form, payload)`: Sends XSS payload
- `analyze_response(response, payload)`: Checks if payload is reflected

**Detection Methods**:
- Checks if payload appears in response
- Verifies if payload is in executable contexts (script, img, body, svg tags)
- Differentiates between sanitized and unsanitized reflections

### 6. **sql_generator.py** - AI Payload Generator
**Purpose**: Uses Google's Gemini AI to generate adaptive SQL injection payloads.

**Class: `GeminiFeedbackAgent`**
- `__init__()`: Loads API key from environment, configures Gemini
- `is_valid_sql(payload)`: Validates SQL syntax
- `generate_refined_payloads(attempt_response_dict)`: Uses AI to generate new payloads based on previous attempts
- `adaptive_loop(tester_func, initial_history, max_rounds)`: Manages adaptive testing rounds

**AI Integration**:
- Sends attempt history to Gemini
- Receives JSON array of refined payloads
- Limits to 2 payloads per round
- Validates SQL syntax before use

---

## API Key Setup

### 1. **Google Gemini API Key**
Required for AI-powered payload generation.

**Steps to obtain:**
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click on "Get API Key" or navigate to API keys section
4. Create a new API key
5. Copy the generated key

### 2. **SerpAPI Key** (Optional)
For future search engine integration.

**Steps to obtain:**
1. Visit [SerpAPI](https://serpapi.com/)
2. Sign up for an account
3. Navigate to Dashboard → API Key
4. Copy your API key

### 3. **Firebase Credentials** (Optional)
For future database integration.

**Steps to obtain:**
1. Visit [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Go to Project Settings → Service Accounts
4. Generate new private key
5. Download the JSON file

### Environment Setup

Create a `.env` file in the root directory:

```env
# Required
GEMINI_API_KEY='your-gemini-api-key-here'

# Optional
Serp_API='your-serpapi-key-here'
FIREBASE_CREDENTIALS_PATH='serviceAccountKey.json'
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/Akshaj-mishra/WebScanPro.git
cd WebScanPro
cd backend
# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.venv\Scripts\activate


# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file with API keys wit the help of .env.example
# Edit .env with your actual API keys

```

### Requirements File (requirements.txt)
```txt
fastapi==0.104.1
uvicorn==0.24.0
requests==2.31.0
beautifulsoup4==4.12.2
google-generativeai==0.3.0
python-dotenv==1.0.0
sqlparse==0.4.4
pydantic==2.4.2
```

---

## Running the Application

### Development Server

```bash
# Start the FastAPI server
uvicorn app:app --reload 
```

### Verify Server is Running

```bash
# Health check
curl http://localhost:8000/

# Expected response:
{"message":"FastAPI backend running"}
```

---

## API Documentation

### Endpoints

#### 1. **GET /** - Health Check
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
    "message": "FastAPI backend running"
}
```

#### 2. **POST /result** - Start Security Scan
```bash
curl -X POST http://localhost:8000/result \
  -H "Content-Type: application/json" \
  -d '{"url": "http://testphp.vulnweb.com/"}'
```

**Request Body:**
```json
{
    "url": "http://target-website.com"
}
```

**Response Structure:**
```json
{
    "status": "Target Scanning Complete",
    "target_url": "http://target-website.com",
    "metadata": [
        {
            "url": "http://target-website.com/page",
            "results": {
                "' OR 1=1--": "VULNERABLE: SQL Error Detected",
                "'/**/OR/**/1=1--": "Normal response",
                "' AND 1=2--": "Normal response",
                "' UNION SELECT NULL,NULL--": "VULNERABLE: SQL Error Detected",
                "' OR IF(1=1,SLEEP(5),0)--": "Normal response"
            }
        }
    ]
}
```

---

## Testing & Usage Examples

### Test with DVWA (Damn Vulnerable Web Application)

**Setup DVWA:**
```bash
# Using Docker
docker run --rm -it -p 80:80 vulnerables/web-dvwa

# Access at http://localhost
# Default credentials: admin/password
```

**Scan DVWA:**
```python
# Python script to test scanner
import requests
import json

url = "http://localhost:8000/result"
payload = {"url": "http://localhost/DVWA/"}

response = requests.post(url, json=payload)
results = response.json()

print(json.dumps(results, indent=2))
```

### Test with TestPHP Vulnerability Scanner

```bash
curl -X POST http://localhost:8000/result \
  -H "Content-Type: application/json" \
  -d '{"url": "http://testphp.vulnweb.com/"}'
```

### Sample Output Analysis

```json
{
  "status": "Target Scanning Complete",
  "target_url": "http://testphp.vulnweb.com/",
  "metadata": [
    {
      "url": "http://testphp.vulnweb.com/search.php",
      "results": {
        "' OR 1=1--": "VULNERABLE: SQL Error Detected",
        "' OR IF(1=1,SLEEP(5),0)--": "VULNERABLE: Time-based delay (5.23s)"
      }
    },
    {
      "url": "http://testphp.vulnweb.com/guestbook.php",
      "results": {
        "<script>alert(1)</script>": "VULNERABLE: Reflected XSS (Unsanitized)"
      }
    }
  ]
}
```

---

## Deployment Guide
#### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV GEMINI_API_KEY=${GEMINI_API_KEY}

EXPOSE 8000

CMD ["uvicorn", "main.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  webscanpro:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

**Build and run:**
```bash
docker-compose up -d
```

---

## Hugging Face Deployment

### Step-by-Step Hugging Face Spaces Deployment

#### 1. **Create Hugging Face Account**
- Go to [huggingface.co](https://huggingface.co/)
- Sign up for a free account
- Verify your email

#### 2. **Create New Space**
- Click on your profile → "New Space"
- Choose "Docker" as Space SDK
- Select a name (e.g., "webscanpro")
- Choose visibility (Public/Private)
- Click "Create Space"
