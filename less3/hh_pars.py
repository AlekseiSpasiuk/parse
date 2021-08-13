from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def transform_price(price):
    import re
    if price:
        out = list(map(lambda a: int(a), re.findall(r'\d+', price)))
        cur = price.split(str(out[-1]))[-1]
        if len(out) < 2:
            out.append(None)
            if "до" in price:
                out = out[::-1]
        return out[0], out[1], cur
    return None, None, None

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
        price = "".join(price_tag.text.split('\u202f')) if price_tag else None
        out_vacancy["min_price"], out_vacancy["max_price"], out_vacancy["currency"] = transform_price(price)
        out_vacancy["company_name"] = company_tag.text if company_tag else None
        out_vacancy["company_url"] = url + company_tag["href"] if company_tag else None
        out_vacancy["city"] = city_tag.text
        res.append(out_vacancy)
    return res

#qtext = "python"
qtext = input("введи свой запрос: ")
out_bd = []

url = "https://hh.ru"
url_path = "/search/vacancy"

params = {"area": 1002,
          "fromSearchLine": "true",
          "st": "searchVacancy",
          "text": qtext,
          "items_on_page": 20,
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
        next_page_num = int(next_page["href"].split("page=")[-1].strip())
        if next_page_num != 0:
            params["page"] = next_page_num

df = pd.DataFrame(out_bd)
df.to_csv(f"./vacancy_{qtext}.csv")
df.to_json(f"./vacancy_{qtext}.json")
