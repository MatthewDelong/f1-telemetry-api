# 🏎️ F1 Telemetry API

A free, open-source **Formula 1 data API** served via GitHub Pages. Access comprehensive F1 data — drivers, constructors, race results, qualifying, sprint results, standings, and team colors — all through simple JSON endpoints with **zero authentication required**.

---

## 📡 Base URL

```
https://matthewdelong.github.io/f1-telemetry-api
```

All endpoints return JSON and are publicly accessible.

---

## 🗂️ API Endpoints

### Drivers

#### All Drivers List

Returns a complete list of every F1 driver in history (880+ drivers).

```
GET /driversList.json
```

<details>
<summary>Response Schema</summary>

```json
[
  {
    "driverId": "alonso",
    "permanentNumber": "14",
    "code": "ALO",
    "url": "http://en.wikipedia.org/wiki/Fernando_Alonso",
    "givenName": "Fernando",
    "familyName": "Alonso",
    "dateOfBirth": "1981-07-29",
    "nationality": "Spanish"
  }
]
```

</details>

#### Individual Driver Data

Returns detailed career statistics for a specific driver including wins, podiums, poles, DNFs, qualifying times, race positions, consistency metrics, and more.

```
GET /drivers/{driverId}.json
```

**Example:**

```
GET /drivers/hamilton.json
GET /drivers/max_verstappen.json
```

<details>
<summary>Response Schema</summary>

```json
{
  "driverId": "hamilton",
  "driverCode": "HAM",
  "driverNumber": "44",
  "lastUpdate": "2026-05-11T...",
  "totalWins": 105,
  "totalPodiums": 202,
  "totalPoles": 104,
  "totalDNFs": 30,
  "seasonWins": { "2007": 4, "2008": 5, ... },
  "seasonPodiums": { ... },
  "seasonPoles": { ... },
  "seasonDNFs": { ... },
  "poles": { "2007": ["Canadian Grand Prix", ...], ... },
  "podiums": { ... },
  "DNFs": { ... },
  "fastLaps": { ... },
  "finalStandings": { "2007": { "year": "2007", "position": "2", "points": "109" }, ... },
  "posAfterRace": { ... },
  "racePosition": { ... },
  "qualiPosition": { ... },
  "driverQualifyingTimes": { ... },
  "consistency": { "mean": { ... }, "std": { ... }, "cv": { ... } },
  "peakSeason": { "wins": { ... }, "podiums": { ... }, "poles": { ... } },
  "avgRacePositions": { ... },
  "avgQualiPositions": { ... },
  "rates": { "wins": { ... }, "podiums": { ... }, "poles": { ... }, "DNFs": { ... } },
  "winRate": 0.25,
  "podiumRate": 0.49,
  "poleRate": 0.25,
  "dnfRate": 0.07,
  "ptwConRate": { ... },
  "positionsGainLost": { ... }
}
```

</details>

---

### Constructors

#### Constructors by Year

Returns all constructors participating in a given season.

```
GET /constructors/{year}.json
```

**Example:**

```
GET /constructors/2026.json
```

<details>
<summary>Response Schema</summary>

```json
[
  {
    "constructorId": "ferrari",
    "url": "https://en.wikipedia.org/wiki/Scuderia_Ferrari",
    "name": "Ferrari",
    "nationality": "Italian"
  }
]
```

</details>

#### Constructor Drivers by Year

Returns the drivers who drove for a specific constructor in a given year.

```
GET /constructors/{year}/{constructorId}.json
```

**Example:**

```
GET /constructors/2026/mercedes.json
```

---

### Races

#### Races by Season

Returns all race meetings for a given season, including meeting keys and locations.

```
GET /races/races.json
```

<details>
<summary>Response Schema</summary>

```json
{
  "2026": {
    "Australian Grand Prix": {
      "meeting_key": 1279,
      "location": "Melbourne"
    },
    "Monaco Grand Prix": {
      "meeting_key": 1286,
      "location": "Monte Carlo"
    }
  }
}
```

</details>

#### Races by Meeting Key

Lookup races by their OpenF1 meeting key.

```
GET /races/racesbyMK.json
```

#### Race Details (Per Season)

Returns full race calendar details for a given season, including circuits, dates, and times.

```
GET /races/{year}/raceDetails.json
```

#### Race Results (Per Season)

Returns race results for all completed races in a given season.

