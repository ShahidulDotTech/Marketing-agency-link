from bs4 import BeautifulSoup
import requests
import csv
import email

with open(r'D:\Work files\job\freelance\reddit\data science\automated task\web scraping\2 clutch href\marketing agency link\healthgrades\sample.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        print(row[0])
        try:
            response = requests.get(row[0])
            soup = BeautifulSoup(response.content, 'html.parser')
            Emails = []
            contact = 'contact'
            www = 'www.'
            linkedin = 'linkedin'

            for a in soup.find_all('a', href=True):
                  if contact in a['href'] and www in a['href']:
                      print(a['href'])
                      response2 = requests.get(a['href'])
                      soup2 = BeautifulSoup(response2.content, 'html.parser')
                      for a in soup2.find_all('a', href=True):
                          if '@' in a['href']:
                              print(a['href'])
                              print(a.string)

        except:
            print('Exception')