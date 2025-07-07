# Changelog

## [0.1.1] - 2025-07-07

### Added
- Support for CSV files where the `ClassValue` column contains descriptive text after the class code (e.g., `C_1 - nezasazena uroda`).
- Automatic detection and processing of any number of classes (`C_1`, `C_2`, `C_3`, ...).

### Fixed
- Fixed a crash when loading CSV files where `ClassValue` did not exactly match `C_1`, `C_2`, etc.
- Improved error messages for invalid or empty data in CSV files.

### Changed
- Metrics calculation is now robust to various CSV formats and works for any number of classes.

---

## [0.1.0] - 2025-06-22

### Added

- **Initial Release** of MetriCalc.
- **Modern User Interface**: Application using PySide6 to provide a modern, responsive, and cross-platform user experience.
- **Internationalization (i18n)**: Full UI and export support for Czech and English, with a simple dropdown to switch languages in real-time.
- **Single File Processing**: Process a single confusion matrix from a `.csv` file and export results to an `.xlsx` file.
- **Batch Processing**: Process all `.csv` files within a selected folder with two output options:
    - **Separate Files**: Generate an individual Excel file for each processed CSV.
    - **Single File**: Consolidate all results into a single Excel file, with each result on its own dedicated sheet.
- **Core Metric Calculation**: 
    - Reads 2x2 confusion matrices from semicolon-separated `.csv` files.
    - Calculates Precision (user accuracy), Recall (producer accuracy), F1-score, Overall Accuracy, and the Kappa Index.
    - Provides metrics for each class and a macro average.
- **User Experience Enhancements**:
    - Asynchronous processing for batch operations to keep the UI responsive.
    - Progress dialog with a cancellation option for batch jobs.
