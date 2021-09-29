import requests
import time
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
from selenium import webdriver


def get_article_urls():
    proceeding_url = 'https://dl.acm.org/doi/proceedings/10.1145/3460231'

    driver = webdriver.Chrome()
    driver.get(proceeding_url)

    time.sleep(1)

    sections = driver.find_elements_by_xpath("//a[contains(@class, 'section__title') and (@aria-expanded='false')]")

    for section in sections:
        section.click()  # expand all artcile sections
        time.sleep(1)

    titles = driver.find_elements_by_xpath("//a[ancestor::h5[contains(@class, 'issue-item__title')]]")
    for title in titles:
        yield title.get_attribute('href')

    driver.quit()


def get_abstract(url):
    try:
        res = requests.get(url)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
    except Exception:
        return ''

    div = soup.find('div', {'class': 'abstractSection'})
    if div is None:
        print('no abstract found')
        return ''
    return div.find('p').decode_contents()


def run():
    sources = []
    for url in get_article_urls():
        print(url)
        sources.append(get_abstract(url))

    stopwords = set(STOPWORDS)
    stopwords |= set(open('stopwords.txt').read().rstrip().split('\n'))
    wordcloud = WordCloud(stopwords=stopwords).generate(' '.join(sources))
    wordcloud.to_file('png/recsys2021.png')


if __name__ == '__main__':
    run()
    # print(get_abstract('https://dl.acm.org/doi/10.1145/3460231.3474241'))
