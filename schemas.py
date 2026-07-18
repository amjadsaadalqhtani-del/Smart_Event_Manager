from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime
# مخطط لبيانات المستخدم عند التسجيل
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# مخطط لشكل بيانات المستخدم المرجعة
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True  # تم تعديلها لتتوافق مع إصدار جهازكِ

# مخطط لبيانات الفعالية عند إنشائها
class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    capacity: int
    date_time: Optional[str] = None

# مخطط لشكل بيانات الفعالية المرجعة
class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    location: str
    capacity: int
    date_time: Optional[str]

    class Config:
        orm_mode = True

        # أضيفي هذا الكود في نهاية ملف schemas.py الحالي

class BookingCreate(BaseModel):
    user_id: int
    event_id: int

class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    booking_date: datetime.datetime

    class Config:
        orm_mode = True