import mysql.connector


class MySQLDB:
    """MySQL database object"""
    def __init__(self, host, user, pwd, db) -> None:
        self.db = mysql.connector.connect(
            host=host, user=user, password=pwd, database=db, autocommit=True
        )

    def send_command(self, query):
        """push MySQL command"""
        mycursor = self.db.cursor(dictionary=True)
        mycursor.execute(query)
        return mycursor.fetchall()


class Select:
    """SELECT command object"""
    def __init__(self, *args) -> None:
        self.__command = "SELECT "
        self.__command += ", ".join(args)

    def append_clause(self, *args):
        """append new claus after current command"""
        for arg in args:
            self.__command += "\n"
            self.__command += arg

    def select_from(self, root_table, *args):
        """format SELECT FROM and LEFT JOIN"""
        if args:
            join_string = root_table
            tables = [root_table]
            tables.extend([arg[0] for arg in args])
            join_on_tables = [
                (tables[i], tables[i + 1]) for i in range(len(tables) - 1)
            ]
            for arg, table in zip(args, join_on_tables):
                join_string += (
                    f"\nJOIN {table[1]} ON {table[0]}.{arg[1]} = {table[1]}.{arg[1]}"
                )
            self.append_clause(f"FROM {join_string}")
        else:
            self.append_clause(f"FROM {root_table}")

    def group_by(self, field):
        """Format GROUP BY"""
        self.append_clause(f"GROUP BY {field}")

    def order_by(self, field, *, order="ASC"):
        """Format ORDER BY"""
        self.append_clause(f"ORDER BY {field} {order}")

    def get_command(self, *, end=True):
        """Return string MySQL command"""
        if end:
            return self.__command + ";"
        else:
            return self.__command


class Insert:
    """MySQL Insert Object"""
    def __init__(self, *args, into_table, fields) -> None:
        """Format INSERT INTO command"""
        self.__command = f"INSERT INTO {into_table} " + f"({', '.join(fields)})"
        value_list = list()
        for arg in args:
            value = ", ".join(arg)
            value_list.append(f"({value})")
        values_string = ", ".join(value_list)
        self.__command += f"\nVALUES {values_string}"
        self.__table = into_table

    def get_command(self, *, end=True):
        """return string MySQL command"""
        if end:
            return self.__command + ";"
        else:
            return self.__command

    def get_table(self):
        """return target table"""
        return self.__table

    def append_clause(self, *args):
        """append new claus after current command"""
        for arg in args:
            self.__command += "\n"
            self.__command += arg


class Update:
    def __init__(self, *args, set_table) -> None:
        self.__command = f"UPDATE {set_table}\nSET "
        values = list()
        for arg in args:
            values.append(f"{arg[0]} = {arg[1]}")
        self.__command += ", ".join(values)
        self.__table = set_table

    def get_command(self, *, end=True):
        """return string MySQL command"""
        if end:
            return self.__command + ";"
        else:
            return self.__command

    def get_table(self):
        """return target table"""
        return self.__table

    def append_clause(self, *args):
        """append new claus after current command"""
        for arg in args:
            self.__command += "\n"
            self.__command += arg

class Delete:
    def __init__(self, *, from_table, condition) -> None:
        self.__command = f"DELETE FROM {from_table}"
        self.__command += f"\nWHERE {condition}"
        self.__table = from_table
    
    def get_command(self, *, end=True):
        """return string MySQL command"""
        if end:
            return self.__command + ";"
        else:
            return self.__command
    
    def get_table(self):
        """return target table"""
        return self.__table

    def append_clause(self, *args):
        """append new claus after current command"""
        for arg in args:
            self.__command += "\n"
            self.__command += arg

def customer_by_country(db, country, *, print_out=False):
    """return list of customer registered in the passed in country"""
    customer_by_country_query = Select(
        "CONCAT(first_name,' ', last_name) AS name, email"
    )
    customer_by_country_query.select_from(
        "customer",
        ("address", "address_id"),
        ("city", "city_id"),
        ("country", "country_id"),
    )
    customer_by_country_query.append_clause(f"WHERE country LIKE '{country}'")
    customer_list = db.send_command(customer_by_country_query.get_command())
    customer_number = len(customer_list)
    if print_out:
        print(f"There are {customer_number} registered customer(s) in China:")
        for customer in customer_list:
            print(f"\t {customer['name']} ({customer['email']})")
    return customer_list, customer_number


def check_store_inventory(db, *, title, store, print_out=False):
    """return bool on whether passed in title is available in passed in store"""
    check_query = Select("COUNT(*)")
    check_query.select_from("store", ("inventory", "store_id"), ("film", "film_id"))
    has_inventory = bool(db.send_command(check_query.get_command())[0]["COUNT(*)"])
    if print_out:
        if has_inventory:
            print(f"{title} is available at store {store}.")
        else:
            print(f"{title} is not available at store {store}.")
    return has_inventory


def count_revenue_per_film(db, *, print_out=False):
    """reture list of title by its total revenue"""
    count_revenue_query = Select("title, SUM(amount) AS revenues")
    count_revenue_query.select_from(
        "film",
        ("inventory", "film_id"),
        ("rental", "inventory_id"),
        ("payment", "rental_id"),
    )
    count_revenue_query.group_by("title")
    count_revenue_query.order_by("revenues", order="DESC")
    results = db.send_command(count_revenue_query.get_command())
    if print_out:
        print("\ttitle: revenues")
        for item in results:
            print(f"\t{item['title']}: ${float(item['revenues'])}")
    return results


def insert_city(db, insert_obj):
    """insert a new city"""
    db.send_command(insert_obj.get_command())


def adjust_film_price(db, category, multiplier):
    """adjust all price of given category"""
    query_sports_film = Select("film_id")
    query_sports_film.select_from("film_category", ("category", "category_id"))
    query_sports_film.append_clause(f"WHERE name = '{category}'")
    update_price = Update(
        ("rental_rate", f"rental_rate*{multiplier}"), set_table="film"
    )
    update_price.append_clause(
        "WHERE film_id IN (", query_sports_film.get_command(end=False), ")"
    )
    db.send_command(update_price.get_command())

def delete_from_payment(db, delete_obj):
    """delete all payments of passed in Delete object"""
    db.send_command(delete_obj.get_command())
    