# 🧹 Data Cleaning & Exploration Tool

A comprehensive Streamlit application for data upload, cleaning, and exploration. This tool enables users to upload various file formats, perform data cleaning operations, and export cleaned datasets.

## ✨ Features

### 📁 File Upload Support
- **CSV/TSV Files**: Automatic delimiter detection with manual override option
- **Excel Files**: Multi-sheet support with preview functionality
- **SAS Files**: Native .sas7bdat file support
- Intelligent file format detection
- Error handling for corrupted or invalid files

### 📊 Data Exploration
- **Show Data Tab**: 
  - Customizable row display
  - Column data types overview
  - Memory usage statistics
  - Basic statistical summaries
  - DataFrame info display

- **Value Counts Tab**:
  - Distribution analysis for any column
  - Count and percentage calculations
  - Visual bar charts for categorical data
  - Unique value metrics

### 🧹 Data Cleaning Operations

#### 🔍 Duplicate Detection
- Check duplicates across all columns or specific columns
- Visual metrics showing duplicate counts and percentages
- One-click duplicate removal
- Preview duplicate rows before removal

#### 🔍 Null Value Handling
- Overall null statistics across dataset
- Column-specific null analysis
- Visual progress bars for null percentages
- Two handling options:
  - **Remove Rows**: Delete rows with null values
  - **Replace Nulls**: Fill nulls with custom values
- Before/after comparison

#### ✏️ Data Editing
- Column-specific value replacement
- Multi-value selection for batch replacement
- Preview affected rows before changes
- Value distribution context
- Automatic type conversion

### 💾 Export Options
- **CSV Export**: Multiple encoding options (UTF-8, Latin1, etc.)
- **Excel Export**: .xlsx format with proper formatting
- **SAS Export**: .sas7bdat format
- Automatic timestamp in filenames
- Current dataset metrics before download

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the repository**
```bash
cd Data_Cleaning_App
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📦 Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file handling
- **pyreadstat**: SAS file reading/writing
- **xlrd**: Legacy Excel file support

## 🎯 Usage Guide

### 1. Upload Your Data
1. Click the file uploader in the sidebar
2. Select your file (CSV, TSV, Excel, or SAS)
3. For CSV/TSV: Choose or confirm the delimiter
4. For Excel: Select the sheet you want to load
5. Click "Load File" or "Load Sheet"

### 2. Explore Your Data
- Navigate to **Show Data** tab to view your dataset
- Use **Value Counts** tab to analyze column distributions
- Adjust display settings (rows, columns) as needed

### 3. Clean Your Data

#### Remove Duplicates
1. Go to **Check Duplicates** tab
2. Optionally select specific columns to check
3. Review duplicate metrics and rows
4. Click "Remove Duplicates" to clean

#### Handle Null Values
1. Go to **Check Nulls** tab
2. Select a column to analyze
3. Choose an action:
   - Remove rows with nulls
   - Replace nulls with a custom value
4. Execute the action

#### Edit Values
1. Go to **Edit Data** tab
2. Select the column to edit
3. Choose values to replace (multi-select)
4. Enter the new replacement value
5. Preview affected rows
6. Click "Replace Values"

### 4. Download Cleaned Data
1. Review current dataset metrics in sidebar
2. Choose your preferred format:
   - CSV (select encoding)
   - Excel
   - SAS
3. Click the download button
4. File will be saved with timestamp

## 🎨 User Interface

### Layout
- **Sidebar**: File upload and download options
- **Main Area**: Tabbed interface for different operations
- **Metrics**: Visual cards showing key statistics
- **Expanders**: Collapsible sections for detailed information

### Visual Elements
- 📊 Metrics with delta indicators
- 📈 Progress bars for percentages
- 🎯 Color-coded status messages
- 📋 Expandable data type information
- 👁️ Preview sections for data inspection

## 🔧 Technical Details

### Session State Management
The application uses Streamlit's session state to:
- Persist DataFrame across tab switches
- Maintain original dataset for reference
- Track file information
- Enable undo functionality (future enhancement)

### Custom Functions

#### `show_df(df, title, n_rows, show_all_cols)`
Displays DataFrames with:
- Shape metrics (rows, columns, memory)
- Column data types in expandable section
- Configurable row display
- Null count per column

#### `load_file(uploaded_file, delimiter, sheet_name)`
Handles file loading with:
- Format detection
- Error handling
- Appropriate pandas readers
- Return None on failure

#### `detect_delimiter(file_content, filename)`
Intelligently detects CSV/TSV delimiters by:
- Checking file extension
- Analyzing first line
- Counting delimiter occurrences

### Error Handling
- Try-except blocks around file operations
- User-friendly error messages
- Validation before destructive operations
- Graceful handling of edge cases

## 📊 Supported File Formats

| Format | Extensions | Features |
|--------|-----------|----------|
| CSV | .csv, .txt | Delimiter detection, encoding selection |
| TSV | .tsv | Tab delimiter support |
| Excel | .xlsx, .xls | Multi-sheet, preview, openpyxl engine |
| SAS | .sas7bdat | Native read/write support |

## ⚡ Performance Considerations

- Configurable row display limits for large datasets
- Lazy loading of data previews
- Efficient pandas operations
- Memory usage monitoring
- Warning messages for large files

## 🐛 Troubleshooting

### Common Issues

**File won't upload:**
- Check file format is supported
- Ensure file is not corrupted
- Try different encoding for CSV files

**Excel sheet not loading:**
- Verify Excel file is not password-protected
- Check if file is in .xlsx or .xls format
- Ensure openpyxl is installed

**SAS file errors:**
- Confirm pyreadstat is properly installed
- Check SAS file version compatibility
- Verify file is not compressed

**Memory errors with large files:**
- Reduce number of displayed rows
- Close other applications
- Consider processing file in chunks

## 🔮 Future Enhancements

- [ ] Undo/Redo functionality
- [ ] Data type conversion tools
- [ ] Column renaming interface
- [ ] Advanced visualizations (histograms, scatter plots)
- [ ] Data cleaning report export
- [ ] Batch operations
- [ ] Custom transformation scripts
- [ ] Data validation rules
- [ ] Column statistics comparison
- [ ] Export cleaning history log

## 📝 Best Practices

1. **Always preview** data before loading (especially Excel sheets)
2. **Check duplicates** before other cleaning operations
3. **Handle nulls** strategically based on your analysis needs
4. **Preview changes** before executing replacements
5. **Download frequently** to save intermediate results
6. **Use appropriate encodings** for international characters

## 🤝 Contributing

Suggestions and improvements are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- Functions include docstrings
- Error handling is comprehensive
- UI remains intuitive and responsive

## 📄 License

This project is open source and available for educational and commercial use.

## 👨‍💻 Author

Created as a comprehensive data cleaning solution for data scientists and analysts.

## 🙏 Acknowledgments

Built with:
- Streamlit for the web framework
- Pandas for data manipulation
- The open-source Python community

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Python Version**: 3.8+
