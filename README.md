# LinkedIn Job Scraper

## Overview
This project is a LinkedIn job scraper that allows users to extract job listings from LinkedIn. The scraped data includes job titles, company names, job descriptions, and more.

## Prerequisites
Before running the script, ensure that your system meets the following requirements:
- **Operating System:** Windows or macOS
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

### Step 2: Install Python
#### **Windows**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and check "Add Python to PATH" before proceeding
3. Verify installation:
   ```sh
   python --version
   ```

#### **macOS**
1. Install Python using Homebrew:
   ```sh
   brew install python
   ```
2. Verify installation:
   ```sh
   python3 --version
   ```

### Step 3: Clone the Repository
```sh
git clone https://github.com/DevenMalekar/Truviq_System.git
cd Truviq_System
```

### Step 4: Install Python Dependencies
Ensure you have Python installed, then install the required dependencies:
```sh
pip install -r requirements.txt
```

### Step 5: Download and Set Up ChromeDriver
1. Find your **Google Chrome version** by navigating to:
   - **Windows/macOS:** Open Chrome and go to `chrome://settings/help`
2. Download the matching **ChromeDriver** from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
3. Extract the ChromeDriver and move it to the project directory
4. Add ChromeDriver to the system PATH:
   - **Windows:** Move `chromedriver.exe` to a known location and add its directory to the PATH variable.
   - **macOS:** Move `chromedriver` to `/usr/local/bin/`:
     ```sh
     mv chromedriver /usr/local/bin/
     ```

## Running the Scraper

### Configure the Scraper
- Open `Main.py` in a text editor.
- Modify the `URLS` list with LinkedIn job search URLs you want to scrape.

### Run the Scraper
#### **Windows**
```sh
python Main.py
```
#### **macOS**
```sh
python3 Main.py
```
The script will display a progress bar as it scrapes each URL, and the extracted job data will be saved in `linkedin_jobs.csv`.

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


