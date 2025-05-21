import os
from datetime import timedelta

class Config:
    # Основные настройки
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = False
    TESTING = False

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки загрузки файлов
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB макс размер файла
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Настройки сессии
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_TYPE = 'filesystem'

    # Настройки почты
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Настройки пагинации
    PRODUCTS_PER_PAGE = 12
    
    # Настройки корзины
    CART_EXPIRATION_DAYS = 30

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'

class ProductionConfig(Config):
    # Настройки базы данных для продакшена
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Настройки безопасности
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

# Словарь конфигураций
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Получение текущей конфигурации на основе переменной окружения."""
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env)

# Дополнительные настройки
class ShopConfig:
    # Настройки магазина
    SHOP_NAME = 'Мой магазин'
    SHOP_DESCRIPTION = 'Лучший интернет-магазин'
    SHOP_PHONE = '+7 (999) 123-45-67'
    SHOP_EMAIL = 'shop@example.com'
    SHOP_ADDRESS = 'г. Москва, ул. Примерная, д. 1'

    # Настройки заказов
    MIN_ORDER_AMOUNT = 500  # Минимальная сумма заказа
    DELIVERY_COST = 300     # Стоимость доставки
    FREE_DELIVERY_AMOUNT = 3000  # Сумма для бесплатной доставки

    # Настройки скидок
    DISCOUNT_LEVELS = {
        5000: 5,   # 5% скидка при заказе от 5000
        10000: 10, # 10% скидка при заказе от 10000
        20000: 15  # 15% скидка при заказе от 20000
    }

    # Способы оплаты
    PAYMENT_METHODS = [
        ('card', 'Банковская карта'),
        ('cash', 'Наличные при получении')
    ]

    # Способы доставки
    DELIVERY_METHODS = [
        ('courier', 'Курьерская доставка'),
        ('pickup', 'Самовывоз'),
        ('post', 'Почта России')
    ]

# Функции-помощники
def allowed_file(filename):
    """Проверка разрешенного расширения файла."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def get_upload_path(filename):
    """Получение пути для загрузки файла."""
    return os.path.join(Config.UPLOAD_FOLDER, filename)

def get_discount(amount):
    """Получение размера скидки на основе суммы заказа."""
    discount = 0
    for threshold, disc in sorted(ShopConfig.DISCOUNT_LEVELS.items()):
        if amount >= threshold:
            discount = disc
    return discount

def calculate_delivery_cost(order_amount):
    """Расчет стоимости доставки."""
    if order_amount >= ShopConfig.FREE_DELIVERY_AMOUNT:
        return 0
    return ShopConfig.DELIVERY_COST