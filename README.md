Это скрипт для наполнения базы данных "academy" произвольными данными.

Описание файлов:
1. config.py - конфигурационный файл
2. requirements.txt - файл с необходимыми для работы зависимостями
3. main.py - основной файл скрипта

Инструкция:
1. Установить зависимости командой `pip install -r requirements.txt`
2. Заполнить конфигурационный файл:
- `DB_HOST` - ip-адрес сервера
- `DB_USER` - имя пользователя
- `DB_PASSWORD` - пароль
- `DB_DATABASE` - имя базы данных
- `TABLES` - таблицы, которые необходимо заполнить
- `COUNT` - количество записей, которое будет внесено в каждую таблицу



3. Запустить основной скрипт `python3 main.py`


ВНИМАНИЕ! Рекомендуется сначала заполнить таблицы `students` и `courses`, а только потом - `exams`. 
В противном случае для таблицы `exams` не будет валидных значений 's_id' и 'c_no', что приведет к ошибкам.