# ...existing code...
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Gir Cow Dairy Farm Management",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try to import database modules and handle configuration errors
try:
    from database import SessionLocal  # optional, may not exist in dev
    import db_utils  # optional helper module for DB operations
    DATABASE_AVAILABLE = True
    DATABASE_ERROR = ""
except Exception as e:
    SessionLocal = None
    db_utils = None
    DATABASE_AVAILABLE = False
    DATABASE_ERROR = str(e)

# If DB not available, show a warning but continue with in-memory dataframes
if not DATABASE_AVAILABLE:
    st.warning("⚠️ Database not configured — running in offline/demo mode. Some features that require DB persistence will use in-memory session state.")
    if DATABASE_ERROR:
        st.caption(f"DB import error: {DATABASE_ERROR}")

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


def ensure_session_dataframes():
    # initialize all expected session_state dataframes if missing
    if 'animals' not in st.session_state:
        st.session_state.animals = pd.DataFrame(columns=[
            "animal_id", "name", "ear_tag", "dob", "sex", "breed",
            "lifecycle_stage", "status", "sire", "dam", "notes"
        ])
    if 'milk_records' not in st.session_state:
        st.session_state.milk_records = pd.DataFrame(columns=[
            "record_id", "animal_id", "date", "yield_litres", "fat_percent", "notes"
        ])
    if 'breeding_records' not in st.session_state:
        st.session_state.breeding_records = pd.DataFrame(columns=[
            "record_id", "female_id", "sire_id", "date", "method", "pregnancy_confirmed", "expected_calving", "notes"
        ])
    if 'health_records' not in st.session_state:
        st.session_state.health_records = pd.DataFrame(columns=[
            "record_id", "animal_id", "date", "issue", "treatment", "vet", "notes"
        ])
    if 'medicine_inventory' not in st.session_state:
        st.session_state.medicine_inventory = pd.DataFrame(columns=[
            "medicine_id", "name", "quantity", "unit", "expiry_date", "notes"
        ])
    if 'fodder_cultivation' not in st.session_state:
        st.session_state.fodder_cultivation = pd.DataFrame(columns=[
            "plot_id", "crop", "area_acres", "sowing_date", "status", "notes"
        ])
    if 'feed_inventory' not in st.session_state:
        st.session_state.feed_inventory = pd.DataFrame(columns=[
            "feed_id", "feed_name", "quantity_kg", "unit_cost", "notes"
        ])
    if 'feed_consumption' not in st.session_state:
        st.session_state.feed_consumption = pd.DataFrame(columns=[
            "consumption_id", "date", "animal_id", "feed_name", "quantity_kg", "notes"
        ])
    if 'labour_records' not in st.session_state:
        st.session_state.labour_records = pd.DataFrame(columns=[
            "worker_id", "name", "role", "wage", "notes"
        ])
    if 'attendance' not in st.session_state:
        st.session_state.attendance = pd.DataFrame(columns=[
            "attendance_id", "date", "worker_id", "present", "notes"
        ])
    if 'equipment' not in st.session_state:
        st.session_state.equipment = pd.DataFrame(columns=[
            "equipment_id", "name", "purchase_date", "cost", "status", "notes"
        ])
    if 'equipment_maintenance' not in st.session_state:
        st.session_state.equipment_maintenance = pd.DataFrame(columns=[
            "maintenance_id", "equipment_id", "date", "description", "cost", "notes"
        ])
    if 'financial_transactions' not in st.session_state:
        st.session_state.financial_transactions = pd.DataFrame(columns=[
            "transaction_id", "date", "type", "subcategory", "amount", "reference_id", "description", "notes"
        ])

ensure_session_dataframes()


def load_data_from_db():
    # If db_utils is available, try to load real data; otherwise keep session data
    if db_utils and SessionLocal:
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
            st.error(f"Error loading data from DB: {e}")
            try:
                db.rollback()
            except Exception:
                pass
        finally:
            try:
                db.close()
            except Exception:
                pass


