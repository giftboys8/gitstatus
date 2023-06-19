import json
from selenium import webdriver
from bs4 import BeautifulSoup
import time


def get_wjx_data(url, output_file):
    url = url

    # 使用Chrome WebDriver，确保驱动程序在系统路径中
    browser = webdriver.Chrome()

    # 获取渲染后的页面
    browser.get(url)

    html = browser.page_source

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("title").text

    # 提取所需的数据
    # 例如：
    fieldsets = soup.find_all("fieldset")
    question = []

    for fieldset in fieldsets:
        div_questions = fieldset.find_all("div", class_="div_question")

        for div_question in div_questions:
            ul_element = div_question.find("ul", class_="ulradiocheck")

            li_elements = ul_element.find_all("li")
            li = []
            for li_element in li_elements:
                li_value = li_element.find("label").text
                li.append(li_value)

            question_title = {}
            question_title["title"] = div_question.find(
                "div", class_="div_title_question").text

            if div_question.find("input", type="checkbox"):
                question_title["type"] = "checkbox"
            elif div_question.find("input", type="radio"):
                question_title["type"] = "radio"
            elif div_question.find("input", type="jqDropdown"):
                question_title["type"] = "dropdown"
            else:
                question_title["type"] = "text"

            question_title["content"] = li
            question.append(question_title)

    # 关闭浏览器
    browser.quit()

    # 保存数据为JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(question, f, ensure_ascii=False, indent=4)

    print("Data saved to output.json")
    return title
