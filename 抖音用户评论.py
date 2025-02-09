from DrissionPage import ChromiumPage
import pandas as pd
import wordcloud
import datetime
import jieba
import logging
import re
import time
jieba.setLogLevel(logging.CRITICAL)

time_s = time.time()


# 找不到这些元素时，说明子评论已全部被展开
def vb(p1):
    f8 = p1.ele('.f8nOLNQF', timeout=1)
    xy = p1.ele('.xYPAOE0i', timeout=1)
    return f8 or xy


# """
def order():
    j = 1
    data_list = []
    # 打开
    page = ChromiumPage()
    # 监听访问
    url = 'https://www.douyin.com/video/7468910530917338378?modeFrom='
    page.listen.start('aweme/v1/web/comment/list')
    page.get(url)
    p1 = page.ele('@data-e2e=comment-list')
    c1 = "@class=kXqO4xu2 comment-title"
    # 依次展开评论
    print("正在展开全部评论......")
    while vb(p1):
        bv = p1.eles('@|class=f8nOLNQF@|class=xYPAOE0i')
        for e in bv:
            e.click()
            page.wait(0.5)
    print('end')
    while True:
        json_uid = ""
        # 加载数据
        page.scroll.to_see(c1)
        # 等待加载
        resp = page.listen.wait(timeout=3)
        # 获取数据
        try:
            json_data = resp.response.body
        except AttributeError:
            print("end")
            break
        print(f"正在分析第{j}页数据......")
        j += 1
        # 解析数据
        json_index = json_data['comments']
        for i in reversed(json_index):
            json_uid = i["user"]["sec_uid"]
            break
        for i in json_index:
            t = i["create_time"]
            date = str(datetime.datetime.fromtimestamp(t))
            text = re.sub(r"\[.*?]", "", i["text"])
            dict_1 = {
                "name": i["user"]["nickname"],
                "id": i["user"]["short_id"],
                "time": date,
                "ip": i["ip_label"],
                "text": text
            }
            print(dict_1)
            data_list.append(dict_1)
            c1 = p1.ele(f"@@href=//www.douyin.com/user/{json_uid}@@class=uz1VJwFY")
    df = pd.DataFrame(data_list)
    df.to_csv("F:/Python/douyin.csv", index=False, encoding='utf-8-sig')
    # 关闭浏览器
    page.close()
    df = pd.read_csv("F:/Python/douyin.csv")
    content = " ".join([str(i).replace("\n", "") for i in df["text"]])
    string = " ".join(jieba.lcut(content))
    wc = wordcloud.WordCloud(
        font_path="simkai.ttf",
        width=1000,
        height=700,
        stopwords={"就", "我", "了", "的", "你", "有", "是", "能", "不", "打", "那", "死", "都", "也", "没", "吗"}
    )
    wc.generate(string)
    wc.to_file("F:/Python/douyin.png")
    time_e = time.time()
    print('%.2f' % float(time_e - time_s) + '秒')


if __name__ == '__main__':
    order()
