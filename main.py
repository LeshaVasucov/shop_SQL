import sqlite3

db = sqlite3.connect("shop.db")


db.execute("""CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);
""")


db.execute("""CREATE TABLE IF NOT EXISTS customers ( 
           customer_id INTEGER PRIMARY KEY, 
           first_name TEXT NOT NULL, 
           last_name TEXT NOT NULL, 
           email TEXT NOT NULL UNIQUE 
);
""")

db.execute("""CREATE TABLE IF NOT EXISTS orders ( 
           order_id INTEGER PRIMARY KEY, 
           customer_id INTEGER NOT NULL, 
           product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, 
           order_date DATE NOT NULL, 
           FOREIGN KEY (customer_id) REFERENCES customers(customer_id), 
           FOREIGN KEY (product_id) REFERENCES products(product_id) 
);
""")

def add_product():
    name = input("Input name :")
    category = input("Input category :")
    price = float(input("Input price :"))
    db.execute("""INSERT INTO products (name , category , price)
               VALUES(?,?,?);""",(name, category, price))
    db.commit()

def add_user():
    name = input("Input name :")
    last_name = input("Input last_name :")
    email = input("Input email :")
    db.execute("""INSERT INTO customers (first_name, last_name, email)
               VALUES(?,?,?);""",(name, last_name, email))
    db.commit()

def add_order():
        customer_id = int(input("Product_id :"))
        product_id = int(input("Product_id :"))
        quantity = int(input("Quantity :"))
        db.execute("""INSERT INTO orders (customer_id, product_id, quantity, order_date)
                   VALUES(?,?,?,CURRENT_DATE)""",(customer_id, product_id, quantity))
        db.commit()

def income():
    income = db.execute("""SELECT SUM(orders.quantity * products.price)
                        FROM orders INNER JOIN products
                        ON products.product_id == orders.order_id""")
    print(income.fetchone())

def users_orders():
    info = db.execute("""SELECT c.first_name, COUNT(o.order_id)
                      FROM orders o INNER JOIN customers c
                      ON o.customer_id == c.customer_id
                      GROUP BY c.first_name   """)
    print(info.fetchall())

def average_price():
    res = db.execute("""SELECT AVG(p.price * o.quantity)
                     FROM orders o INNER JOIN products p
                     ON p.product_id == o.product_id """)
    print(res.fetchone())
def popular_category():
    info = db.execute("""SELECT p.category, COUNT(o.order_id) AS order_count
                      FROM orders o INNER JOIN products p
                      ON p.product_id == o.product_id
                      GROUP BY p.category
                      ORDER BY order_count DESC""")
    print(info.fetchone())

def category_quantity():
    info = db.execute("""SELECT products.category, COUNT(products.product_id) AS amount
                      FROM products
                      GROUP BY category
                      ORDER BY amount""")
    print(info.fetchall())

def edit_price():
    category = input("category :")
    info = db.execute("""UPDATE products
                      SET price = price * 1.1
                      WHERE category == (?)""",(category,)) 
    db.commit()
while True:
    print('''
Select an option:
1 - Add a product
2 - Add a client
3 - Order an item
4 - View total income
5 - View the number of orders for each client
6 - View average order price
7 - View the most popular category
8 - View total quantity of products for each category
9 - Update prices by 10%
0 - Exit''')
    
    cmd = int(input("Choose an option: "))

    match cmd:
        case 0:
            break
        case 1:
            add_product()
        case 2:
            add_user()
        case 3:
            add_order()
        case 4:
            income()
        case 5:
            users_orders()
        case 6:
            average_price()
        case 7:
            popular_category()
        case 8:
            category_quantity()
        case 9:
            edit_price()