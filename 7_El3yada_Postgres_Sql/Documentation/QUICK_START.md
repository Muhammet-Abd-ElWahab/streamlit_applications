# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Create Database
```bash
cd Documentation
bash Create_DB.sh
```
Follow the prompts to create your database.

### Step 2: Insert Sample Data
```bash
python insert_sample_data.py
```
Answer "yes" to truncate tables (if this is first time).

### Step 3: Run Application
```bash
streamlit run 1_⛪Home.py
```

## 📊 What You Get

- **50 Patients** (IDs: P001 to P050)
- **100 Blood Tests** with JSONB results
- **80 Hormonal Tests** with detailed hormone levels
- **60 Tumor Marker Tests** for breast cancer
- **40 Mutation Analyses** for CML
- **150 Clinical Notes** with visit records

## 🔧 Configuration

Edit `.streamlit/secrets.toml`:
```toml
dbname = 'el3yada'
dbusername = 'postgres'
password = "mgamal"
host = "192.168.3.31"
port = '5432'
```

## ✅ Verify Setup

### Check Database
```bash
streamlit run test_db_connection.py
```

### Check Application
1. Open Lab Profile page
2. Click "🔍 Debug: Database Connection Info"
3. Verify all tables have data

## 📝 Key Changes

| Item | Old | New |
|------|-----|-----|
| Patient ID Type | INTEGER | TEXT (P001, P002, etc.) |
| Blood Test Storage | Separate columns | JSONB |
| Auto-increment IDs | Manual | SERIAL/BIGSERIAL |

## 🆘 Troubleshooting

**No data showing?**
```bash
python insert_sample_data.py
```

**Connection error?**
- Check secrets.toml credentials
- Verify PostgreSQL is running
- Check firewall settings

**Column errors?**
- Recreate database with Create_DB.sh
- Run insert_sample_data.py again

## 📚 Documentation

- `NEW_DATABASE_SETUP.md` - Complete setup guide
- `TROUBLESHOOTING.md` - Detailed troubleshooting
- `TABLE_MAPPING.md` - Schema reference
- `BUGFIXES_SUMMARY.md` - All fixes applied

## 🎯 Quick Commands

```bash
# Create database
bash Documentation/Create_DB.sh

# Insert data
python insert_sample_data.py

# Test connection
streamlit run test_db_connection.py

# Run app
streamlit run 1_⛪Home.py

# Check PostgreSQL status
sudo systemctl status postgresql

# Access PostgreSQL
psql -U postgres -d el3yada
```

## 💡 Tips

1. **First time setup**: Always truncate tables when inserting data
2. **Patient IDs**: Use format P001, P002, etc. (TEXT type)
3. **Debug panel**: Use it in Lab Profile to check data status
4. **Backup**: Run `pg_dump` before major changes

## ✨ Features

- ✅ Connection pooling for performance
- ✅ JSONB for flexible blood test results
- ✅ TEXT patient IDs for readability
- ✅ Comprehensive error handling
- ✅ Debug tools built-in
- ✅ Sample data generator
- ✅ All tables indexed

## 🎉 You're Ready!

Your application is fully configured and ready to use with the new database schema!
