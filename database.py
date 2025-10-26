import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Animal(Base):
    __tablename__ = 'animals'
    
    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String)
    ear_tag = Column(String)
    dob = Column(Date, nullable=False)
    sex = Column(String, nullable=False)
    breed = Column(String)
    lifecycle_stage = Column(String, nullable=False)
    sire = Column(String)
    dam = Column(String)
    registration_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    notes = Column(Text)
    photo_path = Column(String)
    
    milk_records = relationship("MilkRecord", back_populates="animal")
    breeding_records = relationship("BreedingRecord", back_populates="animal")
    health_records = relationship("HealthRecord", back_populates="animal")

class MilkRecord(Base):
    __tablename__ = 'milk_records'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    animal_id = Column(String, ForeignKey('animals.animal_id'), nullable=False, index=True)
    session = Column(String, nullable=False)
    yield_litres = Column(Float, nullable=False)
    usage = Column(String, nullable=False)
    price_per_litre = Column(Float)
    notes = Column(Text)
    
    animal = relationship("Animal", back_populates="milk_records")

class BreedingRecord(Base):
    __tablename__ = 'breeding_records'
    
    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(String, ForeignKey('animals.animal_id'), nullable=False, index=True)
    heat_date = Column(Date, nullable=False)
    insemination_date = Column(Date, nullable=False)
    insemination_type = Column(String, nullable=False)
    bull_id = Column(String, nullable=False)
    pregnancy_confirmed = Column(String)
    expected_calving = Column(Date)
    actual_calving = Column(Date)
    calf_id = Column(String)
    calf_sex = Column(String)
    notes = Column(Text)
    
    animal = relationship("Animal", back_populates="breeding_records")

class HealthRecord(Base):
    __tablename__ = 'health_records'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    animal_id = Column(String, ForeignKey('animals.animal_id'), nullable=False, index=True)
    record_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    medicine = Column(String)
    dosage = Column(String)
    cost = Column(Float, default=0.0)
    veterinarian = Column(String)
    next_due = Column(Date)
    notes = Column(Text)
    
    animal = relationship("Animal", back_populates="health_records")

class MedicineInventory(Base):
    __tablename__ = 'medicine_inventory'
    
    id = Column(Integer, primary_key=True, index=True)
    medicine_name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    expiry_date = Column(Date, nullable=False)
    cost_per_unit = Column(Float)
    supplier = Column(String)
    reorder_level = Column(Float, default=0.0)
    notes = Column(Text)

class FodderCultivation(Base):
    __tablename__ = 'fodder_cultivation'
    
    id = Column(Integer, primary_key=True, index=True)
    crop_type = Column(String, nullable=False)
    plot_id = Column(String, nullable=False)
    area_acres = Column(Float, nullable=False)
    sowing_date = Column(Date, nullable=False)
    harvest_date = Column(Date)
    yield_kg = Column(Float, default=0.0)
    cost = Column(Float, default=0.0)
    status = Column(String, nullable=False)
    notes = Column(Text)

class FeedInventory(Base):
    __tablename__ = 'feed_inventory'
    
    id = Column(Integer, primary_key=True, index=True)
    feed_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    purchase_date = Column(Date, nullable=False)
    cost_per_kg = Column(Float)
    supplier = Column(String)
    notes = Column(Text)

class FeedConsumption(Base):
    __tablename__ = 'feed_consumption'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    feed_name = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    herd_size = Column(Integer, nullable=False)
    notes = Column(Text)

class Worker(Base):
    __tablename__ = 'workers'
    
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    phone = Column(String)
    daily_wage = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    
    attendance_records = relationship("Attendance", back_populates="worker")

class Attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    worker_id = Column(String, ForeignKey('workers.worker_id'), nullable=False, index=True)
    present = Column(Boolean, nullable=False)
    tasks = Column(String)
    hours = Column(Float)
    notes = Column(Text)
    
    worker = relationship("Worker", back_populates="attendance_records")

class Equipment(Base):
    __tablename__ = 'equipment'
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    purchase_date = Column(Date)
    purchase_cost = Column(Float, default=0.0)
    status = Column(String, nullable=False)
    notes = Column(Text)
    
    maintenance_records = relationship("EquipmentMaintenance", back_populates="equipment")

class EquipmentMaintenance(Base):
    __tablename__ = 'equipment_maintenance'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    equipment_id = Column(String, ForeignKey('equipment.equipment_id'), nullable=False, index=True)
    maintenance_type = Column(String, nullable=False)
    cost = Column(Float, default=0.0)
    fuel_litres = Column(Float, default=0.0)
    hours_used = Column(Float, default=0.0)
    notes = Column(Text)
    
    equipment = relationship("Equipment", back_populates="maintenance_records")

class FinancialTransaction(Base):
    __tablename__ = 'financial_transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    reference_id = Column(String)
    notes = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
