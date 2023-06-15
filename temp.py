
clientbase = [
    {"clid": 117962626, "name": "Анна  Махитько", "phone": "+19009551582"},
    {"clid": 117964601, "name": "Елена", "phone": "+19050505888"},
    {"clid": 117965432, "name": "Иван", "phone": "+19009551582"}
]

duplicates = {}

for client in clientbase:
    if client['phone'] in duplicates:
        duplicates[client['phone']].append(client['clid'])
    else:
        duplicates[client['phone']] = [client['clid']]

for phone, clids in duplicates.items():
    if len(clids) > 1:
        print(f"Phone {phone} is associated with clids {', '.join(map(str, clids))}")
