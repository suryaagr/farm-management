import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

st.set_page_config(
    page_title="Gir Cow Dairy Farm Management",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try to import database modules and handle configuration errors
try:
    from database import SessionLocal
    import db_utils
    DATABASE_AVAILABLE = True
except ValueError as e:
    DATABASE_AVAILABLE = False
    DATABASE_ERROR = str(e)

# Check if database is configured
if not DATABASE_AVAILABLE:
    st.error("⚠️ **Database Not Configured**")
    st.markdown(f"""
    The application cannot connect to the database. Please configure your database connection:
    
    ### For Streamlit Cloud:
    1. Click the **⋮** menu (three dots) in the top right corner
    2. Select **Settings** → **Secrets**
    3. Add the following configuration:
    
    ```toml
    [connections.postgresql]
    url = "your-database-connection-string"
    ```
    
    ### For Local Development:
    Set the `DATABASE_URL` environment variable to your PostgreSQL connection string.
    
    ---
    
    **Error Details:**
    ```
    {DATABASE_ERROR}
    ```
    
    ### Need a Free PostgreSQL Database?
    - **Neon**: https://neon.tech/ (recommended, no credit card required)
    - **Supabase**: https://supabase.com/
    
    After configuring the database, the app will automatically restart.
    """)
    st.stop()

# Inject custom CSS only once to avoid duplication on reruns
if 'custom_css_loaded' not in st.session_state:
    st.session_state.custom_css_loaded = True
    st.markdown("""
<style>
    /* Simple navigation - clickable label style */
    /* Remove all styling from navigation container */
    [data-testid="stSidebar"] .stRadio > div > label > div {
        background-color: transparent !important;
        padding: 0.3rem 0 !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label > div:hover {
        background-color: transparent !important;
    }
    
    /* Style for selected navigation item using aria-checked attribute */
    [data-testid="stSidebar"] .stRadio label[aria-checked="true"],
    [data-testid="stSidebar"] .stRadio label[aria-checked="true"] *,
    [data-testid="stSidebar"] .stRadio div[role="radio"][aria-checked="true"],
    [data-testid="stSidebar"] .stRadio div[role="radio"][aria-checked="true"] * {
        color: #10b981 !important;
        font-weight: 600 !important;
    }
    
    /* Style for unselected navigation items */
    [data-testid="stSidebar"] .stRadio label[aria-checked="false"],
    [data-testid="stSidebar"] .stRadio label[aria-checked="false"] *,
    [data-testid="stSidebar"] .stRadio div[role="radio"][aria-checked="false"],
    [data-testid="stSidebar"] .stRadio div[role="radio"][aria-checked="false"] * {
        font-weight: 400 !important;
    }
</style>
""", unsafe_allow_html=True)


def load_data_from_db():
    db = SessionLocal()
    try:
        st.session_state.animals = db_utils.get_all_animals(db)
        st.session_state.milk_records = db_utils.get_all_milk_records(db)
        st.session_state.breeding_records = db_utils.get_all_breeding_records(db)
        st.session_state.health_records = db_utils.get_all_health_records(db)
        st.session_state.medicine_inventory = db_utils.get_all_medicine_inventory(db)
        st.session_state.fodder_cultivation = db_utils.get_all_fodder_cultivation(db)
        st.session_state.feed_inventory = db_utils.get_all_feed_inventory(db)
        st.session_state.feed_consumption = db_utils.get_all_feed_consumption(db)
        st.session_state.labour_records = db_utils.get_all_workers(db)
        st.session_state.attendance = db_utils.get_all_attendance(db)
        st.session_state.equipment = db_utils.get_all_equipment(db)
        st.session_state.equipment_maintenance = db_utils.get_all_equipment_maintenance(db)
        st.session_state.financial_transactions = db_utils.get_all_financial_transactions(db)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        db.rollback()
    finally:
        db.close()

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if not st.session_state.data_loaded:
    try:
        load_data_from_db()
        st.session_state.data_loaded = True
    except (ValueError, TypeError) as e:
        st.error("⚠️ **Database Connection Error**")
        st.markdown(f"""
        Cannot load data from the database. This usually means the database is not properly configured.
        
        **Error:** `{str(e)}`
        
        ### For Streamlit Cloud:
        Please configure your database connection in **Settings → Secrets**.
        
        ### For Local Development:
        Make sure the `DATABASE_URL` environment variable is set.
        """)
        st.stop()

st.sidebar.title("🐄 Gir Cow Farm")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🐄 Animal Management",
        "💕 Breeding & Genetics",
        "🥛 Milk Collection & Sales",
        "🌾 Fodder & Feed",
        "💊 Health & Medicine",
        "👷 Labour Management",
        "🚜 Equipment",
        "💰 Financial Accounting",
        "📊 Reports"
    ]
)

def animal_management():
    st.title("🐄 Animal Management")
    
    tab1, tab2, tab3 = st.tabs(["Register Animal", "View Animals", "Animal Details"])
    
    with tab1:
        st.subheader("Register New Animal")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            animal_id = st.text_input("Animal ID*", help="Unique identifier")
            name = st.text_input("Name")
            ear_tag = st.text_input("Ear Tag / RFID")
        
        with col2:
            dob = st.date_input("Date of Birth*", value=datetime.now().date())
            sex = st.selectbox("Sex*", ["Female", "Male"])
            breed = st.text_input("Breed", value="Gir")
        
        with col3:
            lifecycle_stage = st.selectbox(
                "Lifecycle Stage*",
                ["Calf (0-1 year)", "Heifer (1-3 years)", "Adult Cow (3+ years)", "Bull"]
            )
            status = st.selectbox("Status", ["Active", "Sold", "Deceased"])
        
        col4, col5 = st.columns(2)
        with col4:
            sire = st.text_input("Sire (Father) ID")
        with col5:
            dam = st.text_input("Dam (Mother) ID")
        
        notes = st.text_area("Notes / Physical Attributes")
        
        if st.button("Register Animal", type="primary"):
            if animal_id and dob and sex and lifecycle_stage:
                db = SessionLocal()
                try:
                    animal_data = {
                        'animal_id': animal_id,
                        'name': name,
                        'ear_tag': ear_tag,
                        'dob': dob,
                        'sex': sex,
                        'breed': breed,
                        'lifecycle_stage': lifecycle_stage,
                        'sire': sire,
                        'dam': dam,
                        'registration_date': datetime.now().date(),
                        'status': status,
                        'notes': notes
                    }
                    db_utils.add_animal(db, animal_data)
                    st.success(f"Animal {animal_id} registered successfully!")
                    load_data_from_db()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error registering animal: {str(e)}")
                    db.rollback()
                finally:
                    db.close()
            else:
                st.error("Please fill all required fields (*)")
    
    with tab2:
        st.subheader("All Animals")
        
        if not st.session_state.animals.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_stage = st.multiselect(
                    "Filter by Lifecycle Stage",
                    options=st.session_state.animals['lifecycle_stage'].unique(),
                    default=st.session_state.animals['lifecycle_stage'].unique()
                )
            with col2:
                filter_sex = st.multiselect(
                    "Filter by Sex",
                    options=st.session_state.animals['sex'].unique(),
                    default=st.session_state.animals['sex'].unique()
                )
            with col3:
                filter_status = st.multiselect(
                    "Filter by Status",
                    options=st.session_state.animals['status'].unique(),
                    default=st.session_state.animals['status'].unique()
                )
            
            filtered_animals = st.session_state.animals[
                (st.session_state.animals['lifecycle_stage'].isin(filter_stage)) &
                (st.session_state.animals['sex'].isin(filter_sex)) &
                (st.session_state.animals['status'].isin(filter_status))
            ]
            
            st.metric("Total Animals", len(filtered_animals))
            st.dataframe(filtered_animals, use_container_width=True)
            
            csv = filtered_animals.to_csv(index=False)
            st.download_button(
                "📥 Download as CSV",
                csv,
                "animals.csv",
                "text/csv"
            )
        else:
            st.info("No animals registered yet. Use the 'Register Animal' tab to add animals.")
    
    with tab3:
        st.subheader("Animal Details & History")
        
        if not st.session_state.animals.empty:
            animal_options = st.session_state.animals['animal_id'].tolist()
            selected_animal = st.selectbox("Select Animal", animal_options)
            
            if selected_animal:
                animal_data = st.session_state.animals[
                    st.session_state.animals['animal_id'] == selected_animal
                ].iloc[0]
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Animal ID", animal_data['animal_id'])
                    st.metric("Name", animal_data['name'] if animal_data['name'] else "N/A")
                with col2:
                    age_days = (datetime.now().date() - animal_data['dob']).days
                    age_years = age_days / 365.25
                    st.metric("Age", f"{age_years:.1f} years")
                    st.metric("Sex", animal_data['sex'])
                with col3:
                    st.metric("Lifecycle Stage", animal_data['lifecycle_stage'])
                    st.metric("Status", animal_data['status'])
                with col4:
                    st.metric("Breed", animal_data['breed'])
                    st.metric("Ear Tag", animal_data['ear_tag'] if animal_data['ear_tag'] else "N/A")
                
                st.markdown("---")
                
                tab_milk, tab_breeding, tab_health = st.tabs(["Milk Records", "Breeding History", "Health Records"])
                
                with tab_milk:
                    animal_milk = st.session_state.milk_records[
                        st.session_state.milk_records['animal_id'] == selected_animal
                    ]
                    if not animal_milk.empty:
                        st.dataframe(animal_milk, use_container_width=True)
                        total_milk = animal_milk['yield_litres'].sum()
                        st.metric("Total Milk Production", f"{total_milk:.2f} litres")
                    else:
                        st.info("No milk records found")
                
                with tab_breeding:
                    animal_breeding = st.session_state.breeding_records[
                        st.session_state.breeding_records['animal_id'] == selected_animal
                    ]
                    if not animal_breeding.empty:
                        st.dataframe(animal_breeding, use_container_width=True)
                    else:
                        st.info("No breeding records found")
                
                with tab_health:
                    animal_health = st.session_state.health_records[
                        st.session_state.health_records['animal_id'] == selected_animal
                    ]
                    if not animal_health.empty:
                        st.dataframe(animal_health, use_container_width=True)
                    else:
                        st.info("No health records found")
        else:
            st.info("No animals registered yet.")

def breeding_genetics():
    st.title("💕 Breeding & Genetics")
    
    tab1, tab2, tab3 = st.tabs(["Record Breeding", "View Records", "Lineage Tree"])
    
    with tab1:
        st.subheader("Record Breeding Event")
        
        if not st.session_state.animals.empty:
            female_animals = st.session_state.animals[
                (st.session_state.animals['sex'] == 'Female') &
                (st.session_state.animals['status'] == 'Active')
            ]['animal_id'].tolist()
            
            col1, col2 = st.columns(2)
            with col1:
                animal_id = st.selectbox("Select Cow*", female_animals)
                heat_date = st.date_input("Heat Detection Date*")
                insemination_date = st.date_input("Insemination Date*")
            
            with col2:
                insemination_type = st.selectbox(
                    "Insemination Type*",
                    ["Artificial Insemination (AI)", "Natural Service"]
                )
                bull_id = st.text_input("Bull/Sire ID*")
                pregnancy_confirmed = st.selectbox("Pregnancy Confirmed?", ["Pending", "Yes", "No"])
            
            expected_calving = None
            if pregnancy_confirmed == "Yes":
                expected_calving = st.date_input(
                    "Expected Calving Date",
                    value=insemination_date + timedelta(days=283)
                )
            
            notes = st.text_area("Notes")
            
            if st.button("Record Breeding Event", type="primary"):
                if animal_id and heat_date and insemination_date and bull_id:
                    db = SessionLocal()
                    try:
                        breeding_data = {
                            'animal_id': animal_id,
                            'heat_date': heat_date,
                            'insemination_date': insemination_date,
                            'insemination_type': insemination_type,
                            'bull_id': bull_id,
                            'pregnancy_confirmed': pregnancy_confirmed,
                            'expected_calving': expected_calving,
                            'actual_calving': None,
                            'calf_id': None,
                            'calf_sex': None,
                            'notes': notes
                        }
                        db_utils.add_breeding_record(db, breeding_data)
                        st.success("Breeding event recorded successfully!")
                        load_data_from_db()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error recording breeding: {str(e)}")
                        db.rollback()
                    finally:
                        db.close()
                else:
                    st.error("Please fill all required fields (*)")
        else:
            st.warning("Please register animals first in Animal Management.")
    
    with tab2:
        st.subheader("All Breeding Records")
        
        if not st.session_state.breeding_records.empty:
            st.dataframe(st.session_state.breeding_records, use_container_width=True)
            
            st.markdown("#### Update Calving Record")
            db = SessionLocal()
            try:
                records_pending = db_utils.get_breeding_records_pending_calving(db)
                
                if not records_pending.empty:
                    record_id = st.selectbox(
                        "Select Breeding Record to Update",
                        records_pending['id'].tolist(),
                        format_func=lambda x: f"{records_pending[records_pending['id']==x]['animal_id'].iloc[0]} - Expected: {records_pending[records_pending['id']==x]['expected_calving'].iloc[0]}"
                    )
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        actual_calving = st.date_input("Actual Calving Date")
                    with col2:
                        calf_id = st.text_input("Calf ID")
                    with col3:
                        calf_sex = st.selectbox("Calf Sex", ["Female", "Male"])
                    
                    if st.button("Update Calving Record"):
                        try:
                            update_data = {
                                'actual_calving': actual_calving,
                                'calf_id': calf_id,
                                'calf_sex': calf_sex
                            }
                            db_utils.update_breeding_record(db, record_id, update_data)
                            st.success("Calving record updated!")
                            load_data_from_db()
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error updating calving record: {str(e)}")
                            db.rollback()
            except Exception as e:
                st.error(f"Error loading breeding records: {str(e)}")
                db.rollback()
            finally:
                db.close()
        else:
            st.info("No breeding records yet.")
    
    with tab3:
        st.subheader("Lineage Information")
        
        if not st.session_state.animals.empty:
            animal_id = st.selectbox("Select Animal", st.session_state.animals['animal_id'].tolist())
            
            if animal_id:
                animal = st.session_state.animals[st.session_state.animals['animal_id'] == animal_id].iloc[0]
                
                st.markdown(f"### {animal_id} Lineage")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Sire (Father):**")
                    if animal['sire']:
                        st.info(animal['sire'])
                    else:
                        st.warning("Not recorded")
                
                with col2:
                    st.markdown("**Dam (Mother):**")
                    if animal['dam']:
                        st.info(animal['dam'])
                    else:
                        st.warning("Not recorded")
                
                offspring = st.session_state.animals[
                    (st.session_state.animals['dam'] == animal_id) |
                    (st.session_state.animals['sire'] == animal_id)
                ]
                
                if not offspring.empty:
                    st.markdown("**Offspring:**")
                    st.dataframe(offspring[['animal_id', 'name', 'sex', 'dob', 'lifecycle_stage']], use_container_width=True)
        else:
            st.info("No animals registered yet.")

