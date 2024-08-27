import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import re

def scrape_method_location(soup):
    main_div = soup.find('div',id="printMethods")
    tables = main_div.find_all('table')
    method_table = tables[0]
    headers = [th.text.strip() for th in method_table.find('thead').find_all('th')]
    data_points = [re.sub(r'[\s\n]+', ' ', th.text) for th in method_table.find('tbody').find_all('td')]
    method_data_points = {headers[i] : data_points[i] for i in range(len(headers))}

    print("Method Data Points")

    for key,value in method_data_points.items():
        print(f"{key} : {value}")
        
    print("-------------------\n")

    print("Location Data Points")
    location_table = tables[2]
    headers = [th.text.strip() for th in location_table.find('thead').find_all('th')]

    rows = []
    for row in location_table.select('tbody > tr'):
        lst = [re.sub(r'[\s\n]+', ' ', th.text) for th in row.select('td')]
        rows.append(lst)

    location_data_points = {}

    for i in range(len(headers)):
        key = headers[i]
        for row in rows:
            value = row[i]
        
            if key in location_data_points:
                location_data_points[key].append(value)
            else:
                location_data_points[key] = [value]


    for item,row in enumerate(rows):
        print(f"Item: {item+1}")
        for index,value in enumerate(row):
            print(headers[index],value)
        print("--------")

def scrape_basic_points(soup):
    print(soup.find('strong',string="Item ID:").parent.text) # item id

    print("----------")

    raw_text = soup.find('strong',string="Size:").parent.text # item size
    cleaned_text = re.sub(r'[\s\n]+', ' ', raw_text).strip()
    print(cleaned_text)
    print("----------")

    table = soup.find('table',class_= "pricetable")
    rows = table.find_all('tr')

    for index, row in enumerate(rows):
        cols = [col.text.strip() for col in row.find_all('th')]
        if index == 1:
            cols.insert(0,"Price")
        print(' | '.join(cols))

    print("----------")

def is_url(string):
    url_pattern = r"^(?:https?|ftp)://(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:[0-9]{1,3}\.){3}[0-9]{1,3}\])(?::[0-9]+)?(?:/[^\s]*|)$"
    return re.match(url_pattern, string) is not None

def main():

    session = requests.Session()

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Host": "developer.livehelpnow.net",
        "Origin": "https://www.arielpremium.com",
        "Referer": "https://www.arielpremium.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    while True:
        user_input = input("Enter url or press E to exit: ")
        if user_input.lower() == 'e':
            break
        else:
            if not is_url(user_input):
                print("Please provide valid link...")
            response = session.get(user_input,headers=headers)

            if response.status_code == 200:
                # pass logic
                print("Response: ",response.status_code)
                soup = BeautifulSoup(response.content,features="lxml")
                scrape_basic_points(soup)

                scrape_method_location(soup)


            else:
                print("Request time out. Please use proxy or contact developer.")


if __name__=="__main__":
    main()