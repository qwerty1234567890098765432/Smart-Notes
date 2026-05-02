import json
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QRadioButton, QGroupBox, 
QPushButton, QVBoxLayout, QHBoxLayout, QButtonGroup, QMessageBox, QTextEdit, QListWidget, 
QLineEdit, QInputDialog)

app = QApplication([])
window = QWidget()
window.setWindowTitle('Smart notes')
window.resize(700, 500)
text_edit = QTextEdit()
list_notes = QLabel('Список заметок')
notes_list = QListWidget()
note_cre = QPushButton('Создать заметку')
note_del = QPushButton('Удалить заметку')
note_save = QPushButton('Сохранить заметку')
list_tags = QLabel('Список тегов')
tags_list = QListWidget()
enter_tag = QLineEdit()
add_to_note = QPushButton('Добавить к заметке')
del_from_note = QPushButton('Открепить от заметки')
search_for_tag = QPushButton('Искать заметки по тегу')
main = QHBoxLayout()
lay1 = QVBoxLayout()
lay2 = QHBoxLayout()
lay3 = QVBoxLayout()
lay4 = QHBoxLayout()
lay1.addWidget(text_edit)
main.addLayout(lay1)
lay3.addWidget(list_notes)
lay3.addWidget(notes_list)
lay2.addWidget(note_cre)
lay2.addWidget(note_del)
lay3.addLayout(lay2)
lay3.addWidget(note_save)
lay3.addWidget(list_tags)
lay3.addWidget(tags_list)
lay3.addWidget(enter_tag)
lay4.addWidget(add_to_note)
lay4.addWidget(del_from_note)
lay3.addLayout(lay4)
lay3.addWidget(search_for_tag)
main.addLayout(lay3)
window.setLayout(main)

notes = {}

def load_notes():
    global notes
    try:
        with open('notes_data.json', 'r', encoding='utf-8') as json_file:
            notes = json.load(json_file)
    except:
        notes = {
            "Добро пожаловать!": {
                "текст": "Это самое лучшее приложение для заметок в мире!",
                "теги": ["добро", "инструкция"]
            }
        }
        save_notes()

def save_notes():
    global notes
    with open('notes_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(notes, json_file, ensure_ascii=False)

def update_notes_list():
    notes_list.clear()
    tags_list.clear()
    for note_title in notes.keys():
        notes_list.addItem(note_title)

def get_note_data():
    if notes_list.currentItem():
        key = notes_list.currentItem().text()
        if key in notes:
            text_edit.setPlainText(notes[key]["текст"])
            tags_list.clear()
            tags_list.addItems(notes[key]["теги"])
        else:
            text_edit.setPlainText("")
            tags_list.clear()

def cre_note():
    note_name, ok = QInputDialog.getText(window, "Новая заметка", "Введите название заметки:")
    if ok and note_name:
        if note_name not in notes:
            notes[note_name] = {"текст": "", "теги": []}
            save_notes()
            update_notes_list()
        else:
            QMessageBox.warning(window, "Ошибка", "Заметка с таким именем уже существует!")

def del_note():
    if notes_list.currentItem():
        key = notes_list.currentItem().text()
        del notes[key]
        save_notes()
        text_edit.clear()
        tags_list.clear()
        update_notes_list()
    else:
        QMessageBox.warning(window, "Внимание", "Выберите заметку для удаления.")

def save_note():
    if notes_list.currentItem():
        key = notes_list.currentItem().text()
        if key in notes:
            notes[key]["текст"] = text_edit.toPlainText()
            save_notes()
            QMessageBox.information(window, "Успех", f"Заметка '{key}' сохранена.")
    else:
        QMessageBox.warning(window, "Внимание", "Выберите заметку для сохранения.")

def add_tag():
    if notes_list.currentItem() and enter_tag.text():
        key = notes_list.currentItem().text()
        tag = enter_tag.text().strip()
        if tag not in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            save_notes()
            tags_list.addItem(tag)
            enter_tag.clear()
    else:
        QMessageBox.warning(window, "Внимание", "Выберите заметку и введите тег.")

def del_tag():
    if notes_list.currentItem() and tags_list.currentItem():
        note_key = notes_list.currentItem().text()
        tag_item = tags_list.currentItem()
        tag_text = tag_item.text()
        
        notes[note_key]["теги"].remove(tag_text)
        save_notes()
        tags_list.takeItem(tags_list.row(tag_item))
    else:
        QMessageBox.warning(window, "Внимание", "Выберите тег для открепления.")

notes_list.itemClicked.connect(get_note_data) 
note_cre.clicked.connect(cre_note)
note_del.clicked.connect(del_note)
note_save.clicked.connect(save_note)
add_to_note.clicked.connect(add_tag)
del_from_note.clicked.connect(del_tag)

load_notes()          
update_notes_list()   

window.show()
app.exec()
