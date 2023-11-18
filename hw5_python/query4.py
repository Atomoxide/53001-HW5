from sakila_db import MySQLDB, count_revenue_per_film


def main():
    sakiladb = MySQLDB(host="localhost", user="root", pwd="TeeMeow1217!", db="sakila")

    count_revenue_per_film(sakiladb, print_out=True)


if __name__ == "__main__":
    main()
