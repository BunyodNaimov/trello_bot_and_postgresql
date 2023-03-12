## trello_bot_and_postgresql

# table lar yaratish
```sql
CREATE TABLE boards
(
    id        SERIAL PRIMARY KEY,
    name      varchar(255)       not null,
    trello_id varchar(64) UNIQUE NOT NULL
);

CREATE TABLE lists
(
    id        SERIAL PRIMARY KEY,
    name      varchar(255)       not null,
    trello_id varchar(64) UNIQUE NOT NULL,
    board_id  int REFERENCES boards (id)
);

CREATE TABLE cards
(
    id          SERIAL PRIMARY KEY,
    name        varchar            NOT NULL,
    trello_id   varchar(64) UNIQUE NOT NULL,
    url         varchar(255),
    description text,
    list_id     int REFERENCES lists (id)
);

CREATE TABLE users
(
    id              serial PRIMARY KEY,
    chat_id         bigint UNIQUE NOT NULL,
    first_name       varchar(255),
    last_name       varchar(255),
    username        varchar(255),
    trello_username varchar(255) UNIQUE,
    trello_id       varchar(64) UNIQUE
);

CREATE TABLE boards_users
(
    id       serial,
    board_id int REFERENCES boards (id),
    user_id  int REFERENCES users (id),
    primary key (board_id, user_id)
);

CREATE TABLE cards_users
(
    id      serial,
    card_id int references cards (id),
    user_id int references users (id),
    primary key (card_id, user_id)
);

CREATE TABLE labels
(
    id        SERIAL primary key,
    name      varchar(255)       NOT NULL,
    color     varchar(100),
    trello_id varchar(64) UNIQUE NOT NULL,
    board_id  int references boards (id)
);

CREATE TABLE cards_labels
(
    id       serial,
    card_id  int references cards (id),
    label_id int references labels (id),
    primary key (card_id, label_id)
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
