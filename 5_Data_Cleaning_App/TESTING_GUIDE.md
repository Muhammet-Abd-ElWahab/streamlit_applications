# 🧪 Testing Guide

This guide helps you thoroughly test the Data Cleaning & Exploration Tool.

## 📋 Testing Checklist

### ✅ File Upload Tests

#### CSV/TSV Files
- [ ] Upload CSV with comma delimiter
- [ ] Upload CSV with semicolon delimiter
- [ ] Upload TSV with tab delimiter
- [ ] Test auto-detection of delimiter
- [ ] Test manual delimiter selection
- [ ] Upload CSV with special characters
- [ ] Upload CSV with different encodings (UTF-8, Latin1)
- [ ] Test empty CSV file
- [ ] Test CSV with only headers
- [ ] Test very large CSV (>100MB)

#### Excel Files
- [ ] Upload .xlsx file
- [ ] Upload .xls file
- [ ] Upload Excel with single sheet
- [ ] Upload Excel with multiple sheets
- [ ] Test sheet selection dropdown
- [ ] Test sheet preview functionality
- [ ] Upload Excel with empty sheets
- [ ] Upload Excel with merged cells
- [ ] Upload Excel with formulas
- [ ] Test Excel with special characters in sheet names

#### SAS Files
- [ ] Upload .sas7bdat file
- [ ] Test SAS file with various data types
- [ ] Upload compressed SAS file
- [ ] Test large SAS file

#### Error Handling
- [ ] Upload unsupported file format (.txt, .json)
- [ ] Upload corrupted file
- [ ] Upload file with wrong extension
- [ ] Test file size limit (200MB)
- [ ] Cancel file upload mid-process

### ✅ Show Data Tab Tests

#### Display Functionality
- [ ] View default number of rows (100)
- [ ] Change number of rows to display
- [ ] Test with minimum rows (5)
- [ ] Test with maximum rows (all data)
- [ ] Toggle "Show all columns" checkbox
- [ ] Verify shape metrics (rows, columns, memory)

#### Data Type Display
- [ ] Expand "Column Data Types" section
- [ ] Verify all columns are listed
- [ ] Check data types are correct
- [ ] Verify non-null counts
- [ ] Verify null counts

#### Statistics
- [ ] View numerical column statistics
- [ ] Test with dataset having no numerical columns
- [ ] View DataFrame info summary
- [ ] Verify memory usage calculation

### ✅ Value Counts Tab Tests

#### Basic Functionality
- [ ] Select different columns
- [ ] View value counts for categorical column
- [ ] View value counts for numerical column
- [ ] Verify count accuracy
- [ ] Verify percentage calculation (2 decimals)
- [ ] Check sorting (descending by count)

#### Metrics Display
- [ ] Verify "Unique Values" metric
- [ ] Verify "Most Common Value" metric
- [ ] Verify "Most Common Count" metric
- [ ] Check total count at bottom

#### Visualization
- [ ] View bar chart for categorical data
- [ ] View bar chart for numerical data
- [ ] Test with column having >50 unique values
- [ ] Test with column having 1 unique value

### ✅ Check Duplicates Tab Tests

#### Detection
- [ ] Check duplicates across all columns (default)
- [ ] Select single column for duplicate check
- [ ] Select multiple columns for duplicate check
- [ ] Test with dataset having no duplicates
- [ ] Test with dataset having all duplicates

#### Metrics
- [ ] Verify duplicate count metric
- [ ] Verify duplicate percentage metric
- [ ] Verify unique rows metric
- [ ] Check delta indicators (colors)

#### Display
- [ ] View duplicate rows table
- [ ] Verify all duplicates are shown
- [ ] Check table formatting

#### Removal
- [ ] Remove duplicates (all columns)
- [ ] Remove duplicates (specific columns)
- [ ] Verify success message
- [ ] Verify DataFrame is updated
- [ ] Check row count after removal
- [ ] Test removing duplicates when none exist

### ✅ Check Null Values Tab Tests

