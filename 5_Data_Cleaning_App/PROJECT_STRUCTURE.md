# 📁 Project Structure

## Directory Layout

```
Data_Cleaning_App/
│
├── .streamlit/
│   └── config.toml              # Streamlit configuration (theme, server settings)
│
├── app.py                        # Main application file (27KB)
├── requirements.txt              # Python dependencies
├── sample_data.csv              # Sample dataset for testing
│
├── README.md                     # Comprehensive documentation
├── QUICKSTART.md                # Quick start guide for new users
├── TESTING_GUIDE.md             # Complete testing checklist
├── CHANGELOG.md                 # Version history and updates
├── PROJECT_STRUCTURE.md         # This file
│
└── .gitignore                   # Git ignore rules
```

## 📄 File Descriptions

### Core Application Files

#### `app.py` (Main Application)
**Size**: ~27KB | **Lines**: ~800

**Structure**:
```python
# Configuration
- st.set_page_config()

# Custom Functions
- show_df()              # Display DataFrames with formatting
- detect_delimiter()     # Auto-detect CSV/TSV delimiters
- load_file()           # Load various file formats
- get_excel_sheet_names() # Extract Excel sheet names

# Feature Sections
- file_upload_section()  # Handle file uploads
- show_data_tab()       # Display data overview
- value_counts_tab()    # Value distribution analysis
- check_duplicates_tab() # Duplicate detection & removal
- check_null_values_tab() # Null value handling
- edit_data_tab()       # Value replacement
- download_section()    # Export functionality

# Main Application
- main()                # Application entry point
```

**Key Features**:
- Session state management
- Multi-format file support
- Interactive data cleaning
- Real-time updates
- Export capabilities

#### `requirements.txt`
**Dependencies**:
```
streamlit>=1.28.0    # Web framework
pandas>=2.0.0        # Data manipulation
openpyxl>=3.1.0      # Excel support
pyreadstat>=1.2.0    # SAS file support
xlrd>=2.0.1          # Legacy Excel support
```

### Configuration Files

#### `.streamlit/config.toml`
**Purpose**: Streamlit app configuration

**Settings**:
- **Theme**: Custom color scheme
- **Server**: Upload limits, security settings
- **Performance**: Caching, optimization

**Key Configurations**:
```toml
maxUploadSize = 200          # 200MB file limit
enableXsrfProtection = true  # Security enabled
primaryColor = "#FF4B4B"     # Streamlit red
```

#### `.gitignore`
**Purpose**: Version control exclusions

