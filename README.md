**Послідовність запуску:**
1. `git clone -b hometask-12 git@github.com:oleverse/PyEduWebHT11.git PyEduWebHT12`
2. Створимо і запустимо контейнер з БД:  
`docker run --name fastapi-auth-postgres -p 5432:5432 -e POSTGRES_PASSWORD=<secret> -d postgres`
3. Створюємо базу даних (приклад створення за допомогою psql):  
Підключаємося до БД:  
`psql --host localhost --port 5432 --username=postgres`  
PostgreSQL запитає пароль, вводимо пароль нашого контейнера  
Виконаємо запит для створення БД:  
`CREATE DATABASE <db_name> ENCODING 'UTF-8';`  
Відключаємося від БД:  
`\q` => `Enter`
4. Створимо віртуальне середовище і встановимо залежності:     
`cd PyEduWebHT12`  
`poetry shell`  
`poetry update`
5. Далі створюємо файл .env з таким вмістом:  
`SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://postgres:<secret>@localhost:5432/<db_name>`  
Необхідно змінити `<secret>` на той же пароль, що був вказаний при створенні контейнера postgresql,
а також вказати ім'я БД, що ми створили раніше.
6. Виконуємо міграцію БД:  
`alembic upgrade head`
7. Запускаємо uvicorn сервер  
`uvicorn main:app --host=localhost --port=8000 --reload`  
8. Ця робота не сильно відрізняється за функціоналом від попередньої (`PyEduWebHT11`).  
Але для тестування операцій, які потребують авторизації і роботи з JWT токенами, я вирішив
додати до репозиторію каталог `postman`, а у ньому можна знайти два JSON-файли.  
Це імпортоване Postman-середовище, у якому створені дві змінні для зберігання
токенів після автентифікації та імпортована Postman-колекція попередньо заготовлених запитів.
9. Тому можна відкрити `Postman`, натиснути `File -> Import` і обрати файли
`PyEduWebHT12.postman_environment.json` та `PyEduWebHT12.postman_collection.json`
10. Після імпорту не забуваємо перемкнутися на імпортоване середовище у правому верхньому кутку
вікна `Postman`, тобто змінити `No Environment` на `PyEduWebHT12`
11. Далі можна користуватися колекцією імпортованих запитів.
12. Маємо на увазі, що запити `Login` та `Refresh Token` після отримання відповіді від
сервера автоматично зберігають `access_token` i `refresh_token` для подальшої роботи й
робити це вручну не потрібно.
