import pytest
import json
import jsonschema
from scraper import fetch_and_extract
from pytest_snapshot.plugin import Snapshot

# Schema JSON per verificare la struttura dell'output
json_schema = {
    "type": "object",
    "properties": {
        "Ingredient_Name": {"type": "string"},
        "INCI_Name": {"type": "string"},
        "Link": {"type": "string", "format": "uri"}
    },
    "required": ["Ingredient_Name", "INCI_Name", "Link"]
}

# 1. Test Assert: Verifica che il recupero dati non sia vuoto e abbia la struttura corretta
def test_scraper_output():
    records = fetch_and_extract()
    assert len(records) > 0, "La lista di ingredienti non dovrebbe essere vuota"
    
    for record in records:
        assert "Ingredient_Name" in record, "L'output dovrebbe avere 'Ingredient_Name'"
        assert "INCI_Name" in record, "L'output dovrebbe avere 'INCI_Name'"
        assert "Link" in record, "L'output dovrebbe avere 'Link'"

# 2. Test JSON Schema: Verifica che ogni record segua lo schema JSON
def test_json_schema_validation():
    records = fetch_and_extract()
    
    for record in records:
        try:
            jsonschema.validate(instance=record, schema=json_schema)
        except jsonschema.exceptions.ValidationError as err:
            pytest.fail(f"Errore nello schema JSON per l'elemento {record}: {err}")

# 3. Test Snapshot: Confronta l'output con lo snapshot salvato
def test_snapshot(snapshot: Snapshot):
    records = fetch_and_extract()
    
    # Converti la lista di dizionari in una stringa JSON
    records_json = json.dumps(records, indent=2)
    
    # Confronta l'output serializzato (stringa JSON) con lo snapshot
    snapshot.assert_match(records_json, "scraper_output_snapshot.json")
