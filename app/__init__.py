from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Инициализация основных компонентов
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Настройка login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
    login_manager.login_message_category = 'info'

    # Регистрация blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.catalog import bp as catalog_bp
    app.register_blueprint(catalog_bp, url_prefix='/catalog')

    from app.cart import bp as cart_bp
    app.register_blueprint(cart_bp, url_prefix='/cart')

    # Создание таблиц базы данных
    with app.app_context():
        db.create_all()

    return app

# Импорт моделей
from app.models import User, Product, Category, CartItem

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))