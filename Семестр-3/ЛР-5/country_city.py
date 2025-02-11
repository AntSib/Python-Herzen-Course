def find_country_by_city(country_city_dict: dict, city_list: list) -> tuple:
    """
    Iterate over all cities in city_list and for each city, find the country
    in country_city_dict. Yield tuples of city and country.

    :param country_city_dict: dict with countries as keys and lists of cities as values
    :param city_list: list of cities to search for
    :return: tuple of city, country
    """
    for city in city_list:
        for country, cities in country_city_dict.items():   # Iterate over countries
            if city in cities:
                yield city, country


country_city_dict = {                                       # Search dict
    'Russia': ['Moscow', 'Saint-Petersburg', 'Novgorod'],
    'China': ['Beijing', 'Shanghai', 'Nanjing'],
    'USA': ['New York', 'Los Angeles', 'Chicago'],
    'Italy': ['Rome', 'Milan', 'Turin'],
}

city_list = ['Milan', 'Rome', 'Paris', 'Saint-Petersburg', 'Chicago', 'Shanghai']


def main():
    for city, country in find_country_by_city(country_city_dict, city_list):
        print(f"City {city} is in {country}")


if __name__ == "__main__":
    main()
