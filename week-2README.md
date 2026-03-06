📅 Week 2: Target Scanning Module
🎯 Objective

Develop an automated crawler to scan the target application and extract important testing data.

🛠 Technologies Used

Python

requests library

BeautifulSoup (bs4)

Visual Studio Code

🔍 Crawler Features

The crawler:

Discovers internal web pages

Extracts hyperlinks

Identifies forms

Detects input fields (text, password, textarea, select)

Avoids visiting duplicate pages

📊 Metadata Collection

The crawler collects:

URL list

Form action

Form method (GET/POST)

Input name

Input type

This metadata is stored for future vulnerability testing modules.

▶ How to Run

Ensure Apache and MySQL are running

Open terminal in project folder

Run:

python crawler.py


Output will display discovered pages and form details

✅ Week 2 Outcome

✔ Automated web page discovery
✔ Form and input field extraction
✔ Structured metadata collection
✔ Ready for vulnerability testing module

📁 Project Structure
WebScanPro/
│
├── crawler.py
├── README.md
└── requirements.txt
