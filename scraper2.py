from turtle import pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import csv

bright_stars_url = 'https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars'

browser = webdriver.Edge("chromedriver.exe")
browser.get(bright_stars_url)

time.sleep(10)

star_data = []

headers = ["Brown Draft", "Constellation", "Right ascension", "Declination", "App.mag.", "Distance", "Spetral type"]

def scrape():
    for i in range(1, 5):
        while True:
            time.sleep(2)

            soup = BeatufulSoup(browser.page_source, "html.parser")

            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

            if current_page_num < i:
               browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click() 
            else:
                break
        for ul_tag in soup.find_all("ul", attrs={"class", "brightstars"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index ==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try: 
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")  

            hyperlink_li_tag = li_tags[0]

            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs" + hyperlink_li_tag.find_all("a", href=True)[0]["href"]) 

            star_data.append(temp_list)

        browser.find_element(By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click() 
        
        print(f"Page {i} scraping completed")

scrape()

draft_satr_data = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)

        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class" : "fact_row"}):
            td_tags = tr_tag.find_all("td")

            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class" : "value"})[0].contents[0])
                except:
                    temp_list.append("")

        draft_satr_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

for index, data in enumerate(star_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(draft_satr_data[0 : 10])

final_star_data = []

for index, data in enumerate(star_data):
    draft_star_data_element = draft_satr_data[index]
    draft_star_data_element = [elem.replace("\n", "") for elem in draft_star_data_element]
    final_star_data.append(data + draft_star_data_element)

with open("bright_stars.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_star_data)
   