def milk_collection_sales():
    st.title("🥛 Milk Collection & Sales")
    
    tab1, tab2, tab3 = st.tabs(["Record Collection", "View Records", "Sales Analytics"])
    
    with tab1:
        st.subheader("Record Milk Collection")
        
        if not st.session_state.animals.empty:
            lactating_cows = st.session_state.animals[
                (st.session_state.animals['sex'] == 'Female') &
                (st.session_state.animals['lifecycle_stage'] == 'Adult Cow (3+ years)') &
                (st.session_state.animals['status'] == 'Active')
            ]['animal_id'].tolist()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                collection_date = st.date_input("Date*", value=datetime.now().date())
                animal_id = st.selectbox("Cow ID*", lactating_cows)
            
            with col2:
                session = st.selectbox("Session*", ["Morning (AM)", "Evening (PM)"])
                yield_litres = st.number_input("Milk Yield (litres)*", min_value=0.0, step=0.1)
            
            with col3:
                usage = st.selectbox(
                    "Usage*",
                    ["Sold", "Consumed (Home)", "Calf Feeding", "Wastage"]
                )
                price_per_litre = st.number_input("Price per Litre (₹)", min_value=0.0, step=1.0, value=50.0)
            
            notes = st.text_area("Notes")
            
            if st.button("Record Milk Collection", type="primary"):
                if animal_id and yield_litres > 0:
                    db = SessionLocal()
                    try:
                        milk_data = {
                            'date': collection_date,
                            'animal_id': animal_id,
                            'session': session,
                            'yield_litres': yield_litres,
                            'usage': usage,
                            'price_per_litre': price_per_litre,
                            'notes': notes
                        }
                        db_utils.add_milk_record(db, milk_data)
                        
                        if usage == "Sold":
                            revenue = yield_litres * price_per_litre
                            transaction_data = {
                                'date': collection_date,
                                'type': 'Income',
                                'category': 'Milk Sales',
                                'subcategory': animal_id,
                                'amount': revenue,
                                'description': f"Milk sale - {yield_litres}L @ ₹{price_per_litre}/L",
                                'reference_id': animal_id,
                                'notes': notes
                            }
                            db_utils.add_financial_transaction(db, transaction_data)
                        
                        st.success("Milk collection recorded successfully!")
                        load_data_from_db()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error recording milk collection: {str(e)}")
                        db.rollback()
                    finally:
                        db.close()
                else:
                    st.error("Please fill all required fields (*)")
        else:
            st.warning("Please register animals first in Animal Management.")
    
    with tab2:
        st.subheader("Milk Collection Records")
        
        if not st.session_state.milk_records.empty:
            col1, col2 = st.columns(2)
            with col1:
                date_from = st.date_input("From Date", value=datetime.now().date() - timedelta(days=30))
            with col2:
                date_to = st.date_input("To Date", value=datetime.now().date())
            
            filtered_records = st.session_state.milk_records[
                (pd.to_datetime(st.session_state.milk_records['date']) >= pd.to_datetime(date_from)) &
                (pd.to_datetime(st.session_state.milk_records['date']) <= pd.to_datetime(date_to))
            ]
            
            if not filtered_records.empty:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Milk", f"{filtered_records['yield_litres'].sum():.2f} L")
                with col2:
                    sold_milk = filtered_records[filtered_records['usage'] == 'Sold']['yield_litres'].sum()
                    st.metric("Sold", f"{sold_milk:.2f} L")
                with col3:
                    revenue = (filtered_records[filtered_records['usage'] == 'Sold']['yield_litres'] * 
                              filtered_records[filtered_records['usage'] == 'Sold']['price_per_litre']).sum()
                    st.metric("Revenue", f"₹{revenue:.2f}")
                with col4:
                    avg_price = filtered_records[filtered_records['usage'] == 'Sold']['price_per_litre'].mean()
                    st.metric("Avg Price/L", f"₹{avg_price:.2f}" if not pd.isna(avg_price) else "N/A")
                
                st.dataframe(filtered_records, use_container_width=True)
                
                csv = filtered_records.to_csv(index=False)
                st.download_button(
                    "📥 Download as CSV",
                    csv,
                    "milk_records.csv",
                    "text/csv"
                )
        else:
            st.info("No milk records yet.")
    
    with tab3:
        st.subheader("Sales Analytics")
        
        if not st.session_state.milk_records.empty:
            milk_df = st.session_state.milk_records.copy()
            milk_df['date'] = pd.to_datetime(milk_df['date'])
            
            daily_production = milk_df.groupby('date')['yield_litres'].sum().reset_index()
            fig = px.line(
                daily_production,
                x='date',
                y='yield_litres',
                title='Daily Milk Production Trend',
                labels={'yield_litres': 'Milk (Litres)', 'date': 'Date'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                usage_distribution = milk_df.groupby('usage')['yield_litres'].sum().reset_index()
                fig = px.pie(
                    usage_distribution,
                    values='yield_litres',
                    names='usage',
                    title='Milk Usage Distribution'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                top_producers = milk_df.groupby('animal_id')['yield_litres'].sum().nlargest(10).reset_index()
                fig = px.bar(
                    top_producers,
                    x='animal_id',
                    y='yield_litres',
                    title='Top 10 Milk Producers',
                    labels={'yield_litres': 'Total Milk (Litres)', 'animal_id': 'Cow ID'}
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No milk records available for analytics.")

def fodder_feed():
    st.title("🌾 Fodder & Feed Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Cultivation", "Feed Inventory", "Consumption", "Analytics"])
    
    with tab1:
        st.subheader("Fodder Cultivation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Add Cultivation Record")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                crop_type = st.text_input("Crop Type*", placeholder="e.g., Maize, Sorghum, Lucerne")
                plot_id = st.text_input("Plot ID*", placeholder="e.g., Plot-A1")
            with col_b:
                area_acres = st.number_input("Area (Acres)*", min_value=0.0, step=0.1)
                sowing_date = st.date_input("Sowing Date*")
            with col_c:
                harvest_date = st.date_input("Expected Harvest Date")
                cost = st.number_input("Cultivation Cost (₹)", min_value=0.0, step=100.0)
            
            status = st.selectbox("Status", ["Sowing", "Growing", "Ready for Harvest", "Harvested"])
            notes = st.text_area("Notes", key="cultivation_notes")
            
            if st.button("Add Cultivation Record", type="primary"):
                if crop_type and plot_id and area_acres > 0:
                    db = SessionLocal()
                    try:
                        cultivation_data = {
                            'crop_type': crop_type,
                            'plot_id': plot_id,
                            'area_acres': area_acres,
                            'sowing_date': sowing_date,
                            'harvest_date': harvest_date,
                            'yield_kg': 0,
                            'cost': cost,
                            'status': status,
                            'notes': notes
                        }
                        db_utils.add_fodder_cultivation(db, cultivation_data)
                        
                        if cost > 0:
                            transaction_data = {
                                'date': sowing_date,
                                'type': 'Expense',
                                'category': 'Fodder Cultivation',
                                'subcategory': crop_type,
                                'amount': cost,
                                'description': f"{crop_type} cultivation - {plot_id}",
                                'reference_id': plot_id,
                                'notes': notes
                            }
                            db_utils.add_financial_transaction(db, transaction_data)
                        
                        st.success("Cultivation record added!")
                        load_data_from_db()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding cultivation record: {str(e)}")
                        db.rollback()
                    finally:
                        db.close()
                else:
                    st.error("Please fill all required fields (*)")
        
        with col2:
            st.markdown("##### Summary")
            if not st.session_state.fodder_cultivation.empty:
                total_area = st.session_state.fodder_cultivation['area_acres'].sum()
                active_crops = len(st.session_state.fodder_cultivation[
                    st.session_state.fodder_cultivation['status'].isin(['Sowing', 'Growing', 'Ready for Harvest'])
                ])
                st.metric("Total Area", f"{total_area:.2f} acres")
                st.metric("Active Crops", active_crops)
            else:
                st.info("No cultivation records yet")
        
        st.markdown("---")
        
        if not st.session_state.fodder_cultivation.empty:
            st.markdown("##### All Cultivation Records")
            st.dataframe(st.session_state.fodder_cultivation, use_container_width=True)
    
    with tab2:
        st.subheader("Feed Inventory")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Add Feed Purchase")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                feed_name = st.text_input("Feed Name*", placeholder="e.g., Cotton Seed Cake")
                category = st.selectbox("Category*", ["Grains", "Minerals", "Supplements", "Green Fodder", "Dry Fodder"])
            with col_b:
                quantity_kg = st.number_input("Quantity (kg)*", min_value=0.0, step=1.0)
                cost_per_kg = st.number_input("Cost per kg (₹)*", min_value=0.0, step=1.0)
            with col_c:
                purchase_date = st.date_input("Purchase Date*", value=datetime.now().date())
                supplier = st.text_input("Supplier")
            
            feed_notes = st.text_area("Notes", key="feed_notes")
            
            if st.button("Add Feed Purchase", type="primary"):
                if feed_name and quantity_kg > 0 and cost_per_kg >= 0:
                    db = SessionLocal()
                    try:
                        total_cost = quantity_kg * cost_per_kg
                        
                        feed_data = {
                            'feed_name': feed_name,
                            'category': category,
                            'quantity_kg': quantity_kg,
                            'purchase_date': purchase_date,
                            'cost_per_kg': cost_per_kg,
                            'supplier': supplier,
                            'notes': feed_notes
                        }
                        db_utils.add_feed_inventory(db, feed_data)
                        
                        transaction_data = {
                            'date': purchase_date,
                            'type': 'Expense',
                            'category': 'Feed Purchase',
                            'subcategory': category,
                            'amount': total_cost,
                            'description': f"{feed_name} - {quantity_kg}kg @ ₹{cost_per_kg}/kg",
                            'reference_id': feed_name,
                            'notes': feed_notes
                        }
                        db_utils.add_financial_transaction(db, transaction_data)
                        
                        st.success(f"Feed purchase recorded! Total: ₹{total_cost:.2f}")
                        load_data_from_db()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding feed purchase: {str(e)}")
                        db.rollback()
                    finally:
                        db.close()
                else:
                    st.error("Please fill all required fields (*)")
        
        with col2:
            st.markdown("##### Inventory Summary")
            if not st.session_state.feed_inventory.empty:
                total_stock = st.session_state.feed_inventory['quantity_kg'].sum()
                total_value = (st.session_state.feed_inventory['quantity_kg'] * 
                              st.session_state.feed_inventory['cost_per_kg']).sum()
                st.metric("Total Stock", f"{total_stock:.2f} kg")
                st.metric("Total Value", f"₹{total_value:.2f}")
            else:
                st.info("No feed inventory yet")
        
        st.markdown("---")
        
        if not st.session_state.feed_inventory.empty:
            st.markdown("##### Feed Inventory")
            st.dataframe(st.session_state.feed_inventory, use_container_width=True)
    
    with tab3:
        st.subheader("Feed Consumption Tracking")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Record Daily Consumption")
            
            if not st.session_state.feed_inventory.empty:
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    consumption_date = st.date_input("Date*", value=datetime.now().date(), key="consumption_date")
                    feed_options = st.session_state.feed_inventory['feed_name'].unique().tolist()
                    selected_feed = st.selectbox("Feed Type*", feed_options)
                with col_b:
                    consumed_qty = st.number_input("Quantity Consumed (kg)*", min_value=0.0, step=1.0)
                    herd_size = st.number_input("Herd Size*", min_value=1, step=1, value=50)
                with col_c:
                    consumption_notes = st.text_area("Notes", key="consumption_notes")
                
                if st.button("Record Consumption", type="primary"):
                    if selected_feed and consumed_qty > 0:
                        new_consumption = pd.DataFrame([{
                            'date': consumption_date,
                            'feed_name': selected_feed,
                            'quantity_kg': consumed_qty,
                            'herd_size': herd_size,
                            'notes': consumption_notes
                        }])
                        st.session_state.feed_consumption = pd.concat([st.session_state.feed_consumption, new_consumption], ignore_index=True)
                        st.success("Consumption recorded!")
                        st.rerun()
                    else:
                        st.error("Please fill all required fields (*)")
            else:
                st.warning("Please add feed inventory first.")
        
        with col2:
            st.markdown("##### Today's Summary")
            if not st.session_state.feed_consumption.empty:
                today_consumption = st.session_state.feed_consumption[
                    pd.to_datetime(st.session_state.feed_consumption['date']) == pd.to_datetime(datetime.now().date())
                ]
                if not today_consumption.empty:
                    total_today = today_consumption['quantity_kg'].sum()
                    st.metric("Today's Consumption", f"{total_today:.2f} kg")
                else:
                    st.info("No consumption recorded today")
            else:
                st.info("No consumption records yet")
        
        st.markdown("---")
        
        if not st.session_state.feed_consumption.empty:
            st.markdown("##### Recent Consumption Records")
            recent_consumption = st.session_state.feed_consumption.tail(20)
            st.dataframe(recent_consumption, use_container_width=True)
    
    with tab4:
        st.subheader("Feed Analytics")
        
        if not st.session_state.feed_consumption.empty:
            consumption_df = st.session_state.feed_consumption.copy()
            consumption_df['date'] = pd.to_datetime(consumption_df['date'])
            
            daily_consumption = consumption_df.groupby('date')['quantity_kg'].sum().reset_index()
            fig = px.line(
                daily_consumption,
                x='date',
                y='quantity_kg',
                title='Daily Feed Consumption Trend',
                labels={'quantity_kg': 'Feed (kg)', 'date': 'Date'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            feed_type_consumption = consumption_df.groupby('feed_name')['quantity_kg'].sum().reset_index()
            fig = px.bar(
                feed_type_consumption,
                x='feed_name',
                y='quantity_kg',
                title='Consumption by Feed Type',
                labels={'quantity_kg': 'Total Consumed (kg)', 'feed_name': 'Feed Type'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            if not st.session_state.milk_records.empty:
                st.markdown("#### Feed Efficiency Analysis")
                
                milk_df = st.session_state.milk_records.copy()
                milk_df['date'] = pd.to_datetime(milk_df['date'])
                
                daily_milk = milk_df.groupby('date')['yield_litres'].sum().reset_index()
                
                merged = pd.merge(daily_consumption, daily_milk, on='date', how='inner')
                
                if not merged.empty:
                    merged['feed_per_litre'] = merged['quantity_kg'] / merged['yield_litres']
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        avg_efficiency = merged['feed_per_litre'].mean()
                        st.metric("Avg Feed per Litre", f"{avg_efficiency:.2f} kg/L")
                    with col2:
                        if not st.session_state.feed_inventory.empty:
                            avg_feed_cost = st.session_state.feed_inventory['cost_per_kg'].mean()
                            cost_per_litre = avg_efficiency * avg_feed_cost
                            st.metric("Avg Feed Cost per Litre", f"₹{cost_per_litre:.2f}/L")
        else:
            st.info("No consumption data available for analytics.")

def health_medicine():
    st.title("💊 Health & Medicine Management")
    
    tab1, tab2, tab3 = st.tabs(["Health Records", "Medicine Inventory", "Analytics"])
    
    with tab1:
        st.subheader("Health Records")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Add Health Record")
            
            if not st.session_state.animals.empty:
                col_a, col_b = st.columns(2)
                with col_a:
                    record_date = st.date_input("Date*", value=datetime.now().date())
                    animal_id = st.selectbox("Animal ID*", st.session_state.animals['animal_id'].tolist())
                    record_type = st.selectbox(
                        "Record Type*",
                        ["Vaccination", "Disease/Illness", "Treatment", "Veterinary Visit", "General Checkup"]
                    )
                
                with col_b:
                    description = st.text_area("Description*", placeholder="Symptoms, diagnosis, etc.")
                    medicine_options = ["None"]
                    if not st.session_state.medicine_inventory.empty:
                        medicine_options.extend(st.session_state.medicine_inventory['medicine_name'].unique().tolist())
                    medicine = st.selectbox("Medicine Used", medicine_options)
                    dosage = st.text_input("Dosage", placeholder="e.g., 10ml, 2 tablets")
                
                col_c, col_d = st.columns(2)
                with col_c:
                    cost = st.number_input("Cost (₹)", min_value=0.0, step=10.0)
                    veterinarian = st.text_input("Veterinarian Name")
                with col_d:
                    next_due = st.date_input("Next Due Date (if applicable)", value=None)
                    health_notes = st.text_area("Notes", key="health_notes")
                
                if st.button("Add Health Record", type="primary"):
                    if animal_id and description:
                        db = SessionLocal()
                        try:
                            health_data = {
                                'date': record_date,
                                'animal_id': animal_id,
                                'record_type': record_type,
                                'description': description,
                                'medicine': medicine if medicine != "None" else None,
                                'dosage': dosage,
                                'cost': cost,
                                'veterinarian': veterinarian,
                                'next_due': next_due,
                                'notes': health_notes
                            }
                            db_utils.add_health_record(db, health_data)
                            
                            if cost > 0:
                                transaction_data = {
                                    'date': record_date,
                                    'type': 'Expense',
                                    'category': 'Health & Medicine',
                                    'subcategory': record_type,
                                    'amount': cost,
                                    'description': f"{record_type} - {animal_id}",
                                    'reference_id': animal_id,
                                    'notes': health_notes
                                }
                                db_utils.add_financial_transaction(db, transaction_data)
                            
                            st.success("Health record added!")
                            load_data_from_db()
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error adding health record: {str(e)}")
                            db.rollback()
                        finally:
                            db.close()
                    else:
                        st.error("Please fill all required fields (*)")
            else:
                st.warning("Please register animals first.")
        
        with col2:
            st.markdown("##### Upcoming Due")
            if not st.session_state.health_records.empty:
                upcoming = st.session_state.health_records[
                    pd.to_datetime(st.session_state.health_records['next_due']) >= pd.to_datetime(datetime.now().date())
                ].sort_values('next_due')
                
                if not upcoming.empty:
                    for _, record in upcoming.head(5).iterrows():
                        st.info(f"**{record['animal_id']}** - {record['record_type']}\nDue: {record['next_due']}")
                else:
                    st.success("No upcoming procedures")
            else:
                st.info("No health records yet")
        
        st.markdown("---")
        
        if not st.session_state.health_records.empty:
            st.markdown("##### All Health Records")
            st.dataframe(st.session_state.health_records, use_container_width=True)
    
    with tab2:
        st.subheader("Medicine Inventory")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Add Medicine")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                medicine_name = st.text_input("Medicine Name*")
                category = st.selectbox("Category*", ["Antibiotic", "Vaccine", "Vitamin", "Antiparasitic", "Other"])
            with col_b:
                quantity = st.number_input("Quantity*", min_value=0.0, step=1.0)
                unit = st.selectbox("Unit*", ["ml", "tablets", "kg", "doses", "bottles"])
            with col_c:
                expiry_date = st.date_input("Expiry Date*")
                cost_per_unit = st.number_input("Cost per Unit (₹)", min_value=0.0, step=1.0)
            
            col_d, col_e = st.columns(2)
            with col_d:
                supplier = st.text_input("Supplier")
            with col_e:
                reorder_level = st.number_input("Reorder Level", min_value=0.0, step=1.0)
            
            medicine_notes = st.text_area("Notes", key="medicine_notes")
            
            if st.button("Add Medicine", type="primary"):
                if medicine_name and quantity > 0:
                    new_medicine = pd.DataFrame([{
                        'medicine_name': medicine_name,
                        'category': category,
                        'quantity': quantity,
                        'unit': unit,
                        'expiry_date': expiry_date,
                        'cost_per_unit': cost_per_unit,
                        'supplier': supplier,
                        'reorder_level': reorder_level,
                        'notes': medicine_notes
                    }])
                    st.session_state.medicine_inventory = pd.concat([st.session_state.medicine_inventory, new_medicine], ignore_index=True)
                    
                    total_cost = quantity * cost_per_unit
                    if total_cost > 0:
                        new_transaction = pd.DataFrame([{
                            'date': datetime.now().date(),
                            'type': 'Expense',
                            'category': 'Medicine Purchase',
                            'subcategory': category,
                            'amount': total_cost,
                            'description': f"{medicine_name} - {quantity} {unit}",
                            'reference_id': medicine_name,
                            'notes': medicine_notes
                        }])
                        st.session_state.financial_transactions = pd.concat([st.session_state.financial_transactions, new_transaction], ignore_index=True)
                    
                    st.success("Medicine added to inventory!")
                    st.rerun()
                else:
                    st.error("Please fill all required fields (*)")
        
        with col2:
            st.markdown("##### Alerts")
            if not st.session_state.medicine_inventory.empty:
                expiring_soon = st.session_state.medicine_inventory[
                    pd.to_datetime(st.session_state.medicine_inventory['expiry_date']) <= 
                    pd.to_datetime(datetime.now().date() + timedelta(days=30))
                ]
                
                if not expiring_soon.empty:
                    st.warning(f"⚠️ {len(expiring_soon)} medicine(s) expiring soon")
                    for _, med in expiring_soon.iterrows():
                        st.error(f"{med['medicine_name']} - Exp: {med['expiry_date']}")
                
                low_stock = st.session_state.medicine_inventory[
                    st.session_state.medicine_inventory['quantity'] <= 
                    st.session_state.medicine_inventory['reorder_level']
                ]
                
                if not low_stock.empty:
                    st.warning(f"📦 {len(low_stock)} medicine(s) need reorder")
                    for _, med in low_stock.iterrows():
                        st.info(f"{med['medicine_name']} - Stock: {med['quantity']} {med['unit']}")
            else:
                st.info("No medicines in inventory")
        
        st.markdown("---")
        
        if not st.session_state.medicine_inventory.empty:
            st.markdown("##### Medicine Inventory")
            st.dataframe(st.session_state.medicine_inventory, use_container_width=True)
    
    with tab3:
        st.subheader("Health Analytics")
        
        if not st.session_state.health_records.empty:
            health_df = st.session_state.health_records.copy()
            health_df['date'] = pd.to_datetime(health_df['date'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                record_type_dist = health_df['record_type'].value_counts().reset_index()
                record_type_dist.columns = ['record_type', 'count']
                fig = px.pie(
                    record_type_dist,
                    values='count',
                    names='record_type',
                    title='Health Records by Type'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                monthly_cost = health_df.groupby(health_df['date'].dt.to_period('M'))['cost'].sum().reset_index()
                monthly_cost['date'] = monthly_cost['date'].astype(str)
                fig = px.bar(
                    monthly_cost,
                    x='date',
                    y='cost',
                    title='Monthly Health Costs',
                    labels={'cost': 'Cost (₹)', 'date': 'Month'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### Health Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_records = len(health_df)
                st.metric("Total Records", total_records)
            with col2:
                total_cost = health_df['cost'].sum()
                st.metric("Total Health Cost", f"₹{total_cost:.2f}")
            with col3:
                avg_cost = health_df['cost'].mean()
                st.metric("Avg Cost/Record", f"₹{avg_cost:.2f}")
            with col4:
                vaccinations = len(health_df[health_df['record_type'] == 'Vaccination'])
                st.metric("Vaccinations", vaccinations)
        else:
            st.info("No health records available for analytics.")

def labour_management():
    st.title("👷 Labour Management")
    
    tab1, tab2, tab3 = st.tabs(["Worker Registry", "Attendance", "Analytics"])
    
    with tab1:
        st.subheader("Worker Registry")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Add Worker")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                worker_id = st.text_input("Worker ID*", placeholder="e.g., W001")
                name = st.text_input("Name*")
            with col_b:
                category = st.selectbox("Category*", ["Animal Care & Milking", "Farming Operations", "Both"])
                phone = st.text_input("Phone")
            with col_c:
                daily_wage = st.number_input("Daily Wage (₹)*", min_value=0.0, step=50.0)
                status = st.selectbox("Status", ["Active", "Inactive"])
            
            if st.button("Add Worker", type="primary"):
                if worker_id and name and daily_wage > 0:
                    new_worker = pd.DataFrame([{
                        'worker_id': worker_id,
                        'name': name,
                        'category': category,
                        'phone': phone,
                        'daily_wage': daily_wage,
                        'status': status
                    }])
                    st.session_state.labour_records = pd.concat([st.session_state.labour_records, new_worker], ignore_index=True)
                    st.success(f"Worker {worker_id} added!")
                    st.rerun()
                else:
                    st.error("Please fill all required fields (*)")
        
        with col2:
            st.markdown("##### Summary")
            if not st.session_state.labour_records.empty:
                active_workers = len(st.session_state.labour_records[st.session_state.labour_records['status'] == 'Active'])
                total_daily_wage = st.session_state.labour_records[
                    st.session_state.labour_records['status'] == 'Active'
                ]['daily_wage'].sum()
                st.metric("Active Workers", active_workers)
                st.metric("Total Daily Wage", f"₹{total_daily_wage:.2f}")
            else:
                st.info("No workers registered")
        
        st.markdown("---")
        
        if not st.session_state.labour_records.empty:
            st.markdown("##### All Workers")
            st.dataframe(st.session_state.labour_records, use_container_width=True)
    
    with tab2:
        st.subheader("Attendance Tracking")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Mark Attendance")
            
            if not st.session_state.labour_records.empty:
                attendance_date = st.date_input("Date*", value=datetime.now().date())
                
                active_workers = st.session_state.labour_records[
                    st.session_state.labour_records['status'] == 'Active'
                ]
                
                for _, worker in active_workers.iterrows():
                    st.markdown(f"**{worker['name']}** ({worker['worker_id']}) - {worker['category']}")
                    
                    col_a, col_b, col_c = st.columns([1, 2, 2])
                    with col_a:
                        present = st.checkbox(
                            "Present",
                            key=f"present_{worker['worker_id']}",
                            value=True
                        )
                    with col_b:
                        tasks = st.text_input(
                            "Tasks",
                            key=f"tasks_{worker['worker_id']}",
                            placeholder="e.g., Milking, Feeding"
                        )
                    with col_c:
                        hours = st.number_input(
                            "Hours",
                            key=f"hours_{worker['worker_id']}",
                            min_value=0.0,
                            max_value=24.0,
                            step=0.5,
                            value=8.0
                        )
                    
                    st.markdown("---")
                
                if st.button("Save Attendance", type="primary"):
                    attendance_records = []
                    transaction_records = []
                    
                    for _, worker in active_workers.iterrows():
                        present = st.session_state.get(f"present_{worker['worker_id']}", False)
                        tasks = st.session_state.get(f"tasks_{worker['worker_id']}", "")
                        hours = st.session_state.get(f"hours_{worker['worker_id']}", 8.0)
                        
                        attendance_records.append({
                            'date': attendance_date,
                            'worker_id': worker['worker_id'],
                            'present': present,
                            'tasks': tasks,
                            'hours': hours,
                            'notes': ""
                        })
                        
                        if present:
                            wage = worker['daily_wage']
                            transaction_records.append({
                                'date': attendance_date,
                                'type': 'Expense',
                                'category': 'Labour',
                                'subcategory': worker['category'],
                                'amount': wage,
                                'description': f"Daily wage - {worker['name']} ({worker['worker_id']})",
                                'reference_id': worker['worker_id'],
                                'notes': tasks
                            })
                    
                    if attendance_records:
                        new_attendance = pd.DataFrame(attendance_records)
                        st.session_state.attendance = pd.concat([st.session_state.attendance, new_attendance], ignore_index=True)
                    
                    if transaction_records:
                        new_transactions = pd.DataFrame(transaction_records)
                        st.session_state.financial_transactions = pd.concat([st.session_state.financial_transactions, new_transactions], ignore_index=True)
                    
                    st.success("Attendance saved!")
                    st.rerun()
            else:
                st.warning("Please register workers first.")
        
        with col2:
            st.markdown("##### Today's Summary")
            if not st.session_state.attendance.empty:
                today_attendance = st.session_state.attendance[
                    pd.to_datetime(st.session_state.attendance['date']) == pd.to_datetime(datetime.now().date())
                ]
                
                if not today_attendance.empty:
                    present_count = today_attendance['present'].sum()
                    total_hours = today_attendance[today_attendance['present']]['hours'].sum()
                    st.metric("Present Today", int(present_count))
                    st.metric("Total Hours", f"{total_hours:.1f}")
                else:
                    st.info("No attendance recorded today")
            else:
                st.info("No attendance records")
        
        st.markdown("---")
        
        if not st.session_state.attendance.empty:
            st.markdown("##### Recent Attendance")
            recent = st.session_state.attendance.tail(20)
            st.dataframe(recent, use_container_width=True)
    
    with tab3:
        st.subheader("Labour Analytics")
        
        if not st.session_state.attendance.empty:
            attendance_df = st.session_state.attendance.copy()
            attendance_df['date'] = pd.to_datetime(attendance_df['date'])
            
            daily_attendance = attendance_df.groupby('date')['present'].sum().reset_index()
            fig = px.line(
                daily_attendance,
                x='date',
                y='present',
                title='Daily Worker Attendance',
                labels={'present': 'Workers Present', 'date': 'Date'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            if not st.session_state.labour_records.empty:
                worker_attendance = attendance_df[attendance_df['present']].groupby('worker_id').size().reset_index(name='days_present')
                worker_attendance = worker_attendance.merge(
                    st.session_state.labour_records[['worker_id', 'name', 'daily_wage']],
                    on='worker_id',
                    how='left'
                )
                worker_attendance['total_wages'] = worker_attendance['days_present'] * worker_attendance['daily_wage']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(
                        worker_attendance,
                        x='name',
                        y='days_present',
                        title='Attendance by Worker',
                        labels={'days_present': 'Days Present', 'name': 'Worker'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.bar(
                        worker_attendance,
                        x='name',
                        y='total_wages',
                        title='Total Wages by Worker',
                        labels={'total_wages': 'Total Wages (₹)', 'name': 'Worker'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("#### Worker Summary")
                st.dataframe(worker_attendance, use_container_width=True)
        else:
            st.info("No attendance data available for analytics.")

def equipment_management():
    st.title("🚜 Equipment Management")
    
    tab1, tab2, tab3 = st.tabs(["Equipment Registry", "Maintenance & Usage", "Analytics"])
    
    with tab1:
        st.subheader("Equipment Registry")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Add Equipment")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                equipment_id = st.text_input("Equipment ID*", placeholder="e.g., TRAC-001")
                name = st.text_input("Name*", placeholder="e.g., Tractor")
            with col_b:
                equipment_type = st.selectbox(
                    "Type*",
                    ["Tractor", "Implement", "Vehicle", "Machine", "Tool"]
                )
                purchase_date = st.date_input("Purchase Date")
            with col_c:
                purchase_cost = st.number_input("Purchase Cost (₹)", min_value=0.0, step=1000.0)
                status = st.selectbox("Status", ["Active", "Under Repair", "Idle", "Retired"])
            
            equipment_notes = st.text_area("Notes / Specifications", key="equipment_notes")
            
            if st.button("Add Equipment", type="primary"):
                if equipment_id and name:
                    new_equipment = pd.DataFrame([{
                        'equipment_id': equipment_id,
                        'name': name,
                        'type': equipment_type,
                        'purchase_date': purchase_date,
                        'purchase_cost': purchase_cost,
                        'status': status,
                        'notes': equipment_notes
                    }])
                    st.session_state.equipment = pd.concat([st.session_state.equipment, new_equipment], ignore_index=True)
                    
                    if purchase_cost > 0:
                        new_transaction = pd.DataFrame([{
                            'date': purchase_date,
                            'type': 'Expense',
                            'category': 'Equipment Purchase',
                            'subcategory': equipment_type,
                            'amount': purchase_cost,
                            'description': f"{name} - {equipment_id}",
                            'reference_id': equipment_id,
                            'notes': equipment_notes
                        }])
                        st.session_state.financial_transactions = pd.concat([st.session_state.financial_transactions, new_transaction], ignore_index=True)
                    
                    st.success(f"Equipment {equipment_id} added!")
                    st.rerun()
                else:
                    st.error("Please fill all required fields (*)")
        
        with col2:
            st.markdown("##### Summary")
            if not st.session_state.equipment.empty:
                total_equipment = len(st.session_state.equipment)
                active_equipment = len(st.session_state.equipment[st.session_state.equipment['status'] == 'Active'])
                st.metric("Total Equipment", total_equipment)
                st.metric("Active", active_equipment)
            else:
                st.info("No equipment registered")
        
        st.markdown("---")
        
        if not st.session_state.equipment.empty:
            st.markdown("##### All Equipment")
            st.dataframe(st.session_state.equipment, use_container_width=True)
    
    with tab2:
        st.subheader("Maintenance & Usage Log")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### Add Maintenance/Usage Record")
            
            if not st.session_state.equipment.empty:
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    maint_date = st.date_input("Date*", value=datetime.now().date())
                    equipment_id = st.selectbox(
                        "Equipment*",
                        st.session_state.equipment['equipment_id'].tolist()
                    )
                with col_b:
                    maintenance_type = st.selectbox(
                        "Type*",
                        ["Routine Maintenance", "Repair", "Usage Log", "Fuel", "Inspection"]
                    )
                    cost = st.number_input("Cost (₹)", min_value=0.0, step=10.0)
                with col_c:
                    fuel_litres = st.number_input("Fuel (litres)", min_value=0.0, step=1.0)
                    hours_used = st.number_input("Hours Used", min_value=0.0, step=0.5)
                
                maint_notes = st.text_area("Notes / Description", key="maint_notes")
                
                if st.button("Add Record", type="primary"):
                    if equipment_id:
                        new_maintenance = pd.DataFrame([{
                            'date': maint_date,
                            'equipment_id': equipment_id,
                            'maintenance_type': maintenance_type,
                            'cost': cost,
                            'fuel_litres': fuel_litres,
                            'hours_used': hours_used,
                            'notes': maint_notes
                        }])
                        st.session_state.equipment_maintenance = pd.concat([st.session_state.equipment_maintenance, new_maintenance], ignore_index=True)
                        
                        if cost > 0:
                            new_transaction = pd.DataFrame([{
                                'date': maint_date,
                                'type': 'Expense',
                                'category': 'Equipment Maintenance',
                                'subcategory': maintenance_type,
                                'amount': cost,
                                'description': f"{maintenance_type} - {equipment_id}",
                                'reference_id': equipment_id,
                                'notes': maint_notes
                            }])
                            st.session_state.financial_transactions = pd.concat([st.session_state.financial_transactions, new_transaction], ignore_index=True)
                        
                        st.success("Maintenance record added!")
                        st.rerun()
                    else:
                        st.error("Please select equipment")
            else:
                st.warning("Please register equipment first.")
        
        with col2:
            st.markdown("##### This Month")
            if not st.session_state.equipment_maintenance.empty:
                this_month = st.session_state.equipment_maintenance[
                    pd.to_datetime(st.session_state.equipment_maintenance['date']).dt.to_period('M') == 
                    pd.to_datetime(datetime.now()).to_period('M')
                ]
                
                if not this_month.empty:
                    total_cost = this_month['cost'].sum()
                    total_fuel = this_month['fuel_litres'].sum()
                    st.metric("Maintenance Cost", f"₹{total_cost:.2f}")
                    st.metric("Fuel Consumed", f"{total_fuel:.2f} L")
                else:
                    st.info("No records this month")
            else:
                st.info("No maintenance records")
        
        st.markdown("---")
        
        if not st.session_state.equipment_maintenance.empty:
            st.markdown("##### Recent Records")
            recent = st.session_state.equipment_maintenance.tail(20)
            st.dataframe(recent, use_container_width=True)
    
    with tab3:
        st.subheader("Equipment Analytics")
        
        if not st.session_state.equipment_maintenance.empty:
            maint_df = st.session_state.equipment_maintenance.copy()
            maint_df['date'] = pd.to_datetime(maint_df['date'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                equipment_cost = maint_df.groupby('equipment_id')['cost'].sum().reset_index()
                fig = px.bar(
                    equipment_cost,
                    x='equipment_id',
                    y='cost',
                    title='Maintenance Cost by Equipment',
                    labels={'cost': 'Total Cost (₹)', 'equipment_id': 'Equipment'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                equipment_hours = maint_df.groupby('equipment_id')['hours_used'].sum().reset_index()
                fig = px.bar(
                    equipment_hours,
                    x='equipment_id',
                    y='hours_used',
                    title='Total Hours by Equipment',
                    labels={'hours_used': 'Total Hours', 'equipment_id': 'Equipment'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            monthly_cost = maint_df.groupby(maint_df['date'].dt.to_period('M'))['cost'].sum().reset_index()
            monthly_cost['date'] = monthly_cost['date'].astype(str)
            fig = px.line(
                monthly_cost,
                x='date',
                y='cost',
                title='Monthly Equipment Costs',
                labels={'cost': 'Cost (₹)', 'date': 'Month'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No maintenance data available for analytics.")

def financial_accounting():
    st.title("💰 Financial Accounting")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Add Transaction", "View Transactions", "Reports", "Profit & Loss"])
    
    with tab1:
        st.subheader("Add Financial Transaction")
        
        col1, col2 = st.columns(2)
        
        with col1:
            transaction_date = st.date_input("Date*", value=datetime.now().date())
            transaction_type = st.radio("Type*", ["Income", "Expense"])
            
            if transaction_type == "Income":
                category = st.selectbox(
                    "Category*",
                    ["Milk Sales", "Manure Sales", "Equipment Rent", "Calf/Cattle Sale", "Other Income"]
                )
            else:
                category = st.selectbox(
                    "Category*",
                    ["Feed Purchase", "Fodder Cultivation", "Health & Medicine", "Labour", 
                     "Equipment Maintenance", "Equipment Purchase", "Utilities", "Other Expense"]
                )
        
        with col2:
            subcategory = st.text_input("Subcategory")
            amount = st.number_input("Amount (₹)*", min_value=0.0, step=10.0)
            reference_id = st.text_input("Reference ID", placeholder="Animal ID, Worker ID, etc.")
        
        description = st.text_area("Description*")
        transaction_notes = st.text_area("Notes", key="transaction_notes")
        
        if st.button("Add Transaction", type="primary"):
            if amount > 0 and description:
                new_transaction = pd.DataFrame([{
                    'date': transaction_date,
                    'type': transaction_type,
                    'category': category,
                    'subcategory': subcategory,
                    'amount': amount,
                    'description': description,
                    'reference_id': reference_id,
                    'notes': transaction_notes
                }])
                st.session_state.financial_transactions = pd.concat([st.session_state.financial_transactions, new_transaction], ignore_index=True)
                st.success("Transaction added!")
                st.rerun()
            else:
                st.error("Please fill all required fields (*)")
    
    with tab2:
        st.subheader("Transaction History")
        
        if not st.session_state.financial_transactions.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                date_from = st.date_input("From", value=datetime.now().date() - timedelta(days=30), key="trans_from")
            with col2:
                date_to = st.date_input("To", value=datetime.now().date(), key="trans_to")
            with col3:
                filter_type = st.multiselect(
                    "Type",
                    ["Income", "Expense"],
                    default=["Income", "Expense"]
                )
            
            filtered = st.session_state.financial_transactions[
                (pd.to_datetime(st.session_state.financial_transactions['date']) >= pd.to_datetime(date_from)) &
                (pd.to_datetime(st.session_state.financial_transactions['date']) <= pd.to_datetime(date_to)) &
                (st.session_state.financial_transactions['type'].isin(filter_type))
            ]
            
            if not filtered.empty:
                total_income = filtered[filtered['type'] == 'Income']['amount'].sum()
                total_expense = filtered[filtered['type'] == 'Expense']['amount'].sum()
                net = total_income - total_expense
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Income", f"₹{total_income:.2f}")
                with col2:
                    st.metric("Total Expense", f"₹{total_expense:.2f}")
                with col3:
                    st.metric("Net", f"₹{net:.2f}", delta=f"{net:.2f}")
                
                st.dataframe(filtered, use_container_width=True)
                
                csv = filtered.to_csv(index=False)
                st.download_button(
                    "📥 Download as CSV",
                    csv,
                    "transactions.csv",
                    "text/csv"
                )
            else:
                st.info("No transactions in selected period")
        else:
            st.info("No transactions recorded yet")
    
    with tab3:
        st.subheader("Financial Reports")
        
        if not st.session_state.financial_transactions.empty:
            trans_df = st.session_state.financial_transactions.copy()
            trans_df['date'] = pd.to_datetime(trans_df['date'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                income_by_category = trans_df[trans_df['type'] == 'Income'].groupby('category')['amount'].sum().reset_index()
                fig = px.pie(
                    income_by_category,
                    values='amount',
                    names='category',
                    title='Income by Category'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                expense_by_category = trans_df[trans_df['type'] == 'Expense'].groupby('category')['amount'].sum().reset_index()
                fig = px.pie(
                    expense_by_category,
                    values='amount',
                    names='category',
                    title='Expenses by Category'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            monthly_summary = trans_df.groupby([trans_df['date'].dt.to_period('M'), 'type'])['amount'].sum().reset_index()
            monthly_summary['date'] = monthly_summary['date'].astype(str)
            monthly_pivot = monthly_summary.pivot(index='date', columns='type', values='amount').fillna(0).reset_index()
            
            if 'Income' in monthly_pivot.columns and 'Expense' in monthly_pivot.columns:
                monthly_pivot['Net'] = monthly_pivot['Income'] - monthly_pivot['Expense']
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=monthly_pivot['date'], y=monthly_pivot['Income'], name='Income', marker_color='green'))
                fig.add_trace(go.Bar(x=monthly_pivot['date'], y=monthly_pivot['Expense'], name='Expense', marker_color='red'))
                fig.add_trace(go.Scatter(x=monthly_pivot['date'], y=monthly_pivot['Net'], name='Net', mode='lines+markers', line=dict(color='blue', width=3)))
                fig.update_layout(title='Monthly Income vs Expense', xaxis_title='Month', yaxis_title='Amount (₹)', barmode='group')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No financial data available for reports")
    
    with tab4:
        st.subheader("Profit & Loss Statement")
        
        if not st.session_state.financial_transactions.empty:
            col1, col2 = st.columns(2)
            with col1:
                pl_from = st.date_input("From", value=datetime.now().date() - timedelta(days=365), key="pl_from")
            with col2:
                pl_to = st.date_input("To", value=datetime.now().date(), key="pl_to")
            
            trans_df = st.session_state.financial_transactions.copy()
            trans_df['date'] = pd.to_datetime(trans_df['date'])
            
            filtered_pl = trans_df[
                (trans_df['date'] >= pd.to_datetime(pl_from)) &
                (trans_df['date'] <= pd.to_datetime(pl_to))
            ]
            
            if not filtered_pl.empty:
                st.markdown("#### Income")
                income_summary = filtered_pl[filtered_pl['type'] == 'Income'].groupby('category')['amount'].sum().reset_index()
                income_summary.columns = ['Category', 'Amount (₹)']
                st.dataframe(income_summary, use_container_width=True)
                total_income = income_summary['Amount (₹)'].sum()
                st.markdown(f"**Total Income: ₹{total_income:.2f}**")
                
                st.markdown("---")
                
                st.markdown("#### Expenses")
                expense_summary = filtered_pl[filtered_pl['type'] == 'Expense'].groupby('category')['amount'].sum().reset_index()
                expense_summary.columns = ['Category', 'Amount (₹)']
                st.dataframe(expense_summary, use_container_width=True)
                total_expense = expense_summary['Amount (₹)'].sum()
                st.markdown(f"**Total Expense: ₹{total_expense:.2f}**")
                
                st.markdown("---")
                
                net_profit = total_income - total_expense
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Income", f"₹{total_income:.2f}")
                with col2:
                    st.metric("Total Expense", f"₹{total_expense:.2f}")
                with col3:
                    st.metric("Net Profit/Loss", f"₹{net_profit:.2f}", delta=f"{net_profit:.2f}")
                
                if not st.session_state.milk_records.empty:
                    milk_df = st.session_state.milk_records.copy()
                    milk_df['date'] = pd.to_datetime(milk_df['date'])
                    filtered_milk = milk_df[
                        (milk_df['date'] >= pd.to_datetime(pl_from)) &
                        (milk_df['date'] <= pd.to_datetime(pl_to))
                    ]
                    
                    if not filtered_milk.empty:
                        total_milk = filtered_milk['yield_litres'].sum()
                        if total_milk > 0:
                            cost_per_litre = total_expense / total_milk
                            profit_per_litre = net_profit / total_milk
                            
                            st.markdown("---")
                            st.markdown("#### Per Litre Analysis")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Milk Produced", f"{total_milk:.2f} L")
                            with col2:
                                st.metric("Cost per Litre", f"₹{cost_per_litre:.2f}/L")
                            with col3:
                                st.metric("Profit per Litre", f"₹{profit_per_litre:.2f}/L")
            else:
                st.info("No transactions in selected period")
        else:
            st.info("No financial data available")

def reports():
    st.title("📊 Comprehensive Reports")
    
    report_type = st.selectbox(
        "Select Report Type",
        [
            "Cow-wise Productivity",
            "Calving History & Expected Deliveries",
            "Feed Efficiency Analysis",
            "Labour Cost Breakdown",
            "Annual Herd Health Summary",
            "Asset Summary"
        ]
    )
    
    if report_type == "Cow-wise Productivity":
        st.subheader("Cow-wise Productivity Report")
        
        if not st.session_state.animals.empty and not st.session_state.milk_records.empty:
            milk_df = st.session_state.milk_records.copy()
            
            productivity = milk_df.groupby('animal_id').agg({
                'yield_litres': ['sum', 'mean', 'count']
            }).reset_index()
            productivity.columns = ['animal_id', 'Total Milk (L)', 'Avg per Session (L)', 'Sessions']
            
            productivity = productivity.merge(
                st.session_state.animals[['animal_id', 'name', 'dob', 'lifecycle_stage']],
                on='animal_id',
                how='left'
            )
            
            productivity = productivity.sort_values('Total Milk (L)', ascending=False)
            
            st.dataframe(productivity, use_container_width=True)
            
            csv = productivity.to_csv(index=False)
            st.download_button(
                "📥 Download Report",
                csv,
                "cow_productivity_report.csv",
                "text/csv"
            )
        else:
            st.info("Insufficient data for this report")
    
    elif report_type == "Calving History & Expected Deliveries":
        st.subheader("Calving History & Expected Deliveries")
        
        if not st.session_state.breeding_records.empty:
            breeding_df = st.session_state.breeding_records.copy()
            
            st.markdown("#### Expected Calvings")
            expected = breeding_df[
                (breeding_df['pregnancy_confirmed'] == 'Yes') &
                (breeding_df['actual_calving'].isna())
            ].sort_values('expected_calving')
            
            if not expected.empty:
                st.dataframe(expected[['animal_id', 'insemination_date', 'expected_calving', 'bull_id']], use_container_width=True)
            else:
                st.info("No expected calvings")
            
            st.markdown("#### Completed Calvings")
            completed = breeding_df[breeding_df['actual_calving'].notna()].sort_values('actual_calving', ascending=False)
            
            if not completed.empty:
                st.dataframe(completed, use_container_width=True)
                
                csv = completed.to_csv(index=False)
                st.download_button(
                    "📥 Download Report",
                    csv,
                    "calving_history_report.csv",
                    "text/csv"
                )
            else:
                st.info("No completed calvings recorded")
        else:
            st.info("No breeding records available")
    
    elif report_type == "Feed Efficiency Analysis":
        st.subheader("Feed Efficiency Analysis")
        
        if not st.session_state.feed_consumption.empty and not st.session_state.milk_records.empty:
            feed_df = st.session_state.feed_consumption.copy()
            feed_df['date'] = pd.to_datetime(feed_df['date'])
            
            milk_df = st.session_state.milk_records.copy()
            milk_df['date'] = pd.to_datetime(milk_df['date'])
            
            daily_feed = feed_df.groupby('date')['quantity_kg'].sum().reset_index()
            daily_feed.columns = ['date', 'feed_kg']
            
            daily_milk = milk_df.groupby('date')['yield_litres'].sum().reset_index()
            daily_milk.columns = ['date', 'milk_litres']
            
            efficiency = pd.merge(daily_feed, daily_milk, on='date', how='inner')
            efficiency['feed_per_litre'] = efficiency['feed_kg'] / efficiency['milk_litres']
            
            if not st.session_state.feed_inventory.empty:
                avg_feed_cost = st.session_state.feed_inventory['cost_per_kg'].mean()
                efficiency['feed_cost_per_litre'] = efficiency['feed_per_litre'] * avg_feed_cost
            
            st.dataframe(efficiency, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                avg_efficiency = efficiency['feed_per_litre'].mean()
                st.metric("Average Feed Efficiency", f"{avg_efficiency:.2f} kg/L")
            with col2:
                if 'feed_cost_per_litre' in efficiency.columns:
                    avg_cost = efficiency['feed_cost_per_litre'].mean()
                    st.metric("Average Feed Cost per Litre", f"₹{avg_cost:.2f}/L")
            
            csv = efficiency.to_csv(index=False)
            st.download_button(
                "📥 Download Report",
                csv,
                "feed_efficiency_report.csv",
                "text/csv"
            )
        else:
            st.info("Insufficient data for this report")
    
    elif report_type == "Labour Cost Breakdown":
        st.subheader("Labour Cost Breakdown")
        
        if not st.session_state.attendance.empty and not st.session_state.labour_records.empty:
            attendance_df = st.session_state.attendance.copy()
            attendance_df['date'] = pd.to_datetime(attendance_df['date'])
            
            worker_summary = attendance_df[attendance_df['present']].groupby('worker_id').agg({
                'present': 'sum',
                'hours': 'sum'
            }).reset_index()
            worker_summary.columns = ['worker_id', 'days_worked', 'total_hours']
            
            worker_summary = worker_summary.merge(
                st.session_state.labour_records[['worker_id', 'name', 'category', 'daily_wage']],
                on='worker_id',
                how='left'
            )
            
            worker_summary['total_wages'] = worker_summary['days_worked'] * worker_summary['daily_wage']
            
            st.dataframe(worker_summary, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                total_wages = worker_summary['total_wages'].sum()
                st.metric("Total Labour Cost", f"₹{total_wages:.2f}")
            with col2:
                total_days = worker_summary['days_worked'].sum()
                st.metric("Total Worker-Days", int(total_days))
            with col3:
                total_hours = worker_summary['total_hours'].sum()
                st.metric("Total Hours", f"{total_hours:.1f}")
            
            category_breakdown = worker_summary.groupby('category')['total_wages'].sum().reset_index()
            fig = px.pie(
                category_breakdown,
                values='total_wages',
                names='category',
                title='Labour Cost by Category'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            csv = worker_summary.to_csv(index=False)
            st.download_button(
                "📥 Download Report",
                csv,
                "labour_cost_report.csv",
                "text/csv"
            )
        else:
            st.info("Insufficient data for this report")
    
    elif report_type == "Annual Herd Health Summary":
        st.subheader("Annual Herd Health Summary")
        
        if not st.session_state.health_records.empty:
            health_df = st.session_state.health_records.copy()
            health_df['date'] = pd.to_datetime(health_df['date'])
            
            col1, col2 = st.columns(2)
            with col1:
                year = st.selectbox("Select Year", sorted(health_df['date'].dt.year.unique(), reverse=True))
            
            yearly_health = health_df[health_df['date'].dt.year == year]
            
            if not yearly_health.empty:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    total_records = len(yearly_health)
                    st.metric("Total Health Records", total_records)
                with col2:
                    vaccinations = len(yearly_health[yearly_health['record_type'] == 'Vaccination'])
                    st.metric("Vaccinations", vaccinations)
                with col3:
                    diseases = len(yearly_health[yearly_health['record_type'] == 'Disease/Illness'])
                    st.metric("Disease Cases", diseases)
                with col4:
                    total_cost = yearly_health['cost'].sum()
                    st.metric("Total Health Cost", f"₹{total_cost:.2f}")
                
                st.markdown("#### Records by Type")
                type_summary = yearly_health.groupby('record_type').agg({
                    'animal_id': 'count',
                    'cost': 'sum'
                }).reset_index()
                type_summary.columns = ['Record Type', 'Count', 'Total Cost (₹)']
                st.dataframe(type_summary, use_container_width=True)
                
                st.markdown("#### All Health Records")
                st.dataframe(yearly_health, use_container_width=True)
                
                csv = yearly_health.to_csv(index=False)
                st.download_button(
                    "📥 Download Report",
                    csv,
                    f"health_summary_{year}.csv",
                    "text/csv"
                )
            else:
                st.info(f"No health records for {year}")
        else:
            st.info("No health records available")
    
    elif report_type == "Asset Summary":
        st.subheader("Asset Summary Report")
        
        st.markdown("#### Animals")
        if not st.session_state.animals.empty:
            animal_summary = st.session_state.animals.groupby(['lifecycle_stage', 'sex']).size().reset_index(name='count')
            st.dataframe(animal_summary, use_container_width=True)
            
            total_animals = len(st.session_state.animals)
            active_animals = len(st.session_state.animals[st.session_state.animals['status'] == 'Active'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Animals", total_animals)
            with col2:
                st.metric("Active Animals", active_animals)
        else:
            st.info("No animal records")
        
        st.markdown("---")
        
        st.markdown("#### Equipment")
        if not st.session_state.equipment.empty:
            equipment_summary = st.session_state.equipment.groupby(['type', 'status']).size().reset_index(name='count')
            st.dataframe(equipment_summary, use_container_width=True)
            
            total_value = st.session_state.equipment['purchase_cost'].sum()
            st.metric("Total Equipment Value", f"₹{total_value:.2f}")
        else:
            st.info("No equipment records")
        
        st.markdown("---")
        
        st.markdown("#### Financial Summary")
        if not st.session_state.financial_transactions.empty:
            trans_df = st.session_state.financial_transactions.copy()
            
            total_income = trans_df[trans_df['type'] == 'Income']['amount'].sum()
            total_expense = trans_df[trans_df['type'] == 'Expense']['amount'].sum()
            net = total_income - total_expense
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Income", f"₹{total_income:.2f}")
            with col2:
                st.metric("Total Expense", f"₹{total_expense:.2f}")
            with col3:
                st.metric("Net Position", f"₹{net:.2f}")
        else:
            st.info("No financial records")

def dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 3rem 0;">
        <h1 style="font-size: 3.5rem; margin: 0; background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;">
            🏠 Farm Dashboard
        </h1>
        <p style="font-size: 1.2rem; color: #94a3b8; margin-top: 1rem;">
            Real-time insights into your dairy operations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not st.session_state.animals.empty:
            active_animals = len(st.session_state.animals[st.session_state.animals['status'] == 'Active'])
            st.metric("Active Animals", active_animals)
        else:
            st.metric("Active Animals", 0)
    
    with col2:
        if not st.session_state.milk_records.empty:
            today_milk = st.session_state.milk_records[
                pd.to_datetime(st.session_state.milk_records['date']) == pd.to_datetime(datetime.now().date())
            ]['yield_litres'].sum()
            st.metric("Today's Milk", f"{today_milk:.2f} L")
        else:
            st.metric("Today's Milk", "0 L")
    
    with col3:
        if not st.session_state.labour_records.empty:
            active_workers = len(st.session_state.labour_records[st.session_state.labour_records['status'] == 'Active'])
            st.metric("Active Workers", active_workers)
        else:
            st.metric("Active Workers", 0)
    
    with col4:
        if not st.session_state.equipment.empty:
            active_equipment = len(st.session_state.equipment[st.session_state.equipment['status'] == 'Active'])
            st.metric("Active Equipment", active_equipment)
        else:
            st.metric("Active Equipment", 0)
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Dairy Dashboard", "Financial Dashboard", "Health Dashboard", "Farm Dashboard"])
    
    with tab1:
        st.subheader("Dairy Operations")
        
        if not st.session_state.milk_records.empty:
            milk_df = st.session_state.milk_records.copy()
            milk_df['date'] = pd.to_datetime(milk_df['date'])
            
            last_30_days = milk_df[milk_df['date'] >= (datetime.now() - timedelta(days=30))]
            
            if not last_30_days.empty:
                daily_production = last_30_days.groupby('date')['yield_litres'].sum().reset_index()
                fig = px.line(
                    daily_production,
                    x='date',
                    y='yield_litres',
                    title='Last 30 Days Milk Production',
                    labels={'yield_litres': 'Milk (Litres)', 'date': 'Date'}
                )
                fig.update_traces(line_color='#10b981', line_width=3)
                st.plotly_chart(fig, use_container_width=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    top_producers = last_30_days.groupby('animal_id')['yield_litres'].sum().nlargest(5).reset_index()
                    fig = px.bar(
                        top_producers,
                        x='animal_id',
                        y='yield_litres',
                        title='Top 5 Producers (Last 30 Days)',
                        labels={'yield_litres': 'Milk (Litres)', 'animal_id': 'Cow ID'},
                        color_discrete_sequence=['#10b981']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    if not st.session_state.breeding_records.empty:
                        breeding_df = st.session_state.breeding_records.copy()
                        pregnant = len(breeding_df[breeding_df['pregnancy_confirmed'] == 'Yes'])
                        pending = len(breeding_df[breeding_df['pregnancy_confirmed'] == 'Pending'])
                        
                        fertility_data = pd.DataFrame({
                            'Status': ['Pregnant', 'Pending Confirmation'],
                            'Count': [pregnant, pending]
                        })
                        
                        fig = px.bar(
                            fertility_data,
                            x='Status',
                            y='Count',
                            title='Herd Fertility Summary',
                            labels={'Count': 'Number of Cows'},
                            color_discrete_sequence=['#3b82f6', '#8b5cf6']
                        )
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No milk production data available")
    
    with tab2:
        st.subheader("Financial Overview")
        
        if not st.session_state.financial_transactions.empty:
            trans_df = st.session_state.financial_transactions.copy()
            trans_df['date'] = pd.to_datetime(trans_df['date'])
            
            last_6_months = trans_df[trans_df['date'] >= (datetime.now() - timedelta(days=180))]
            
            if not last_6_months.empty:
                monthly_summary = last_6_months.groupby([last_6_months['date'].dt.to_period('M'), 'type'])['amount'].sum().reset_index()
                monthly_summary['date'] = monthly_summary['date'].astype(str)
                monthly_pivot = monthly_summary.pivot(index='date', columns='type', values='amount').fillna(0).reset_index()
                
                if 'Income' in monthly_pivot.columns and 'Expense' in monthly_pivot.columns:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=monthly_pivot['date'], y=monthly_pivot['Income'], name='Income', marker_color='#10b981'))
                    fig.add_trace(go.Bar(x=monthly_pivot['date'], y=monthly_pivot['Expense'], name='Expense', marker_color='#ef4444'))
                    fig.update_layout(
                        title='Monthly Income vs Expense (Last 6 Months)',
                        xaxis_title='Month',
                        yaxis_title='Amount (₹)',
                        barmode='group'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    expense_by_cat = last_6_months[last_6_months['type'] == 'Expense'].groupby('category')['amount'].sum().reset_index()
                    fig = px.pie(
                        expense_by_cat,
                        values='amount',
                        names='category',
                        title='Expense Distribution by Category',
                        color_discrete_sequence=px.colors.sequential.Teal
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    income_by_cat = last_6_months[last_6_months['type'] == 'Income'].groupby('category')['amount'].sum().reset_index()
                    fig = px.pie(
                        income_by_cat,
                        values='amount',
                        names='category',
                        title='Income Distribution by Category',
                        color_discrete_sequence=px.colors.sequential.Mint
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No financial data available")
    
    with tab3:
        st.subheader("Health Overview")
        
        if not st.session_state.health_records.empty:
            health_df = st.session_state.health_records.copy()
            health_df['date'] = pd.to_datetime(health_df['date'])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                sick_animals = health_df[
                    (health_df['record_type'] == 'Disease/Illness') &
                    (health_df['date'] >= (datetime.now() - timedelta(days=30)))
                ]['animal_id'].nunique()
                st.metric("Sick Animals (Last 30 Days)", sick_animals)
            
            with col2:
                upcoming_vaccines = health_df[
                    (pd.to_datetime(health_df['next_due']) >= pd.to_datetime(datetime.now().date())) &
                    (pd.to_datetime(health_df['next_due']) <= pd.to_datetime(datetime.now().date() + timedelta(days=30)))
                ]
                st.metric("Vaccines Due (Next 30 Days)", len(upcoming_vaccines))
            
            with col3:
                health_cost = health_df[health_df['date'] >= (datetime.now() - timedelta(days=30))]['cost'].sum()
                st.metric("Health Cost (Last 30 Days)", f"₹{health_cost:.2f}")
            
            record_type_trend = health_df[health_df['date'] >= (datetime.now() - timedelta(days=90))].groupby(
                [health_df['date'].dt.to_period('M'), 'record_type']
            ).size().reset_index(name='count')
            record_type_trend['date'] = record_type_trend['date'].astype(str)
            
            fig = px.bar(
                record_type_trend,
                x='date',
                y='count',
                color='record_type',
                title='Health Records Trend (Last 3 Months)',
                labels={'count': 'Number of Records', 'date': 'Month'},
                barmode='stack',
                color_discrete_sequence=['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b']
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No health data available")
    
    with tab4:
        st.subheader("Farm Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not st.session_state.fodder_cultivation.empty:
                st.markdown("#### Fodder Cultivation Status")
                cultivation_status = st.session_state.fodder_cultivation.groupby('status').size().reset_index(name='count')
                fig = px.pie(
                    cultivation_status,
                    values='count',
                    names='status',
                    title='Cultivation Status'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No cultivation data")
        
        with col2:
            if not st.session_state.equipment_maintenance.empty:
                st.markdown("#### Equipment Usage")
                equip_df = st.session_state.equipment_maintenance.copy()
                equip_df['date'] = pd.to_datetime(equip_df['date'])
                
                recent_usage = equip_df[equip_df['date'] >= (datetime.now() - timedelta(days=30))]
                equipment_hours = recent_usage.groupby('equipment_id')['hours_used'].sum().reset_index()
                
                fig = px.bar(
                    equipment_hours,
                    x='equipment_id',
                    y='hours_used',
                    title='Equipment Usage (Last 30 Days)',
                    labels={'hours_used': 'Hours', 'equipment_id': 'Equipment'}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No equipment usage data")
        
        if not st.session_state.feed_inventory.empty:
            st.markdown("#### Feed Stock Status")
            feed_stock = st.session_state.feed_inventory.groupby('category')['quantity_kg'].sum().reset_index()
            fig = px.bar(
                feed_stock,
                x='category',
                y='quantity_kg',
                title='Feed Stock by Category',
                labels={'quantity_kg': 'Stock (kg)', 'category': 'Category'}
            )
            st.plotly_chart(fig, use_container_width=True)

if menu == "🏠 Dashboard":
    dashboard()
elif menu == "🐄 Animal Management":
    animal_management()
elif menu == "💕 Breeding & Genetics":
    breeding_genetics()
elif menu == "🥛 Milk Collection & Sales":
    milk_collection_sales()
elif menu == "🌾 Fodder & Feed":
    fodder_feed()
elif menu == "💊 Health & Medicine":
    health_medicine()
elif menu == "👷 Labour Management":
    labour_management()
elif menu == "🚜 Equipment":
    equipment_management()
elif menu == "💰 Financial Accounting":
    financial_accounting()
elif menu == "📊 Reports":
    reports()

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("Gir Cow Dairy Farm Management System - Integrated biological and financial tracking for dairy operations.")
