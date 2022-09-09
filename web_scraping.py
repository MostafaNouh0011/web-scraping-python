
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title = []
company_name = []
location_name = []
skills = []
date = []
page_num = 0

while True:
    try:
        # use requests library to fetch the url
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=spbg&q=python&start={page_num}")

        # save page content/markup
        scr = result.content

        # create soup object to parse content
        soup = BeautifulSoup(scr, "lxml")
    
        page_limit = int(soup.find("strong").text)

        if page_num > page_limit // 15:
            print("pages ended, terminate")
            break

        # find the elements containing info we need
        # for example: job titles, job skills, company names, location names
        job_titles = soup.find_all("h2", {"class":"css-m604qf"})
        company_names = soup.find_all("a", {"class":"css-17s97q8"})
        location_names = soup.find_all("span", {"class":"css-5wys0k"})
        job_skills = soup.find_all("div", {"class":"css-y4udm8"})
        posted_new = soup.find_all("div", {"class":"css-4c4ojb"})
        posted_old = soup.find_all("div", {"class":"css-do6t5g"})
        posted = [*posted_new, *posted_old]

        # loop over returned lists to extract needed info into other lists
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text.strip())
            company_name.append(company_names[i].text.strip())
            location_name.append(location_names[i].text.strip())
            skills.append(job_skills[i].text.strip())
            date.append(posted[i].text.strip())
        page_num += 1
        print("page switched")
    except:
        print("error occured")
        break

# create csv file and fill it with values
file_lst = [job_title, company_name, date, location_name, skills]
exported = zip_longest(*file_lst)
with open("/pythonProjects/web-scraping-result/JobsTest.csv", "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Job title", "Company name", "job post", "Location", "Skills"])
    wr.writerows(exported)