#### Overall Statistics
- [ ] View total null values metric
- [ ] View percentage of nulls metric
- [ ] View columns with nulls metric
- [ ] Verify null values by column table
- [ ] Check sorting by null count

#### Column-Specific Analysis
- [ ] Select column with nulls
- [ ] Select column without nulls
- [ ] View null count metric
- [ ] View null percentage metric
- [ ] Check progress bar display

#### View Null Rows
- [ ] Expand "View Rows with Null Values"
- [ ] Verify correct rows are shown
- [ ] Check table formatting

#### Remove Rows Action
- [ ] Remove rows with nulls
- [ ] Verify success message
- [ ] Verify row count decreases
- [ ] Check DataFrame is updated
- [ ] Test with column having all nulls

#### Replace Nulls Action
- [ ] Replace nulls with text value
- [ ] Replace nulls with numeric value
- [ ] Replace nulls in numeric column with text
- [ ] Replace nulls with empty string
- [ ] Verify success message
- [ ] Verify null count becomes 0
- [ ] Check DataFrame is updated

### ✅ Edit Data Tab Tests

#### Column Selection
- [ ] Select different columns
- [ ] View value distribution in expander
- [ ] Verify value counts are accurate

#### Value Selection
- [ ] Select single value to replace
- [ ] Select multiple values to replace
- [ ] Test with column having many unique values
- [ ] Test with column having few unique values

#### Replacement
- [ ] Enter replacement value (text)
- [ ] Enter replacement value (numeric)
- [ ] View affected rows count
- [ ] Expand "View Affected Rows (Before)"
- [ ] Verify preview is accurate

#### Execution
- [ ] Execute replacement
- [ ] Verify success message
- [ ] Verify affected row count in message
- [ ] Check DataFrame is updated
- [ ] Verify values are replaced correctly
- [ ] Test type conversion (text to number)

### ✅ Download Section Tests

#### CSV Download
- [ ] Select UTF-8 encoding
- [ ] Select UTF-8-sig encoding
- [ ] Select Latin1 encoding
- [ ] Select cp1252 encoding
- [ ] Download CSV file
- [ ] Verify filename has timestamp
- [ ] Open downloaded CSV in Excel
- [ ] Verify data integrity

#### Excel Download
- [ ] Download Excel file
- [ ] Verify filename has timestamp
- [ ] Open downloaded Excel file
- [ ] Verify sheet name is "Cleaned Data"
- [ ] Verify data integrity
- [ ] Check formatting is preserved

#### SAS Download
- [ ] Download SAS file
- [ ] Verify filename has timestamp
- [ ] Verify file size is reasonable
- [ ] Test opening in SAS (if available)

#### Current Dataset Info
- [ ] Verify row count is accurate
- [ ] Verify column count is accurate
- [ ] Check info updates after cleaning operations

### ✅ Session State Tests

#### Persistence
- [ ] Upload file and switch tabs
- [ ] Verify data persists across tabs
- [ ] Perform cleaning operation
- [ ] Switch tabs and verify changes persist
- [ ] Refresh page and verify data is lost (expected)

#### Multiple Operations
- [ ] Remove duplicates, then check nulls
- [ ] Remove nulls, then edit data
- [ ] Edit data, then remove duplicates
- [ ] Perform all operations in sequence
- [ ] Verify each operation updates the DataFrame

### ✅ Edge Cases

#### Empty Data
- [ ] Upload file with only headers
- [ ] Test all tabs with empty DataFrame
- [ ] Verify appropriate messages are shown

#### Single Column
- [ ] Upload file with single column
- [ ] Test all operations
- [ ] Verify no errors occur

#### All Nulls
- [ ] Test column with all null values
- [ ] Remove rows with nulls
- [ ] Replace all nulls

#### Large Files
- [ ] Upload file with 100,000+ rows
- [ ] Test display performance
- [ ] Test cleaning operations
- [ ] Verify memory usage warnings

