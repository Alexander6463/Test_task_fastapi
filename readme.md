Создать простой REST-сервис на FastAPI для управления списком пользователей. 
 
Список полей для модели пользователя: 
- Идентификатор 
- Имя 
- Фамилия 
- Отчество 
- Email 
- Пароль 
- Дата и время создания 
- Дата и время обновления 
 
Сервис должен реализовывать следующие операции: 
- Добавление пользователя 
- Обновление пользователя 
- Удаление пользователя 
- Получение списка пользователей 
- Получение информации о пользователе по идентификатору 
- Поиск пользователей по текстовым полям 
 
Проверки: 
- Имя и фамилия пользователя обязательны для заполнения 
- Email должен быть уникальным среди всех пользователей 
- Пароль должен содержать не менее 6 символов и содержать хотя бы одну цифру и 
одну букву. 
 
Требования 
1. Код в репозитории на GitHub 
2. Управление зависимостями проекта через pipenv 
3. Работа с БД через SQLAlchemy. Структура БД должна создаваться через миграции с 
помощью Alembic 
4. Получение настроек через переменные окружения. 
 
Наличие юнит-тестов на pytest или unittest будет плюсом. 


Running
1. Use 'make build' for running app
2. Use 'make test' for running tests
