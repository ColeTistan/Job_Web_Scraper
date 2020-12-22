# Cole Tistan
# Indeed Job Search / Web Scraper Tool

# job card: jobsearch-SerpJobCard
# job title: title under div class: jobsearch-SerpJobCard
# company name class: company
# job location: location accessible-contrast-color-location
# job summary class: summary

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

from requests.api import request

print("Enter a job title")
job_title_search = input('>')
print("Enter a location")
job_location = input('>')

# global variables 

def extract_content(title, location):
    """Generate a url from the parameters: title & location"""
    url_template = f'https://www.indeed.com/jobs?q={title}&l={location}'
    url = url_template.format(title, location)
    """parse html content into response"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup

def get_job_cards(soup):
    job_cards = soup.find_all('div', class_='jobsearch-SerpJobCard')
    for item in job_cards:
        """extract job title and company who posted job"""
        job_title = item.find('a').text
        company = item.find('span', class_='company').text.strip()
        location = get_location(item)
        salary = get_salary(item)

        """extract job summary"""
        summary = item.find('div', {'class': 'summary'}).text.strip().replace('\n', '')
        
        job = {
            'Job title': job_title,
            'Company name': company,
            'Location': location,
            'Salary': salary,
            'Summary': summary,
        }
        joblist.append(job)
    return

def get_location(soup):
    """extract job location if it is available"""
    try: 
        location = soup.find('span', class_='location').text.replace('\n', '')
    except:
        location = 'None'
    return location

def get_salary(soup):
    """extract job salary or wage if it is available"""
    try:
        salary = soup.find('span', class_='salaryText').text.strip()
    except:
        salary = ''
    return salary

joblist = []
    

for index in range(0, 40, 10):
    print(f'Extracting page, {index}')
    url = extract_content(job_title_search, job_location)
    get_job_cards(url)

data_frame = pd.DataFrame(joblist)
print(data_frame.head())
data_frame.to_csv('jobs.csv')

# if __name__ == '__main__':
#     while True:
#         print()
#         find_jobs()
#         time_stamp = 10
#         print(f"Waiting {time_stamp} minutes...")
#         time.sleep(time_stamp * 60)

