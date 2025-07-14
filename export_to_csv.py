import csv

def export_to_csv(json_file, csv_file):
    import json
    with open(json_file, "r") as f:
        data = json.load(f)

    rows = []
    for url, info in data.items():
        for entry in info["history"]:
            rows.append({
                "url": url,
                "title": entry.get("title", ""),
                "price": entry.get("price", ""),
                "date": entry.get("date", "")
            })

    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "title", "price", "date"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported to {csv_file}")
