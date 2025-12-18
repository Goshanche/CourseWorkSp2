import sys
import os
import re
from pathlib import Path
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QPlainTextEdit, QFileDialog,
    QCheckBox, QMessageBox, QGroupBox, QSplitter, QTextEdit
)
from PyQt6.QtCore import Qt, QRegularExpression, QRect, QSize
from PyQt6.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter, QPainter, QTextFormat

class LineNumbersWidget(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setFont(editor.font())

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumbersWidget(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width()
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
        self.highlight_current_line()

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(240, 240, 240))
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        font = self.font()
        painter.setFont(font)
        painter.setPen(QColor(100, 100, 100))

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, top, self.line_number_area.width(), self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(250, 250, 220)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

class CWHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("darkBlue"))
        self.keyword_format.setFontWeight(QFont.Weight.Bold)

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("darkGreen"))

        self.comment_format = QTextCharFormat()
        comment_color = QColor(128, 128, 128)
        self.comment_format.setForeground(comment_color)
        self.comment_format.setFontItalic(True)

        self.operator_format = QTextCharFormat()
        self.operator_format.setForeground(QColor("darkRed"))

        self.keywords = {
            "Integer", "And", "Else", "If", "While", "Continue", "Break",
            "Exit", "Input", "Output", "Program", "BODY", "Data", "Start", "Finish"
        }

        self.operators = {
            ":>", "==", "!=", "Le", "Ge", "Mul", "Div", "Mod",
            "+", "-", "!!", "||", ",", "[", "]", "(", ")", "{", "}", ";"
        }

        self._build_rules()

    def _build_rules(self):
        self.comment_start = "$*"
        self.comment_end = "*$"

        self.number_pattern = QRegularExpression(r"\b(?:0|[1-9]\d*)\b")

        keyword_pattern_str = r"\b(" + "|".join(re.escape(kw) for kw in self.keywords) + r")\b"
        self.keyword_pattern = QRegularExpression(keyword_pattern_str)

        sorted_ops = sorted(self.operators, key=len, reverse=True)
        op_pattern_str = "(" + "|".join(re.escape(op) for op in sorted_ops) + ")"
        self.operator_pattern = QRegularExpression(op_pattern_str)

    def highlightBlock(self, text):
        start_index = 0
        if self.currentBlockState() == 1:
            comment_length = len(text)
            if self.comment_end in text:
                end_index = text.find(self.comment_end)
                comment_length = end_index + len(self.comment_end)
                self.setCurrentBlockState(0)
                self.setFormat(0, comment_length, self.comment_format)
            else:
                self.setFormat(0, len(text), self.comment_format)
            return
        else:
            while start_index < len(text):
                start_marker = text.find(self.comment_start, start_index)
                if start_marker == -1:
                    break
                end_marker = text.find(self.comment_end, start_marker + len(self.comment_start))
                if end_marker == -1:
                    self.setFormat(start_marker, len(text) - start_marker, self.comment_format)
                    self.setCurrentBlockState(1)
                    break
                else:
                    comment_length = end_marker + len(self.comment_end) - start_marker
                    self.setFormat(start_marker, comment_length, self.comment_format)
                    start_index = end_marker + len(self.comment_end)

        match = self.number_pattern.globalMatch(text)
        while match.hasNext():
            m = match.next()
            self.setFormat(m.capturedStart(), m.capturedLength(), self.number_format)

        match = self.keyword_pattern.globalMatch(text)
        while match.hasNext():
            m = match.next()
            self.setFormat(m.capturedStart(), m.capturedLength(), self.keyword_format)

        match = self.operator_pattern.globalMatch(text)
        while match.hasNext():
            m = match.next()
            self.setFormat(m.capturedStart(), m.capturedLength(), self.operator_format)


class CWCompilerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CW Compiler GUI")
        self.resize(950, 700) 

        self.compiler_exe = None
        self.original_input_file = None
        self.last_saved_content = ""

        self.show_lexemes = True
        self.show_ast = True
        self.show_errors = True

        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Compiler selection
        compiler_layout = QHBoxLayout()
        compiler_layout.addWidget(QLabel("Compiler:"))
        self.compiler_line = QLineEdit()
        self.compiler_line.setPlaceholderText("Select compiler executable (cw_sp2__2025_2026.exe)")
        compiler_layout.addWidget(self.compiler_line)
        browse_compiler = QPushButton("Browse...")
        browse_compiler.clicked.connect(self.select_compiler)
        compiler_layout.addWidget(browse_compiler)
        main_layout.addLayout(compiler_layout)

        # Input section
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Input file:"))
        self.input_line = QLineEdit()
        input_layout.addWidget(self.input_line)
        browse_input = QPushButton("Browse...")
        browse_input.clicked.connect(self.select_input_file)
        input_layout.addWidget(browse_input)
        main_layout.addLayout(input_layout)

        # Splitter
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Редактор з нумерацією
        self.source_viewer = CodeEditor()
        self.source_viewer.setPlaceholderText("Enter or edit source code here.")
        self.highlighter = CWHighlighter(self.source_viewer.document())
        splitter.addWidget(self.source_viewer)

        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setPlaceholderText("Compilation output and logs will appear here.")
        splitter.addWidget(self.log_text)

        splitter.setSizes([400, 250])
        main_layout.addWidget(splitter)

        # Output options
        output_group = QGroupBox("Output Generation")
        output_layout = QVBoxLayout()

        c_layout = QHBoxLayout()
        c_layout.addWidget(QLabel("C output:"))
        self.c_line = QLineEdit()
        c_layout.addWidget(self.c_line)
        browse_c = QPushButton("Browse...")
        browse_c.clicked.connect(lambda: self.select_output_file(self.c_line, "C files (*.c)"))
        c_layout.addWidget(browse_c)
        output_layout.addLayout(c_layout)

        obj_layout = QHBoxLayout()
        obj_layout.addWidget(QLabel("Object output:"))
        self.obj_line = QLineEdit()
        obj_layout.addWidget(self.obj_line)
        browse_obj = QPushButton("Browse...")
        browse_obj.clicked.connect(lambda: self.select_output_file(self.obj_line, "Object files (*.obj)"))
        obj_layout.addWidget(browse_obj)
        output_layout.addLayout(obj_layout)

        exe_layout = QHBoxLayout()
        exe_layout.addWidget(QLabel("Executable output:"))
        self.exe_line = QLineEdit()
        exe_layout.addWidget(self.exe_line)
        browse_exe = QPushButton("Browse...")
        browse_exe.clicked.connect(lambda: self.select_output_file(self.exe_line, "Executables (*.exe)"))
        exe_layout.addWidget(browse_exe)
        output_layout.addLayout(exe_layout)

        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)

        # Log display options
        log_options_group = QGroupBox("Log Display Options")
        log_options_layout = QHBoxLayout()
        self.show_lexemes_cb = QCheckBox("Show Lexemes")
        self.show_lexemes_cb.setChecked(True)
        self.show_lexemes_cb.stateChanged.connect(self.on_log_option_changed)
        log_options_layout.addWidget(self.show_lexemes_cb)

        self.show_ast_cb = QCheckBox("Show AST")
        self.show_ast_cb.setChecked(True)
        self.show_ast_cb.stateChanged.connect(self.on_log_option_changed)
        log_options_layout.addWidget(self.show_ast_cb)

        self.show_errors_cb = QCheckBox("Show Errors")
        self.show_errors_cb.setChecked(True)
        self.show_errors_cb.stateChanged.connect(self.on_log_option_changed)
        log_options_layout.addWidget(self.show_errors_cb)

        log_options_group.setLayout(log_options_layout)
        main_layout.addWidget(log_options_group)

        # Options
        options_layout = QHBoxLayout()
        self.run_checkbox = QCheckBox("Run executable after build (--run)")
        options_layout.addWidget(self.run_checkbox)
        main_layout.addLayout(options_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.compile_btn = QPushButton("Compile")
        self.compile_btn.clicked.connect(self.run_compilation)
        self.compile_btn.setEnabled(False)
        button_layout.addWidget(self.compile_btn)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_source_file)
        button_layout.addWidget(save_btn)

        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.clicked.connect(self.clear_log)
        button_layout.addWidget(clear_log_btn)

        clear_all_btn = QPushButton("Clear All")
        clear_all_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_all_btn)

        main_layout.addLayout(button_layout)

        self.auto_detect_compiler()

    def on_log_option_changed(self):
        self.show_lexemes = self.show_lexemes_cb.isChecked()
        self.show_ast = self.show_ast_cb.isChecked()
        self.show_errors = self.show_errors_cb.isChecked()

    def auto_detect_compiler(self):
        if getattr(sys, 'frozen', False):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).parent

        candidates = [
            base_dir / "cw_sp2__2025_2026.exe",
            base_dir.parent / "x64" / "Debug" / "cw_sp2__2025_2026.exe",
            base_dir.parent / "x64" / "Release" / "cw_sp2__2025_2026.exe",
        ]

        for candidate in candidates:
            if candidate.exists():
                self.set_compiler_path(str(candidate))
                return

        self.log_text.appendPlainText("Compiler not found automatically. Please select it manually.\n")

    def select_compiler(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select Compiler Executable", "",
            "Executable (*.exe);;All files (*)"
        )
        if file:
            self.set_compiler_path(file)

    def set_compiler_path(self, path):
        self.compiler_line.setText(path)
        self.compiler_exe = Path(path)
        if self.compiler_exe.exists() and self.compiler_exe.suffix.lower() == ".exe":
            self.compile_btn.setEnabled(True)
            self.log_text.appendPlainText(f"Compiler selected: {self.compiler_exe}\n")
        else:
            self.compile_btn.setEnabled(False)
            QMessageBox.warning(self, "Invalid Compiler", "Selected file is not a valid .exe file.")

    def select_input_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select input file", "", "Source files (*.d09);;All files (*)"
        )
        if file:
            self.input_line.setText(file)
            self.original_input_file = file
            self.load_source_file(file)
            with open(file, "r", encoding="utf-8") as f:
                self.last_saved_content = f.read()

            base = Path(file).stem
            dir_path = Path(file).parent
            if not self.c_line.text():
                self.c_line.setText(str(dir_path / f"{base}.c"))
            if not self.obj_line.text():
                self.obj_line.setText(str(dir_path / f"{base}.obj"))
            if not self.exe_line.text():
                self.exe_line.setText(str(dir_path / f"{base}.exe"))

    def load_source_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.source_viewer.setPlainText(content)
        except Exception as e:
            self.source_viewer.setPlainText(f"Failed to load file:\n{str(e)}")

    def save_source_file(self):
        current_text = self.source_viewer.toPlainText()
        if not current_text.strip():
            QMessageBox.warning(self, "Warning", "Nothing to save.")
            return

        if self.original_input_file:
            save_path = self.original_input_file
        else:
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Source File", "", "Source files (*.d09);;All files (*)"
            )
            if not save_path:
                return
            if not save_path.endswith(".d09"):
                save_path += ".d09"

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(current_text)
            self.original_input_file = save_path
            self.input_line.setText(save_path)
            self.last_saved_content = current_text
            self.log_text.appendPlainText(f"Saved source to: {save_path}\n")

            base = Path(save_path).stem
            dir_path = Path(save_path).parent
            if not self.c_line.text():
                self.c_line.setText(str(dir_path / f"{base}.c"))
            if not self.obj_line.text():
                self.obj_line.setText(str(dir_path / f"{base}.obj"))
            if not self.exe_line.text():
                self.exe_line.setText(str(dir_path / f"{base}.exe"))
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save file:\n{str(e)}")

    def select_output_file(self, line_edit, file_filter):
        file, _ = QFileDialog.getSaveFileName(self, "Save output", "", file_filter)
        if file:
            line_edit.setText(file)

    def clear_log(self):
        self.log_text.clear()

    def clear_all(self):
        self.input_line.clear()
        self.c_line.clear()
        self.obj_line.clear()
        self.exe_line.clear()
        self.source_viewer.clear()
        self.log_text.clear()
        self.run_checkbox.setChecked(False)
        self.original_input_file = None
        self.last_saved_content = ""
        self.source_viewer.setPlaceholderText("Enter or edit source code here.")
        self.log_text.setPlaceholderText("Compilation output and logs will appear here.")

    def run_compilation(self):
        if not self.compiler_exe or not self.compiler_exe.exists():
            QMessageBox.warning(self, "Error", "Please select a valid compiler executable first.")
            return

        current_text = self.source_viewer.toPlainText().strip()
        if not current_text:
            QMessageBox.warning(self, "Error", "No source code to compile.")
            return

        if not self.original_input_file or current_text != self.last_saved_content:
            self.save_source_file()
            if not self.original_input_file:
                self.log_text.appendPlainText("Compilation cancelled: source file not saved.\n")
                return

            with open(self.original_input_file, "r", encoding="utf-8") as f:
                self.last_saved_content = f.read()

        input_path = Path(self.original_input_file)
        input_dir = input_path.parent
        input_filename = input_path.name
        base = input_path.stem

        if not self.c_line.text():
            self.c_line.setText(str(input_dir / f"{base}.c"))
        if not self.obj_line.text():
            self.obj_line.setText(str(input_dir / f"{base}.obj"))
        if not self.exe_line.text():
            self.exe_line.setText(str(input_dir / f"{base}.exe"))

        cmd = [str(self.compiler_exe), "--input-file", input_filename]

        c_path = Path(self.c_line.text().strip())
        obj_path = Path(self.obj_line.text().strip())
        exe_path = Path(self.exe_line.text().strip())

        cmd.extend(["--c-gen-file", c_path.name])
        cmd.extend(["--obj-gen-file", obj_path.name])
        cmd.extend(["--exe-gen-file", exe_path.name])

        self.log_text.appendPlainText(f"> Compiling in directory: {input_dir}\n")
        self.log_text.appendPlainText(f"> Command: {' '.join(cmd)}\n")

        try:
            result = subprocess.run(
                cmd,
                cwd=input_dir,
                capture_output=True,
                text=True,
                timeout=20
            )

            if result.returncode == 0:
                self.log_text.appendPlainText("SUCCESS: Compilation completed.\n")
            else:
                self.log_text.appendPlainText("ERROR: Compilation failed.\n")

            if result.stdout.strip():
                self.log_text.appendPlainText("STDOUT:\n" + result.stdout)
            if result.stderr.strip():
                self.log_text.appendPlainText("STDERR:\n" + result.stderr)

            self.load_compiler_logs(input_path)

            if self.run_checkbox.isChecked() and exe_path.exists():
                self.log_text.appendPlainText(f"> Launching: {exe_path}\n")
                try:
                    subprocess.Popen(["cmd", "/k", str(exe_path)], cwd=input_dir)
                    self.log_text.appendPlainText("Launched executable (non-blocking).\n")
                except Exception as e:
                    self.log_text.appendPlainText(f"Failed to launch executable: {e}\n")

        except subprocess.TimeoutExpired:
            self.log_text.appendPlainText("ERROR: Compilation took too long (20 seconds).\n")
        except Exception as e:
            self.log_text.appendPlainText(f"CRITICAL ERROR: {str(e)}\n")

    def load_compiler_logs(self, input_path: Path):
        stem = input_path.stem
        parent_dir = input_path.parent

        files_to_load = []

        if self.show_lexemes:
            files_to_load.extend([
                (parent_dir / f"{stem}_lexemes.txt", "Lexemes"),
                (parent_dir / f"{stem}_prepared_lexemes.txt", "Prepared Lexemes"),
            ])

        if self.show_ast:
            files_to_load.append((parent_dir / f"{stem}.ast", "AST"))

        if self.show_errors:
            files_to_load.extend([
                (parent_dir / f"{stem}_lexeme_error.txt", "Lexical Errors"),
                (parent_dir / f"{stem}_syntax_error.txt", "Syntax Errors"),
                (parent_dir / f"{stem}_semantix_error.txt", "Semantic Errors"),
            ])

        for file_path, title in files_to_load:
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                        if content.strip():
                            self.log_text.appendPlainText(f"\n=== {title} ===\n")
                            self.log_text.appendPlainText(content)
                except Exception as e:
                    self.log_text.appendPlainText(f"Failed to read {title}: {e}\n")


def main():
    app = QApplication(sys.argv)
    window = CWCompilerGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()