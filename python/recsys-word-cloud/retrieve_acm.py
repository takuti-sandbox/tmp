import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver


proceeding_urls = {
    2008: 'https://dl.acm.org/doi/proceedings/10.1145/1454008',
    2009: 'https://dl.acm.org/doi/proceedings/10.1145/1639714',
    2010: 'https://dl.acm.org/doi/proceedings/10.1145/1864708',
    2011: 'https://dl.acm.org/doi/proceedings/10.1145/2043932',
    2012: 'https://dl.acm.org/doi/proceedings/10.1145/2365952',
    2013: 'https://dl.acm.org/doi/proceedings/10.1145/2507157',
    2014: 'https://dl.acm.org/doi/proceedings/10.1145/2645710',
    2015: 'https://dl.acm.org/doi/proceedings/10.1145/2792838',
    2016: 'https://dl.acm.org/doi/proceedings/10.1145/2959100',
    2017: 'https://dl.acm.org/doi/proceedings/10.1145/3109859',
    2018: 'https://dl.acm.org/doi/proceedings/10.1145/3240323',
    2019: 'https://dl.acm.org/doi/proceedings/10.1145/3298689',
    2020: 'https://dl.acm.org/doi/proceedings/10.1145/3383313',
    2021: 'https://dl.acm.org/doi/proceedings/10.1145/3460231',
}


def get_article_urls(root_url):
    driver = webdriver.Chrome()
    driver.get(root_url)

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


def process_year(year):
    print('Year: {}'.format(year))

    file = open('csv/{}.csv'.format(year), 'w')
    file.write('url,abstract\n')
    for url in get_article_urls(proceeding_urls[year]):
        print(url)
        file.write('{},{}'.format(url, get_abstract(url)))
        file.write('\n')
    file.close()


def run():
    for year in proceeding_urls.keys():
        process_year(year)


if __name__ == '__main__':
    run()
    # print(get_abstract('https://dl.acm.org/doi/10.1145/3460231.3474241'))
