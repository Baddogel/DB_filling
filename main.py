from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, \
                   TABLES, COUNT  # Импорт данных для подключения к БД и работы скрипта
import psycopg2  # Библиотека для работы с PostgreSQL
import faker  # Библиотека для генерации фейковых персональных данных
import random  # Библиотека для генерации случайных чисел


# Функция для получения списка таблиц из базы данных
def get_tables_from_db():
    cursor.execute("SELECT table_name FROM information_schema.tables "
                   "WHERE table_schema NOT IN ('information_schema','pg_catalog');")
    tables = zip(*cursor.fetchall())
    return list(tables)[0]


# Функция для заполнения таблицы 'students'.
# В качестве имени берем случайное имя из библиотеки faker.
# В качестве года начала обучения - случайный год от 2010 до 2024.
def fill_students():
    name = faker.first_name()
    start_year = random.randint(2010, 2024)
    cursor.execute("INSERT INTO students (name, start_year) VALUES (%s, %s)", (name, start_year))


# Функция для заполнения таблицы 'courses'
# В качестве названия берем случайные 3 слова из библиотеки faker.
# В качестве количества часов - случайное число от 50 до 300 с шагом 50.
def fill_courses():
    title = ' '.join(faker.words(nb=3))
    hours = random.randrange(50, 301, 50)
    cursor.execute("INSERT INTO courses (title, hours) VALUES (%s, %s)", (title, hours))


# Функция для получения списка id студентов
def get_student_id():
    cursor.execute("SELECT DISTINCT(s_id) FROM students")
    student_ids = zip(*cursor.fetchall())
    return list(student_ids)[0]


# Функция для получения списка id курсов
def get_course_id():
    cursor.execute("SELECT DISTINCT(c_no) FROM courses")
    course_ids = zip(*cursor.fetchall())
    return list(course_ids)[0]


# Функция для заполнения таблицы 'exams'
# В качестве id студента выбираем случайный из списка, полученного через функцию get_student_id.
# В качестве id курса выбираем случайный из списка, полученного через функцию get_course_id.
# В качестве оценки - случайное число от 1 до 100.
def fill_exams():
    student_id = random.choice(get_student_id())
    course_id = random.choice(get_course_id())
    score = random.randint(1, 100)
    cursor.execute("INSERT INTO exams (s_id, c_no, score) VALUES (%s, %s, %s)", (student_id, course_id, score))


# Основоной блок работы.
# Устанавливаем английскую локализацию для библиотеки faker
faker = faker.Faker('EN')

# Проверяем, что переданный из конфига параметр COUNT положительный.
if COUNT < 1:
    raise ValueError('[ERROR] Parameter "COUNT" must be a positive integer.')

try:
    # Устанавливаем соединение с базой данных
    connection = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_DATABASE)
    connection.autocommit = True

    with connection.cursor() as cursor:
        # Перебираем в цикле список таблиц, полученный из конфига
        for table in TABLES:
            # Проверяем, что в базе данных есть таблица, с которой работаем на этой итерации цикла.
            # Иначе выведем уведомление от том, что искомой таблицы нет в БД.
            if table not in get_tables_from_db():
                print(f'[ERROR] There is no table "{table}" in "{DB_DATABASE}" database.')

            # Заполняем таблицу 'students'
            if table == 'students':
                for i in range(COUNT):
                    fill_students()

            # Заполняем таблицу 'courses'
            if table == 'courses':
                for i in range(COUNT):
                    fill_courses()

            # Заполняем таблицу 'exams'
            if table == 'exams':
                for i in range(COUNT):
                    fill_exams()

# В случае возникновения ошибок - выведем их
except Exception as _ex:
    print('[ERROR] Error while working with PostgreSQL', _ex)

# Независимо от результатов выполнения предыдущего кода закроем соединение с базой данных
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')
