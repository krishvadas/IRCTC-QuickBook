import json

STATION_FILE = "utils/cleaned_station_codes.json"

def load_station_data():
    try:
        with open(STATION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            unique = {}
            for station in data:
                code = station.get("sc", "")
                if code and code not in unique:
                    unique[code] = station
            return list(unique.values())
    except Exception as e:
        print("❌ Error loading station file:", e)
        return []

def score_station_match(station, query):
    query = query.lower()
    sc = station.get("sc", "").lower()
    name = station.get("en", "").lower()
    cluster = station.get("ec", "").lower()

    if query == sc:
        return 3
    elif sc.startswith(query) or name.startswith(query) or cluster.startswith(query):
        return 2
    elif query in sc or query in name or query in cluster:
        return 1
    return 0

def filter_stations(query, pool):
    query = query.lower()
    scored = []

    for s in pool:
        score = score_station_match(s, query)
        if score > 0:
            scored.append((score, s))

    best = {}
    for score, station in scored:
        sc = station.get("sc", "")
        if sc and (sc not in best or score > best[sc][0]):
            best[sc] = (score, station)

    return [s for _, s in sorted(best.values(), key=lambda x: -x[0])]

def format_station(s):
    name = s.get('en', 'N/A')
    code = s.get('sc', 'N/A')
    cluster = s.get('ec', '')
    return f"{name} - {code} ({cluster})" if cluster else f"{name} - {code}"

if __name__ == "__main__":
    while True:
        query = input("🔍 Enter station search text: ").strip()
        if not query:
            print("❌ Please enter a valid search term.")
            continue

        stations = load_station_data()
        matches = filter_stations(query, stations)

        if matches:
            print(f"\n📋 Search Results with {len(matches)} result(s):")
            for s in matches:
                print(f"- {format_station(s)}")
        else:
            print("❌ No matching stations found.")
