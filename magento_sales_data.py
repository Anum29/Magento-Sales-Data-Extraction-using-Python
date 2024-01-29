import pandas as pd
import mysql.connector

# Production DB credentials
host = "XXXXXXX"
user = "xxx"
passwd = "yyy"
# db_name = "abc"

# Connect to data mart
cnx = mysql.connector.connect(
    host=host,
    user=user,
    password=passwd)
print(cnx)
cursor = cnx.cursor(buffered=True)

db_connection = mysql.connector.connect(host=host, database=db_name, user=user, password=passwd)

db_cursor = db_connection.cursor()

# Overall sales stats
db_cursor.execute("""
    SELECT
        DATE(DATE_ADD(created_at, INTERVAL 5 HOUR)) as Date,
        SUM(`Actual Revenue`) as `Actual revenue`,
        SUM(`Lost Revenue`) as `Lost revenue`,
        COUNT(*) as `Total orders`,
        SUM(closed_order) as `Total closed`,
        SUM(canceled_order) as `Total canceled`,
        SUM(canceled_value) as `Canceled value`,
        SUM(closed_value) as `Closed value`
    FROM
        (
            SELECT
                DATE(DATE_ADD(created_at, INTERVAL 5 HOUR)) as created_at,
                order_currency_code,
                status,
                subtotal,
                base_discount_amount,
                CASE
                    WHEN (status='complete' OR status='processing' OR status='pending') AND order_currency_code='PKR' THEN (subtotal + base_discount_amount + tax_amount)
                    WHEN (status='complete' OR status='processing' OR status='pending') AND order_currency_code='USD' THEN (subtotal + base_discount_amount + tax_amount) * 175.29
                    WHEN (status='complete' OR status='processing' OR status='pending') AND order_currency_code='AED' THEN (subtotal + base_discount_amount + tax_amount) * 47.72
                    WHEN (status='complete' OR status='processing' OR status='pending') AND order_currency_code='GBP' THEN (subtotal + base_discount_amount + tax_amount) * 242.32
                    WHEN (status='complete' OR status='processing' OR status='pending') AND order_currency_code='CAD' THEN (subtotal + base_discount_amount + tax_amount) * 141.90
                END AS `Actual Revenue`,
                CASE
                    WHEN (status='closed' OR status='canceled') AND order_currency_code='PKR' THEN (subtotal + base_discount_amount + tax_amount)
                    WHEN (status='closed' OR status='canceled') AND order_currency_code='USD' THEN (subtotal + base_discount_amount + tax_amount) * 175.29
                    WHEN (status='closed' OR status='canceled') AND order_currency_code='AED' THEN (subtotal + base_discount_amount + tax_amount) * 47.72
                    WHEN (status='closed' OR status='canceled') AND order_currency_code='GBP' THEN (subtotal + base_discount_amount + tax_amount) * 242.32
                    WHEN (status='closed' OR status='canceled') AND order_currency_code='CAD' THEN (subtotal + base_discount_amount + tax_amount) * 141.90
                END AS `Lost Revenue`,
                CASE
                    WHEN (status='closed') THEN 1
                    ELSE 0
                END AS closed_order,
                CASE
                    WHEN (status='canceled') THEN 1
                    ELSE 0
                END AS canceled_order,
                CASE
                    WHEN (status='canceled') AND order_currency_code='PKR' THEN (subtotal + base_discount_amount + tax_amount)
                    WHEN (status='canceled') AND order_currency_code='USD' THEN (subtotal + base_discount_amount + tax_amount) * 175.29
                    WHEN (status='canceled') AND order_currency_code='AED' THEN (subtotal + base_discount_amount + tax_amount) * 47.72
                    WHEN (status='canceled') AND order_currency_code='GBP' THEN (subtotal + base_discount_amount + tax_amount) * 242.32
                    WHEN (status='canceled') AND order_currency_code='CAD' THEN (subtotal + base_discount_amount + tax_amount) * 141.90
                    ELSE 0
                END AS canceled_value,
                CASE
                    WHEN (status='closed') AND order_currency_code='PKR' THEN (subtotal + base_discount_amount + tax_amount)
                    WHEN (status='closed') AND order_currency_code='USD' THEN (subtotal + base_discount_amount + tax_amount) * 175.29
                    WHEN (status='closed') AND order_currency_code='AED' THEN (subtotal + base_discount_amount + tax_amount) * 47.72
                    WHEN (status='closed') AND order_currency_code='GBP' THEN (subtotal + base_discount_amount + tax_amount) * 242.32
                    WHEN (status='closed') AND order_currency_code='CAD' THEN (subtotal + base_discount_amount + tax_amount) * 141.90
                    ELSE 0
                END AS closed_value
            FROM
                sales_order
            WHERE
                (status='complete' OR status='processing' OR status='pending' OR status='closed' OR status='canceled') AND DATE(DATE_ADD(created_at, INTERVAL 5 HOUR))<='2021-11-23'
        ) AS derived
    GROUP BY
        DATE(DATE_ADD(created_at, INTERVAL 5 HOUR))
    ORDER BY
        DATE(DATE_ADD(created_at, INTERVAL 5 HOUR))
""")

table_rows = db_cursor.fetchall()

sales_stats_date = pd.DataFrame(table_rows)
sales_stats_date.columns = ['date', 'actual_revenue', 'lost_revenue', 'total_orders', 'total_closed', 'total_canceled', 'canceled_value', 'closed_value']
