# 🔒 Intelligent PII Redaction Tool

> A professional Python-based application for detecting and anonymizing Personally Identifiable Information (PII) in Microsoft Word documents while preserving the original formatting.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![spaCy](https://img.shields.io/badge/spaCy-NLP-green.svg)
![Presidio](https://img.shields.io/badge/Microsoft-Presidio-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📖 Overview

The **Intelligent PII Redaction Tool** is designed to automatically identify and replace sensitive personal information from Microsoft Word (.docx) documents.

The application combines:

- Microsoft Presidio
- spaCy Named Entity Recognition
- Regular Expressions

to provide accurate hybrid PII detection.

Instead of masking sensitive information, realistic fake values are generated using the **Faker** library while maintaining document readability.

The tool preserves:

- Paragraph formatting
- Tables
- Headers
- Footers
- Fonts
- Bold/Italic/Underline styles

making it suitable for preparing documents for sharing, testing, demonstrations, and research.

---

# ✨ Features

## 🔍 Hybrid PII Detection

- Regular Expression Detection
- spaCy Named Entity Recognition
- Microsoft Presidio Analyzer
- Duplicate Removal
- Overlap Resolution

---

## 🔒 Supported PII Types

| Entity | Supported |
|---------|-----------|
| Person Name | ✅ |
| Email Address | ✅ |
| Phone Number | ✅ |
| Company Name | ✅ |
| Address | ✅ |
| PAN Number | ✅ |
| Credit Card | ✅ |
| URL | ✅ |
| IP Address | ✅ |
| Date | ✅ |

---

## 📝 Intelligent Replacement

Instead of masking data:

```
John Doe
```

becomes

```
Michael Smith
```

Example:

Original

```
John Doe
john@gmail.com
9876543210
```

↓

Redacted

```
Michael Smith
andrew92@gmail.com
9156423810
```

using realistic fake values generated with **Faker**.

---

# 📂 Project Structure

```
PII-Redaction-Tool/

│
├── app.py
├── detector.py
├── redactor.py
├── fake_generator.py
├── requirements.txt
├── README.md
│
├── sample_documents/
│     sample_input.docx
│     sample_output.docx
│
├── screenshots/
│
├── logs/
│
└── LICENSE
```

---

# ⚙️ Technologies Used

- Python
- Streamlit
- spaCy
- Microsoft Presidio
- Faker
- python-docx
- Pandas
- Matplotlib

---

# 🏗 Architecture

```
             DOCX Document
                    │
                    ▼
         Document Parser (python-docx)
                    │
                    ▼
      Hybrid Detection Engine
      ├───────────────┐
      │               │
      ▼               ▼
   Regex          spaCy NER
      │               │
      └──────┬────────┘
             ▼
     Microsoft Presidio
             │
             ▼
      Duplicate Removal
             │
             ▼
     Fake Data Generator
             │
             ▼
   Format Preserving Replacement
             │
             ▼
     Redacted DOCX + CSV Log
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/PII-Redaction-Tool.git
```

Move into the project directory

```bash
cd PII-Redaction-Tool
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Download the spaCy model

```bash
python -m spacy download en_core_web_sm
```

---

# ▶ Running the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 📊 Dashboard

The Streamlit dashboard includes:

- Upload DOCX
- Hybrid PII Detection
- Real-time Progress
- Analytics Dashboard
- Entity Distribution
- Bar Chart
- Pie Chart
- CSV Log
- Download Redacted Document

---

# 📸 Screenshots

## Home

> *(Add screenshot here)*

---

## Upload Document

> *(Add screenshot here)*

---

## Analytics Dashboard

> *(Add screenshot here)*

---

## Redacted Output

> *(Add screenshot here)*

---

# 📁 Output

The application generates:

- Redacted DOCX document
- CSV Redaction Log

Example CSV

| Original | Fake | Entity |
|----------|------|---------|
| John Doe | Michael Smith | PERSON |
| john@gmail.com | david12@gmail.com | EMAIL |

---

# ⚡ Performance

Typical execution time

| Document Size | Time |
|---------------|------|
| 10 Pages | ~5 sec |
| 50 Pages | ~18 sec |
| 100 Pages | ~35 sec |
| 150 Pages | ~45 sec |

*(Times may vary depending on system configuration.)*

---

# 🎯 Applications

This project can be used for:

- Healthcare document anonymization
- Legal document redaction
- HR data anonymization
- Research datasets
- Educational projects
- Compliance demonstrations
- Software testing

---

# 🔮 Future Improvements

- PDF Support
- OCR for scanned documents
- Batch document processing
- Custom entity selection
- REST API
- Docker deployment
- Multi-language support

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository

2. Create a new branch

```
git checkout -b feature-name
```

3. Commit changes

```
git commit -m "Added new feature"
```

4. Push

```
git push origin feature-name
```

5. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Harshajeet Chanda**

Electronics & Communication Engineering

Python • AI • Machine Learning • NLP • Embedded Systems

---

⭐ If you found this project useful, consider giving it a **Star** on GitHub.