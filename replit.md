# Gir Cow Dairy Farm Management System

## Overview

This is a comprehensive dairy farm management system built with Streamlit for managing Gir cow operations. The application handles end-to-end farm operations including animal management, milk production tracking, breeding records, health monitoring, fodder cultivation, feed inventory, labor management, equipment tracking, and financial accounting. It uses SQLAlchemy ORM for database operations and provides interactive visualizations using Plotly.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with a single-page, multi-section interface
- **Layout**: Wide layout with expandable sidebar for navigation between different management modules
- **Visualization**: Plotly Express and Plotly Graph Objects for interactive charts and dashboards
- **State Management**: Dual approach using both session state (legacy) and database persistence
- **UI Design**: Custom CSS styling with modern dark theme, gradient backgrounds, and card-based layout

### Backend Architecture
- **Application Layer**: Python-based with Streamlit serving as both frontend and backend
- **ORM**: SQLAlchemy declarative models for database abstraction
- **Data Access Pattern**: Utility functions in `db_utils.py` that wrap database operations and return pandas DataFrames
- **Session Management**: SQLAlchemy SessionLocal factory for database connections
- **Data Processing**: Pandas DataFrames for data manipulation and display

### Database Design
- **Schema**: Relational database with 11 core tables interconnected through foreign keys
- **Core Entities**:
  - **Animal**: Central entity storing animal profiles with lifecycle tracking
  - **MilkRecord**: Daily milk production data linked to animals
  - **BreedingRecord**: Breeding history, insemination, and calving records
  - **HealthRecord**: Medical history, vaccinations, and treatments
  - **MedicineInventory**: Medicine stock management with expiry tracking
  - **FodderCultivation**: Crop cultivation records for self-grown fodder
  - **FeedInventory** & **FeedConsumption**: Purchased feed stock and usage tracking
  - **Worker** & **Attendance**: Labor management and daily attendance
  - **Equipment** & **EquipmentMaintenance**: Asset register and maintenance logs
  - **FinancialTransaction**: Income and expense tracking with categorization

- **Relationships**: One-to-many relationships between Animal and its related records (milk, breeding, health)
- **Indexing**: Primary keys on ID fields, indexes on foreign keys (animal_id) and date fields for query performance

### Design Patterns
- **Repository Pattern**: Database operations abstracted through utility functions that return DataFrames
- **Session Factory Pattern**: SessionLocal factory for database session creation
- **Declarative Models**: SQLAlchemy Base class inheritance for all data models
- **Module Separation**: Clear separation between UI (app.py), database schema (database.py), and data access (db_utils.py)

### Migration Approach
The codebase shows evidence of migration from session state to persistent database storage:
- **Legacy**: `app_backup.py` contains original session state implementation
- **Current**: Database-backed implementation with SQLAlchemy models
- **Transition**: Both approaches present in codebase, suggesting ongoing migration

## External Dependencies

### Core Framework
- **Streamlit**: Web application framework for the entire UI
- **Pandas**: Data manipulation and DataFrame operations
- **SQLAlchemy**: ORM for database operations and schema definition

### Visualization
- **Plotly Express**: High-level charting for standard visualizations
- **Plotly Graph Objects**: Low-level API for custom interactive charts

### Database
- **Database Connection**: PostgreSQL expected (via DATABASE_URL environment variable)
- **Connection String**: Environment variable `DATABASE_URL` for database configuration
- **Driver**: SQLAlchemy engine with standard database URL format

### Date/Time Operations
- **datetime**: Standard library for date and time manipulation
- **timedelta**: For date calculations and range queries

### Data Export
- **io**: Standard library for in-memory file operations (likely for data export features)

### Environment Configuration
- **os**: Environment variable access for database URL configuration