import pandas as pd
from sqlalchemy.orm import Session
from database import (
    Animal, MilkRecord, BreedingRecord, HealthRecord, MedicineInventory,
    FodderCultivation, FeedInventory, FeedConsumption, Worker, Attendance,
    Equipment, EquipmentMaintenance, FinancialTransaction, SessionLocal
)
from datetime import date

def get_all_animals(db: Session) -> pd.DataFrame:
    animals = db.query(Animal).all()
    if not animals:
        return pd.DataFrame(columns=[
            'animal_id', 'name', 'ear_tag', 'dob', 'sex', 'breed', 'lifecycle_stage',
            'sire', 'dam', 'registration_date', 'status', 'notes'
        ])
    
    data = [{
        'animal_id': a.animal_id,
        'name': a.name,
        'ear_tag': a.ear_tag,
        'dob': a.dob,
        'sex': a.sex,
        'breed': a.breed,
        'lifecycle_stage': a.lifecycle_stage,
        'sire': a.sire,
        'dam': a.dam,
        'registration_date': a.registration_date,
        'status': a.status,
        'notes': a.notes
    } for a in animals]
    return pd.DataFrame(data)

def add_animal(db: Session, animal_data: dict):
    animal = Animal(**animal_data)
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal

def get_all_milk_records(db: Session) -> pd.DataFrame:
    records = db.query(MilkRecord).all()
    if not records:
        return pd.DataFrame(columns=[
            'date', 'animal_id', 'session', 'yield_litres', 'usage', 'price_per_litre', 'notes'
        ])
    
    data = [{
        'date': r.date,
        'animal_id': r.animal_id,
        'session': r.session,
        'yield_litres': r.yield_litres,
        'usage': r.usage,
        'price_per_litre': r.price_per_litre,
        'notes': r.notes
    } for r in records]
    return pd.DataFrame(data)

