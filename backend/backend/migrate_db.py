from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres.nbninvjhxuvizrderppe:SportsDB123987654@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL)

def run_migration():
    with engine.connect() as conn:
        print("Running migration to add captain_id...")
        try:
            conn.execute(text("ALTER TABLE teams ADD COLUMN IF NOT EXISTS captain_id VARCHAR;"))
            conn.commit()
            print("Successfully added captain_id column to teams table.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_migration()
