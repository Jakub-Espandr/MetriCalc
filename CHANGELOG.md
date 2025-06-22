# Changelog

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
