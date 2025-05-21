from app import create_app
from app.models import db, User, Product, Category
from config import get_config

app = create_app()

# Создание контекста приложения
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Category': Category
    }

# Команда для создания администратора
@app.cli.command("create-admin")
def create_admin():
    """Создание администратора."""
    username = input("Введите имя пользователя: ")
    email = input("Введите email: ")
    password = input("Введите пароль: ")

    user = User(
        username=username,
        email=email,
        is_admin=True
    )
    user.set_password(password)

    db.session.add(user)
    try:
        db.session.commit()
        print(f"Администратор {username} успешно создан!")
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при создании администратора: {e}")

# Команда для инициализации базы данных тестовыми данными
@app.cli.command("init-db")
def init_db():
    """Инициализация базы данных тестовыми данными."""
    try:
        # Создание категорий
        categories = [
            Category(name="Электроника", slug="electronics"),
            Category(name="Одежда", slug="clothes"),
            Category(name="Книги", slug="books")
        ]
        db.session.add_all(categories)
        db.session.commit()

        # Создание товаров
        products = [
            Product(
                name="Смартфон",
                slug="smartphone",
                price=29999,
                description="Современный смартфон",
                category_id=1,
                stock=10
            ),
            Product(
                name="Футболка",
                slug="tshirt",
                price=999,
                description="Хлопковая футболка",
                category_id=2,
                stock=50
            ),
            Product(
                name="Книга Python",
                slug="python-book",
                price=1499,
                description="Книга по программированию",
                category_id=3,
                stock=20
            )
        ]
        db.session.add_all(products)
        db.session.commit()

        print("База данных успешно инициализирована!")
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при инициализации базы данных: {e}")

# Обработчик ошибки 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# Обработчик ошибки 500
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    # Проверка наличия папки для загрузки файлов
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Запуск приложения
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )