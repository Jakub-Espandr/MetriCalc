import os
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, 
    QFileDialog, QMessageBox, QProgressDialog, QRadioButton, QButtonGroup, 
    QGroupBox, QComboBox, QProxyStyle, QStyle
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from core.translations import TRANSLATIONS
from core.processing import ProcessingThread
from core.metrics import export_to_excel
from .widgets import ModernButton, FileLabel
from .custom_dropdown import CustomDropdown

class NoArrowProxyStyle(QProxyStyle):
    """A proxy style to prevent drawing the default dropdown arrow."""
    def drawPrimitive(self, element, option, painter, widget=None):
        if element == QStyle.PrimitiveElement.PE_IndicatorArrowDown:
            return
        super().drawPrimitive(element, option, painter, widget)

class MetriCalcApp(QMainWindow):
    def __init__(self, app_icon=None):
        super().__init__()
        self.selected_file = None
        self.save_path = None
        self.batch_input_dir = None
        self.batch_output_dir = None
        self.batch_single_file = None
        self.processing_thread = None
        self.language = 'cs'  # Default language
        
        self.init_ui(app_icon)
        self.apply_modern_style()
    
    def init_ui(self, app_icon=None):
        self.setWindowTitle(TRANSLATIONS[self.language]['app_title'])
        
        # Set application icon on the window
        if app_icon:
            self.setWindowIcon(app_icon)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        title_label = QLabel("📊 MetriCalc")
        title_font = QFont("fccTYPO", 24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel(TRANSLATIONS[self.language]['app_subtitle'])
        subtitle_label.setFont(QFont("fccTYPO", 12))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        main_layout.addWidget(subtitle_label)
        
        language_layout = QHBoxLayout()
        language_label = QLabel(TRANSLATIONS[self.language]['language'])
        language_label.setFont(QFont("fccTYPO", 10))
        language_label.setStyleSheet("color: #495057;")
        
        self.language_combo = CustomDropdown()
        self.language_combo.addItem("🇨🇿 Čeština", "cs")
        self.language_combo.addItem("🇺🇸 English", "en")
        self.language_combo.setCurrentText("🇨🇿 Čeština")
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        self.language_combo.setFont(QFont("fccTYPO", 10))
        self.language_combo.setStyleSheet("""
            CustomDropdown {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                text-align: center;
            }
            CustomDropdown::menu-indicator {
                image: none;
            }
        """)
        
        language_layout.addWidget(language_label)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch()
        main_layout.addLayout(language_layout)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("fccTYPO", 10))
        main_layout.addWidget(self.tab_widget)
        
        self.create_single_tab()
        self.create_batch_tab()

        # Set the minimum size to the optimal size calculated by the layout, with added width
        hint = self.sizeHint()
        self.setMinimumSize(hint.width() + 150, hint.height())
    
    def _create_group_box(self, title):
        group_box = QGroupBox(title)
        bold_font = QFont("fccTYPO", 11)
        bold_font.setBold(True)
        group_box.setFont(bold_font)
        return group_box

    def create_single_tab(self):
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout(self.tab1)
        self.tab1_layout.setContentsMargins(30, 30, 30, 30)
        self.tab1_layout.setSpacing(20)
        
        self.step1_group = self._create_group_box(TRANSLATIONS[self.language]['step_1'])
        self.step1_layout = QVBoxLayout(self.step1_group)
        self.btn_select_file = ModernButton(TRANSLATIONS[self.language]['select_csv_file'], "📂", "#2196F3")
        self.btn_select_file.clicked.connect(self.select_file)
        self.step1_layout.addWidget(self.btn_select_file)
        self.label_file = FileLabel(TRANSLATIONS[self.language]['file_none'])
        self.step1_layout.addWidget(self.label_file)
        self.tab1_layout.addWidget(self.step1_group)
        
        self.step2_group = self._create_group_box(TRANSLATIONS[self.language]['step_2'])
        self.step2_layout = QVBoxLayout(self.step2_group)
        self.btn_select_output = ModernButton(TRANSLATIONS[self.language]['select_output'], "💾", "#2196F3")
        self.btn_select_output.clicked.connect(self.select_output)
        self.step2_layout.addWidget(self.btn_select_output)
        self.label_output = FileLabel(TRANSLATIONS[self.language]['output_none'])
        self.step2_layout.addWidget(self.label_output)
        self.tab1_layout.addWidget(self.step2_group)
        
        self.step3_group = self._create_group_box(TRANSLATIONS[self.language]['step_3'])
        self.step3_layout = QVBoxLayout(self.step3_group)
        self.btn_process = ModernButton(TRANSLATIONS[self.language]['start_processing'], "⚡", "#4CAF50")
        self.btn_process.clicked.connect(self.process_single)
        self.step3_layout.addWidget(self.btn_process)
        self.tab1_layout.addWidget(self.step3_group)
        
        self.tab1_layout.addStretch()
        self.tab_widget.addTab(self.tab1, TRANSLATIONS[self.language]['single_processing'])
    
    def create_batch_tab(self):
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout(self.tab2)
        self.tab2_layout.setContentsMargins(30, 30, 30, 30)
        self.tab2_layout.setSpacing(20)
        
        self.step1_batch_group = self._create_group_box(TRANSLATIONS[self.language]['step_1_batch'])
        self.step1_batch_layout = QVBoxLayout(self.step1_batch_group)
        self.btn_select_input_folder = ModernButton(TRANSLATIONS[self.language]['select_input_folder'], "📂", "#2196F3")
        self.btn_select_input_folder.clicked.connect(self.select_input_folder)
        self.step1_batch_layout.addWidget(self.btn_select_input_folder)
        self.label_input_folder = FileLabel(TRANSLATIONS[self.language]['input_folder_none'])
        self.step1_batch_layout.addWidget(self.label_input_folder)
        self.tab2_layout.addWidget(self.step1_batch_group)
        
        self.step2_batch_group = self._create_group_box(TRANSLATIONS[self.language]['step_2_batch'])
        self.step2_batch_layout = QVBoxLayout(self.step2_batch_group)
        self.button_group = QButtonGroup()
        self.rb_separate = QRadioButton(TRANSLATIONS[self.language]['separate_files'])
        self.rb_separate.setFont(QFont("fccTYPO", 10))
        self.rb_separate.setChecked(True)
        self.rb_separate.toggled.connect(self.on_batch_mode_changed)
        self.button_group.addButton(self.rb_separate, 1)
        self.step2_batch_layout.addWidget(self.rb_separate)
        self.rb_single = QRadioButton(TRANSLATIONS[self.language]['single_file'])
        self.rb_single.setFont(QFont("fccTYPO", 10))
        self.rb_single.toggled.connect(self.on_batch_mode_changed)
        self.button_group.addButton(self.rb_single, 2)
        self.step2_batch_layout.addWidget(self.rb_single)
        self.tab2_layout.addWidget(self.step2_batch_group)
        
        self.step3_batch_group = self._create_group_box(TRANSLATIONS[self.language]['step_3_batch'])
        self.step3_batch_layout = QVBoxLayout(self.step3_batch_group)
        self.btn_select_output_folder = ModernButton(TRANSLATIONS[self.language]['select_output_folder'], "📁", "#2196F3")
        self.btn_select_output_folder.clicked.connect(self.select_output_folder)
        self.step3_batch_layout.addWidget(self.btn_select_output_folder)
        self.label_output_folder = FileLabel(TRANSLATIONS[self.language]['output_folder_none'])
        self.step3_batch_layout.addWidget(self.label_output_folder)
        self.btn_select_single_file = ModernButton(TRANSLATIONS[self.language]['select_single_file'], "📊", "#2196F3")
        self.btn_select_single_file.clicked.connect(self.select_single_file)
        self.btn_select_single_file.hide()
        self.step3_batch_layout.addWidget(self.btn_select_single_file)
        self.label_single_file = FileLabel(TRANSLATIONS[self.language]['single_file_none'])
        self.label_single_file.hide()
        self.step3_batch_layout.addWidget(self.label_single_file)
        self.tab2_layout.addWidget(self.step3_batch_group)
        
        self.step4_batch_group = self._create_group_box(TRANSLATIONS[self.language]['step_4_batch'])
        self.step4_batch_layout = QVBoxLayout(self.step4_batch_group)
        self.btn_process_batch = ModernButton(TRANSLATIONS[self.language]['start_batch_processing'], "🚀", "#4CAF50")
        self.btn_process_batch.clicked.connect(self.process_batch)
        self.step4_batch_layout.addWidget(self.btn_process_batch)
        self.tab2_layout.addWidget(self.step4_batch_group)
        
        self.tab2_layout.addStretch()
        self.tab_widget.addTab(self.tab2, TRANSLATIONS[self.language]['batch_processing'])
    
    def _create_styled_message_box(self, icon, title, text):
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setFont(QFont("fccTYPO", 10))
        msg_box.setStyleSheet("""
            QMessageBox { background-color: #f8f9fa; }
            QLabel { color: #495057; font-family: fccTYPO; font-size: 11px; }
            QPushButton {
                background-color: #2196F3; color: white; border: none;
                border-radius: 6px; padding: 8px 16px; font-family: fccTYPO;
                font-weight: bold; font-size: 10px; min-width: 80px;
            }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:pressed { background-color: #1565C0; }
        """)
        msg_box.exec()

    def on_language_changed(self, text):
        if "Čeština" in text:
            new_lang = 'cs'
        else:
            new_lang = 'en'
        
        if new_lang != self.language:
            self.language = new_lang
            self.update_ui_language()
    
    def update_ui_language(self):
        self.setWindowTitle(TRANSLATIONS[self.language]['app_title'])
        self.findChildren(QLabel)[1].setText(TRANSLATIONS[self.language]['app_subtitle'])
        
        self.tab_widget.setTabText(0, TRANSLATIONS[self.language]['single_processing'])
        self.tab_widget.setTabText(1, TRANSLATIONS[self.language]['batch_processing'])
        
        self.step1_group.setTitle(TRANSLATIONS[self.language]['step_1'])
        self.step2_group.setTitle(TRANSLATIONS[self.language]['step_2'])
        self.step3_group.setTitle(TRANSLATIONS[self.language]['step_3'])
        self.step1_batch_group.setTitle(TRANSLATIONS[self.language]['step_1_batch'])
        self.step2_batch_group.setTitle(TRANSLATIONS[self.language]['step_2_batch'])
        self.step3_batch_group.setTitle(TRANSLATIONS[self.language]['step_3_batch'])
        self.step4_batch_group.setTitle(TRANSLATIONS[self.language]['step_4_batch'])
        
        self.btn_select_file.setText(f"📂 {TRANSLATIONS[self.language]['select_csv_file']}")
        self.btn_select_output.setText(f"💾 {TRANSLATIONS[self.language]['select_output']}")
        self.btn_process.setText(f"⚡ {TRANSLATIONS[self.language]['start_processing']}")
        self.btn_select_input_folder.setText(f"📂 {TRANSLATIONS[self.language]['select_input_folder']}")
        self.btn_select_output_folder.setText(f"📁 {TRANSLATIONS[self.language]['select_output_folder']}")
        self.btn_select_single_file.setText(f"📊 {TRANSLATIONS[self.language]['select_single_file']}")
        self.btn_process_batch.setText(f"🚀 {TRANSLATIONS[self.language]['start_batch_processing']}")
        
        self.rb_separate.setText(TRANSLATIONS[self.language]['separate_files'])
        self.rb_single.setText(TRANSLATIONS[self.language]['single_file'])
        
        if not self.selected_file: self.label_file.setText(TRANSLATIONS[self.language]['file_none'])
        if not self.save_path: self.label_output.setText(TRANSLATIONS[self.language]['output_none'])
        if not self.batch_input_dir: self.label_input_folder.setText(TRANSLATIONS[self.language]['input_folder_none'])
        if not self.batch_output_dir: self.label_output_folder.setText(TRANSLATIONS[self.language]['output_folder_none'])
        if not self.batch_single_file: self.label_single_file.setText(TRANSLATIONS[self.language]['single_file_none'])
    
    def apply_modern_style(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f8f9fa; }
            QTabWidget::pane { border: 1px solid #dee2e6; border-radius: 8px; background-color: white; }
            QTabBar::tab {
                background-color: #e9ecef; color: #495057; padding: 12px 20px;
                margin-right: 2px; border-top-left-radius: 6px; border-top-right-radius: 6px;
                font-weight: bold;
            }
            QTabBar::tab:selected { background-color: white; color: #2196F3; border-bottom: 2px solid #2196F3; }
            QTabBar::tab:hover { background-color: #dee2e6; }
            QGroupBox {
                font-weight: bold; border: 2px solid #dee2e6; border-radius: 8px;
                margin-top: 10px; padding-top: 10px; background-color: white;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 8px; color: #495057; }
            QRadioButton { color: #495057; spacing: 8px; }
            QRadioButton::indicator { width: 18px; height: 18px; }
            QRadioButton::indicator:unchecked { border: 2px solid #dee2e6; border-radius: 9px; background-color: white; }
            QRadioButton::indicator:checked { border: 2px solid #2196F3; border-radius: 9px; background-color: #2196F3; }
        """)
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, TRANSLATIONS[self.language]['select_csv_file'], "", "CSV soubory (*.csv)")
        if file_path:
            self.selected_file = file_path
            self.label_file.setText(TRANSLATIONS[self.language]['file_selected'].format(Path(file_path).name))
    
    def select_output(self):
        file_path, _ = QFileDialog.getSaveFileName(self, TRANSLATIONS[self.language]['select_output'], "", "Excel soubory (*.xlsx)")
        if file_path:
            self.save_path = file_path
            self.label_output.setText(TRANSLATIONS[self.language]['output_selected'].format(Path(file_path).name))
    
    def select_input_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, TRANSLATIONS[self.language]['select_input_folder'])
        if folder_path:
            self.batch_input_dir = folder_path
            self.label_input_folder.setText(TRANSLATIONS[self.language]['input_folder_selected'].format(Path(folder_path).name))
    
    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, TRANSLATIONS[self.language]['select_output_folder'])
        if folder_path:
            self.batch_output_dir = folder_path
            self.label_output_folder.setText(TRANSLATIONS[self.language]['output_folder_selected'].format(Path(folder_path).name))
    
    def select_single_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, TRANSLATIONS[self.language]['select_single_file'], "", "Excel soubory (*.xlsx)")
        if file_path:
            self.batch_single_file = file_path
            self.label_single_file.setText(TRANSLATIONS[self.language]['single_file_selected'].format(Path(file_path).name))
    
    def on_batch_mode_changed(self):
        mode = self.button_group.checkedId()
        is_separate = mode == 1
        self.btn_select_output_folder.setVisible(is_separate)
        self.label_output_folder.setVisible(is_separate)
        self.btn_select_single_file.setVisible(not is_separate)
        self.label_single_file.setVisible(not is_separate)
    
    def process_single(self):
        if not self.selected_file or not self.save_path:
            self._create_styled_message_box(QMessageBox.Warning, TRANSLATIONS[self.language]['missing_input'], TRANSLATIONS[self.language]['select_input_file_output'])
            return
        
        success, error, _ = export_to_excel(self.selected_file, self.save_path, self.language)
        if success:
            self._create_styled_message_box(QMessageBox.Information, TRANSLATIONS[self.language]['done'], TRANSLATIONS[self.language]['file_saved_as'].format(self.save_path))
        else:
            self._create_styled_message_box(QMessageBox.Critical, TRANSLATIONS[self.language]['error'], TRANSLATIONS[self.language]['something_went_wrong'].format(error))
    
    def process_batch(self):
        if not self.batch_input_dir:
            self._create_styled_message_box(QMessageBox.Warning, TRANSLATIONS[self.language]['missing_input'], TRANSLATIONS[self.language]['select_input_folder_first'])
            return
        
        batch_mode = self.button_group.checkedId()
        if batch_mode == 1 and not self.batch_output_dir:
            self._create_styled_message_box(QMessageBox.Warning, TRANSLATIONS[self.language]['missing_output'], TRANSLATIONS[self.language]['select_output_folder_first'])
            return
        elif batch_mode == 2 and not self.batch_single_file:
            self._create_styled_message_box(QMessageBox.Warning, TRANSLATIONS[self.language]['missing_output'], TRANSLATIONS[self.language]['select_single_file_first'])
            return
        
        csv_files = [f for f in os.listdir(self.batch_input_dir) if f.lower().endswith('.csv')]
        if not csv_files:
            self._create_styled_message_box(QMessageBox.Information, TRANSLATIONS[self.language]['no_csv_files'], TRANSLATIONS[self.language]['no_csv_files_in_folder'])
            return
        
        self.processing_thread = ProcessingThread(
            self.batch_input_dir, self.batch_output_dir, self.batch_single_file, 
            batch_mode, csv_files, self.language
        )
        
        self.progress_dialog = QProgressDialog(TRANSLATIONS[self.language]['processing_files'], 
                                             TRANSLATIONS[self.language]['cancel'], 0, len(csv_files), self)
        self.progress_dialog.setWindowTitle(TRANSLATIONS[self.language]['processing_files'])
        self.progress_dialog.setFont(QFont("fccTYPO", 10))
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        
        self.processing_thread.progress_updated.connect(self.update_progress)
        self.processing_thread.finished.connect(self.on_batch_finished)
        self.progress_dialog.canceled.connect(self.processing_thread.terminate)
        
        self.processing_thread.start()
        self.progress_dialog.show()
    
    def update_progress(self, value, text):
        self.progress_dialog.setValue(value)
        self.progress_dialog.setLabelText(text)
    
    def on_batch_finished(self, success, error, success_count, error_files):
        self.progress_dialog.close()
        
        if error_files:
            error_msg = "\n".join([f"{f}: {e}" for f, e in error_files])
            self._create_styled_message_box(QMessageBox.Warning, TRANSLATIONS[self.language]['done_with_errors'], 
                                          TRANSLATIONS[self.language]['processed_files'].format(success_count, error_msg))
        else:
            self._create_styled_message_box(QMessageBox.Information, TRANSLATIONS[self.language]['done'], 
                                          TRANSLATIONS[self.language]['all_files_processed'].format(success_count)) 