def add_milk_record(db: Session, record_data: dict):
    record = MilkRecord(**record_data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_breeding_records(db: Session) -> pd.DataFrame:
    records = db.query(BreedingRecord).all()
    if not records:
        return pd.DataFrame(columns=[
            'animal_id', 'heat_date', 'insemination_date', 'insemination_type',
            'bull_id', 'pregnancy_confirmed', 'expected_calving', 'actual_calving',
            'calf_id', 'calf_sex', 'notes'
        ])
    
    data = [{
        'animal_id': r.animal_id,
        'heat_date': r.heat_date,
        'insemination_date': r.insemination_date,
        'insemination_type': r.insemination_type,
        'bull_id': r.bull_id,
        'pregnancy_confirmed': r.pregnancy_confirmed,
        'expected_calving': r.expected_calving,
        'actual_calving': r.actual_calving,
        'calf_id': r.calf_id,
        'calf_sex': r.calf_sex,
        'notes': r.notes
    } for r in records]
    return pd.DataFrame(data)

def add_breeding_record(db: Session, record_data: dict):
    record = BreedingRecord(**record_data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def update_breeding_record(db: Session, record_id: int, update_data: dict):
    record = db.query(BreedingRecord).filter(BreedingRecord.id == record_id).first()
    if record:
        for key, value in update_data.items():
            setattr(record, key, value)
        db.commit()
        db.refresh(record)
    return record

def get_all_health_records(db: Session) -> pd.DataFrame:
    records = db.query(HealthRecord).all()
    if not records:
        return pd.DataFrame(columns=[
            'date', 'animal_id', 'record_type', 'description', 'medicine',
            'dosage', 'cost', 'veterinarian', 'next_due', 'notes'
        ])
    
    data = [{
        'date': r.date,
        'animal_id': r.animal_id,
        'record_type': r.record_type,
        'description': r.description,
        'medicine': r.medicine,
        'dosage': r.dosage,
        'cost': r.cost,
        'veterinarian': r.veterinarian,
        'next_due': r.next_due,
        'notes': r.notes
    } for r in records]
    return pd.DataFrame(data)

def add_health_record(db: Session, record_data: dict):
    record = HealthRecord(**record_data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_medicine_inventory(db: Session) -> pd.DataFrame:
    medicines = db.query(MedicineInventory).all()
    if not medicines:
        return pd.DataFrame(columns=[
            'medicine_name', 'category', 'quantity', 'unit', 'expiry_date',
            'cost_per_unit', 'supplier', 'reorder_level', 'notes'
        ])
    
    data = [{
        'medicine_name': m.medicine_name,
        'category': m.category,
        'quantity': m.quantity,
        'unit': m.unit,
        'expiry_date': m.expiry_date,
        'cost_per_unit': m.cost_per_unit,
        'supplier': m.supplier,
        'reorder_level': m.reorder_level,
        'notes': m.notes
    } for m in medicines]
    return pd.DataFrame(data)

def add_medicine(db: Session, medicine_data: dict):
    medicine = MedicineInventory(**medicine_data)
    db.add(medicine)
    db.commit()
    db.refresh(medicine)
    return medicine

def get_all_fodder_cultivation(db: Session) -> pd.DataFrame:
    records = db.query(FodderCultivation).all()
    if not records:
        return pd.DataFrame(columns=[
            'crop_type', 'plot_id', 'area_acres', 'sowing_date', 'harvest_date',
            'yield_kg', 'cost', 'status', 'notes'
        ])
    
    data = [{
        'crop_type': r.crop_type,
        'plot_id': r.plot_id,
        'area_acres': r.area_acres,
        'sowing_date': r.sowing_date,
        'harvest_date': r.harvest_date,
        'yield_kg': r.yield_kg,
        'cost': r.cost,
        'status': r.status,
        'notes': r.notes
    } for r in records]
    return pd.DataFrame(data)

def add_fodder_cultivation(db: Session, record_data: dict):
    record = FodderCultivation(**record_data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_feed_inventory(db: Session) -> pd.DataFrame:
    records = db.query(FeedInventory).all()
    if not records:
        return pd.DataFrame(columns=[
            'feed_name', 'category', 'quantity_kg', 'purchase_date',
            'cost_per_kg', 'supplier', 'notes'
        ])
    
    data = [{
        'feed_name': r.feed_name,
        'category': r.category,
        'quantity_kg': r.quantity_kg,
        'purchase_date': r.purchase_date,
        'cost_per_kg': r.cost_per_kg,
        'supplier': r.supplier,
        'notes': r.notes
    } for r in records]
    return pd.DataFrame(data)

def add_feed_inventory(db: Session, record_data: dict):
    record = FeedInventory(**record_data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_feed_consumption(db: Session) -> pd.DataFrame:
    records = db.query(FeedConsumption).all()
    if not records:
        return pd.DataFrame(columns=[
            'date', 'feed_name', 'quantity_kg', 'herd_size', 'notes'
        ])
    
    data = [{
        'date': r.date,
        'feed_name': r.feed_name,
        'quantity_kg': r.quantity_kg,
        'herd_size': r.herd_size,
        'notes': r.notes
    } for r in records]
    return pd.DataFrame(data)

def add_feed_consumption(db: Session, record_data: dict):
    record = FeedConsumption(**record_data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_workers(db: Session) -> pd.DataFrame:
    workers = db.query(Worker).all()
    if not workers:
        return pd.DataFrame(columns=[
            'worker_id', 'name', 'category', 'phone', 'daily_wage', 'status'
        ])
    
    data = [{
        'worker_id': w.worker_id,
        'name': w.name,
        'category': w.category,
        'phone': w.phone,
        'daily_wage': w.daily_wage,
        'status': w.status
    } for w in workers]
    return pd.DataFrame(data)

def add_worker(db: Session, worker_data: dict):
    worker = Worker(**worker_data)
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker

def get_all_attendance(db: Session) -> pd.DataFrame:
    records = db.query(Attendance).all()
    if not records:
        return pd.DataFrame(columns=[
            'date', 'worker_id', 'present', 'tasks', 'hours', 'notes'
        ])
    
    data = [{
        'date': r.date,
        'worker_id': r.worker_id,
        'present': r.present,
        'tasks': r.tasks,
        'hours': r.hours,
        'notes': r.notes
    } for r in records]
    return pd.DataFrame(data)

def add_attendance(db: Session, record_data: dict):
    record = Attendance(**record_data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_equipment(db: Session) -> pd.DataFrame:
    equipment = db.query(Equipment).all()
    if not equipment:
        return pd.DataFrame(columns=[
            'equipment_id', 'name', 'type', 'purchase_date', 'purchase_cost',
            'status', 'notes'
        ])
    
    data = [{
        'equipment_id': e.equipment_id,
        'name': e.name,
        'type': e.type,
        'purchase_date': e.purchase_date,
        'purchase_cost': e.purchase_cost,
        'status': e.status,
        'notes': e.notes
    } for e in equipment]
    return pd.DataFrame(data)

def add_equipment(db: Session, equipment_data: dict):
    equipment = Equipment(**equipment_data)
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment

def get_all_equipment_maintenance(db: Session) -> pd.DataFrame:
    records = db.query(EquipmentMaintenance).all()
    if not records:
        return pd.DataFrame(columns=[
            'date', 'equipment_id', 'maintenance_type', 'cost', 'fuel_litres',
            'hours_used', 'notes'
        ])
    
    data = [{
        'date': r.date,
        'equipment_id': r.equipment_id,
        'maintenance_type': r.maintenance_type,
        'cost': r.cost,
        'fuel_litres': r.fuel_litres,
        'hours_used': r.hours_used,
        'notes': r.notes
    } for r in records]
    return pd.DataFrame(data)

def add_equipment_maintenance(db: Session, record_data: dict):
    record = EquipmentMaintenance(**record_data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_financial_transactions(db: Session) -> pd.DataFrame:
    records = db.query(FinancialTransaction).all()
    if not records:
        return pd.DataFrame(columns=[
            'date', 'type', 'category', 'subcategory', 'amount',
            'description', 'reference_id', 'notes'
        ])
    
    data = [{
        'date': r.date,
        'type': r.type,
        'category': r.category,
        'subcategory': r.subcategory,
        'amount': r.amount,
        'description': r.description,
        'reference_id': r.reference_id,
        'notes': r.notes
    } for r in records]
    return pd.DataFrame(data)

def add_financial_transaction(db: Session, record_data: dict):
    record = FinancialTransaction(**record_data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_breeding_record_by_index(db: Session, index: int):
    records = db.query(BreedingRecord).all()
    if index < len(records):
        return records[index]
    return None

def get_breeding_records_pending_calving(db: Session) -> pd.DataFrame:
    records = db.query(BreedingRecord).filter(BreedingRecord.actual_calving == None).all()
    if not records:
        return pd.DataFrame()
    
    data = [{
        'id': r.id,
        'animal_id': r.animal_id,
        'heat_date': r.heat_date,
        'insemination_date': r.insemination_date,
        'insemination_type': r.insemination_type,
        'bull_id': r.bull_id,
        'pregnancy_confirmed': r.pregnancy_confirmed,
        'expected_calving': r.expected_calving,
        'actual_calving': r.actual_calving,
        'calf_id': r.calf_id,
        'calf_sex': r.calf_sex,
        'notes': r.notes
    } for r in records]
    return pd.DataFrame(data)
