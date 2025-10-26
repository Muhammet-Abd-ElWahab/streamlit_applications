# Installation and Setup Guide

## Prerequisites
- Python 3.8 or higher
- PostgreSQL database server running
- Access to the PostgreSQL database with credentials

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- psycopg2-binary (PostgreSQL driver)
- streamlit
- pandas, numpy, plotly
- All other required packages

## Step 2: Configure Database Connection

Edit `.streamlit/secrets.toml` with your PostgreSQL credentials:

```toml
dbname = 'your_database_name'
dbusername = 'your_username'
password = "your_password"
host = "your_host_ip"
port = '5432'
```

**Current Configuration:**
- dbname = 'sdf'
- dbusername = 'sdf'
- password = "sdfsdf"
- host = "192.168.1.11"
- port = '5432'

## Step 3: Setup Database Schema

Run the provided database insertion script to create tables and populate with sample data:

```bash
python database_insertion_script.py
```

This will create all necessary tables:
- patients
- blood_test
- hormonal_test
- tumor_marks
- mutation_analysis
- clinical_notes
- And other supporting tables

## Step 4: Run the Application

```bash
streamlit run 1_⛪Home.py
```

The application will be available at: `http://localhost:8501`

## Step 5: Login

Use the credentials configured in `.streamlit/secrets.toml` under `[credentials]` section.

Example users:
- **Mohamed**: muhammetgamal5@gmail.com
- **Hamza**: mah.mo.hamza@gmail.com
- **Menna**: menna.radwan@dataclin.com
- **Yasmin**: yasmin.zahran@dataclin.com
- **Abeer**: abeermahmoud739@gmail.com

## Troubleshooting

### Connection Issues
If you see connection errors:
1. Verify PostgreSQL is running
2. Check firewall settings allow connection to port 5432
3. Verify credentials in secrets.toml
4. Ensure database exists

### Import Errors
If you see import errors:
```bash
pip install --upgrade -r requirements.txt
```

### Database Schema Issues
If tables don't exist:
1. Run the database insertion script
2. Or manually create tables using the schema from the script

## Database Schema Notes

The application expects these table names:
- `patients` (not `Patient_Information`)
- `blood_test` (not `Blood_Test`)
- `hormonal_test` (not `Hormonal_Test`)
- `tumor_marks` (not `Tumor_Marks`)
- `mutation_analysis` (not `Mutation_Analysis`)

Make sure your database schema matches these table names.

## Performance Tips

1. **Connection Pooling**: The application uses connection pooling (1-10 connections)
2. **Caching**: Streamlit caching is enabled for data fetching
3. **Indexes**: Ensure proper indexes on frequently queried columns (patient_id, test_date, etc.)

## Security Notes

1. Never commit `.streamlit/secrets.toml` to version control
2. Use strong passwords for database access
3. Restrict database access to specific IP addresses
4. Use SSL/TLS for database connections in production

## Support

For issues or questions, refer to:
- MIGRATION_SUMMARY.md for technical details
- Database insertion script for schema reference
