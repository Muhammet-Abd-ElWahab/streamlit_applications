# 🌐 SweetViz Data Profiler - Streamlit Web Application

A professional web-based application for comprehensive data profiling using SweetViz, built with Streamlit.

![DataClin Logo](Logo.png)

## ✨ Features

- **Modern Web Interface** with professional teal color scheme
- **Drag & Drop File Upload** - Easy file uploading
- **Multiple File Format Support**:
  - CSV files (`.csv`)
  - Excel files (`.xlsx`, `.xls`) with sheet selection
  - SAS files (`.sas7bdat`)
- **Excel Sheet Selection** - Interactive dropdown for multi-sheet files
- **Real-time Data Preview** - View your data before analysis
- **Interactive Statistics** - Live metrics and data overview
- **Embedded Report Viewer** - View reports directly in browser
- **One-Click Download** - Download HTML reports instantly
- **Responsive Design** - Works on desktop and tablet devices

## 🚀 Quick Start

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

### Using Batch Script (Windows)

```bash
# Double-click or run from command line
run_app.bat
```

The application will automatically open in your default browser at `http://localhost:8501`

## 📋 Requirements

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- 4GB RAM minimum (8GB recommended for large datasets)

### Python Dependencies

```
streamlit==1.28.1
pandas==2.0.3
sweetviz==2.1.4
numpy==1.24.3
openpyxl==3.1.2
xlrd==2.0.1
```

## 🎨 User Interface

The application features a professional design with:

- **Header with Logo** - DataClin branding
- **File Upload Section** - Drag & drop or browse
- **Configuration Sidebar** - File type selection and info
- **Data Overview** - Metrics cards showing key statistics
- **Data Preview** - Interactive table with first 10 rows
- **Column Information** - Expandable section with detailed column stats
- **Report Viewer** - Embedded HTML report display
- **Download Section** - One-click report download

## 📊 How to Use

1. **Select File Type**: Choose CSV, Excel, or SAS from the sidebar
2. **Upload File**: Drag & drop or click to browse for your data file
3. **Select Sheet** (Excel only): Choose the specific sheet to analyze
4. **Review Data**: Check the preview and statistics
5. **Generate Report**: Click "Generate SweetViz Report" button
6. **View & Download**: Explore the interactive report and download it

## 🌟 Key Features

### File Upload with Proper MIME Type Handling

The application correctly handles all file types:
- **CSV**: Standard text/csv MIME type
- **Excel**: Proper handling of .xlsx and .xls files
- **SAS**: Correct .sas7bdat file recognition

### Excel Sheet Selection

When you upload an Excel file:
1. Application automatically detects all sheets
2. Displays a dropdown with sheet names
3. Allows selection of specific sheet for analysis
4. Updates analysis based on selected sheet

### Interactive Data Preview

Before generating the report, you can:
- View first 10 rows of data
- See total rows, columns, memory usage
- Check missing value counts
- Expand column information for detailed stats

### Embedded Report Viewing

Reports are displayed directly in the browser:
- No need to download first
- Interactive visualizations
- Scrollable content
- Full SweetViz functionality

### One-Click Download

Download reports easily:
- Click the download button
- Report saved with descriptive filename
- HTML format for easy sharing
- Can be opened offline

## 🔧 Advanced Configuration

### Custom Port

```bash
streamlit run streamlit_app.py --server.port 8502
```

### Disable Browser Auto-Open

```bash
streamlit run streamlit_app.py --server.headless true
```

### Increase Upload Limit

Create `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 500
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: "numpy has no attribute 'VisibleDeprecationWarning'"
- **Solution**: Fixed in the code with numpy compatibility patch

**Issue**: "File type not allowed"
- **Solution**: Ensure file extension matches selected type (.csv, .xlsx, .xls, .sas7bdat)

**Issue**: Excel sheets not showing
- **Solution**: Verify Excel file is not corrupted and has proper structure

**Issue**: Large file upload fails
- **Solution**: Increase maxUploadSize in Streamlit config

**Issue**: Report generation takes too long
- **Solution**: Normal for large datasets (>100K rows), be patient

### File Format Requirements

- **CSV**: UTF-8 encoding recommended, comma-separated
- **Excel**: `.xlsx` or `.xls` format, not password protected
- **SAS**: `.sas7bdat` format only, not compressed

## 📁 Project Structure

```
Streamlit_SweetViz_App/
├── streamlit_app.py         # Main application
├── run_app.bat             # Launch script
├── requirements.txt        # Python dependencies
├── Logo.png               # Application logo
└── README.md             # This file
```

## 🎯 Technical Details

### Numpy Compatibility Fix
```python
if not hasattr(np, 'VisibleDeprecationWarning'):
    np.VisibleDeprecationWarning = DeprecationWarning
```

### File Type Handling
The application uses proper file type specifications:
```python
file_extensions = {
    "CSV": ["csv"],
    "Excel": ["xlsx", "xls"],
    "SAS": ["sas7bdat"]
}
```

### Temporary File Management
- Files are processed in temporary directories
- Automatic cleanup after processing
- No permanent storage of uploaded data

### Professional Styling
- **Teal color scheme** (#00796B, #00897B, #00695C)
- **Card-based layout** with shadows and borders
- **Gradient headers** for visual appeal
- **Responsive metrics** that adapt to screen size

## 🚀 Deployment Options

### Local Network

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

Access from other devices: `http://[your-ip]:8501`

### Streamlit Cloud

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with one click

### Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## 📊 What You Get

The SweetViz report includes:

- **Dataset Overview**: Shape, size, and basic statistics
- **Variable Analysis**: Distribution, missing values, unique counts
- **Numeric Variables**: Histograms, statistics, outliers
- **Categorical Variables**: Bar charts, frequency tables
- **Correlations**: Correlation matrix and insights
- **Missing Data**: Patterns and visualizations
- **Data Types**: Automatic type detection and validation

## 💡 Tips for Best Results

1. **Clean Your Data**: Remove unnecessary columns before upload
2. **Check Encoding**: Use UTF-8 for CSV files
3. **File Size**: Keep under 200MB for optimal performance
4. **Excel Files**: Ensure proper headers in first row
5. **SAS Files**: Verify file integrity before upload
6. **Browser**: Use Chrome or Firefox for best experience

## 🔒 Security Notes

- Files are processed in temporary directories
- No data is permanently stored
- Reports are generated on-the-fly
- Temporary files are automatically cleaned up
- No data is sent to external servers

## 📝 License

This application is for internal use. Ensure compliance with SweetViz, Streamlit, and other library licenses.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Test with sample data first
4. Check browser console for errors

## 📞 Contact

**DataClin** - Enabling data-driven decisions

---

*Built with ❤️ using Streamlit and SweetViz*
