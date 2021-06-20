# look_at_Selenium

# Base
Парсер данных через селениум на сайте https://www.nseindia.com/
Алгоритм:
1. Зайти на https://www.nseindia.com
2. Навестись (hover) на MARKET DATA
3. Кликнуть на Pre-Open Market
4. Спарсить данные Final Price по всем позициям на странице и вывести их в csv файл. Имя;цена

После этого сымитировать небольшой пользовательский сценарий использования сайта. Здесь по своему желанию, но как пример:
1. Зайти на главную страницу
2. Пролистать вниз до графика
3. Выбрать график "NIFTY BANK"
4. Нажать “View all” под "TOP 5 STOCKS - NIFTY BANK"
5. Выбрать в селекторе “NIFTY ALPHA 50”
6. Пролистать таблицу до конца
# Знакомился с Selenium, крутил-вертел - поэтому тут все так страшно.

# Hard_1
1. Парсинг данных об аккаунтах (простое).
Взять 100 случайных адресов почты Mail.ru (не важно каким образом и необязательно настоящих). 
Узнать от сервера mail.ru информацию об этих ящиках (существует, установлена 2fa, иная информация). 
Полученный результат записать в файл в формате JSON.

# Hard_2
2. Поиск результатов Twitch (среднее).
Повторить действия пользователя по вводу запроса "Pool" (ну или свой по желанию) в строку поиска. 
Получить результаты предпросмотра поискового запроса (подзказки перед отправкой запроса поиска) и результаты самого поиска. 
Из результатов поиска достать все ссылки и вывести в лог.

# Hard_3
3. Парсинг последних твитов Elon Musk (сложное).
Получить список последних 20 твитов Илона Маска используя HTTP-запрос. 
Вывести в лог только текст (если есть) последних твитов.
# Надо повторять regex
