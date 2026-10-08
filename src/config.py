"""Settings shared by the pipeline: countries, categories, colours, years."""

# Countries in the order they appear in the deck (ENTSO-E MapCode -> name)
COUNTRIES = {
    "AT": "Austria",
    "BG": "Bulgaria",
    "CZ": "Czechia",
    "DE": "Germany",
    "IT": "Italy",
    "PL": "Poland",
    "SK": "Slovakia",
}

# Years compared side by side on each slide
BASE_YEAR = 2021
COMPARISON_YEAR = 2026

# Deck categories, in legend/doughnut order, with their colour and whether
# they count as non-fossil (renewables + nuclear).
CATEGORIES = {
    "Solar":            {"color": "EDA100", "non_fossil": True},
    "Wind":             {"color": "1BAF7A", "non_fossil": True},
    "Hydro":            {"color": "2A78D6", "non_fossil": True},
    "Biomass":          {"color": "008300", "non_fossil": True},
    "Other renewables": {"color": "7FB77E", "non_fossil": True},
    "Nuclear":          {"color": "8E5AC8", "non_fossil": True},
    "Gas":              {"color": "EB6834", "non_fossil": False},
    "Coal and lignite": {"color": "4D4D4D", "non_fossil": False},
    "Oil":              {"color": "7A4A2B", "non_fossil": False},
    "Other":            {"color": "8A8F98", "non_fossil": False},
}

# ENTSO-E production types -> deck categories.
# None = excluded (storage is not generation).
PRODUCTION_TYPE_MAP = {
    "Solar": "Solar",
    "Wind Onshore": "Wind",
    "Wind Offshore": "Wind",
    "Hydro Run-of-river and poundage": "Hydro",
    "Hydro Run-of-river and pondage": "Hydro",
    "Hydro Water Reservoir": "Hydro",
    "Hydro Pumped Storage": None,
    "Biomass": "Biomass",
    "Geothermal": "Other renewables",
    "Marine": "Other renewables",
    "Other renewable": "Other renewables",
    "Nuclear": "Nuclear",
    "Fossil Gas": "Gas",
    "Fossil Hard coal": "Coal and lignite",
    "Fossil Brown coal/Lignite": "Coal and lignite",
    "Fossil Coal-derived gas": "Coal and lignite",
    "Fossil Peat": "Coal and lignite",
    "Fossil Oil": "Oil",
    "Fossil Oil shale": "Oil",
    "Waste": "Other",
    "Other": "Other",
    "Energy storage": None,
}

# Slice labels are shown only for shares at or above this threshold
LABEL_MIN_SHARE = 0.05

# Text style (matches the original deck)
FONT = "Arial"
NAVY = "0B3C6F"
GREY = "5B6470"
