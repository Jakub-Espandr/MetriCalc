import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, cohen_kappa_score
from .translations import TRANSLATIONS

def compute_metrics(df, language='cs'):
    """Compute metrics from confusion matrix data"""
    df = df.copy()
    df.columns = df.columns.astype(str)

    # Filter for C_1 and C_2 rows
    df_cm = df[df['ClassValue'].isin(['C_1', 'C_2'])]

    # Handle decimal commas
    df_cm['C_1'] = df_cm['C_1'].astype(str).str.replace(',', '.').astype(float).astype(int)
    df_cm['C_2'] = df_cm['C_2'].astype(str).str.replace(',', '.').astype(float).astype(int)

    cm = df_cm[['C_1', 'C_2']].to_numpy()

    y_true = [0] * int(cm[0, :].sum()) + [1] * int(cm[1, :].sum())
    y_pred = [0] * int(cm[0, 0]) + [1] * int(cm[0, 1]) + [0] * int(cm[1, 0]) + [1] * int(cm[1, 1])

    precision = precision_score(y_true, y_pred, average=None, zero_division=0)
    recall = recall_score(y_true, y_pred, average=None, zero_division=0)
    f1 = f1_score(y_true, y_pred, average=None, zero_division=0)
    accuracy = round(accuracy_score(y_true, y_pred), 3)
    kappa = round(cohen_kappa_score(y_true, y_pred), 3)

    avg_precision = round(precision_score(y_true, y_pred, average='macro', zero_division=0), 3)
    avg_recall = round(recall_score(y_true, y_pred, average='macro', zero_division=0), 3)
    avg_f1 = round(f1_score(y_true, y_pred, average='macro', zero_division=0), 3)

    class_names = TRANSLATIONS[language]['class_names']
    return [
        [class_names[0], round(precision[0], 3), round(recall[0], 3), round(f1[0], 3), accuracy, kappa],
        [class_names[1], round(precision[1], 3), round(recall[1], 3), round(f1[1], 3), accuracy, kappa],
        [class_names[2], avg_precision, avg_recall, avg_f1, accuracy, kappa]
    ]

def export_to_excel(input_path, output_path, language='cs'):
    """Export metrics to Excel file"""
    try:
        df = pd.read_csv(input_path, sep=';')
        metrics = compute_metrics(df, language)
        wb = Workbook()
        sheetname = Path(input_path).stem

        # Metrics sheet
        ws1 = wb.active
        ws1.title = f"{TRANSLATIONS[language]['excel_metrics_sheet']}_{sheetname}"
        headers = TRANSLATIONS[language]['headers']
        for col, header in enumerate(headers, start=1):
            ws1.cell(row=1, column=col).value = header
        for row_i, row_data in enumerate(metrics, start=2):
            for col_i, value in enumerate(row_data, start=1):
                ws1.cell(row=row_i, column=col_i).value = value

        # Data sheet
        ws2 = wb.create_sheet(f"{TRANSLATIONS[language]['excel_data_sheet']}_{sheetname}")
        ws2.append(list(df.columns))
        for r in df.itertuples(index=False):
            ws2.append(list(r))

        wb.save(output_path)
        return True, None, (metrics, df)
    except Exception as e:
        return False, str(e), None

def add_to_workbook(wb, input_path, metrics, df, language='cs'):
    """Add data to existing workbook"""
    try:
        sheetname = Path(input_path).stem
        
        # Metrics sheet
        ws1 = wb.create_sheet(f"{TRANSLATIONS[language]['excel_metrics_sheet']}_{sheetname}")
        headers = TRANSLATIONS[language]['headers']
        for col, header in enumerate(headers, start=1):
            ws1.cell(row=1, column=col).value = header
        for row_i, row_data in enumerate(metrics, start=2):
            for col_i, value in enumerate(row_data, start=1):
                ws1.cell(row=row_i, column=col_i).value = value

        # Data sheet
        ws2 = wb.create_sheet(f"{TRANSLATIONS[language]['excel_data_sheet']}_{sheetname}")
        ws2.append(list(df.columns))
        for r in df.itertuples(index=False):
            ws2.append(list(r))
        
        return True, None
    except Exception as e:
        return False, str(e) 