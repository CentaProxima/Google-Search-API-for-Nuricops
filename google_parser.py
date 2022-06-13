import traceback
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

URL = 'https://google.co.kr/search?q={query}&start={idx}'
robot_text = 'Our systems have detected unusual traffic from your computer network.'

class GoogleParser:
    def __init__(self):                
        self._initialize_client()
    
    def _initialize_client(self):
        self.client = requests.Session()
        self.client.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '+\
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'+\
                '100.0.4896.57 Whale/3.14.133.23 Safari/537.36',
            'referer': 'https://google.co.kr',
            'accept': 'text/html,application/xhtml+xml,'+\
                'application/xml;q=0.9,image/avif,'+\
                'image/webp,image/apng,*/*;q=0.8,'+\
                'application/signed-exchange;v=b3;q=0.9'
        }

    def _parse(self, element: BeautifulSoup):        
        divlist = element.find_all('div', {'style': 'width:600px'})
        result = []
        if len(divlist) == 0:
            divlist.append(element)
        
        for div in divlist:
            try:       
                url = div.find('a').attrs['href']
                title = div.find('a').find('h3').text
                content = div.find_all('span', {'class': None})[-1]                
                content = None if content == None else content.text
                _result = {
                    'title': title,
                    'url': url,
                    'content': content
                }
                result.append(_result)
            except AttributeError:
                return None
        return result      
    
    def search(self, query, count=10, start=0):
        global URL
        result = []

        if query is None or count is None or start is None:
            return
        
        idx = start
        while len(result) < count:
            '''
            검색 url 생성
            query: 검색어
            idx: 출력 index(index부터 9개까지 결과 출력)
            '''
            url = URL.format_map({'query': query, 'idx': idx})    
            html = self.client.get(url).text

            if robot_text in html:
                return {'error': 'Google detected our system as bot'}
            
            soup = BeautifulSoup(html, 'lxml')
            try:                
                search_result = soup.find('div', 
                    {
                        'data-async-context': 'query:'+quote(query) #검색 결과 영역 가져오기
                    }
                ).find_all('div', {'class': 'g'}) #검색 결과 각 요소 list 변환            

                for elem in search_result:
                    _result = self._parse(elem) #검색 결과 api 결과값으로 변환
                    if _result is not None:
                        result += _result
                idx += 10
                return {'result': result[:count]}
            except:
                traceback.print_exc()
                return {'error': 'Unexpected error occured'}