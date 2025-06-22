<p align="center">
  <a href="https://i.ibb.co/0pyTV8nq/icon.png">
    <img src="https://i.ibb.co/0pyTV8nq/icon.png" alt="MetriCalc Logo" width="220"/>
  </a>
</p>

<h1 align="center">MetriCalc</h1>
<p align="center"><em>(Born4Flight | FlyCamCzech)</em></p>

## Overview
MetriCalc is a clean, efficient tool designed to calculate key statistical metrics from confusion matrices exported from ArcGIS Pro or other platforms. With support for single and batch processing, multi-language output, and polished export to Excel, MetriCalc is ideal for rapid performance evaluation in classification tasks.

---

## ✨ Features

- **Modern & Responsive UI**
  - Built with PySide6 for a fast, native user experience
  - Segmented tabs for single and batch processing workflows

- **Internationalization (i18n)**
  - Toggle between **Czech** and **English** for both interface and output
  - Instant language switching without restart

- **Metric Computation**
  - Reads semicolon-delimited confusion matrix `.csv` files
  - Calculates:
    - Precision (User Accuracy)
    - Recall (Producer Accuracy)
    - F1-score
    - Overall Accuracy
    - Kappa Index
  - Reports metrics per class and macro average

- **Batch Processing**
  - Process all `.csv` files in a selected folder
  - Two export modes:
    - One Excel per file
    - One Excel file with multiple sheets

- **Excel Export**
  - XLSX output with localized metric headers
  - Two sheets per result:
    - **Metrics**: Computed values
    - **Data**: Raw confusion matrix

- **Performance**
  - Asynchronous background thread keeps the interface responsive
  - Real-time progress bar with cancel option

---

## 📦 Requirements

- Python 3.8+
- PySide6 >= 6.5.0
- pandas >= 1.5.0
- scikit-learn >= 1.2.0
- openpyxl >= 3.1.0

---

## 🚀 Installation

```bash
git clone https://github.com/Jakub-Espandr/MetriCalc.git
cd MetriCalc
pip install -r requirements.txt
python main.py
```

---

## 🛠️ Usage

1. Open the app and select **Single** or **Batch** tab
2. Load `.csv` confusion matrix or folder
3. Choose output location
4. Select language: 🇨🇿 Čeština / 🇺🇸 English
5. Click **Start Processing**

---

## 📁 Project Structure

```
MetriCalc/
├── main.py
├── core/            # Metric calculations and logic
├── ui/              # PySide6 GUI components
├── utils/           # Helpers and localization
├── assets/
│   ├── fonts/
│   └── icons/
├── requirements.txt
└── LICENSE
```

---

## 🔐 License

This project is licensed under the **MIT License**  
© 2025 Jakub Ešpandr – Born4Flight, FlyCamCzech

See the [LICENSE](https://github.com/Jakub-Espandr/MetriCalc/raw/main/LICENSE) file for full terms.

---

## 🙏 Acknowledgments

- Built with ❤️ using PySide6, pandas, and openpyxl
