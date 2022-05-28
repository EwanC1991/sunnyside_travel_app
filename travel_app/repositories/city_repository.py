from db.run_sql import run_sql

from models.city import City
from models.country import Country

import repositories.country_repository as country_repository

def save(city):
    sql = "INSERT INTO cities (name, visited, country_id) VALUES (?, ?, ?) RETURNING *"
    values = [city.name, city.visited, city.country.id]
    results = run_sql(sql, values)
    id = results[0]['id']
    city.id = id
    return city

def select_all():
    cities = []

    sql = "SELECT * FROM cities"
    results = run_sql(sql)

    for row in results:
        visited = True if row['visited'] == 1 else False
        country = country_repository.select(row['country_id'])
        city = City(row['name'], visited, country, row['id'])
        cities.append(city)
    return cities

def select(id):
    city = None
    sql = "SELECT * FROM cities WHERE id = ?"
    values = [id]
    result = run_sql(sql, values)[0]

    if result is not None:
        visited = True if result['visited'] == 1 else False
        country = country_repository.select(result['country_id'])
        city = City(result['name'], visited, country, result['id'])
    return city

def delete_all():
    sql = "DELETE FROM cities"
    run_sql(sql)