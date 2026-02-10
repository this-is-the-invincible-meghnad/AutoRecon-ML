# AutoRecon-ML: AI-Powered Reconnaissance Tool 🛡️

**AutoRecon-ML** is an automated footprinting and reconnaissance tool designed for Ethical Hackers and Penetration Testers. It automates the "boring" parts of the CEH methodology using Python and Machine Learning.

## 🚀 Features
* **Passive Recon:** Scrapes subdomains using Certificate Transparency logs (`crt.sh`) without touching the target.
* **Active Recon:** Automates Google Dorking to find exposed `.env` files, SQL backups, and admin panels.
* **AI Threat Analysis:** Uses a **Naive Bayes Classifier (Scikit-Learn)** to filter URLs and identify "High-Risk" targets automatically.
* **Tech Stack Fingerprinting:** Identifies server technologies (Nginx, Apache, PHP, etc.).
* **Employee Enumeration:** Extracts potential email addresses for social engineering audits.

## 🛠️ Installation
```bash
git clone [https://github.com/this-is-the-invincible-meghnad/AutoRecon-ML.git](https://github.com/this-is-the-invincible-meghnad/AutoRecon-ML.git)
cd AutoRecon-ML
pip install -r requirements.txt