```
GET /races/{year}/results.json
```

#### Qualifying Results (Per Season)

Returns qualifying results (Q1, Q2, Q3 times) for all completed qualifying sessions.

```
GET /races/{year}/qualifying.json
```

#### Sprint Results (Per Season)

Returns sprint race results for all completed sprint events.

```
GET /races/{year}/sprint.json
```

#### Driver Standings (Per Season)

```
GET /races/{year}/driverStandings.json
```

#### Constructor Standings (Per Season)

```
GET /races/{year}/constructorStandings.json
```

---

### Team Colors

#### Colors by Team

Returns hex color codes for each constructor, keyed by year and `constructorId`.

```
GET /colors/teams.json
```

<details>
<summary>Response Schema</summary>

```json
{
  "2025": {
    "red_bull": "3671C6",
    "ferrari": "E80020",
    "mercedes": "27F4D2",
    "mclaren": "FF8000",
    "aston_martin": "229971",
    "alpine": "0093cc",
    "williams": "64C4FF",
    "rb": "6692FF",
    "haas": "B6BABD",
    "sauber": "52E252"
  }
}
```

</details>

#### Colors by Driver

Returns hex color codes keyed by `driverId`.

```
GET /colors/drivers.json
```

---

## 📁 Repository Structure

```
f1-telemetry-api/
├── .github/workflows/
│   └── static.yml          # GitHub Pages deployment
├── colors/
│   ├── drivers.json        # Team colors indexed by driver ID
│   └── teams.json          # Team colors indexed by constructor ID & year
├── constructors/
│   ├── {year}.json         # Constructors list for each season
│   └── {year}/             # Per-season constructor → driver mappings
│       └── {constructorId}.json
├── drivers/
│   └── {driverId}.json     # Detailed stats for each driver (889 files)
├── races/
│   ├── races.json          # All races indexed by season
│   ├── racesbyMK.json      # Races indexed by OpenF1 meeting key
│   └── {year}/             # Per-season race data
│       ├── raceDetails.json
│       ├── results.json
│       ├── qualifying.json
│       ├── sprint.json
│       ├── driverStandings.json
│       └── constructorStandings.json
├── api_update.py           # Data update script
├── driversList.json        # Master list of all F1 drivers
├── index.html              # API documentation landing page
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Data Sources

| Source | Used For |
|--------|----------|
| [Jolpi Ergast API](https://api.jolpi.ca/ergast/f1) | Driver data, race results, qualifying, sprint, standings, constructors |
| [OpenF1 API](https://api.openf1.org) | Race meeting details (meeting keys, locations) |

---

## 🔄 Updating Data

Data is updated **manually** by running `api_update.py` locally. There is no automated schedule — you have full control over when data is refreshed.

**Process:**
1. Run the desired update functions in `api_update.py` (see [Local Development](#-local-development))
2. Commit and push the updated JSON files
3. GitHub Pages automatically redeploys via the `static.yml` workflow

---

## 🛠️ Local Development

### Prerequisites

- Python 3.10+
- `pip`

### Setup

```bash
# Clone the repository
git clone https://github.com/MatthewDelong/f1-telemetry-api.git
cd f1-telemetry-api

# Install dependencies
pip install -r requirements.txt
```

### Running the Update Script

The `api_update.py` script contains several update functions that can be called individually:

```python
import api_update

# Update constructor lists for the current season
api_update.update_constructors()

# Update which drivers drive for each constructor
api_update.update_constructor_drivers()

# Update race meeting details from OpenF1
api_update.update_races()

# Fetch and update driver statistics from latest race
api_update.update_driverData()

# Run statistical analysis on all driver data
api_update.analyse_driverData()

# Clean NaN values in driver data
api_update.replace_NaN()

# Update race results, qualifying, sprint, and standings
api_update.update_raceResults()
api_update.update_qualifying()
api_update.update_sprint()
api_update.update_standings()
```

---

## 📊 Data Coverage

- **Seasons:** 1950 – 2026 (77 seasons)
- **Drivers:** 889 individual driver profiles
- **Constructors:** Full history from 1950 onwards
- **Race Data:** Results, qualifying, sprints, standings per season

---

## 📜 License

This project is open source. Data is sourced from the Ergast/Jolpi API and OpenF1 API.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to add new endpoints, fix data issues, or improve the update scripts:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request
