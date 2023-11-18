from sakila_db import MySQLDB, Select, adjust_film_price


def main():
    sakiladb = MySQLDB(host="localhost", user="root", pwd="TeeMeow1217!", db="sakila")

    # calling function to adjust prices
    adjust_film_price(sakiladb, "Sports", 1.1)
    
    # printing out adjusted prices
    query_sports_film_rate = Select("film.title AS title", "rental_rate")
    query_sports_film_rate.select_from("film", ("film_category", "film_id"), ("category", "category_id"))
    query_sports_film_rate.append_clause("WHERE name LIKE 'Sports'")
    results = sakiladb.send_command(query_sports_film_rate.get_command())
    print("List of Sports film with updated price")
    for title in results:
        print(f"\t{title['title']}: ${title['rental_rate']}")


if __name__ == "__main__":
    main()