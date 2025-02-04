# Truviq_System

# LinkedIn Job Scraper

## Overview
This project is a LinkedIn job scraper that allows users to extract job listings from LinkedIn. The scraped data includes job titles, company names, job descriptions, and more.

## Prerequisites
Before running the script, ensure that your system meets the following requirements:
- **Operating System:** Windows, macOS, or Linux
- **Python Version:** Python 3.7 or later
- **Google Chrome** (latest version)
- **ChromeDriver** (matching your Chrome version)

## Installation Guide

### Step 1: Install Git (if not already installed)
#### **Windows**
1. Download Git from [git-scm.com](https://git-scm.com/downloads)
2. Run the installer and follow the setup instructions
3. Verify installation by running:
   ```sh
   git --version
   ```

#### **macOS**
1. Install Git using Homebrew:
   ```sh
   brew install git
   ```
2. Verify installation:
   ```sh
   git --version
   ```

#### **Linux**
1. Install Git using the package manager:
   ```sh
   sudo apt install git  # Debian/Ubuntu
   sudo yum install git  # CentOS/RHEL
   ```
2. Verify installation:
   ```sh
   git --version
   ```

### Step 2: Clone the Repository
```sh
git clone https://github.com/your-repo/linkedin-job-scraper.git
cd linkedin-job-scraper
```

### Step 3: Install Python Dependencies
Ensure you have Python 3 installed, then install the required dependencies:
```sh
pip install -r requirements.txt
```

### Step 4: Download and Set Up ChromeDriver
1. Find your **Google Chrome version** by navigating to:
   - **Windows/macOS/Linux:** Open Chrome and go to `chrome://settings/help`
2. Download the matching **ChromeDriver** from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
3. Extract the ChromeDriver and move it to the project directory

## Running the Scraper

### Configure the Scraper
- Open `Main.py` in a text editor.
- Modify the `URLS` list with LinkedIn job search URLs you want to scrape.

### Run the Scraper
```sh
python Main.py
```
The script will display a progress bar as it scrapes each URL, and the extracted job data will be saved in `linkedin-jobs.csv`.

## Structure of Scraped Data
| Column Name     | Definition                                        |
| --------------- | ------------------------------------------------- |
| title           | Title of the job listing                          |
| full_url        | LinkedIn URL of the job posting                   |
| company         | Name of the company                              |
| company_url     | Company's LinkedIn URL                            |
| location        | Job's location                                    |


## Notes
- Ensure that you comply with LinkedIn's scraping policies and terms of service.
- If the script encounters issues, check if ChromeDriver is compatible with your Chrome version.



