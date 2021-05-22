from ai.search_engine.data import get_data

data = get_data()
type = set(item["type"] for item in data)
print(type)

district = sorted(set(item["district"] for item in data))
print(district)