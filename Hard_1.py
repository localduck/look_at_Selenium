import requests
import json
from time import sleep


__requirements__ = "requests: 2.25.1, python: 3.8.3"
__date__ = "18.06.2021"


mails_list = ["duck.green..@mail.ru", "zz11jh@mail.ru", "mail@mail.ru"]
[mails_list.append(f"mail{i}@mail.ru") for i in range(97)]


def recovery_test(mails):
    with open('data.json', 'w') as f:
        for mail in mails:
            r = requests.post('https://account.mail.ru/api/v1/user/password/restore', data={'email': mail})
            j_string = json.loads(r.text)
            # print(j_string["email"], j_string["status"])
            json.dump(j_string, f, ensure_ascii=False)
            sleep(4)
    f.close()


recovery_test(mails_list)
