# 🔧 Installation Guide

Complete installation instructions for the Data Cleaning & Exploration Tool.

---

## 📋 Prerequisites

### Required
- **Python**: Version 3.8 or higher
- **pip**: Python package installer
- **Internet connection**: For downloading packages

### Recommended
- **Virtual environment**: To isolate dependencies
- **Modern browser**: Chrome, Firefox, Safari, or Edge
- **4GB RAM**: Minimum for handling large files

---

## 🚀 Installation Methods

### Method 1: Quick Install (Recommended)

**Step 1: Navigate to project directory**
```bash
cd Data_Cleaning_App
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Run the application**
```bash
streamlit run app.py
```

**Total Time**: ~2 minutes

---

### Method 2: Virtual Environment (Best Practice)

**Step 1: Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Step 2: Navigate to project**
```bash
cd Data_Cleaning_App
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Run the application**
```bash
streamlit run app.py
```

**Total Time**: ~3 minutes

---

### Method 3: Manual Installation

**Step 1: Install each package individually**
```bash
pip install streamlit>=1.28.0
pip install pandas>=2.0.0
pip install openpyxl>=3.1.0
pip install pyreadstat>=1.2.0
pip install xlrd>=2.0.1
```

**Step 2: Run the application**
```bash
streamlit run app.py
```

**Total Time**: ~3 minutes

---

## 🔍 Verify Installation

### Check Python Version
```bash
python --version
# Should show: Python 3.8.x or higher
```

### Check pip Version
```bash
pip --version
# Should show: pip 20.x or higher
```

### Check Installed Packages
```bash
pip list
# Should show: streamlit, pandas, openpyxl, pyreadstat, xlrd
```

### Test Application
```bash
streamlit run app.py
# Should open browser at http://localhost:8501
```

---

## 🐛 Troubleshooting

### Issue: Python not found
**Solution**:
```bash
# Windows: Add Python to PATH
# macOS/Linux: Install Python 3
brew install python3  # macOS
sudo apt install python3  # Ubuntu/Debian
```

### Issue: pip not found
**Solution**:
```bash
python -m ensurepip --upgrade
```

### Issue: Permission denied
**Solution**:
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
```

### Issue: Package installation fails
**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

### Issue: pyreadstat installation fails
**Solution**:
```bash
# Windows: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# macOS: Install Xcode Command Line Tools
xcode-select --install

# Linux: Install build essentials
sudo apt-get install build-essential
```

### Issue: Streamlit won't start
**Solution**:
```bash
# Check if port 8501 is in use
# Windows
netstat -ano | findstr :8501

# macOS/Linux
lsof -i :8501

# Use different port
streamlit run app.py --server.port 8502
```

### Issue: Browser doesn't open
**Solution**:
- Manually open: `http://localhost:8501`
- Check firewall settings
- Try different browser

---

## 🌐 Platform-Specific Instructions

### Windows

