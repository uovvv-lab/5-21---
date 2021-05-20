import requests
import json
from bs4 import BeautifulSoup

url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'

queryParams = '?' + \
              'serviceKey=' + '37UU8R3Yo9wt%2Bvm7CENV%2BwV6UJJv4Lzr9EH%2Bqpx4waegyPHLCYfJsiSLHnFgpZ7y0evNjHyioAoovOmfrdqBrQ%3D%3D' + \
              '&pageNo=' + '1' + \
              '&numOfRows=' + '999' + \
              '&dataType=' + 'JSON' + \
              '&dataCd=' + 'ASOS' + \
              '&dateCd=' + 'DAY' + \
              '&startDt=' + '20210519' + \
              '&endDt=' + '20210519' + \
              '&stnIds=' + '108'


def get_wdata(cname):
    page=requests.get('https://www.weather.go.kr/weather/observation/currentweather.jsp')
    html = page.text
    soup = BeautifulSoup(html, 'lxml')

    data=soup.find('table','table_develop3')
    trdata= data.find_all('tr')



    result=[]
    for temp in trdata:
        citydata= temp.find_all('td')
        cnt=0
        cdata={}
        for temp1 in citydata:
            if cnt ==0:
                cdata['지역']=temp1.text
            elif cnt==1:
                cdata['현재일기']=temp1.text
            elif cnt==5:
                cdata['현재기온']=temp1.text
            elif cnt==8:
                cdata['일강수']=temp1.text
            cnt+=1

        if cdata !={}:
            result.append(cdata)
            if cname in cdata['지역']:
                return cdata

    return {}


