## trello_bot_and_postgresql

# table lar yaratish
```sql
create table boards(
    id bigserial primary key,
    name varchar(500) not null,
    board_trello_id varchar(50) unique not null
);

create table lists(
    id bigserial primary key,
    name varchar (500) not null,
    list_trello_id varchar(50) unique not null,
    board_id integer references boards(id)
);
create table cards(
    id bigserial primary key,
    name varchar(500) not null,
    card_trello_id varchar(50) unique not null,
    url varchar(500) not null,
    Description text,
    lists_id integer references lists(id)
);
create table members(
    id bigserial primary key,
    fullname varchar(100) not null,
    trello_username varchar(100) unique not null,
    member_trello_id varchar(50) unique not null
);
create table cards_members(
    id serial,
    card_id integer references cards(id),
    member_id integer references members(id),
    primary key (card_id, member_id)
);
create table board_members(
    id serial,
    board_id integer references boards(id) unique not null ,
    member_id integer references members(id)
);
create table labels(
    id bigserial primary key,
    name varchar check ( name > '0' ),
    label_trello_id varchar not null unique,
    board_id integer references boards(id)
);
create table cards_labels(
    id serial,
    card_id integer references cards(id),
    labels_id integer references labels(id),
    primary key (card_id, labels_id)
);
create table users(
    id bigserial primary key,
    chat_id bigint not null unique,
    fullname varchar(100),
    username varchar(100) not null unique,
    member_id integer references members(id)
);
```
![image](https://user-images.githubusercontent.com/122611882/224089219-e32d46c3-2596-4194-83e9-a1852ddadae2.png)


# Pycharm bilan database integratsiya
```sql
import psycopg2
from environs import Env

env = Env()
env.read_env()
connection = psycopg2.connect(
    dbname=env('dbname'),
    user=env('user'),
    password=env('password'),
    host=env('host'),
    port=env('port')
)
```
![image](https://user-images.githubusercontent.com/122611882/224089348-57dbbfd4-bca6-4331-acf0-c1c41fc977b5.png)


## Telegram bot


![image](https://user-images.githubusercontent.com/122611882/224088709-58768aa8-c407-4915-aaff-61b5b34a5e2b.png)
#

![image](https://user-images.githubusercontent.com/122611882/224088755-5fb9a4ac-c92e-46bf-bc95-be7153c2429e.png)
#

![image](https://user-images.githubusercontent.com/122611882/224088796-c16ab870-0ea4-4052-ae0c-edca92aefcc4.png)
#
