import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

#wyciąganie danych o spółkach w Dow Jones Industrial Average ze strony CNN

siteURL = 'https://money.cnn.com/data/dow30/'
cnn_request=requests.get(siteURL, timeout=10)
rec=[]
soup=BeautifulSoup(cnn_request.text,'html.parser')

#funkcja, która ściąga te dane ze strony i wrzuca do pliku
def extract_stock_price_data(cnn_request):
 
    if cnn_request is None:
        print("something is wrong")
        return
    
    tableResults = soup.find_all('tr')[2:]
        
    for res in tableResults:

        try:

            base = res.find('td',attrs={ "class":"wsod_aRight"})
            #nazwa spółki, którą wyciągam
            name = res.find('span').text

            #url prowadzi do informacji o danej spółce na cnn
            urlR=res.find('a')['href']
            url = "https://money.cnn.com"+urlR

            #sciagam cene ze strony
            price = res.find('td', attrs={'class':"wsod_aRight"}).find('span').contents[0]

            #zmiana wartości                           
            changeR = base.find_next('td', attrs={'class':"wsod_aRight"})
            change = changeR.text

            #zmiana wartości w procentach
            #perc = res.find("span", attrs= {"class":"posChangePct"}) or res.find("span", attrs= {"class":"negChangePct"})
            perc = changeR.find_next('td', attrs={'class':"wsod_aRight"})
            percent = perc.text
               
            #wolumen
            vol = perc.find_next('td', attrs={'class':"wsod_aRight"})
            volume = vol.text
               
            #YTD change - co to jest?
            ytdR = vol.find_next('td', attrs={'class':"wsod_aRight"})
            ytd = ytdR.text            
               
            print ("name of the company: ",name,"\n","price: ",price,"\n","change:", change,"\n","change in percentages: ",percent,"\n","volume:",volume, "\n","YTD change:",ytd,"\n", "link: ",url)
                
            rec.append((name, price, change, percent,volume, ytd, url))
            
        except requests.RequestException as e:

            print("can't do")
            print(str(e))

        except requests.ConnectionError as e:

            print ("something is wrong with connection")
            print(str(e))

        except requests.Timeout as e:

            print("Timeout Error")
            print(str(e))

        except KeyboardInterrupt:

            print("someone clicked your program")

    #zapisywanie danych do pliku csv
    df = pd.DataFrame(rec, columns=['Company', 'Price', 'Change', 'Change(%)','Volume', 'YTD Change', 'URL'])
    df.to_csv('DJIdata.csv', index=False, encoding='utf-8')


if __name__ == "__main__":
   # cnn_HTML = download_HTML(siteURL)
    extract_stock_price_data(cnn_request)
    
                 

