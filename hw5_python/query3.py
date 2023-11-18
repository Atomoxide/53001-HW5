from sakila_db import MySQLDB, check_store_inventory


def main():
    sakiladb = MySQLDB(host="localhost", user="root", pwd="TeeMeow1217!", db="sakila")

    check_store_inventory(sakiladb, title="Academy Dinosaur", store=1, print_out=True)


if __name__ == "__main__":
    main()
