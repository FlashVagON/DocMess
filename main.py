import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):   # Основное окно программы
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):   # Размещение всех виджетов и размеров на основном окне
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)  # Тулбар верхний для размещения на нем активных картинок
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='icon-add-0.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить письмо', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)  # вставка активного изображения Добавить письмо

        self.edit_img = tk.PhotoImage(file='edit.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать письмо', command=self.open_update_dialog, bg='#d7d8e0',
                                    bd=0,
                                    compound=tk.TOP, image=self.edit_img)
        btn_edit_dialog.pack(side=tk.LEFT)  # вставка активного изображения Редактировать письмо

        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'costs', 'total'), height=15, show='headings')

        v_scrollbar = ttk.Scrollbar(orient="vertical", command=self.tree.yview)   # СкроллБар вертикальный для ТриВью
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)  # СкроллБар горизонтальный для ТриВью
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscroll=h_scrollbar.set)

        self.tree.column('ID', minwidth=30, anchor=tk.CENTER)
        self.tree.column('description', minwidth=365, anchor=tk.CENTER)
        self.tree.column('costs', minwidth=150, anchor=tk.CENTER)
        self.tree.column('total', minwidth=100, anchor=tk.CENTER, stretch=True)

        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('costs', text='Статья Дохода\расхода')
        self.tree.heading('total', text='Сумма')

        self.tree.pack(side=tk.BOTTOM, fill=tk.Y)
        # self.tree.config(height=len(self.tree.get_children()))

    def records(self, description, costs, total):
        self.db.insert_data(description, costs, total)
        self.view_records()

    def update_record(self, description, costs, total):
        self.db.c.execute('''UPDATE letters SET description=?, costs=?, total=? WHERE ID=?''',
                          (description, costs, total, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM letters ''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()


class Child(tk.Toplevel):  # Класс окна второго уровня для добавления письма
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить входящие письма')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_discription = tk.Label(self, text='Наименование:')
        label_discription.place(x=50, y=50)
        label_select = tk.Label(self, text='Статья дохода\расхода:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Сумма')
        label_sum.place(x=50, y=110)

        self.entry_desctiption = ttk.Entry(self)
        self.entry_desctiption.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_desctiption.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_money.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):  # Класс открывает тоже окно второго уровня для редактирования Писем
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Редактирование')
        btn_edit = ttk.Button(self, text='Изменить')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_desctiption.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_money.get()))
        self.btn_ok.destroy()


class DB:  # Класс работы с базой данных
    def __init__(self):
        self.conn = sqlite3.connect('letters.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS letters (id integer primary key, description text, costs text, total real)'''
        )
        self.conn.commit()

    def insert_data(self, description, costs, total):
        self.c.execute('''INSERT INTO letters (description, costs, total) VALUES (?, ?, ?)''',
                       (description, costs, total))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Документы ИТ отдела")

    root.update_idletasks()   # ставим окно по середине экрана и шириной по элементам
    s = root.geometry()
    s = s.split('+')
    s = s[0].split('x')
    width_root = int(s[0])
    height_root = int(s[1])

    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    w = w // 2
    h = h // 2
    w = w - width_root // 2
    h = h - height_root // 2
    root.geometry('+{}+{}'.format(w, h))
    # root.geometry("650x450+300+200")
    root.resizable(True, False)
    root.mainloop()
