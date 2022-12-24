import json
import uuid


heartbeat_json_file = open("heartbeat_data.json")

heartbeat_data = json.load(heartbeat_json_file)

data = list()
for heartbeat_record in heartbeat_data:
    print(heartbeat_record)
    heartbeat_record["heartbeat_id"] = str(uuid.uuid4())
    data.append(heartbeat_record)


with open("heartbeat_data_with_uuid.json", "w", encoding="utf-8") as fout:
    json.dump(data, fout, ensure_ascii=False, indent=4)
