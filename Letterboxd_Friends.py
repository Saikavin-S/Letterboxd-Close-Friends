from bs4 import BeautifulSoup
import requests
import csv
import time
print("As of now, this program only supports 5 friends.")
try:
    f=open('usernames.csv','r')
    data = list(csv.reader(f, delimiter=","))
    usernames=data[0]
    f.close()
except OSError as e:
    f=open('usernames.csv','w')
    usernames=[]
    no=int(input("Enter number of close friends (<=5):"))
    while no>5:
        no=int(input("enter number <=5:"))
    for i in range(1,no+1):
        usernames.append(input(f'Enter Username {i}:').lower())
    writer = csv.writer(f,delimiter=",")
    writer.writerow(usernames)
    f.close()
def Function():
    for username in usernames:
        try:
            page=requests.get(f'https://letterboxd.com/{username}/films/diary/').text
        except requests.exceptions.ConnectionError as conerr:
            print("No Internet Connection\nPlease connect to internet and try again")
            return
        soup= BeautifulSoup(page,"lxml")
        denied=soup.find('title').text
        count=0
        while denied=="Access denied | letterboxd.com used Cloudflare to restrict access":
            time.sleep(0.1)
            count+=1
            if count==10:
                print("Too Many Requests In A Short Amount Of Time")
                return
        if denied=='Letterboxd - Not Found':
            print(f'Username \"{username}\" does not exist\n')
            continue
        first_entry=soup.find('tr',class_='diary-entry-row viewing-poster-container')
        entry=first_entry.find('td',class_='col-production js-td-production')
        entrydate=first_entry.find('td',class_='col-daydate _aligncenter _paddinginlinelg').a['href'].split('/')
        entrydate_date=entrydate[-2]
        entrydate_month=entrydate[-3]
        entrydate_year=entrydate[-4]
        movie_name=entry.find('h2',class_='name -primary prettify')
        name=movie_name.a.text
        release=entry.find('span',class_='releasedate').a.text
        print(username)
        print(name,end=" ")
        print(f'({release})')
        print(entrydate_date,entrydate_month,entrydate_year,sep="/")
        print("")
a=time.time()
Function()
b=time.time()
print("time taken to fetch results:",round(b-a,2))