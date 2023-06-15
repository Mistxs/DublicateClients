import json
import requests
import math
from tqdm import tqdm
from config import headers


dataset = [{}]
duplicates = {}
salon_id = [163813]


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

def run():
    global clid
    global phones
    page = 1
    it = parseclient(salon_id[0],page)
    print("Scanning clientbase...")
    for i in tqdm(range(2,it+1)):
        parseclient(salon_id[0],i)
    dataset.pop(-1)
    print(f"Done. Total count: {len(dataset)}")

run()



for client in dataset:
    if client['phone'] in duplicates:
        duplicates[client['phone']].append(client['clid'])
    else:
        duplicates[client['phone']] = [client['clid']]

for phone, clids in duplicates.items():
    if len(clids) > 1:
        print(f"Phone {phone} is associated with clientids {', '.join(map(str, clids))}")
