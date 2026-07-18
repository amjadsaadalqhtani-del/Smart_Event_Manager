from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import engine, get_db

app = FastAPI(title="Smart Event Manager API")

# بناء الجداول تلقائياً
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Welcome to Smart Event Manager API (Abha Edition)!"}


# --- بوابات المستخدمين (Users Endpoints) ---

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 2. جلب كل المستخدمين (جديد!)
@app.get("/users/", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# 3. جلب مستخدم محدد بالـ ID (جديد! هذا الذي كنتِ تبحثين عنه)
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found! (المستخدم غير موجود)")
    return user
# --- بوابات الفعاليات (Events Endpoints) ---

# 1. إضافة فعالية جديدة
@app.post("/events/", response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    new_event = models.Event(
        title=event.title,
        description=event.description,
        location=event.location,
        capacity=event.capacity,
        date_time=event.date_time
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

# 2. جلب كل الفعاليات
@app.get("/events/", response_model=List[schemas.EventResponse])
def get_all_events(db: Session = Depends(get_db)):
    events = db.query(models.Event).all()
    return events

# 3. جلب فعالية واحدة بالـ ID
@app.get("/events/{event_id}", response_model=schemas.EventResponse)
def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found!")
    return event

# 4. تعديل بيانات فعالية (PUT)
@app.put("/events/{event_id}", response_model=schemas.EventResponse)
def update_event(event_id: int, updated_event: schemas.EventCreate, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found! (الفعالية غير موجودة لتعديلها)")
    
    # تحديث الحقول بالقيم الجديدة
    event.title = updated_event.title
    event.description = updated_event.description
    event.location = updated_event.location
    event.capacity = updated_event.capacity
    event.date_time = updated_event.date_time
    
    db.commit()
    db.refresh(event)
    return event

# 5. حذف فعالية بالكامل (DELETE)
@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found! (الفعالية غير موجودة لحذفها)")
    
    db.delete(event)
    db.commit()
    return {"message": f"Event with ID {event_id} has been successfully deleted. (تم حذف الفعالية بنجاح)"}
# --- بوابات الحجوزات (Bookings Endpoints) ---

# 1. إنشاء حجز جديد (POST Booking)
@app.post("/bookings/", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    # التأكد من وجود المستخدم أولاً
    user_exists = db.query(models.User).filter(models.User.id == booking.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found! (المستخدم غير موجود)")
        
    # التأكد من وجود الفعالية ثانياً
    event_exists = db.query(models.Event).filter(models.Event.id == booking.event_id).first()
    if not event_exists:
        raise HTTPException(status_code=404, detail="Event not found! (الفعالية غير موجودة)")

    # إذا كان كل شيء سليم، يتم تسجيل الحجز
    new_booking = models.Booking(
        user_id=booking.user_id,
        event_id=booking.event_id
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

# 2. جلب كل الحجوزات (GET All Bookings)
@app.get("/bookings/", response_model=List[schemas.BookingResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).all()
    return bookings