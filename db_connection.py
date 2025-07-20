from pathlib import Path
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

file_config = Path(__file__).parent.joinpath('db.ini')
config = ConfigParser()
config.read(file_config)

user = config.get('POSTGRES_DB', 'USER')
password = config.get('POSTGRES_DB', 'PASSWORD')
host = config.get('POSTGRES_DB', 'HOST')
port = config.get('POSTGRES_DB', 'PORT')
db = config.get('POSTGRES_DB', 'DB_NAME')

URI = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(URI, echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# if __name__ == '__main__':
#     from sqlalchemy import text
#     try:
#         result = session.execute(text("SELECT 1"))
#         print("Сесія активна:", result.scalar() == 1)
#     except Exception as e:
#         print("Не вдалося виконати запит через сесію:", e)