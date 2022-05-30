import requests
from bs4 import BeautifulSoup
import re


def request(url, header):
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def cspeech(i, u, t, s):
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39"}
    html = request(u, header)
    soup = BeautifulSoup(html, 'html.parser')
    dp = soup.find(face='Arial').text.replace('\r', '').replace('\n', '')
    dp = re.sub('\\s+', ' ', dp)
    if soup.find(face='Verdana') is not None:
        s1 = soup.find(face='Verdana').sourceline
    else:
        s1 = float('inf')
    if soup.find(style="font-size:10.0pt;font-family:Verdana") is not None:
        s2 = soup.find(style="font-size:10.0pt;font-family:Verdana").sourceline
    else:
        s2 = float('inf')
    if soup.find(style="font-family:Verdana") is not None:
        s3 = soup.find(style="font-family:Verdana").sourceline
    else:
        s3 = float('inf')
    startline = min(s1, s2, s3)
    els = [el.sourceline for el in soup.find_all('hr')]
    endline = max(els) + 1
    speech = ''
    hylk = soup.find_all('a')
    h_list = []
    for h in hylk:
        h_list.append(h.sourceline + 1)
    if i != 43:
        sentences = soup.find_all('font')
    else:
        sentences = soup.find_all('span')
    for p in sentences:
        if startline <= p.sourceline < endline and p.text not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                                                  '**'] and p.sourceline not in h_list:
            sent = re.sub('\\s+', ' ',
                          p.text.replace('			', '').replace('		', '').replace('\r', ' ').replace('\n', ' ')).strip()
            if len(sent) == 1:
                if len(speech) != 0:
                    if sent != speech[-1]:
                        speech += sent
            else:
                if sent[-3:-1] == 'to':
                    speech += sent
                else:
                    speech += sent + '\n'
    speech = re.sub('\n\n', '\n', speech)
    path = 'Speech100/' + str(i + 1) + ' ' + t + '.txt'
    f = open(path, "w", encoding='utf-8')
    f.write(t + '\n')
    f.write(s + '\n')
    f.write(dp + '\n')
    f.write(speech)
    f.close()


def main():
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39"}
    url = "https://www.americanrhetoric.com/top100speechesall.html"
    html = request(url, header)
    soup = BeautifulSoup(html, 'html.parser')
    hyperlist = soup.find(id="AutoNumber1").find_all(width="341")
    urllist = []
    titlelist = []
    offsites = []
    for i in range(100):
        urllist.append('https://www.americanrhetoric.com/' + hyperlist[i].a.get('href'))
        title = hyperlist[i].a.text.replace('\r', '').replace('\n', '')
        title = re.sub('\\s+', ' ', title).strip().strip('?')
        titlelist.append(title)
        if title[-1] == ')':
            offsites.append(i)
    offsites.append(58)
    spakers = soup.find(id="AutoNumber1").find_all(width="203")
    spakerlist = []
    for i in range(100):
        spakerlist.append(spakers[i].text.replace('\n', '').strip())

    for i in range(100):
        if i not in offsites:
            print(i + 1, titlelist[i])
            cspeech(i, urllist[i], titlelist[i], spakerlist[i])

    # i = 1
    # print(i + 1, titlelist[i])
    # cspeech(i, urllist[i], titlelist[i], spakerlist[i])


if __name__ == '__main__':
    main()
