import json
import requests
import math
from tqdm import tqdm
import pandas as pd


dataset = [{}]
duplicates = []
duplicates_dict = {}
salon_id = 163813


def parseclient(salon, page):
    url = f"https://api.yclients.com/api/v1/company/{salon}/clients/search"

    payload = json.dumps({
        "page": page,
        "page_size": 200,
        "fields": [
            "id",
            "name",
            "phone"
        ]
    })


    response = requests.request("POST", url, headers=headers, data=payload)
    pretty_response = response.json()
    global clid
    global phones
    total_count = pretty_response["meta"]["total_count"]
    iterations = math.ceil(total_count / 200)

    for i in range(len(pretty_response["data"])):
        dataset[-1]["clid"] = pretty_response["data"][i]["id"]
        dataset[-1]["name"] = pretty_response["data"][i]["name"]
        dataset[-1]["phone"] = pretty_response["data"][i]["phone"]
        dataset.append({})

    return iterations


def findduplicates():
    global duplicates_dict

    duplicates = {}

    for client in dataset:
        if client['phone'] in duplicates:
            duplicates[client['phone']]['clid'].append(client['clid'])
        else:
            duplicates[client['phone']] = {"phone": client['phone'], "clid": [client['clid']]}

    # Создаем список словарей только с дублирующимися номерами телефонов и их clid
    duplicates_dict = [{"phone": phone, "clid": values['clid']} for phone, values in duplicates.items() if
                       len(values['clid']) > 1]


def run():
    global clid
    global phones
    page = 1
    it = parseclient(salon_id,page)
    print("Scanning clientbase...")
    for i in tqdm(range(2,it+1)):
        parseclient(salon_id,i)
    dataset.pop(-1)
    print(f"Done. Total count: {len(dataset)}")
    findduplicates() # поиск дублей из полученной КБ

# run()

duplicates_dict = [{'phone': '+79688353353', 'clid': [23638880, 119809131]}, {'phone': '+79154740507', 'clid': [23639518, 162716883]}, {'phone': '+79250251398', 'clid': [24512702, 25506863]}, {'phone': '+79175943459', 'clid': [34095392, 42936211]}, {'phone': '+79859912555', 'clid': [101921756, 101922321, 101922972]}, {'phone': '+79221555510', 'clid': [164308027, 164308030]}]


def clientinfo(clid):
    url = f"https://api.yclients.com/api/v1/client/{salon_id}/{clid}"
    payload = ""
    response = requests.request("GET", url, headers=headers, data=payload).json()
    return response["data"]["visits"]



for i in range(len(duplicates_dict)):
    print(f"Клиент {duplicates_dict[i]['phone']}")
    visits = []
    for j in range(len(duplicates_dict[i]["clid"])):
        print(f'Карточка (clid) {j+1}: {duplicates_dict[i]["clid"][j]}')
        visits.append(clientinfo(duplicates_dict[i]["clid"][j]))
        print(f"Визитов у данного клиента: {visits}")
        duplicates_dict[i]["visits"] = visits


print(duplicates_dict)



duplicates_dict = [{'phone': '+79688353353', 'clid': [23638880, 119809131], 'visits': [9, 0]}, {'phone': '+79154740507', 'clid': [23639518, 162716883], 'visits': [0, 0]}, {'phone': '+79250251398', 'clid': [24512702, 25506863], 'visits': [2, 33]}, {'phone': '+79175943459', 'clid': [34095392, 42936211], 'visits': [5, 3]}, {'phone': '+79859912555', 'clid': [101921756, 101922321, 101922972], 'visits': [5, 2, 0]}, {'phone': '+79221555510', 'clid': [164308027, 164308030], 'visits': [0, 0]}]


data = []

for item in duplicates_dict:
    clid_visits = list(zip(item['clid'], item['visits']))
    if len(clid_visits) > 0:
        data.append([item['phone'], clid_visits[0][0], clid_visits[0][1]])
        for clid, visits in clid_visits[1:]:
            data.append(['', clid, visits])

def generate_sql_queries(data):
    sql_queries = []

    for item in data:
        visits = item['visits']
        clid = item['clid']

        # Проверяем случаи, описанные в задаче
        if all(visit == 0 for visit in visits):
            # Если все значения визитов равны 0
            min_clid = min(clid)
            query = f"UPDATE clients SET deleted=1 WHERE id={min_clid};"
            sql_queries.append(query)
        elif len(visits) == 2:
            # Если визитов 2
            max_visits = max(visits)
            min_clid = min(clid)
            query = f"UPDATE clients SET deleted=1 WHERE id={max(clid)};"
            sql_queries.append(query)
        elif len(visits) > 2:
            # Если визитов 3 и более
            zero_visits = [clid[i] for i, visit in enumerate(visits) if visit == 0]
            max_visits = max(visits)
            min_clid = min(clid)
            for zero_visit in zero_visits:
                query = f"UPDATE clients SET deleted=1 WHERE id={zero_visit};"
                sql_queries.append(query)
            query = f"UPDATE transactions SET client_id={min_clid} WHERE client_id={max(clid)};"
            sql_queries.append(query)
            query = f"UPDATE tt_records SET client_id={min_clid} WHERE client_id={max(clid)};"
            sql_queries.append(query)
            query = f"UPDATE client_visits SET client_id={min_clid} WHERE client_id={max(clid)};"
            sql_queries.append(query)
            query = f"UPDATE clients SET deleted=1 WHERE id={max(clid)};"
            sql_queries.append(query)

    return sql_queries

sql_queries = generate_sql_queries(data)

for query in sql_queries:
    print(query)

df = pd.DataFrame(data, columns=['Номер телефона', 'Client ID', 'Количество визитов (из API)'])
df.to_excel('data.xlsx', index=False)
