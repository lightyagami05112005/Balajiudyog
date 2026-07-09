import json

file_path = r"c:\Users\Shubham\Downloads\balaji udhyog-handoff\balaji-udhyog\project\scripts\catalog-extras.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total items in catalog-extras.json: {len(data)}")

# Search for "FLO" in category or SKU
flo_items = []
for idx, item in enumerate(data):
    if "FLO" in str(item.values()) or "flo" in str(item.values()):
        flo_items.append(item)

print(f"Found {len(flo_items)} items matching FLO:")
for item in flo_items[:10]:
    print(item)
