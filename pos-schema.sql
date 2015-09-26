CREATE DATABASE pos;
USE pos;

CREATE TABLE sales_h(
or_no varchar(20),
register_date date,
cashier_id int(10),
customer_id int(10),
sales_gross_amount int,
PRIMARY KEY(or_no)
);

CREATE TABLE sales_d(
link_or varchar(20),
link_item int(10),
quantity int,
price int,
discount_rate int,
PRIMARY KEY(link_or)
);

CREATE TABLE customer(
cust_id int(10),
cust_name varchar(80),
cust_address varchar(80),
cust_cp_no varchar(20),
cust_gender varchar(2),
PRIMARY KEY(cust_id)
);

CREATE TABLE employee(
emp_id int(10),
emp_name varchar(80),
emp_address varchar(80),
emp_cp_no varchar(20),
emp_position varchar(40),
PRIMARY KEY(emp_id)
);

CREATE TABLE item(
item_id int(10),
item_description varchar(60),
latest_qoh int(10),
selling_price int,
item_status varchar(2),
PRIMARY KEY(item_id)
);

-- LOAD DATA LOCAL INFILE 'data/sales_h.txt' INTO TABLE sales_h COLUMNS TERMINATED BY '|' LINES TERMINATED BY '\n;
-- LOAD DATA LOCAL INFILE 'data/sales_d.txt' INTO TABLE sales_d COLUMNS TERMINATED BY '|' LINES TERMINATED BY '\n;
-- LOAD DATA LOCAL INFILE 'data/customer.txt' INTO TABLE customer COLUMNS TERMINATED BY '|' LINES TERMINATED BY '\n;
-- LOAD DATA LOCAL INFILE 'data/employee.txt' INTO TABLE employee COLUMNS TERMINATED BY '|' LINES TERMINATED BY '\n;
-- LOAD DATA LOCAL INFILE 'data/item.txt' INTO TABLE item COLUMNS TERMINATED BY '|' LINES TERMINATED BY '\n;