import csv
import psycopg2
conn = psycopg2.connect(
    dbname = "Markets"
    , host = "127.0.0.1"
    , user = "nastya"
    , password = "Nastya"
    , port = "5432")

# 1) выводит список всех рынков
def list_of_markets(conn):
    cur = conn.cursor()
    cur.execute("SELECT marketname, city, state FROM Markets ORDER BY city;")
    for marketname, market_city, market_state in cur.fetchall():
        print(marketname, market_city, market_state, sep="  -  ")


# 2) Поиск рынка по городу и штату
def markets_city(conn):
    cur = conn.cursor()
    global city_search_near
    city_search_near = input("Введите Ваш город: ")
    state_search_near = input("Введите Ваш штат: ")
    cur.execute("SELECT marketname, state, city, street, website FROM Markets where city ~ %s AND state ~ %s;", (city_search_near,state_search_near,))
    print("\nСписок рынков в ", city_search_near, "-", state_search_near, ": ")
    for marketname, market_state, market_city, street, website in cur.fetchall():
        print(marketname, market_state, market_city, street, website, sep=" - ")


# 3) Поиск рынка по наименованию
def markets_names(conn):
    cur = conn.cursor()
    global marketsname_search
    marketsname_search = input("Введите название рынка: ")
    print("Вот что удалось найти по рынку ", marketsname_search, ": ")
    cur.execute("SELECT marketname, state, city, street, website FROM Markets where marketname ~ %s;", (marketsname_search,))
    for marketname, market_state, market_city, street, website in cur.fetchall():
        print(marketname, market_state, market_city, street, website, sep=" - ")
    marketsname_search = "none"


#4) Поиск ближайших рынков
def markets_near(conn):
    cur = conn.cursor()
    global city_search_near
    city_search_near = input("Введите Ваш город: ")
    state_search_near = input("Введите Ваш штат: ")
    cur.execute("SELECT city, state_name, lat, lng FROM uscities WHERE city = %s AND state_name = %s;", (city_search_near,state_search_near,))
    for city, state_name, lat, lng in cur.fetchall():
        your_lat=lat
        your_lng = lng
        print('Ваши координаты:', your_lat, ', ', your_lng)
        print("\nСписок ближайших рынков: \n")
        cur.execute("SELECT marketname, state, city, street, y, x, website FROM Markets WHERE ABS(y-%s)<0.1 AND ABS(x-%s)<0.1 ORDER BY city;", (your_lat,your_lng,))
        for marketname, state, city, street, y, x, website in cur.fetchall():
            print(marketname, state, city, street, y, x, website, sep=" - ")


# 5) Просмотр информации о рынке по названию
def info_market(conn):
    cur = conn.cursor()
    global marketsname_search1
    marketsname_search1 = input("Введите название рынка: ")
    print("Вот что удалось найти по рынку ", marketsname_search1, ": ")
    cur.execute("SELECT marketname, state, city, street, website, season1time FROM markets where marketname ~ %s;" , (marketsname_search1,))
    for marketname, state, city, street, website, season1time in cur.fetchall():
        print(marketname, state, city, street, website, season1time, sep=" - ")


print("Приветствуем! \n\n"
      "Перед Вами программа управления данными рынков.\n\n"
      "Здесь Вы можете: \n"
      "1. Посмотреть список всех рынков.\n"
      "2. Найти рынок по городу.\n"
      "3. Найти рынок по названию.\n"
      "4. Найти ближайший рынок.\n"
      "5. Посмотреть информацию о рынке.\n")
answ1 = int(input("Пожалуйста, выберете желаемое действие: \n"))
if answ1 == 1:
    print("Перед вами список всех рынков: \n")
    list_of_markets(conn)
elif answ1 == 2:
    markets_city(conn)
elif answ1 == 3:
    markets_names(conn)
elif answ1 == 4:
    markets_near(conn)
elif answ1 == 5:
    info_market(conn)


