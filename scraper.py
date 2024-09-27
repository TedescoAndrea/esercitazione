import requests

# Lista degli URL da cui fare scraping
urls = [
    "https://cir-reports.cir-safety.org/FetchCIRReports",
    "https://cir-reports.cir-safety.org/FetchCIRReports/?&pagingcookie=%26lt%3bcookie%20page%3d%26quot%3b1%26quot%3b%26gt%3b%26lt%3bpcpc_name%20last%3d%26quot%3bPEG-50%20Stearate%26quot%3b%20first%3d%26quot%3b1%2c10-Decanediol%26quot%3b%20%2f%26gt%3b%26lt%3bpcpc_ingredientidname%20last%3d%26quot%3bPEG-50%20Stearate%26quot%3b%20first%3d%26quot%3b1%2c10-Decanediol%26quot%3b%20%2f%26gt%3b%26lt%3bpcpc_cirrelatedingredientsid%20last%3d%26quot%3b%7bC223037E-F278-416D-A287-2007B9671D0C%7d%26quot%3b%20first%3d%26quot%3b%7b940AF697-52B5-4A3A-90A6-B9DB30EF4A7E%7d%26quot%3b%20%2f%26gt%3b%26lt%3b%2fcookie%26gt%3b&page=2",
]

def fetch_cir_reports(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Errore durante il recupero dei dati:", response.status_code)
        return None

def extract_data_from_json(data):
    records = []
    if data:
        results = data.get("results", [])
        for result in results:
            ingredient_name = result.get("pcpc_ingredientname", "")
            inci_name = result.get("pcpc_ciringredientname", "")
            id_link = result.get("pcpc_ingredientid", "")
            link = f"https://cir-reports.cir-safety.org/cir-ingredient-status-report/?id={id_link}"
            records.append({
                "Ingredient_Name": ingredient_name,
                "INCI_Name": inci_name,
                "Link": link
            })
    else:
        print("Nessun dato disponibile")
    return records

def fetch_and_extract():
    all_records = []
    for url in urls:
        print(f"Recupero dati dall'URL: {url}")
        cir_data = fetch_cir_reports(url)
        if cir_data:
            records = extract_data_from_json(cir_data)
            all_records.extend(records)
    return all_records
