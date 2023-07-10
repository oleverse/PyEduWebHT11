**Послідовність запуску:**
1. `git clone git@github.com:oleverse/PyEduWebHT11.git`
2. Створимо і запустимо контейнер з БД:  
`docker run --name fastapi-postgres -p 5432:5432 -e POSTGRES_PASSWORD=<secret> -d postgres`
3. Створюємо базу даних (приклад створення за допомогою psql):  
Підключаємося до БД:  
`psql --host localhost --port 5432 --username=postgres`  
PostgreSQL запитає пароль, вводимо пароль нашого контейнера  
Виконаємо запит для створення БД:  
`CREATE DATABASE <db_name> ENCODING 'UTF-8';`  
Відключаємося від БД:  
`\q` => `Enter`
4. Створимо віртуальне середовище і встановимо залежності:     
`cd PyEduWebHT11`  
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
8. Відкриваємо у браузері адресу застосунку і граємося з запитами :)    
`http://127.0.0.1:8000/docs`
9. Для отримання списку контактів, у яких ДН найближчого тижня, потрібно задати Query параметрові
`bt_within_week` значення `true` або `1`