**Excludes**:
- Python cache files (`__pycache__/`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Streamlit secrets
- OS files (`.DS_Store`, `Thumbs.db`)

### Documentation Files

#### `README.md` (~8KB)
**Sections**:
1. Features overview
2. Installation instructions
3. Usage guide
4. Technical details
5. Troubleshooting
6. Future enhancements

**Audience**: All users, developers

#### `QUICKSTART.md` (~3KB)
**Sections**:
1. 2-minute installation
2. 5-minute first use
3. Common workflows
4. Pro tips

**Audience**: New users

#### `TESTING_GUIDE.md` (~11KB)
**Sections**:
1. Complete testing checklist
2. Test scenarios
3. Performance benchmarks
4. Bug reporting guidelines

**Audience**: Testers, QA, developers

#### `CHANGELOG.md` (~4KB)
**Sections**:
1. Version history
2. Features added
3. Bug fixes
4. Future enhancements

**Audience**: All users, developers

#### `PROJECT_STRUCTURE.md` (This file)
**Sections**:
1. Directory layout
2. File descriptions
3. Code organization
4. Data flow

**Audience**: Developers, contributors

### Sample Data

#### `sample_data.csv` (~2KB)
**Purpose**: Testing and demonstration

**Contents**:
- 30 rows of employee data
- 8 columns (ID, Name, Age, Department, Salary, City, Join_Date, Status)
- Intentional data quality issues:
  - 2 duplicate rows
  - 3 null salaries
  - 3 null cities
  - 2 "Inactive" status values

**Use Cases**:
- Testing all features
- User training
- Demo presentations

## 🔄 Data Flow

```
┌─────────────────┐
│  File Upload    │
│  (Sidebar)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Load File      │
│  - CSV/TSV      │
│  - Excel        │
│  - SAS          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Session State   │
│  st.session_    │
│  state['df']    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│         Tab Operations              │
├─────────────────────────────────────┤
│  Show Data  │  Value Counts         │
│  Duplicates │  Null Values          │
│  Edit Data  │                       │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Download       │
│  (Sidebar)      │
│  - CSV          │
│  - Excel        │
│  - SAS          │
└─────────────────┘
```

## 🏗️ Code Organization

### Function Categories

#### 1. Utility Functions
- `show_df()`: Display formatted DataFrames
- `detect_delimiter()`: Auto-detect file delimiters
- `load_file()`: Universal file loader
- `get_excel_sheet_names()`: Excel sheet extraction

#### 2. UI Sections
- `file_upload_section()`: File upload interface
- `download_section()`: Export interface

#### 3. Tab Functions
- `show_data_tab()`: Data overview
- `value_counts_tab()`: Distribution analysis
- `check_duplicates_tab()`: Duplicate management
- `check_null_values_tab()`: Null handling
- `edit_data_tab()`: Value editing

#### 4. Main Function
- `main()`: Application orchestration

### Session State Variables

```python
st.session_state = {
    'df': pd.DataFrame,           # Current DataFrame
    'original_df': pd.DataFrame,  # Original DataFrame (backup)
    'file_name': str              # Uploaded file name
}
```

## 🎨 UI Components

### Sidebar
- File upload controls
- Delimiter/sheet selection
- Load buttons
- Download section
- Current dataset info

### Main Area
- App title and description
- Tab navigation
- Content display
- Action buttons
- Metrics and visualizations

### Component Types
- `st.file_uploader()`: File upload
- `st.selectbox()`: Dropdown menus
- `st.multiselect()`: Multi-selection
- `st.button()`: Action buttons
- `st.metric()`: Metric cards
- `st.dataframe()`: Data tables
- `st.tabs()`: Tab navigation
- `st.expander()`: Collapsible sections
- `st.progress()`: Progress bars
- `st.download_button()`: File downloads

## 📊 Supported Operations

### File Operations
- **Upload**: CSV, TSV, Excel, SAS
- **Load**: Multiple sheets (Excel)
- **Preview**: Sheet preview (Excel)
- **Download**: CSV, Excel, SAS

### Data Operations
- **View**: Customizable display
- **Analyze**: Value counts, statistics
- **Clean**: Duplicates, nulls
- **Edit**: Value replacement
- **Export**: Multiple formats

## 🔐 Security Considerations

### Implemented
- XSRF protection enabled
- File size limits (200MB)
- Input validation
- Error handling
- No data persistence (session only)

### Best Practices
- No hardcoded credentials
- No external API calls
- Local processing only
- Secure file handling

## 📈 Performance Optimization

### Techniques Used
- Configurable row display limits
- Lazy loading of previews
- Efficient pandas operations
- Memory usage monitoring
- Progress indicators for long operations

### Recommended Limits
- Display rows: 100 (default)
- File size: < 200MB
- Unique values: < 10,000 for visualizations

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy from repository

### Docker (Future)
```dockerfile
FROM python:3.9
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## 🔧 Customization Points

### Easy to Modify
- **Theme**: Edit `.streamlit/config.toml`
- **Upload limit**: Change `maxUploadSize`
- **Default rows**: Modify `n_rows` default
- **Color scheme**: Update theme colors

### Requires Code Changes
- Add new file formats: Modify `load_file()`
- Add new operations: Create new tab function
- Change layout: Modify `main()`
- Add visualizations: Extend tab functions

## 📝 Code Style

### Standards
- **PEP 8**: Python style guide
- **Docstrings**: All functions documented
- **Comments**: Inline for complex logic
- **Naming**: Descriptive variable names

### Conventions
- Functions: `snake_case`
- Constants: `UPPER_CASE`
- Classes: `PascalCase` (if added)
- Private: `_leading_underscore`

## 🎯 Key Metrics

### Application
- **Total Lines**: ~800
- **Functions**: 11
- **Dependencies**: 5
- **File Size**: 27KB

### Documentation
- **Total Docs**: 5 files
- **Total Size**: ~35KB
- **Sections**: 50+
- **Examples**: 20+

## 🤝 Contributing Guidelines

### Adding Features
1. Create new function in appropriate section
2. Add to `main()` if new tab
3. Update documentation
4. Add to testing guide
5. Update changelog

### Code Review Checklist
- [ ] Follows PEP 8
- [ ] Has docstrings
- [ ] Includes error handling
- [ ] Updates session state correctly
- [ ] Tested with sample data
- [ ] Documentation updated

## 📞 Support Resources

### Internal Documentation
- `README.md`: Full documentation
- `QUICKSTART.md`: Getting started
- `TESTING_GUIDE.md`: Testing procedures
- `CHANGELOG.md`: Version history

### Code Documentation
- Function docstrings
- Inline comments
- Type hints (where applicable)

---

**Last Updated**: 2024-10-12  
**Version**: 1.0.0  
**Maintainer**: Development Team
