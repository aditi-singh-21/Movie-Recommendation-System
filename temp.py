url_2 = "https://www.imdb.com/list/ls099106768/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.google.com/',
}

response = requests.get(url_2, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

movies = soup.find_all('li',{'class' : "ipc-metadata-list__item ipc-metadata-list__item--inline ipc-metadata-list-item--link"})

for mov in movies:
    parent_span = mov.find('span', class_='sc-551fcf62-4 iYlNDF')
    if parent_span:
        nested_span = parent_span.find('span', class_='sc-551fcf62-5 igzEFP')
        if nested_span:
           nested_span.extract()  # Remove the nested span
           title = parent_span.text.strip()
           movies_name.append(title)
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '/title/' in href:
            url = "https://www.imdb.com" + href
            movies_url.append(url)
            
