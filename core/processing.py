import os
from pathlib import Path
from openpyxl import Workbook
from PySide6.QtCore import QThread, Signal
from .metrics import export_to_excel, add_to_workbook
from .translations import TRANSLATIONS

class ProcessingThread(QThread):
    """Thread for processing files to avoid UI freezing"""
    progress_updated = Signal(int, str)
    finished = Signal(bool, str, int, list)
    
    def __init__(self, input_dir, output_dir, single_file, batch_mode, csv_files, language='cs'):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.single_file = single_file
        self.batch_mode = batch_mode
        self.csv_files = csv_files
        self.language = language
    
    def run(self):
        success_count = 0
        error_files = []
        
        # For single file mode, create one workbook
        if self.batch_mode == 2:
            wb = Workbook()
            wb.remove(wb.active)
        
        for i, csv_file in enumerate(self.csv_files):
            input_path = os.path.join(self.input_dir, csv_file)
            
            self.progress_updated.emit(i, TRANSLATIONS[self.language]['processing_file'].format(csv_file))
            
            if self.batch_mode == 1:  # Separate files
                output_path = os.path.join(self.output_dir, Path(csv_file).stem + ".xlsx")
                success, error, _ = export_to_excel(input_path, output_path, self.language)
                if success:
                    success_count += 1
                else:
                    error_files.append((csv_file, error))
            else:  # Single file
                try:
                    success, error, data = export_to_excel(input_path, "temp.xlsx", self.language)
                    if success and data:
                        metrics, df = data
                        add_success, add_error = add_to_workbook(wb, input_path, metrics, df, self.language)
                        if add_success:
                            success_count += 1
                        else:
                            error_files.append((csv_file, add_error))
                    else:
                        error_files.append((csv_file, error))
                except Exception as e:
                    error_files.append((csv_file, str(e)))
        
        # Save single file
        if self.batch_mode == 2:
            try:
                wb.save(self.single_file)
            except Exception as e:
                error_files.append((TRANSLATIONS[self.language]['save_error'], str(e)))
        
        self.finished.emit(True, "", success_count, error_files) 