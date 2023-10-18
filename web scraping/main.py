from bs4 import BeautifulSoup
import requests
import pandas as pd
with open("validproxies.txt","r") as f:
    proxies=f.read().split("\n")
url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_2"
HEADERS = {'accept':
'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'accept-Encoding':
'gzip, deflate, br',
'accept-Language':
'en-US,en;q=0.9',
'User-Agent':
'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'}
# counter=0
# for sites in url:
#     try:
#         webpage=requests.get(url,headers=HEADERS,proxies={'http':proxies[counter],'https':proxies[counter]})
#         print(webpage.status_code)
#         print(sites)
#     except:
#         print("failed")
#     finally:
#         counter+=1
webpage=requests.get(url,headers=HEADERS)        
# print(webpage.content)
soup=BeautifulSoup(webpage.content,'html.parser')
# print(soup)
# print(soup.prettify)
print(webpage.status_code)
links=soup.find_all('a',attrs={'class':'a-link-normal s-faceout-link a-text-normal'})
print(links)