if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if not st.session_state.data_loaded and DATABASE_AVAILABLE:
    try:
        load_data_from_db()
        st.session_state.data_loaded = True
    except (ValueError, TypeError, Exception) as e:
        st.error("⚠️ Database Connection Error")
        st.markdown(f"Cannot load data from the database. Error: `{str(e)}`")
        st.session_state.data_loaded = False

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
                new = {
                    "animal_id": animal_id,
                    "name": name,
                    "ear_tag": ear_tag,
                    "dob": pd.to_datetime(dob).date(),
                    "sex": sex,
                    "breed": breed,
                    "lifecycle_stage": lifecycle_stage,
                    "status": status,
                    "sire": sire,
                    "dam": dam,
                    "notes": notes
                }
                st.session_state.animals = pd.concat([st.session_state.animals, pd.DataFrame([new])], ignore_index=True)
                st.success(f"Registered animal {animal_id}")
            else:
                st.error("Please fill required fields: Animal ID, Date of Birth, Sex, Lifecycle Stage")

    with tab2:
        st.subheader("All Animals")

        if not st.session_state.animals.empty:
            # filters
            all_stages = st.session_state.animals['lifecycle_stage'].dropna().unique().tolist() or [
                "Calf (0-1 year)", "Heifer (1-3 years)", "Adult Cow (3+ years)", "Bull"
            ]
            all_sex = st.session_state.animals['sex'].dropna().unique().tolist() or ["Female", "Male"]
            all_status = st.session_state.animals['status'].dropna().unique().tolist() or ["Active", "Sold", "Deceased"]

            col1, col2, col3 = st.columns(3)
            with col1:
                filter_stage = st.multiselect("Lifecycle Stage", all_stages, default=all_stages)
            with col2:
                filter_sex = st.multiselect("Sex", all_sex, default=all_sex)
            with col3:
                filter_status = st.multiselect("Status", all_status, default=all_status)

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
                a = st.session_state.animals[st.session_state.animals['animal_id'] == selected_animal]
                if not a.empty:
                    st.write(a.T)
                    # related records
                    milk = st.session_state.milk_records[st.session_state.milk_records['animal_id'] == selected_animal]
                    breed = st.session_state.breeding_records[
                        (st.session_state.breeding_records['female_id'] == selected_animal) |
                        (st.session_state.breeding_records['sire_id'] == selected_animal)
                    ]
                    health = st.session_state.health_records[st.session_state.health_records['animal_id'] == selected_animal]

                    st.markdown("#### Milk Records")
                    st.dataframe(milk, use_container_width=True)
                    st.markdown("#### Breeding")
                    st.dataframe(breed, use_container_width=True)
                    st.markdown("#### Health")
                    st.dataframe(health, use_container_width=True)
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
                female_id = st.selectbox("Female (Dam)", female_animals)
                method = st.selectbox("Method", ["Natural", "AI"])
            with col2:
                sire_id = st.text_input("Sire ID (or bull)")
                breeding_date = st.date_input("Date", value=datetime.now().date())

            pregnancy_confirmed = st.selectbox("Pregnancy Confirmed?", ["No", "Yes"])
            expected_calving = None
            if pregnancy_confirmed == "Yes":
                expected_calving = breeding_date + timedelta(days=283)  # approximate

            notes = st.text_area("Notes")

            if st.button("Record Breeding Event", type="primary"):
                new = {
                    "record_id": f"br-{len(st.session_state.breeding_records)+1}",
                    "female_id": female_id,
                    "sire_id": sire_id,
                    "date": pd.to_datetime(breeding_date),
                    "method": method,
                    "pregnancy_confirmed": pregnancy_confirmed,
                    "expected_calving": expected_calving,
                    "notes": notes
                }
                st.session_state.breeding_records = pd.concat([st.session_state.breeding_records, pd.DataFrame([new])], ignore_index=True)
                st.success("Breeding event recorded.")
        else:
            st.warning("Please register animals first in Animal Management.")

    with tab2:
        st.subheader("All Breeding Records")

        if not st.session_state.breeding_records.empty:
            st.dataframe(st.session_state.breeding_records, use_container_width=True)
        else:
            st.info("No breeding records yet.")

    with tab3:
        st.subheader("Lineage Information")

        if not st.session_state.animals.empty:
            animal_id = st.selectbox("Select Animal", st.session_state.animals['animal_id'].tolist())

            if animal_id:
                # simple two-generation lineage
                row = st.session_state.animals[st.session_state.animals['animal_id'] == animal_id]
                if not row.empty:
                    sire = row.iloc[0].get('sire')
                    dam = row.iloc[0].get('dam')
                    st.markdown(f"**Sire:** {sire or 'Unknown'}")
                    st.markdown(f"**Dam:** {dam or 'Unknown'}")
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
                animal_id = st.selectbox("Cow", lactating_cows)
            with col2:
                date = st.date_input("Date", value=datetime.now().date())
            with col3:
                yield_litres = st.number_input("Yield (litres)", min_value=0.0, step=0.1)

            notes = st.text_area("Notes")

            if st.button("Record Milk Collection", type="primary"):
                new = {
                    "record_id": f"m-{len(st.session_state.milk_records)+1}",
                    "animal_id": animal_id,
                    "date": pd.to_datetime(date),
                    "yield_litres": float(yield_litres),
                    "fat_percent": None,
                    "notes": notes
                }
                st.session_state.milk_records = pd.concat([st.session_state.milk_records, pd.DataFrame([new])], ignore_index=True)
                st.success("Milk collection recorded.")
        else:
            st.warning("Please register animals first in Animal Management.")

    with tab2:
        st.subheader("Milk Collection Records")

        if not st.session_state.milk_records.empty:
            col1, col2 = st.columns(2)
            with col1:
                date_from = st.date_input("From", value=(datetime.now() - timedelta(days=30)).date())
            with col2:
                date_to = st.date_input("To", value=datetime.now().date())

            filtered_records = st.session_state.milk_records[
                (pd.to_datetime(st.session_state.milk_records['date']) >= pd.to_datetime(date_from)) &
                (pd.to_datetime(st.session_state.milk_records['date']) <= pd.to_datetime(date_to))
            ]

            if not filtered_records.empty:
                st.dataframe(filtered_records, use_container_width=True)
            else:
                st.info("No milk records in selected range.")
        else:
            st.info("No milk records yet.")

    with tab3:
        st.subheader("Sales Analytics")

        if not st.session_state.milk_records.empty:
            milk_df = st.session_state.milk_records.copy()
            milk_df['date'] = pd.to_datetime(milk_df['date']).dt.date

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
                st.metric("Total Production (selected)", f"{milk_df['yield_litres'].sum():.2f} L")
            with col2:
                st.metric("Average per Day", f"{daily_production['yield_litres'].mean():.2f} L")
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
                crop = st.text_input("Crop")
            with col_b:
                area = st.number_input("Area (acres)", min_value=0.0, step=0.1)
            with col_c:
                sowing = st.date_input("Sowing Date", value=datetime.now().date())

            status = st.selectbox("Status", ["Sowing", "Growing", "Ready for Harvest", "Harvested"])
            notes = st.text_area("Notes", key="cultivation_notes")

            if st.button("Add Cultivation Record", type="primary"):
                new = {
                    "plot_id": f"plot-{len(st.session_state.fodder_cultivation)+1}",
                    "crop": crop,
                    "area_acres": area,
                    "sowing_date": pd.to_datetime(sowing),
                    "status": status,
                    "notes": notes
                }
                st.session_state.fodder_cultivation = pd.concat([st.session_state.fodder_cultivation, pd.DataFrame([new])], ignore_index=True)
                st.success("Cultivation record added.")

        with col2:
            st.markdown("##### Summary")
            if not st.session_state.fodder_cultivation.empty:
                st.metric("Total Plots", len(st.session_state.fodder_cultivation))
            else:
                st.info("No cultivation records.")

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
                feed_name = st.text_input("Feed Name")
            with col_b:
                qty = st.number_input("Quantity (kg)", min_value=0.0, step=0.1)
            with col_c:
                unit_cost = st.number_input("Unit Cost (₹/kg)", min_value=0.0, step=1.0)

            feed_notes = st.text_area("Notes", key="feed_notes")

            if st.button("Add Feed Purchase", type="primary"):
                new = {
                    "feed_id": f"feed-{len(st.session_state.feed_inventory)+1}",
                    "feed_name": feed_name,
                    "quantity_kg": qty,
                    "unit_cost": unit_cost,
                    "notes": feed_notes
                }
                st.session_state.feed_inventory = pd.concat([st.session_state.feed_inventory, pd.DataFrame([new])], ignore_index=True)
                st.success("Feed purchase recorded.")

        with col2:
            st.markdown("##### Inventory Summary")
            if not st.session_state.feed_inventory.empty:
                st.metric("Total Feed Entries", len(st.session_state.feed_inventory))
            else:
                st.info("No feed inventory.")

        st.markdown("---")

        if not st.session_state.feed_inventory.empty:
            st.markdown("##### Feed Inventory")
            st.dataframe(st.session_state.feed_inventory, use_container_width=True)

    with tab3:
        st.subheader("Feed Consumption Tracking")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("##### Record Daily Consumption")

            if not st.session_state.feed_inventory.empty and not st.session_state.animals.empty:
                animal_list = st.session_state.animals['animal_id'].tolist()
                feed_list = st.session_state.feed_inventory['feed_name'].tolist()
                selected_animal = st.selectbox("Animal", animal_list)
                selected_feed = st.selectbox("Feed", feed_list)
                cons_qty = st.number_input("Quantity (kg)", min_value=0.0, step=0.1)
                cons_date = st.date_input("Date", value=datetime.now().date())

                if st.button("Record Consumption", type="primary"):
                    new = {
                        "consumption_id": f"c-{len(st.session_state.feed_consumption)+1}",
                        "date": pd.to_datetime(cons_date),
                        "animal_id": selected_animal,
                        "feed_name": selected_feed,
                        "quantity_kg": cons_qty,
                        "notes": ""
                    }
                    st.session_state.feed_consumption = pd.concat([st.session_state.feed_consumption, pd.DataFrame([new])], ignore_index=True)
                    st.success("Consumption recorded.")
            else:
                st.info("Add feed inventory and animals to record consumption.")

        with col2:
            st.markdown("##### Today's Summary")
            if not st.session_state.feed_consumption.empty:
                today = pd.to_datetime(datetime.now().date())
                summary = st.session_state.feed_consumption[pd.to_datetime(st.session_state.feed_consumption['date']) == today]
                st.dataframe(summary, use_container_width=True)
            else:
                st.info("No consumption recorded today.")

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
            fig2 = px.bar(
                feed_type_consumption,
                x='feed_name',
                y='quantity_kg',
                title='Consumption by Feed Type',
                labels={'quantity_kg': 'Total Consumed (kg)', 'feed_name': 'Feed Type'}
            )
            st.plotly_chart(fig2, use_container_width=True)

            if not st.session_state.milk_records.empty:
                st.markdown("Feed vs Milk correlation: (simple totals)")
                total_feed = consumption_df['quantity_kg'].sum()
                total_milk = st.session_state.milk_records['yield_litres'].sum() if not st.session_state.milk_records.empty else 0
                st.write(f"Total feed (kg): {total_feed:.2f}, Total milk (L): {total_milk:.2f}")
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
                animal_list = st.session_state.animals['animal_id'].tolist()
                h_animal = st.selectbox("Animal", animal_list)
                h_date = st.date_input("Date", value=datetime.now().date())
                issue = st.text_input("Issue/Diagnosis")
                treatment = st.text_area("Treatment / Medicines")
                vet = st.text_input("Vet / Responsible")

                if st.button("Add Health Record", type="primary"):
                    new = {
                        "record_id": f"h-{len(st.session_state.health_records)+1}",
                        "animal_id": h_animal,
                        "date": pd.to_datetime(h_date),
                        "issue": issue,
                        "treatment": treatment,
                        "vet": vet,
                        "notes": ""
                    }
                    st.session_state.health_records = pd.concat([st.session_state.health_records, pd.DataFrame([new])], ignore_index=True)
                    st.success("Health record added.")
            else:
                st.info("Please add animals first.")

        with col2:
            st.markdown("##### Upcoming Due")
            st.info("No scheduled vaccinations tracked in demo mode.")

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
                med_name = st.text_input("Medicine Name")
            with col_b:
                med_qty = st.number_input("Quantity", min_value=0.0, step=1.0)
            with col_c:
                med_unit = st.text_input("Unit", value="units")

            col_d, col_e = st.columns(2)
            with col_d:
                expiry = st.date_input("Expiry Date", value=datetime.now().date())
            with col_e:
                batch = st.text_input("Batch / Supplier")

            medicine_notes = st.text_area("Notes", key="medicine_notes")

            if st.button("Add Medicine", type="primary"):
                new = {
                    "medicine_id": f"med-{len(st.session_state.medicine_inventory)+1}",
                    "name": med_name,
                    "quantity": med_qty,
                    "unit": med_unit,
                    "expiry_date": pd.to_datetime(expiry),
                    "notes": medicine_notes
                }
                st.session_state.medicine_inventory = pd.concat([st.session_state.medicine_inventory, pd.DataFrame([new])], ignore_index=True)
                st.success("Medicine added.")

        with col2:
            st.markdown("##### Alerts")
            if not st.session_state.medicine_inventory.empty:
                soon = pd.to_datetime(datetime.now().date() + timedelta(days=30))
                expiring = st.session_state.medicine_inventory[
                    pd.to_datetime(st.session_state.medicine_inventory['expiry_date']) <= soon
                ]
                st.dataframe(expiring, use_container_width=True)
            else:
                st.info("No medicines in inventory.")

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
                counts = health_df.groupby('issue').size().reset_index(name='count').sort_values('count', ascending=False).head(10)
                st.markdown("#### Top Issues")
                st.dataframe(counts, use_container_width=True)

            with col2:
                st.markdown("#### Recent Treatments")
                st.dataframe(health_df.sort_values('date', ascending=False).head(10), use_container_width=True)

            st.markdown("#### Health Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Records", len(health_df))
            with col2:
                st.metric("Unique Issues", health_df['issue'].nunique())
            with col3:
                st.metric("Animals treated", health_df['animal_id'].nunique())
            with col4:
                st.metric("Last record", str(health_df['date'].max().date()))
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
                w_name = st.text_input("Name")
            with col_b:
                w_role = st.text_input("Role")
            with col_c:
                w_wage = st.number_input("Wage (₹)", min_value=0.0, step=1.0)

            if st.button("Add Worker", type="primary"):
                new = {
                    "worker_id": f"w-{len(st.session_state.labour_records)+1}",
                    "name": w_name,
                    "role": w_role,
                    "wage": w_wage,
                    "notes": ""
                }
                st.session_state.labour_records = pd.concat([st.session_state.labour_records, pd.DataFrame([new])], ignore_index=True)
                st.success("Worker added.")

        with col2:
            st.markdown("##### Summary")
            if not st.session_state.labour_records.empty:
                st.metric("Total Workers", len(st.session_state.labour_records))
            else:
                st.info("No workers registered.")

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
                worker_list = st.session_state.labour_records['worker_id'].tolist()
                a_date = st.date_input("Date", value=datetime.now().date())
                sel_worker = st.selectbox("Worker", worker_list)
                present = st.checkbox("Present", value=True)

                if st.button("Mark Attendance", type="primary"):
                    new = {
                        "attendance_id": f"a-{len(st.session_state.attendance)+1}",
                        "date": pd.to_datetime(a_date),
                        "worker_id": sel_worker,
                        "present": int(bool(present)),
                        "notes": ""
                    }
                    st.session_state.attendance = pd.concat([st.session_state.attendance, pd.DataFrame([new])], ignore_index=True)
                    st.success("Attendance recorded.")
            else:
                st.info("Add workers first.")

        with col2:
            st.markdown("##### Today's Summary")
            if not st.session_state.attendance.empty:
                today = pd.to_datetime(datetime.now().date())
                summary = st.session_state.attendance[pd.to_datetime(st.session_state.attendance['date']) == today]
                st.dataframe(summary, use_container_width=True)
            else:
                st.info("No attendance recorded today.")

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
                avg_wage = st.session_state.labour_records['wage'].mean()
                st.metric("Avg Wage", f"₹{avg_wage:.2f}")
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
                eq_name = st.text_input("Equipment Name")
            with col_b:
                purchase = st.date_input("Purchase Date", value=datetime.now().date())
            with col_c:
                cost = st.number_input("Cost (₹)", min_value=0.0, step=1.0)

            equipment_notes = st.text_area("Notes / Specifications", key="equipment_notes")

            if st.button("Add Equipment", type="primary"):
                new = {
                    "equipment_id": f"e-{len(st.session_state.equipment)+1}",
                    "name": eq_name,
                    "purchase_date": pd.to_datetime(purchase),
                    "cost": cost,
                    "status": "Operational",
                    "notes": equipment_notes
                }
                st.session_state.equipment = pd.concat([st.session_state.equipment, pd.DataFrame([new])], ignore_index=True)
                st.success("Equipment added.")

        with col2:
            st.markdown("##### Summary")
            if not st.session_state.equipment.empty:
                st.metric("Total Equipment", len(st.session_state.equipment))
            else:
                st.info("No equipment registered.")

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
                equip_list = st.session_state.equipment['equipment_id'].tolist()
                sel_e = st.selectbox("Equipment", equip_list)
                m_date = st.date_input("Date", value=datetime.now().date())
                desc = st.text_area("Description")
                m_cost = st.number_input("Cost (₹)", min_value=0.0, step=1.0)

                if st.button("Add Maintenance Record", type="primary"):
                    new = {
                        "maintenance_id": f"m-{len(st.session_state.equipment_maintenance)+1}",
                        "equipment_id": sel_e,
                        "date": pd.to_datetime(m_date),
                        "description": desc,
                        "cost": m_cost,
                        "notes": ""
                    }
                    st.session_state.equipment_maintenance = pd.concat([st.session_state.equipment_maintenance, pd.DataFrame([new])], ignore_index=True)
                    st.success("Maintenance record added.")
            else:
                st.info("No equipment to log maintenance for.")

        with col2:
            st.markdown("##### This Month")
            if not st.session_state.equipment_maintenance.empty:
                this_month = pd.to_datetime(datetime.now().date()).to_period("M")
                maint = st.session_state.equipment_maintenance
                maint['period'] = pd.to_datetime(maint['date']).dt.to_period("M")
                st.dataframe(maint[maint['period'] == this_month], use_container_width=True)
            else:
                st.info("No maintenance records.")

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
                st.markdown("Top maintenance costs")
                top = maint_df.groupby('equipment_id')['cost'].sum().reset_index().sort_values('cost', ascending=False).head(10)
                st.dataframe(top, use_container_width=True)

            with col2:
                st.markdown("Monthly cost trend")

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

        with col2:
            subcategory = st.text_input("Subcategory")
            amount = st.number_input("Amount (₹)*", min_value=0.0, step=10.0)
            reference_id = st.text_input("Reference ID", placeholder="Animal ID, Worker ID, etc.")

        description = st.text_area("Description*")
        transaction_notes = st.text_area("Notes", key="transaction_notes")

        if st.button("Add Transaction", type="primary"):
            if amount > 0 and description:
                new = {
                    "transaction_id": f"t-{len(st.session_state.financial_transactions)+1}",
                    "date": pd.to_datetime(transaction_date),
                    "type": transaction_type,
                    "subcategory": subcategory,
                    "amount": float(amount),
                    "reference_id": reference_id,
                    "description": description,
                    "notes": transaction_notes
                }
                st.session_state.financial_transactions = pd.concat([st.session_state.financial_transactions, pd.DataFrame([new])], ignore_index=True)
                st.success("Transaction recorded.")
            else:
                st.error("Amount and description are required.")

    with tab2:
        st.subheader("Transaction History")

        if not st.session_state.financial_transactions.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                date_from = st.date_input("From", value=(datetime.now() - timedelta(days=30)).date())
            with col2:
                date_to = st.date_input("To", value=datetime.now().date())
            with col3:
                filter_type = st.multiselect("Type", ["Income", "Expense"], default=["Income", "Expense"])

            filtered = st.session_state.financial_transactions[
                (pd.to_datetime(st.session_state.financial_transactions['date']) >= pd.to_datetime(date_from)) &
                (pd.to_datetime(st.session_state.financial_transactions['date']) <= pd.to_datetime(date_to)) &
                (st.session_state.financial_transactions['type'].isin(filter_type))
            ]

            if not filtered.empty:
                st.dataframe(filtered, use_container_width=True)
            else:
                st.info("No transactions in the selected range.")
        else:
            st.info("No transactions recorded yet")

    with tab3:
        st.subheader("Financial Reports")

        if not st.session_state.financial_transactions.empty:
            trans_df = st.session_state.financial_transactions.copy()
            trans_df['date'] = pd.to_datetime(trans_df['date'])
            st.dataframe(trans_df.tail(50), use_container_width=True)
        else:
            st.info("No transactions to report.")

    with tab4:
        st.subheader("Profit & Loss Statement")

        if not st.session_state.financial_transactions.empty:
            trans = st.session_state.financial_transactions
            income = trans[trans['type'] == 'Income']['amount'].sum()
            expense = trans[trans['type'] == 'Expense']['amount'].sum()
            st.metric("Total Income", f"₹{income:.2f}")
            st.metric("Total Expense", f"₹{expense:.2f}")
            st.metric("Net", f"₹{(income - expense):.2f}")
        else:
            st.info("No financial data.")


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
            milk = st.session_state.milk_records.copy()
            milk['date'] = pd.to_datetime(milk['date'])
            prod = milk.groupby('animal_id')['yield_litres'].sum().reset_index().sort_values('yield_litres', ascending=False)
            st.dataframe(prod, use_container_width=True)
        else:
            st.info("Need animal and milk records to produce this report.")

    elif report_type == "Calving History & Expected Deliveries":
        st.subheader("Calving History & Expected Deliveries")

        if not st.session_state.breeding_records.empty:
            st.dataframe(st.session_state.breeding_records, use_container_width=True)
        else:
            st.info("No breeding records yet.")

    elif report_type == "Feed Efficiency Analysis":
        st.subheader("Feed Efficiency Analysis")

        if not st.session_state.feed_consumption.empty and not st.session_state.milk_records.empty:
            st.info("Basic feed efficiency: total milk / total feed")
            total_feed = st.session_state.feed_consumption['quantity_kg'].sum()
            total_milk = st.session_state.milk_records['yield_litres'].sum()
            if total_feed > 0:
                st.write(f"Efficiency: {total_milk / total_feed:.3f} L/kg")
            else:
                st.info("No feed consumption data.")
        else:
            st.info("Need feed consumption and milk records.")

    elif report_type == "Labour Cost Breakdown":
        st.subheader("Labour Cost Breakdown")

        if not st.session_state.attendance.empty and not st.session_state.labour_records.empty:
            st.write("Simple summary by worker (demo)")
            merged = st.session_state.attendance.merge(st.session_state.labour_records, left_on='worker_id', right_on='worker_id', how='left')
            merged['present'] = merged['present'].astype(int)
            cost = merged.groupby('worker_id')['present'].sum().reset_index()
            cost = cost.merge(st.session_state.labour_records[['worker_id', 'wage']], on='worker_id', how='left')
            cost['estimated_cost'] = cost['present'] * cost['wage']
            st.dataframe(cost, use_container_width=True)
        else:
            st.info("Need attendance and labour records.")

    elif report_type == "Annual Herd Health Summary":
        st.subheader("Annual Herd Health Summary")

        if not st.session_state.health_records.empty:
            h = st.session_state.health_records.copy()
            h['date'] = pd.to_datetime(h['date'])
            h['year'] = h['date'].dt.year
            summary = h.groupby('year').size().reset_index(name='records')
            st.dataframe(summary, use_container_width=True)
        else:
            st.info("No health records available.")

    elif report_type == "Asset Summary":
        st.subheader("Asset Summary Report")

        st.markdown("#### Animals")
        if not st.session_state.animals.empty:
            st.metric("Total Animals", len(st.session_state.animals))
        else:
            st.info("No animals.")

        st.markdown("---")

        st.markdown("#### Equipment")
        if not st.session_state.equipment.empty:
            st.metric("Total Equipment", len(st.session_state.equipment))
        else:
            st.info("No equipment.")

        st.markdown("---")

        st.markdown("#### Financial Summary")
        if not st.session_state.financial_transactions.empty:
            trans = st.session_state.financial_transactions
            income = trans[trans['type'] == 'Income']['amount'].sum()
            expense = trans[trans['type'] == 'Expense']['amount'].sum()
            st.write(f"Income ₹{income:.2f}, Expense ₹{expense:.2f}, Net ₹{income - expense:.2f}")
        else:
            st.info("No financial transactions.")

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
            st.metric("Animals", len(st.session_state.animals))
        else:
            st.metric("Animals", 0)

    with col2:
        if not st.session_state.milk_records.empty:
            total_milk = st.session_state.milk_records['yield_litres'].sum()
            st.metric("Total Milk (L)", f"{total_milk:.2f}")
        else:
            st.metric("Total Milk (L)", "0.00")

    with col3:
        if not st.session_state.labour_records.empty:
            st.metric("Workers", len(st.session_state.labour_records))
        else:
            st.metric("Workers", 0)

    with col4:
        if not st.session_state.equipment.empty:
            st.metric("Equipment", len(st.session_state.equipment))
        else:
            st.metric("Equipment", 0)

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["Dairy Dashboard", "Financial Dashboard", "Health Dashboard", "Farm Dashboard"])

    with tab1:
        st.subheader("Dairy Operations")
        if not st.session_state.milk_records.empty:
            milk_df = st.session_state.milk_records.copy()
            milk_df['date'] = pd.to_datetime(milk_df['date']).dt.date
            daily = milk_df.groupby('date')['yield_litres'].sum().reset_index()
            st.dataframe(daily.tail(14), use_container_width=True)
        else:
            st.info("No milk data.")

    with tab2:
        st.subheader("Financial Overview")
        if not st.session_state.financial_transactions.empty:
            trans = st.session_state.financial_transactions.copy()
            income = trans[trans['type'] == 'Income']['amount'].sum()
            expense = trans[trans['type'] == 'Expense']['amount'].sum()
            st.metric("Income", f"₹{income:.2f}")
            st.metric("Expense", f"₹{expense:.2f}")
        else:
            st.info("No financial data.")

    with tab3:
        st.subheader("Health Overview")
        if not st.session_state.health_records.empty:
            st.metric("Health Records", len(st.session_state.health_records))
        else:
            st.info("No health records.")

    with tab4:
        st.subheader("Farm Operations")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Feed Inventory")
            if not st.session_state.feed_inventory.empty:
                st.metric("Feed types", len(st.session_state.feed_inventory))
            else:
                st.info("No feed inventory.")
        with col2:
            st.markdown("Cultivation")
            if not st.session_state.fodder_cultivation.empty:
                st.metric("Planted plots", len(st.session_state.fodder_cultivation))
            else:
                st.info("No cultivation records.")

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
# ...existing code...