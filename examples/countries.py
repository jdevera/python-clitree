from clitree import tree

# Nested dictionary structure for countries and capitals
COUNTRY_DATA = {
    "Europe": [
        {"country": "France", "capital": "Paris"},
        {"country": "Germany", "capital": "Berlin"},
        {"country": "Italy", "capital": "Rome"},
        {"country": "Spain", "capital": "Madrid"},
        {"country": "United Kingdom", "capital": "London"},
    ],
    "Africa": [
        {"country": "Egypt", "capital": "Cairo"},
        {"country": "Nigeria", "capital": "Abuja"},
        {"country": "South Africa", "capital": "Pretoria"},
        {"country": "Kenya", "capital": "Nairobi"},
        {"country": "Morocco", "capital": "Rabat"},
    ],
}


def build_tree(data):
    root = {"name": "Earth", "children": []}
    for continent, countries in data.items():
        continent_node = {"name": f"{continent} (Continent)", "children": []}
        for country_data in countries:
            country_node = {
                "name": f"{country_data['country']} (Country)",
                "children": [{"name": f"{country_data['capital']} (Capital)"}],
            }
            continent_node["children"].append(country_node)
        root["children"].append(continent_node)
    return root


if __name__ == "__main__":
    country_tree = build_tree(COUNTRY_DATA)
    print(tree(country_tree, children="children"))
