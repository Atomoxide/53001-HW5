from sakila_db import MySQLDB, Insert, Select, insert_city


def main():
    sakiladb = MySQLDB(host="localhost", user="root", pwd="TeeMeow1217!", db="sakila")

    # initialize Insert object
    insert_chicago = Insert(
        ("'Chicago'", "103", "NOW()"),
        into_table="city",
        fields=("city", "country_id", "last_update"),
    )
    # calling function to insert
    insert_city(sakiladb, insert_chicago)
    
    # printing out result
    select_chicago = Select("*")
    select_chicago.select_from("city")
    select_chicago.append_clause("WHERE city LIKE 'Chicago'")
    print(sakiladb.send_command(select_chicago.get_command()))


if __name__ == "__main__":
    main()