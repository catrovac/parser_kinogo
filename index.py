from bs4 import BeautifulSoup
import requests
import fake_useragent
import os
import json
import csv
import time


class Parser:
    user = fake_useragent.UserAgent().data_browsers['chrome'][0]
    headers = {"user-agent": user}
    last = 275
    counter = 0
    name_film = ''
    year = ''

    def parser_kinogo(self):
        while self.last <= 1382:
            try:
                url = f'https://kinokrad.co/page/{self.last}/'
                result = requests.get(url, headers=self.headers)
                if result.status_code == 200:

                    with open('index.html', 'w', encoding='utf-8-sig') as file:
                        file.write(result.text)
                    with open('index.html', encoding='utf-8-sig') as file:
                        data = file.read()
                    soup = BeautifulSoup(data, 'lxml')
                    last_page = soup.find("div", class_="navcent").find_all("a")[-1].text

                    print(last_page)
                    content = soup.find('div', id='dle-content').find_all("div", class_="shorposterbox")
                    for n in content:
                        name = n.find("h2").text
                        url_film = n.find("h2").find("a").get("href")
                        raiting = n.find("li", class_="current-rating").text
                        year = n.find_all('div', class_="godshort")[0].text
                        self.year = year
                        self.name_film = name
                        country = n.find_all('div', class_="godshort")[1].text
                        janr = n.find_all('div', class_="godshort")[2].text
                        times = n.find_all('div', class_="godshort")[4].text

                        if float(raiting) >= 7:
                            self.counter += 1
                            self.print_info(self)
                            with open(f"film.csv", "a", newline="") as tabble:
                                writer = csv.writer(tabble, delimiter=";")
                                writer.writerow(
                                    (
                                        name,
                                        raiting,
                                        year,
                                        janr,
                                        url_film,
                                        country,
                                        times
                                    )
                                )
                    # print(content)
                    self.last += 1
                    time.sleep(1)
            except Exception as _ex:
                print(_ex)
                self.last += 1

    def print_info(self):
        astr = f"[INFO] Addet film {self.counter} name {self.name_film} year {self.year}"
        info_str = f"[INFO] oобработано страниц {self.last}"
        print(astr, info_str, sep='\n')


def main():
    kinogo = Parser.parser_kinogo(self=Parser)


if __name__ == "__main__":
    main()
