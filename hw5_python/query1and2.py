from sakila_db import MySQLDB, customer_by_country


def main():
    sakiladb = MySQLDB(host="localhost", user="root", pwd="TeeMeow1217!", db="sakila")

    customer_in_china_list, customer_in_china_number = customer_by_country(
        sakiladb, "CHINA", print_out=True
    )


if __name__ == "__main__":
    main()
