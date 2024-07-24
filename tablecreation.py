from sqlalchemy import create_engine,MetaData,Table,Integer,String,Text,Column

# database detail 

server = 'airlineserver14.database.windows.net'
database = 'airlinedatabase'
username = 'airlineadmin'
password = 'Airline@14'
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

con = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")

metadata = MetaData()

airlinetable = Table('airlinetable', metadata,
    Column('id', Integer, primary_key=True),
    Column('recorded_date', String(255)),
    Column('title', String(255)),
    Column('review_date', String(255)),
    Column('country', String(255)),
    Column('review', Text),
    Column('rating', String(255)),
    Column('aircraft', String(255)),
    Column('type_of_traveller', String(255)),
    Column('seat_type', String(255)),
    Column('route', String(255)),
    Column('date_flown', String(255)),
    Column('seat_comfort', String(255)),
    Column('cabin_staff_service', String(255)),
    Column('food_beverages', String(255)),
    Column('inflight_entertainment', String(255)),
    Column('ground_service', String(255)),
    Column('value_for_money', String(255)),
    Column('recommended', String(255)),
    Column('wifi_connectivity', String(255))
)

metadata.create_all(con)