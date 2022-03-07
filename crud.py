from sqlalchemy import create_engine
from config import DATABASE_URI
from models import db

engine = create_engine(DATABASE_URI)

# db.metadata.drop_all(engine)
# db.metadata.create_all(engine)

