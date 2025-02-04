import time
import logging
import pandas as pd
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from tqdm import tqdm
import numpy as np

# Chrome Driver Options
__chrome_options = webdriver.ChromeOptions()
ua = UserAgent()
__chrome_options.add_argument(f"user-agent={ua.random}")
__chrome_options.add_argument("--start-maximized")
__chrome_options.add_argument("--disable-gpu")
__chrome_options.add_argument("--headless")
__chrome_options.add_argument("window-size=2100,700")
__chrome_options.add_argument("--no-sandbox")
__chrome_options.add_argument("--disable-dev-shm-usage")
__chrome_options.add_argument("--disable-software-rasterizer")
__chrome_options.add_argument("--enable-unsafe-swiftshader")
__chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Chrome Driver Service
webdriver_path = "chromedriver.exe"
__chrome_service = Service(webdriver_path)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def __scrape_job(job, wd):
    job_data = {
        'title': np.nan,
        'full_url': np.nan,
        'company': np.nan,
        'location': np.nan,
        'company_url': np.nan,
    }
    
    try:
        url_element = WebDriverWait(job, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a')))
        wd.execute_script("arguments[0].scrollIntoView();", url_element)  # Scroll into view
        full_url = url_element.get_attribute('href')
        job_data['full_url'] = full_url
    except Exception as e:
        logging.warning(f"Skipping job due to URL extraction failure: {str(e)}")
        return None  # Skip this job and return None

    try:
        job_data['title'] = job.find_element(By.CLASS_NAME, 'base-search-card__title').text
    except Exception:
        pass
    
    try:
        job_data['location'] = job.find_element(By.CLASS_NAME, 'job-search-card__location').text
    except Exception:
        pass

    try:
        job_data['company_url'] = job.find_element(By.CSS_SELECTOR, 'h4>a').get_attribute('href')
    except Exception:
        pass

    try:
        job_data['company'] = job.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text
    except Exception:
        pass
    
    return pd.DataFrame([job_data])

def __scrape(url, max_results, position=0):
    wd = None
    try:
        wd = webdriver.Chrome(service=__chrome_service, options=__chrome_options)
        wd.get(url)
        time.sleep(5)

        jobs_data = []
        last_scraped_job = 0
        pbar = tqdm(desc='Scraping...', total=max_results, position=position)

        while last_scraped_job < max_results:
            # Get all current job elements
            try:
                jobs = WebDriverWait(wd, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.jobs-search__results-list > li"))
                )
            except Exception as e:
                logging.error(f"Failed to locate jobs list: {str(e)}")
                break

            # Check if we've exhausted available jobs
            if last_scraped_job >= len(jobs):
                prev_job_count = len(jobs)
                
                # Attempt to load more jobs
                try:
                    see_more_button = wd.find_element(By.CLASS_NAME, 'infinite-scroller__show-more-button')
                    wd.execute_script("arguments[0].click();", see_more_button)
                    time.sleep(3)
                    
                    # Check if new jobs were actually loaded
                    new_jobs = wd.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list > li")
                    if len(new_jobs) == prev_job_count:
                        logging.info("No new jobs loaded after clicking 'See More'. Stopping early.")
                        break
                    else:
                        continue  # New jobs loaded, reprocess the list
                        
                except Exception:
                    logging.info("No more jobs available.")
                    break

            try:
                next_job = jobs[last_scraped_job]
                job_df = __scrape_job(next_job, wd)
                if job_df is not None:
                    jobs_data.append(job_df)
                last_scraped_job += 1
                pbar.update(1)
            except Exception as e:
                logging.warning(f"Skipping job {last_scraped_job + 1} due to error: {str(e)}")
                last_scraped_job += 1

        pbar.close()

        if jobs_data:
            return pd.concat(jobs_data, ignore_index=True)
        return pd.DataFrame(columns=['title', 'full_url', 'location', 'company_url', 'company'])

    except Exception as e:
        logging.error(f"Error in __scrape: {str(e)}")
        return pd.DataFrame()
    finally:
        if wd:
            wd.quit()

def get_listings_from(keyword: str, location: str, max_results: int, filter_type: str) -> pd.DataFrame:
    keyword = keyword.replace(" ", "%20")
    location = location.replace(" ", "%20")

    filter_mapping = {
        "latest": "f_TPR=r86400",     # Past 24 hours
        "recent": "f_TPR=r604800",    # Past week
        "last_2_days": "f_TPR=r172800",  # Past 2 days
        "all": ""                     # No filter (all jobs)
    }

    filter_query = filter_mapping.get(filter_type.lower(), "")

    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
    if filter_query:
        url += f"&{filter_query}"

    with mp.Pool() as pool:
        url_data = [(url, max_results, 0)]
        results = pool.map(process_url, url_data)

    valid_results = [df for df in results if not df.empty]

    if valid_results:
        final_df = pd.concat(valid_results, ignore_index=True)
        logging.info(f'Done Scraping! Found {len(final_df)} jobs.')
        return final_df
    else:
        logging.warning("No jobs were scraped.")
        return pd.DataFrame(columns=['title', 'full_url', 'location', 'company_url', 'company'])

def process_url(url_data):
    url, max_results, position = url_data
    return __scrape(url, max_results, position)

if __name__ == "__main__":
    # Get user inputs for keyword, location, max results, and filter type
    keyword = input("Enter the job keyword: ")
    location = input("Enter the job location: ")
    max_results = int(input("Enter the number of jobs to scrape: "))

    print("Select a filter option: latest (past 24h), recent (past week), last_2_days (past 2 days), all (no filter)")
    filter_type = input("Enter filter type (latest/recent/last_2_days/all): ").strip().lower()

    # Fetch job listings based on user input
    results = get_listings_from(keyword, location, max_results, filter_type)

    # Output results
    if not results.empty:
        print(f"Successfully scraped {len(results)} jobs")
        results.to_csv('linkedin_jobs.csv', index=False)
    else:
        print("No jobs were scraped")