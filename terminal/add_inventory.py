import mysql.connector
import os
from dotenv import load_dotenv
import random

from pprint import pprint

# loading variables from .env file
load_dotenv()


def connect_to_database():
    try:
        return mysql.connector.connect(
            user=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            host="136.244.224.221",
            database="com303fplu",
        )
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL:", error)
        return None


# FUNCTIONS
# 1. Add inventory to a warehouse (table product)
def add_inventory_to_product():
    cnx = connect_to_database()
    cursor = cnx.cursor()

    # Input product details
    print(
        "Caution: Following fields cannot be null: product id, name, quantity and cost"
    )
    id = input("Enter product id: ")
    name = input("Enter product name: ")
    details = input("Enter product details: ") or "NA"
    material_care = input("Enter material care: ") or "NA"
    quantity = input("Enter quantity: ")
    cost = input("Enter cost: ")

    # Insert into product table
    try:
        query = """INSERT INTO product (id, name, details, material_care, quantity, cost, is_active) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(
            query,
            (
                id,
                name,
                details,
                material_care,
                quantity,
                cost,
                1,
            ),
        )
        cnx.commit()
    except mysql.connector.Error as error:
        cnx.rollback()
        print("Rolled back on product: ", id, name)
        print("Error adding inventory to product")
        print("MySQL Error:", error)

    cursor.close()
    cnx.close()

    return id


# 1.2. Add new inventory to appropiate specialization table
# Helper method
def get_category2id(cnx):
    cursor = cnx.cursor()

    category2id = {}
    try:
        query = """SELECT * FROM category"""
        cursor.execute(query)
        results = cursor.fetchall()
        for id, category in results:
            category2id[category] = id
    except mysql.connector.Error as error:
        cnx.rollback()
        print("Rolled back on: ")
        print("MySQL Error:", error)

    cursor.close()

    return category2id


def add_inventory_to_specialization(product_id):
    cnx = connect_to_database()
    cursor = cnx.cursor()

    # Get category id
    category2id = get_category2id(cnx)
    category_id = ""

    # Input product specialization
    print(
        "\n1. Apparel | 2. Home | 3. Stationery | 4. Travel | 5. Health and Beauty | 6. Food"
    )
    choice = input("Choose category: ")

    # auto-generated attribute
    upc = str(random.randint(10**12, 10**13 - 1))

    # apparel
    if choice == "1":
        category_id = category2id["Apparel"]
        size = input("Enter product size (max 5 characters): ") or "NA"
        gender = input("Enter product gender (F/M/U): ") or "NA"
        color = input("Enter product color (max 20 characters): ") or "NA"
        material = input("Enter product material (max 15 characters): ") or "NA"
        purpose = input("Enter product purpose (max 20 characters): ") or "NA"
        try:
            query = """INSERT INTO apparel (id, UPC, size, gender, color, material, purpose) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(
                query,
                (
                    product_id,
                    upc,
                    size,
                    gender,
                    color,
                    material,
                    purpose,
                ),
            )
            cnx.commit()
        except mysql.connector.Error as error:
            cnx.rollback()
            print("Rolled back on specialization: ", product_id)
            print("MySQL Error:", error)

    # home
    elif choice == "2":
        category_id = category2id["Home"]
        color = input("Enter product color (max 20 characters): ") or "NA"
        purpose = input("Enter product purpose (max 20 characters): ") or "NA"
        dimension = input("Enter product dimension (max 50 characters): ") or "NA"
        try:
            query = """INSERT INTO home (id, UPC, color, purpose, dimension) 
                        VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (product_id, upc, color, purpose, dimension))
            cnx.commit()
        except mysql.connector.Error as error:
            cnx.rollback()
            print("Rolled back on specialization: ", product_id)
            print("MySQL Error:", error)

    # stationery
    elif choice == "3":
        category_id = category2id["Stationery"]
        type = input("Enter product type (max 20 characters): ") or "NA"
        size = input("Enter product size (max 20 characters): ") or "NA"
        color = input("Enter product color (max 20 characters): ") or "NA"
        material = input("Enter product material (max 15 characters): ") or "NA"
        purpose = input("Enter product purpose (max 20 characters): ") or "NA"
        try:
            query = """INSERT INTO stationery (id, UPC, type, size, color, material, purpose) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(
                query, (product_id, upc, type, size, color, material, purpose)
            )
            cnx.commit()
        except mysql.connector.Error as error:
            cnx.rollback()
            print("Rolled back on specialization: ", product_id)
            print("MySQL Error:", error)

    # travel
    elif choice == "4":
        category_id = category2id["Travel"]
        type = input("Enter product type (max 20 characters): ") or "NA"
        size = input("Enter product size (max 20 characters): ") or "NA"
        color = input("Enter product color (max 20 characters): ") or "NA"
        material = input("Enter product material (max 15 characters): ") or "NA"
        purpose = input("Enter product purpose (max 20 characters): ") or "NA"
        try:
            query = """INSERT INTO travel (id, UPC, type, size, color, material, purpose) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(
                query, (product_id, upc, type, size, color, material, purpose)
            )
            cnx.commit()
        except mysql.connector.Error as error:
            cnx.rollback()
            print("Rolled back on specialization: ", product_id)
            print("MySQL Error:", error)

    # health_beauty
    elif choice == "5":
        category_id = category2id["Health & Beauty"]
        type = input("Enter product type (max 20 characters): ") or "NA"
        size = input("Enter product size (max 20 characters): ") or "NA"
        material = input("Enter product material (max 15 characters): ") or "NA"
        purpose = input("Enter product purpose (max 20 characters): ") or "NA"
        try:
            query = """INSERT INTO health_beauty (id, UPC, type, size, material, purpose) 
                        VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (product_id, upc, type, size, material, purpose))
            cnx.commit()
        except mysql.connector.Error as error:
            cnx.rollback()
            print("Rolled back on specialization: ", product_id)
            print("MySQL Error:", error)

    # food
    elif choice == "6":
        category_id = category2id["Food"]
        type = input("Enter product type (max 20 characters): ") or "NA"
        size = input("Enter product size (max 20 characters): ") or "NA"
        material = input("Enter product material (max 15 characters): ") or "NA"
        purpose = input("Enter product purpose (max 20 characters): ") or "NA"
        try:
            query = """INSERT INTO food (id, UPC, type, size, material, purpose) 
                        VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (product_id, upc, type, size, material, purpose))
            cnx.commit()
        except mysql.connector.Error as error:
            cnx.rollback()
            print("Rolled back on specialization: ", product_id)
            print("MySQL Error:", error)
    else:
        print(
            "Invalid choice. Failed to add product specialization. Please contact your DB admin"
        )

    # Insert into belongs table
    try:
        query = """INSERT INTO belongs (product_id, category_id) 
                    VALUES (%s, %s)"""
        cursor.execute(query, (product_id, category_id))
        cnx.commit()
    except mysql.connector.Error as error:
        cnx.rollback()
        print("Rolled back on: ", product_id)
        print("MySQL Error:", error)

    cursor.close()
    cnx.close()


# 2. Add inventory to a store from a warehouse
# 2.1. Check the inventory of the product in the warehouse
def add_inventory_to_store():
    try:
        cnx = connect_to_database()
        cursor = cnx.cursor()
        product_id = input("Enter product id:")
        store_id = input("Enter store id:")
        number_of_entities = int(input("Enter number of entities to add:"))

        check_invent_query = "SELECT COUNT(1) FROM product WHERE id = %s"
        cursor.execute(check_invent_query, (product_id,))
        does_exist = cursor.fetchone()[0]

        # 2.2. Take n unit(s) off of the product in warehouse
        try:
            get_current_quantity = "SELECT quantity FROM product WHERE id=%s"
            cursor.execute(get_current_quantity, (product_id,))
            current_quantity = cursor.fetchone()[0]
            update_query = "UPDATE product \
                            SET quantity = %s\
                            WHERE id = %s"

            if current_quantity >= number_of_entities:
                cursor.execute(
                    update_query,
                    (
                        current_quantity - number_of_entities,
                        product_id,
                    ),
                )
                # print(f"Moved {number_of_entities} units of product from warehouse. Current quantity in warehouse for this product is {current_quantity-number_of_entities}")
        except:
            print("Product doesn't exist.")
        # 2.3. Add n unit(s) of the product to the store
        # if product already exists, update quantity
        try:
            get_current_quantity_store = (
                "SELECT quantity FROM owns WHERE product_id=%s AND store_id=%s"
            )
            cursor.execute(
                get_current_quantity_store,
                (
                    product_id,
                    store_id,
                ),
            )
            current_quantity_store = cursor.fetchall()[0][0]
            # print("Current quantity of this product in store: ", current_quantity_store)
            if current_quantity != 0:
                # print('product already exists in store. Need to update quantity')
                update_quantity = current_quantity_store + number_of_entities
                # print("update quantity", update_quantity)
                update_query_owns = "UPDATE owns \
                                    SET quantity = %s\
                                    WHERE product_id = %s\
                                    AND store_id = %s"
                cursor.execute(
                    update_query_owns,
                    (
                        update_quantity,
                        product_id,
                        store_id,
                    ),
                )
                print(
                    f"Added {number_of_entities} unit of product_id {product_id} into storeId {store_id}"
                )
                print(
                    "Current quantity of this product in store: ",
                    current_quantity_store + number_of_entities,
                )
            else:
                print(
                    "Product doesn't exist in store. Need to create new record for this product"
                )
                insert_query_owns = (
                    "INSERT INTO owns (product_id, store_id, price, quantity) VALUES %s"
                )
                cursor.execute(insert_query_owns)
                # print("...")
                # print("Added new record to table owns")
        except:
            print("Error adding product into DB. Check storeId and productId.")
        cnx.commit()
        cursor.close()
        cnx.close()
    except:
        print("An error occurs.")


if __name__ == "__main__":
    add_inventory_to_product()