**Install Python**:
1. Download from [python.org](https://www.python.org/downloads/)
2. Check "Add Python to PATH" during installation
3. Verify: `python --version`

**Install Dependencies**:
```bash
cd Data_Cleaning_App
pip install -r requirements.txt
```

**Run Application**:
```bash
streamlit run app.py
```

**Common Issues**:
- Use `python` instead of `python3`
- Use `\` for paths instead of `/`
- May need Visual C++ Build Tools for pyreadstat

---

### macOS

**Install Python** (if not installed):
```bash
# Using Homebrew (recommended)
brew install python3

# Verify
python3 --version
```

**Install Dependencies**:
```bash
cd Data_Cleaning_App
pip3 install -r requirements.txt
```

**Run Application**:
```bash
streamlit run app.py
```

**Common Issues**:
- Use `python3` and `pip3` instead of `python` and `pip`
- May need Xcode Command Line Tools
- Check PATH if commands not found

---

### Linux (Ubuntu/Debian)

**Install Python**:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Install Dependencies**:
```bash
cd Data_Cleaning_App
pip3 install -r requirements.txt
```

**Run Application**:
```bash
streamlit run app.py
```

**Common Issues**:
- Use `python3` and `pip3`
- May need `sudo` for system-wide installation
- Install build-essential for pyreadstat

---

## 📦 Dependency Details

### Streamlit (≥1.28.0)
**Purpose**: Web application framework  
**Size**: ~15 MB  
**Installation Time**: ~30 seconds

### Pandas (≥2.0.0)
**Purpose**: Data manipulation and analysis  
**Size**: ~30 MB  
**Installation Time**: ~45 seconds

### OpenPyXL (≥3.1.0)
**Purpose**: Excel file reading/writing  
**Size**: ~2 MB  
**Installation Time**: ~10 seconds

### PyReadStat (≥1.2.0)
**Purpose**: SAS file support  
**Size**: ~5 MB  
**Installation Time**: ~20 seconds  
**Note**: May require C compiler

### XLRD (≥2.0.1)
**Purpose**: Legacy Excel file support  
**Size**: ~1 MB  
**Installation Time**: ~5 seconds

**Total Size**: ~53 MB  
**Total Installation Time**: ~2 minutes

---

## 🔐 Security Considerations

### Virtual Environment (Recommended)
- Isolates project dependencies
- Prevents conflicts with other projects
- Easy to remove/recreate

### User Installation
- Use `--user` flag if no admin rights
- Installs in user directory
- No system-wide changes

### Trusted Sources
- All packages from PyPI (official repository)
- Well-maintained packages
- Regular security updates

---

## 🎯 Post-Installation

### Verify Everything Works

**1. Check Installation**
```bash
pip list | grep streamlit
pip list | grep pandas
pip list | grep openpyxl
pip list | grep pyreadstat
```

**2. Test Application**
```bash
streamlit run app.py
```

**3. Load Sample Data**
- Open browser at http://localhost:8501
- Upload `sample_data.csv`
- Verify data loads correctly

**4. Test Features**
- Try Show Data tab
- Check Value Counts
- Test duplicate removal
- Test null handling

---

## 🔄 Updating

### Update All Packages
```bash
pip install --upgrade -r requirements.txt
```

### Update Specific Package
```bash
pip install --upgrade streamlit
pip install --upgrade pandas
```

### Check for Updates
```bash
pip list --outdated
```

---

## 🗑️ Uninstallation

### Remove Packages
```bash
pip uninstall streamlit pandas openpyxl pyreadstat xlrd
```

### Remove Virtual Environment
```bash
# Deactivate first
deactivate

# Remove directory
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows
```

### Remove Project
```bash
# Navigate to parent directory
cd ..

# Remove project folder
rm -rf Data_Cleaning_App  # macOS/Linux
rmdir /s Data_Cleaning_App  # Windows
```

---

## 📊 System Requirements

### Minimum
- **CPU**: 1 GHz processor
- **RAM**: 2 GB
- **Storage**: 500 MB free space
- **OS**: Windows 7+, macOS 10.12+, Linux (any modern distro)
- **Python**: 3.8+

### Recommended
- **CPU**: 2 GHz dual-core processor
- **RAM**: 4 GB
- **Storage**: 1 GB free space
- **OS**: Windows 10+, macOS 11+, Ubuntu 20.04+
- **Python**: 3.9+

### For Large Files (>50MB)
- **RAM**: 8 GB or more
- **CPU**: Quad-core processor
- **Storage**: 2 GB free space

---

## 🌟 Quick Start After Installation

```bash
# 1. Navigate to directory
cd Data_Cleaning_App

# 2. Run application
streamlit run app.py

# 3. Open browser (automatic)
# http://localhost:8501

# 4. Upload sample_data.csv

# 5. Start cleaning!
```

---

## 💡 Tips

### Performance
- Use virtual environment for better performance
- Close other applications when handling large files
- Increase system RAM for very large datasets

### Development
- Use IDE with Python support (VS Code, PyCharm)
- Enable Python linting for code quality
- Use Git for version control

### Production
- Consider using Docker for deployment
- Use Streamlit Cloud for easy hosting
- Monitor memory usage for large files

---

## 🆘 Getting Help

### Installation Issues
1. Check error message carefully
2. Search error on Google/Stack Overflow
3. Check package documentation
4. Try virtual environment
5. Update pip: `pip install --upgrade pip`

### Application Issues
1. Check [README.md](README.md) troubleshooting section
2. Review [TESTING_GUIDE.md](TESTING_GUIDE.md)
3. Try with sample_data.csv
4. Check browser console for errors

### Still Stuck?
- Verify Python version: `python --version`
- Verify pip version: `pip --version`
- Check installed packages: `pip list`
- Try reinstalling: `pip uninstall -y -r requirements.txt && pip install -r requirements.txt`

---

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] pip working correctly
- [ ] Virtual environment created (optional)
- [ ] Dependencies installed
- [ ] Application runs successfully
- [ ] Browser opens at localhost:8501
- [ ] Sample data loads correctly
- [ ] All tabs accessible
- [ ] Features working as expected

---

## 🎉 Success!

If you can see the application in your browser and upload sample_data.csv successfully, you're all set!

**Next Steps**:
1. Read [QUICKSTART.md](QUICKSTART.md) for usage guide
2. Try all features with sample data
3. Upload your own data
4. Start cleaning!

---

**Installation Complete!** 🚀

```bash
streamlit run app.py
```

---

**Need Help?** Check [README.md](README.md) or [TESTING_GUIDE.md](TESTING_GUIDE.md)
