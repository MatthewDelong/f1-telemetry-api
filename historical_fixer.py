import requests, json, os, numpy as np

api_url = 'https://api.jolpi.ca/ergast/f1'

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return super(NpEncoder, self).default(obj)

def fetch_data(url):
    print(f"Fetching: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def write_compact_json(data, filepath, results_key="Results"):
    """Format using the 2026 'One Line per Result' style"""
    lines = ["["]
    for i, race in enumerate(data):
        lines.append("    {")
        header_keys = ["season", "round", "url", "raceName"]
        header = ", ".join(f'"{k}": {json.dumps(race.get(k, ""), ensure_ascii=False)}' for k in header_keys)
        lines.append(f"        {header},")
        lines.append(f'        "Circuit": {json.dumps(race.get("Circuit", {}), ensure_ascii=False)},')
        dt_parts = ", ".join(f'"{k}": {json.dumps(race.get(k, ""), ensure_ascii=False)}' for k in ["date", "time"])
        lines.append(f"        {dt_parts},")
        
        results = race.get(results_key, [])
        lines.append(f'        "{results_key}": [')
        for j, result in enumerate(results):
            comma = "," if j < len(results) - 1 else ""
            lines.append(f"            {json.dumps(result, ensure_ascii=False, cls=NpEncoder)}{comma}")
        lines.append("        ]")
        
        comma = "," if i < len(data) - 1 else ""
        lines.append(f"    }}{comma}")
    lines.append("]")
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")

def update_year(year):
    print(f"\n--- PROCESSING {year} ---")
    
    # 1. Results
    res_data = fetch_data(f"{api_url}/{year}/results.json?limit=1000")
    if res_data:
        races = res_data["MRData"]["RaceTable"]["Races"]
        write_compact_json(races, f"races/{year}/results.json", "Results")
        print(f"Updated results.json for {year} ({len(races)} races)")

    # 2. Qualifying
    qual_data = fetch_data(f"{api_url}/{year}/qualifying.json?limit=1000")
    if qual_data:
        races = qual_data["MRData"]["RaceTable"]["Races"]
        write_compact_json(races, f"races/{year}/qualifying.json", "QualifyingResults")
        print(f"Updated qualifying.json for {year}")

    # 3. Sprint
    sprint_data = fetch_data(f"{api_url}/{year}/sprint.json?limit=1000")
    if sprint_data:
        races = sprint_data["MRData"]["RaceTable"]["Races"]
        write_compact_json(races, f"races/{year}/sprint.json", "Results")
        print(f"Updated sprint.json for {year}")

if __name__ == "__main__":
    update_year(2023)
    update_year(2025)
    print("\nAll historical data fixed and formatted!")