#### Special Characters
- [ ] Test with column names having special characters
- [ ] Test with values having special characters
- [ ] Test with Unicode characters
- [ ] Test with emojis in data

### ✅ UI/UX Tests

#### Layout
- [ ] Verify sidebar is visible
- [ ] Verify tabs are properly labeled
- [ ] Check responsive design (resize window)
- [ ] Verify icons are displayed correctly

#### Messages
- [ ] Verify success messages are green
- [ ] Verify error messages are red
- [ ] Verify info messages are blue
- [ ] Verify warning messages are yellow
- [ ] Check message clarity and helpfulness

#### Interactions
- [ ] Test all buttons
- [ ] Test all dropdowns
- [ ] Test all text inputs
- [ ] Test all checkboxes
- [ ] Test all expanders
- [ ] Verify spinners appear for long operations

#### Accessibility
- [ ] Check color contrast
- [ ] Verify text is readable
- [ ] Test with keyboard navigation
- [ ] Verify tooltips are helpful

## 🎯 Test Scenarios

### Scenario 1: Complete Cleaning Workflow
1. Upload sample_data.csv
2. View data in Show Data tab
3. Check value counts for Department column
4. Remove duplicate rows (should find 2)
5. Handle nulls in Salary column (replace with 0)
6. Handle nulls in City column (remove rows)
7. Edit Status column (replace "Inactive" with "Active")
8. Download cleaned CSV file
9. Verify final dataset is clean

### Scenario 2: Excel Multi-Sheet
1. Upload Excel file with 3 sheets
2. Preview each sheet
3. Load second sheet
4. Perform cleaning operations
5. Download as Excel
6. Verify correct sheet was processed

### Scenario 3: Large Dataset
1. Upload file with 50,000+ rows
2. Display only 50 rows
3. Check duplicates (should be fast)
4. Remove duplicates
5. Download cleaned file
6. Verify performance is acceptable

### Scenario 4: Error Recovery
1. Upload corrupted file (expect error)
2. Upload valid file
3. Perform operation that causes error
4. Verify app recovers gracefully
5. Continue with normal operations

## 📊 Sample Data Tests

Use the provided `sample_data.csv` to test:
- **Duplicates**: Rows 1 & 7, Rows 2 & 13 are duplicates
- **Null Salaries**: Rows 9, 15, 21 have null salaries
- **Null Cities**: Rows 11, 20, 29 have null cities
- **Status Values**: Rows 14, 27 have "Inactive" status
- **30 total rows**: Good for testing display limits

## ✅ Performance Benchmarks

Expected performance:
- **File upload**: < 5 seconds for 10MB file
- **Duplicate check**: < 2 seconds for 10,000 rows
- **Null check**: < 1 second for any size
- **Value replacement**: < 2 seconds for 10,000 rows
- **Download**: < 3 seconds for 10MB file

## 🐛 Bug Reporting

If you find a bug, document:
1. **Steps to reproduce**
2. **Expected behavior**
3. **Actual behavior**
4. **Error message** (if any)
5. **File characteristics** (size, format, structure)
6. **Browser and OS**

## ✨ Testing Tips

1. **Test incrementally**: One feature at a time
2. **Use sample data**: Start with provided sample_data.csv
3. **Check console**: Look for JavaScript errors
4. **Monitor memory**: Watch for memory leaks with large files
5. **Test edge cases**: Empty, single row, all nulls, etc.
6. **Verify downloads**: Always open downloaded files
7. **Cross-browser**: Test in Chrome, Firefox, Safari
8. **Document issues**: Keep notes of any problems

## 🎉 Success Criteria

The app passes testing if:
- ✅ All file formats load correctly
- ✅ All cleaning operations work as expected
- ✅ No data loss or corruption occurs
- ✅ Downloads produce valid files
- ✅ UI is responsive and intuitive
- ✅ Error messages are clear and helpful
- ✅ Performance is acceptable for typical use cases
- ✅ Session state persists correctly across tabs

---

**Happy Testing!** 🚀
