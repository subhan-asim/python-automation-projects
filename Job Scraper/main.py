from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import undetected_chromedriver as uc
import json
import time

uc.Chrome.__del__ = lambda self: None

query = input("What jobs would you like to scrape: ").strip().replace(" ", "%20")
if not query:
    print("Please enter a valid query.")
    exit()

try:
    total_jobs = int(input("How many jobs would you like scraped (e.g. 20): ").strip())
    if total_jobs <= 0:
        raise ValueError
except ValueError:
    print("Please enter a positive number.")
    exit()

pages = total_jobs // 10 + (1 if total_jobs % 10 != 0 else 0)

options = uc.ChromeOptions()
driver = None
all_jobs = []

try:
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    driver.get(f"https://www.upwork.com/nx/search/jobs/?q={query}")

    for page in range(pages):
        wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "air3-card")))
        jobs = driver.find_elements(By.CLASS_NAME, "air3-card")
        print(f"Scraping page {page + 1} with {len(jobs)} jobs found")

        for job in jobs:
            if len(all_jobs) >= total_jobs:
                break
            try:
                title_elem = job.find_element(By.CSS_SELECTOR, "h2.job-tile-title > a")
                title = title_elem.text
                job_url = title_elem.get_attribute("href")

                spans = job.find_elements(By.CSS_SELECTOR, "small.mb-1 > span")
                posted = ' '.join([spans[0].text, spans[1].text]) if len(spans) >= 2 else spans[0].text

                full_desc = job.find_element(By.CSS_SELECTOR, "p.text-body-sm").text.split()
                desc = ' '.join(full_desc[:30]) if len(full_desc) > 30 else ' '.join(full_desc)

                job_type = job.find_element(By.CSS_SELECTOR, "[data-test='job-type-label']").text
                exp_level = job.find_element(By.CSS_SELECTOR, "[data-test='experience-level']").text

                all_jobs.append({
                    'title': title,
                    'url': job_url,
                    'posted_time': posted,
                    'summary': desc,
                    'type': job_type,
                    'experience': exp_level
                })

            except Exception as e:
                print("Error extracting job:", e)

        if len(all_jobs) >= total_jobs:
            break

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "[data-test='next-page']")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)
        except:
            print("No more pages or failed to click next.")
            break

finally:
    if driver:
        try:
            driver.quit()
        except Exception as e:
            print("Error quitting driver:", e)

with open("Jobs.json", "w", encoding='utf-8') as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=4)

print(f"Saved {len(all_jobs)} jobs to Jobs.json")