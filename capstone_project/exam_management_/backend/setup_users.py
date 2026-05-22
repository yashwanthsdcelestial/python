from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.security import get_password_hash

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    # Create users table
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL DEFAULT 'student',
        is_active BOOLEAN DEFAULT true,
        is_deleted BOOLEAN DEFAULT false,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    )
    """))
    conn.commit()
    
    # Check if users table is empty
    result = conn.execute(text("SELECT COUNT(*) FROM users"))
    count = result.scalar()
    
    if count == 0:
        # Insert sample users
        users_data = [
            ("admin@examportal.com", "Admin@1234", "Alice Admin", "admin"),
            ("proctor@examportal.com", "Admin@1234", "Bob Proctor", "admin"),
            ("student1@example.com", "Student@1234", "Charlie Brown", "student"),
            ("student2@example.com", "Student@1234", "Diana Prince", "student"),
            ("student3@example.com", "Student@1234", "Eve Johnson", "student"),
        ]
        
        for email, password, full_name, role in users_data:
            hashed = get_password_hash(password)
            conn.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, role, is_active, is_deleted)
            VALUES (:email, :hashed, :full_name, :role, true, false)
            """), {
                "email": email,
                "hashed": hashed,
                "full_name": full_name,
                "role": role
            })
        conn.commit()
        print("✅ Users table created and populated with sample data!")
    else:
        print(f"✅ Users table already has {count} users")

print("Database setup complete")
