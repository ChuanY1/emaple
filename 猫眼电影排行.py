from DrissionPage import ChromiumPage, ChromiumOptions
import pandas as pd
import requests
from bs4 import BeautifulSoup


def order(z):
    html = ChromiumOptions().headless()
    page = ChromiumPage(html)
    page.get(url)
    page_index = page.ele("#ranks-list")
    for i in page_index.eles(".row"):
        s = round(int(i.ele(".col2 tr").text) / 10000, 2)
        c = round(float(i.ele(".col3 tr").text), 2)
        dict_1 = {"电影名称": i.ele(".first-line").text,
                  "上映时间": i.ele(".second-line").text,
                  "总票房": str(s) + "亿元",
                  "平均票价": str(c) + "元",
                  "平均人次": i.ele(".col4 tr").text}
        lict_1.append(dict_1)
        print(z, dict_1)
        z += 1
    page.quit()


def order_2(z):
    html = requests.get(url)
    resp = BeautifulSoup(html.content, "html.parser")
    page = resp.find_all("ul", class_="row")[1:]
    for i in page:
        s = round(int(i.find("li", class_="col2 tr").text) / 10000, 2)
        c = round(float(i.find("li", class_="col3 tr").text), 2)
        dict_1 = {"电影名称": i.find("p", class_="first-line").text,
                  "上映时间": i.find("p", class_="second-line").text,
                  "总票房": str(s) + "亿元",
                  "平均票价": str(c) + "元",
                  "平均人次": i.find("li", class_="col4 tr").text}
        lict_1.append(dict_1)
        print(z, dict_1)
        z += 1


z = 1
lict_1 = []
url = "https://piaofang.maoyan.com/rankings/year"
if __name__ == '__main__':
    n = int(input("动态输入1\t静态输入2\n"))
    print("————>猫眼电影票房排行<————")
    if n == 1:
        order(z)
    else:
        order_2(z)
    df = pd.DataFrame(lict_1)
    df.to_csv("F:/Python/movie.csv", index=True, encoding='utf-8-sig')
    print("程序执行完毕！")
    input("按回车键退出...")
