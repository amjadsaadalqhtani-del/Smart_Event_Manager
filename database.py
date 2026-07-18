from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# تحديد مسار قاعدة البيانات (سنستخدم SQLite محلياً وسينشأ ملف باسم project.db تلقائياً)
DATABASE_URL = "sqlite:///./project.db"

# إنشاء محرك قاعدة البيانات
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# إنشاء جلسة للتعامل مع قاعدة البيانات (إدخال، تعديل، جلب بيانات)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# دالة سنستخدمها مستقبلاً لفتح وإغلاق الاتصال بأمان مع كل طلب لـ API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()