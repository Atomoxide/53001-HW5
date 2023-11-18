from sakila_db import MySQLDB, Delete, Select, delete_from_payment


def main():
    sakiladb = MySQLDB(host="localhost", user="root", pwd="TeeMeow1217!", db="sakila")

    # construct Delete object to delete all payments with the condition
    delete_payment = Delete(from_table="payment", condition="DATE(payment_date) = '2005-08-07'")

    # calling function to adjust prices
    delete_from_payment(sakiladb, delete_payment)
    
    # print out table
    select_payment = Select("payment_id AS id", "amount", "payment_date")
    select_payment.select_from("payment")
    select_payment.append_clause("WHERE DATE(payment_date) = '2005-08-07'")
    results = sakiladb.send_command(select_payment.get_command())
    for result in results:
        print(f"\t{result['id']}: ${result['amount']}, paid on {result['payment_date']}")

if __name__ == "__main__":
    main()