#!/usr/bin/env python3
"""
Database Connection Test Script
Tests PostgreSQL connection and shows available tables and columns
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

# Database connection parameters from secrets
DB_CONFIG = {
    'dbname': st.secrets['dbname'],
    'user': st.secrets['dbusername'],
    'password': st.secrets['password'],
    'host': st.secrets['host'],
    'port': st.secrets['port']
}

def test_connection():
    """Test database connection and show available tables"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Successfully connected to PostgreSQL database!")
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get all tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cur.fetchall()
        
        print(f"\n📊 Found {len(tables)} tables in database '{DB_CONFIG['dbname']}':\n")
        
        for table in tables:
            table_name = table['table_name']
            print(f"  📋 Table: {table_name}")
            
            # Get columns for this table
            cur.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position;
            """)
            
            columns = cur.fetchall()
            for col in columns:
                print(f"      - {col['column_name']} ({col['data_type']})")
            
            # Get row count
            cur.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cur.fetchone()['count']
            print(f"      → {count} rows\n")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("  PostgreSQL Database Connection Test")
    print("=" * 70)
    print(f"\nConnecting to:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Port: {DB_CONFIG['port']}")
    print(f"  Database: {DB_CONFIG['dbname']}")
    print(f"  User: {DB_CONFIG['user']}")
    print("\n" + "=" * 70 + "\n")
    
    test_connection()
    
    print("=" * 70)
    print("  Test Complete")
    print("=" * 70)
