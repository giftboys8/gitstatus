import openai
import os
import json

# from dotenv import load_dotenv
# load_dotenv()

openai.organization = "org-tHTF3d09rQY7wgiGQ07a87qk"
openai.api_key = "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"

# En = openai.Engine.list()
# Models = openai.Model.list()

# print(En)
# print(Models)

# text = f"""[{"issueId": 1612144, "summary": "【生产issue】数据集编辑sql，名为key的字段 显示成了0/1/2，实际返回值是正常的", "devPlainCompletionDate": "2023-03-14 23:59:59", "enterDevelopTime": "2023-03-13 09:48:48", "enterTestTime": "2023-03-20 09:51:20", "developer": "01373984", "developerName": "肖宇", "tester": "01373984", "testerName": "肖宇", "leaveDevelopTime": "2023-03-20 09:51:12", "leaveTestTime": "2023-03-20 17:57:44"}, {"issueId": 1614083, "summary": "【REST API】extcontrol接口支持收藏/取消收藏 报表、数据集", "devPlainCompletionDate": "2023-03-23 23:59:59", "enterDevelopTime": "2023-03-10 15:20:47", "enterTestTime": "2023-03-31 16:34:55", "developer": "01413112", "developerName": "马子尧", "tester": "01422708", "testerName": "仉薇", "leaveDevelopTime": "2023-03-13 09:20:48", "leaveTestTime": "2023-03-31 16:35:04"}, {"issueId": 1704270, "summary": "【SP补丁】-VPN环境放开报表下载（数据集仍限制） & 流程节点新增", "devPlainCompletionDate": "2023-03-30 23:59:59", "enterDevelopTime": "2023-03-29 11:36:33", "enterTestTime": "2023-03-30 14:15:59", "developer": "01413112", "developerName": "马子尧", "tester": "01422708", "testerName": "仉薇", "leaveDevelopTime": "2023-03-29 11:36:55", "leaveTestTime": "2023-03-30 14:16:04"}, {"issueId": 1704285, "summary": "TODO-【取数下载】VPN环境下载中心点击下载判断是否为VPN报表，否则报错", "devPlainCompletionDate": null, "enterDevelopTime": "2023-03-23 19:07:24", "enterTestTime": "2023-03-31 18:41:20", "developer": "01413112", "developerName": "马子尧", "tester": "01380994", "testerName": "许国彪", "leaveDevelopTime": "2023-03-27 11:22:51", "leaveTestTime": "2023-03-31 18:41:25"},
# {"issueId": 1713923, "summary": "DOING-【工作空间/数据集】我管理的（个人&协作），列表项仅保留管理链接跳转至单独管理页面按tab进行管理", "devPlainCompletionDate": "2023-03-31 23:59:59", "enterDevelopTime": "2023-03-29 11:44:43", "enterTestTime": "2023-03-31 10:17:22", "developer": "01428548", "developerName": "李逸君", "tester": "01422708", "testerName": "仉薇", "leaveDevelopTime": "2023-03-30 18:12:48", "leaveTestTime": "2023-03-31 18:41:15"}, {"issueId": 1716237, "summary": "【运营】数据盟友学习培训页面（仅内网，私有化/公网屏蔽）", "devPlainCompletionDate": "2023-04-03 23:59:59", "enterDevelopTime": "2023-04-03 17:12:07", "enterTestTime": "2023-04-04 17:24:21", "developer": "01349951", "developerName": "孙冬冬", "tester": "01422708", "testerName": "仉薇", "leaveDevelopTime": "2023-04-03 17:16:04", "leaveTestTime": "2023-04-07 17:56:26"}, {"issueId": 1716249, "summary": "【报表发布】按组织授权屏蔽一级组织，二级组织如果有子组织屏蔽否则不屏蔽", "devPlainCompletionDate": "2023-04-03 23:59:59", "enterDevelopTime": "2023-04-03 17:11:58", "enterTestTime": "2023-04-06 19:00:21", "developer": "01349951", "developerName": "孙冬冬", "tester": "01422708", "testerName": "仉薇", "leaveDevelopTime": "2023-04-03 17:12:27", "leaveTestTime": "2023-04-07 17:56:00"}, {"issueId": 1721389, "summary": "【数据市场整合】解决数据市场会话先于丰景台会话失效问题", "devPlainCompletionDate": "2023-04-04 23:59:59", "enterDevelopTime": "2023-04-03 17:12:13", "enterTestTime": "2023-04-07 13:52:45", "developer": "01349951", "developerName": "孙冬冬", "tester": "01422708", "testerName": "仉薇", "leaveDevelopTime": "2023-04-06 20:22:25", "leaveTestTime": "2023-04-07 13:53:04"}]"""


def get_completion(prompt,   model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt, "name": "Edwin_Assista"}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.2,
        n=2,
    )
    return response.choices[0].message["content"]


text = f"""How to carry out efficiency traction in a team?"""
prompt = f"""
As a research and development efficiency expert ```{text}```
"""

response = get_completion(prompt)
print(response)
