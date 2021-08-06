from bs4 import BeautifulSoup as bs
import requests

def parse_soup(soup):
    res = []
    vacancy_list = soup.find_all(name = "div", attrs = {"class": "vacancy-serp-item"})
    for vacancy in vacancy_list:
        out_vacancy = {}
        title_tag = vacancy.find(name = "a", attrs = {"data-qa": "vacancy-serp__vacancy-title"})
        price_tag = vacancy.find(name = "span", attrs = {"data-qa":"vacancy-serp__vacancy-compensation"})
        company_tag = vacancy.find(name = "a", attrs = {"data-qa":"vacancy-serp__vacancy-employer"})
        city_tag = vacancy.find(name = "span", attrs = {"data-qa": "vacancy-serp__vacancy-address"})

        out_vacancy["href"] = title_tag["href"]
        out_vacancy["jobs_title"] = title_tag.text
        out_vacancy["price"] = " ".join(price_tag.text.split('\u202f')) if price_tag else None
        out_vacancy["company_name"] = company_tag.text
        out_vacancy["company_url"] = url + company_tag["href"]
        out_vacancy["city"] = city_tag.text
        res.append(out_vacancy)
    return res

qtext = "python"
out_bd = []

url = "https://hh.ru"
url_path = "/search/vacancy"

params = {"area": 1002,
          "fromSearchLine": "true",
          "st": "searchVacancy",
          "text": qtext,
          "page": 0}

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
           + "AppleWebKit/605.1.15 (KHTML, like Gecko) "
           + "Version/14.1.2 Safari/605.1.15"}

cont = True
while(cont):
    response = requests.get(url + url_path, params = params, headers = headers)
    print(response.url)
    soup = bs(response.text, "html.parser")
    out_bd += parse_soup(soup)
    next_page = soup.find(name = "a", attrs = {"data-qa": "pager-next"})
    if not next_page:
        cont = False
    else:
        params["page"] = int(next_page["href"].split("page=")[-1].strip())

print(out_bd)
print(len(out_bd))
