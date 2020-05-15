import requests
import csv
from bs4 import BeautifulSoup as bs
def get_html(url):
    r = requests.get(url) #Response
    return r.content #html_code
def get_streets(html):
    streets = []
    soup = bs(html,'html.parser')
    links = soup.find_all('div', class_='span4')
    for div in links:
        for a in div.find_all('a'):
            streets.append(a.get_text().strip().split(' '))
    return list(map(lambda x: (' '.join(x[:-1]), x[-1]),streets))
def write_csv(data):
    with open('streats.csv', 'a') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


def main():
    page = get_html('https://kladr-rf.ru/46/000/001/')
    streets = get_streets(page)
    write_csv(streets)



if __name__ == "__main__":
    main()
