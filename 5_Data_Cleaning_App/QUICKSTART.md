# 🚀 Quick Start Guide

## Installation (2 minutes)

```bash
# Navigate to the app directory
cd Data_Cleaning_App

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## First Use (5 minutes)

### Step 1: Upload Data
1. Look at the **left sidebar**
2. Click **"Browse files"** under "File Upload"
3. Select your CSV, Excel, or SAS file
4. For Excel: Choose the sheet you want
5. Click **"Load File"** or **"Load Sheet"**

### Step 2: Explore Your Data
1. Click the **"📊 Show Data"** tab
2. Adjust how many rows to display
3. View column types by expanding "Column Data Types"
4. Check basic statistics at the bottom

### Step 3: Clean Your Data

#### Remove Duplicates
- Go to **"🔍 Check Duplicates"** tab
- See how many duplicates exist
- Click **"Remove Duplicates"** button

#### Handle Missing Values
- Go to **"🔍 Check Nulls"** tab
- Select a column with null values
- Choose to either:
  - Remove rows with nulls
  - Replace nulls with a value

#### Edit Values
- Go to **"✏️ Edit Data"** tab
- Select column to edit
- Choose values to replace
- Enter new value
- Click **"Replace Values"**

### Step 4: Download Clean Data
1. Look at the **left sidebar** (scroll down)
2. Choose format: CSV, Excel, or SAS
3. Click the download button
4. Your file is saved with a timestamp!

## 💡 Pro Tips

- **Preview Excel sheets** before loading to save time
- **Check duplicates first** before other cleaning operations
- **Use Value Counts** to understand your data distribution
- **Download frequently** to save your progress
- **Multi-select columns** in duplicate check for specific analysis

## 🎯 Common Workflows

### Workflow 1: Basic Cleaning
1. Upload file
2. Check duplicates → Remove
3. Check nulls → Handle
4. Download clean file

### Workflow 2: Value Standardization
1. Upload file
2. Go to Value Counts tab
3. Identify inconsistent values
4. Use Edit Data to standardize
5. Download

### Workflow 3: Column-Specific Cleaning
1. Upload file
2. Check Nulls tab → Select column
3. Remove or replace nulls
4. Edit Data tab → Replace values
5. Download

## ⚠️ Important Notes

- **File size limit**: 200MB (configurable)
- **Supported formats**: CSV, TSV, Excel (.xlsx, .xls), SAS (.sas7bdat)
- **Changes persist** across tabs during your session
- **Download early and often** - no auto-save feature

## 🆘 Need Help?

- Check the full README.md for detailed documentation
- Error messages are shown in red at the top
- Success messages are shown in green
- Info messages are shown in blue

## 🎨 Interface Guide

### Sidebar (Left)
- File upload controls
- Download options
- Current dataset info

### Main Area (Center)
- Tabs for different operations
- Data display and metrics
- Action buttons

### Metrics (Cards)
- Show key statistics
- Green arrow = good
- Red arrow = needs attention

---

**Ready to start?** Run `streamlit run app.py` and open your browser! 🎉
