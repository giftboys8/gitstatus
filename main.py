import utils
import os
import time

if __name__ == '__main__':
    lists = [
        '27316180',
        '103864723',
        '110896110',
        '100656619',
    ]

    for i in lists:
        title = utils.get_wjx_data(
            "https://www.wjx.cn/jq/"+i+".aspx", "output.json")
        time.sleep(2)
        print(title)
        os.rename("output.json", title+".json")
