import requests, json
from bs4 import BeautifulSoup

class NaverNews:
    def __init__(self):
        self.list = self.getlist()

    def getlist(self, as_json=False):
        URL = 'https://news.naver.com'
        html = requests.get(URL).text 
        news_list = BeautifulSoup(html, 'html.parser').find(id='today_main_news').find_all('div', {'class': 'newsnow_tx_inner'})
        result = []
        for news in news_list: 
            href = news.a.attrs["href"]
            if 'read.nhn' in href:
                result.append({
                    'head': news.a.string,
                    'src': news.a.attrs["href"]
                })
        if as_json:
            return json.dumps(result, ensure_ascii=False)
        return result

    def getcontent(self, URL, as_json=False):
        if type(URL) == int:
            URL = self.list[URL]['src']
        print('[*] URL:', URL)
        html = requests.get(URL).text 
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find(id='articleBodyContents')
        # print('[*] content:', content)
        try:
            content.find('h4', {'class': 'blind'}).decompose()
        except: pass
        try:
            content.find('script').decompose()
        except: pass
        result = {
            'title': soup.find(id='articleTitle').text,
            'src': URL,
            'date-written': soup.find_all('span', {'class': 't11'})[0].text,
            'date-modified': soup.find_all('span', {'class': 't11'})[1].text,
            'content': content.get_text('\n').strip()
        }
        if as_json:
            return json.dumps(result, ensure_ascii=False)
        return result

if __name__ == '__main__':
    navernews = NaverNews()
    print(navernews.list)
    print(navernews.getcontent(0))
