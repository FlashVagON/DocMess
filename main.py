import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):   # Основное окно программы
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Размещение всех виджетов и размеров на основном окне
    def init_main(self):

        # Тулбар верхний для размещения на нем активных картинок
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # вставка активного изображения Добавить письмо
        self.add_img = tk.PhotoImage(file='icon-add-0.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить письмо', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        # вставка активного изображения Редактировать письмо
        self.edit_img = tk.PhotoImage(file='edit.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать письмо', command=self.open_update_dialog, bg='#d7d8e0',
                                    bd=0,
                                    compound=tk.TOP, image=self.edit_img)
        btn_edit_dialog.pack(side=tk.LEFT)

        # Создаем Тривью с колонками
        self.tree = ttk.Treeview(self, columns=('ID', 'create_date', 'in_number', 'in_date', 'out_number',
                                                'out_date', 'about', 'deadend', 'out_mail', 'date_came',
                                                'state', 'mail_date'), height=15, show='headings')

        # СкроллБар вертикальный для ТриВью
        v_scrollbar = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=v_scrollbar.set)

        # СкроллБар горизонтальный для ТриВью
        h_scrollbar = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscroll=h_scrollbar.set)

        # размеры колонок Тривью
        self.tree.column('ID', width=20, anchor=tk.CENTER)
        self.tree.column('create_date', width=90, anchor=tk.CENTER)
        self.tree.column('in_number', width=80, anchor=tk.CENTER)
        self.tree.column('in_date', width=90, anchor=tk.CENTER)
        self.tree.column('out_number', width=90, anchor=tk.CENTER)
        self.tree.column('out_date', width=95, anchor=tk.CENTER)
        self.tree.column('about', width=300, anchor=tk.CENTER)
        self.tree.column('deadend', width=90, anchor=tk.CENTER)
        self.tree.column('out_mail', width=80, anchor=tk.CENTER)
        self.tree.column('date_came', width=110, anchor=tk.CENTER)
        self.tree.column('state', width=70, anchor=tk.CENTER)
        self.tree.column('mail_date', width=90, anchor=tk.CENTER)

        # названия колонок в тривью
        self.tree.heading('ID', text='ID')
        self.tree.heading('create_date', text='Дата создания')
        self.tree.heading('in_number', text='№ входящий')
        self.tree.heading('in_date', text='Дата входящая')
        self.tree.heading('out_number', text='№ исходящий')
        self.tree.heading('out_date', text='Дата исходящая')
        self.tree.heading('about', text='Краткое описание')
        self.tree.heading('deadend', text='Дата контроля')
        self.tree.heading('out_mail', text='mail ответа')
        self.tree.heading('date_came', text='Дата поступления')
        self.tree.heading('state', text='Статус')
        self.tree.heading('mail_date', text='Дата отправки')

        self.tree.pack(side=tk.BOTTOM, fill=tk.BOTH)
        # self.tree.config(height=len(self.tree.get_children()))

    def records(self, create_date, in_number, in_date, out_number, out_date, about, deadend, out_mail,
                date_came, state, mail_date):
        self.db.insert_data(create_date, in_number, in_date, out_number, out_date, about, deadend, out_mail,
                            date_came, state, mail_date)
        self.view_records()

    def update_record(self, create_date, in_number, in_date, out_number, out_date, about, deadend, out_mail,
                      date_came, state, mail_date):
        self.db.c.execute('''UPDATE letters SET create_date=?, in_number=?, in_date=?, out_number=?, out_date=?, 
        about=?, deadend=?, out_mail=?, date_came=?, state=?, mail_date=? WHERE ID=?''',
                          (create_date, in_number, in_date, out_number, out_date, about, deadend, out_mail,
                           date_came, state, mail_date, self.tree.set(self.tree.selection()[0], '#1')))
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
    # Создание базы данных SQLite3 (если существует то просто открывает)
    def __init__(self):
        self.conn = sqlite3.connect('letters.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS letters (id integer primary key, create_date date, in_number text, 
            in_date date, out_number text, out_date date, about text, deadend date, out_mail text, date_came date,
            state text, mail_date date)'''
        )
        self.conn.commit()

    # Добавление данных в БД
    def insert_data(self, create_date, in_number, in_date, out_number, out_date, about, deadend, out_mail,
                    date_came, state, mail_date):
        self.c.execute('''INSERT INTO letters (create_date, in_number, in_date, out_number, out_date, about, 
        deadend, out_mail, date_came, state, mail_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (create_date, in_number, in_date, out_number, out_date, about, deadend, out_mail,
                        date_came, state, mail_date))
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
    root.resizable(True, True)
    root.mainloop()
