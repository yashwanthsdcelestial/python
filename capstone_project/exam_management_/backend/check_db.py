from sqlalchemy import create_engine, inspect
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
inspector = inspect(engine)

print("Existing tables:")
for table in inspector.get_table_names():
    print(f"\n{table}:")
    cols = inspector.get_columns(table)
    for col in cols:
        print(f"  - {col['name']}: {col['type']}")
