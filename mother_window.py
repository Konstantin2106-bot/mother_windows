#from _typeshed import Self
from io import open_code
import sqlite3
import tkinter as tk #Импортируем графический фреймворк
import tkinter.ttk as ttk
from tkinter.ttk import Treeview, Style
from tkinter import Canvas, Label, PhotoImage, StringVar, Toplevel, messagebox
import datetime
from typing import Sized 
from tkinter.messagebox import showinfo
from subprocess import call
#from service_win import *
#import pandas as pd

def service_wind():
    call(["python", "service_win.py"])

mwin = tk.Tk()
mwin.title('Мастер обслуживания')
mwin.geometry('1520x700')
mwin.resizable(0,0)
mwin ['bg'] = '#CDC9C9'
mwin.wm_attributes('-alpha', 0.90)

meny = tk.Menu(mwin)
mwin.config(menu = meny)
fm = tk.Menu(meny)
meny.add_cascade(label='Обслуживание', menu=fm)
fm.add_command(label='Заявка на ремонт/ТО', command=service_wind)
fm.add_command(label='Замечания')   





class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)
        
        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings
  
        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER, width=20)
  
        for row in rows:
            table.insert('', tk.END, values=tuple(row))
        
        table.bind("<ButtonRelease-1>", lambda event, tree = table: self.CopyTextToClipboard(event, tree))
  
        scrolltable = tk.Scrollbar(self, command=table.yview)
        scrolltable1 = tk.Scrollbar(self, command= table.xview)
        table.configure(yscrollcommand=scrolltable.set)
        table.configure(xscrollcommand=scrolltable1.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        scrolltable1.pack(side=tk.BOTTOM, fill=tk.X)
        table.pack(expand=tk.YES, fill=tk.BOTH)

    def CopyTextToClipboard (self, event, tree):
        global id_num
        id_num = tree.item(tree.focus())['values'][0]
        print(id_num)
        

data = (',')
with sqlite3.connect('mydatabase.db') as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM service_data WHERE [Вид обслуживания] ='РЕМОНТ'")
    data = (row for row in cursor.fetchall())

data1 = (',')
with sqlite3.connect('mydatabase.db') as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM service_data WHERE [Вид обслуживания] = 'TO'")
    data1 = (row for row in cursor.fetchall())

table = Table(mwin, headings=('Номер заявки', 'Дата заявки', 'Гаражный номер', 'Вид ТС', 'Модель ТС', 'Гос. рег. знак','ДЭУ','Вид обслуживания','Категория обслуживания','Описание неисправности'), rows=data)
table.pack ( fill=tk.BOTH, padx=150, pady=80)

table1 = Table(mwin, headings=('Номер заявки', 'Дата заявки', 'Гаражный номер', 'Вид ТС', 'Модель ТС', 'Гос. рег. знак','ДЭУ','Вид обслуживания','Категория обслуживания','Описание неисправности'), rows=data1)
table1.pack ( fill=tk.BOTH,  padx=150, pady=60)
 


left_image1 = PhotoImage(file= "Обслуживание.png")
left_image1 = left_image1.subsample(7,7)
left_bt1 = tk.Button(mwin, image=left_image1, highlightthickness=0, bd=0, bg='White', command=service_wind).place(x=5,y=20)
left_image2 = PhotoImage (file="Склад.png")
left_image2 = left_image2.subsample(1,1)
left_bt2 =tk.Button (mwin, image=left_image2, highlightthickness=0, bd=0, bg='#CDC9C9', command=lambda: print('Выбрано окно склада')).place(x=5,y=100)

def Win_status ():
    global id_num
    ws = tk.Toplevel(mwin)
    ws.title('Окно осмотра ТС')
    ws.geometry ('300x650')
    ws.resizable(0,0)
    spec_written = StringVar()
    spec_lbl1 = tk.Label(ws, text='По заявке', fg= 'Black', font='Arial 12 bold')
    spec_lbl1.place(x= 10, y = 10)
    spec_lbl2 = tk.Label(ws,text = id_num, fg= 'Green', font='Complex 12 bold')
    spec_lbl2.place(x= 120, y = 10)
    spec_lbl3 = tk.Label(ws,text='В ходе диагностического осмотра ', fg= 'Black', font='Arial 10')
    spec_lbl3.place(x= 50, y = 35)
    spec_lbl4 = tk.Label(ws,text='были установлены следующие неисправности:', fg= 'Black', font='Arial 10')
    spec_lbl4.place(x= 10, y = 60)
    t_b_desk = tk.Text(ws, width =34, height = 8, bg = 'black', fg = 'white')
    t_b_desk.place(x=10, y= 100)  
    spec_lbl5 = tk.Label(ws,text='ТС установлен статус:', fg= 'Black', font='Arial 10')
    spec_lbl5.place(x= 70, y = 250)
    spec_com = ttk.Combobox(ws, width=32, height=4, font= 'Arial 11', values= ['Обслуживается -- не требует зпч',
                                                                               'Обслуживается -- требует зпч', 
                                                                                'Отложен с правом выезда',
                                                                                'Отложен без права выезда'
                                                                                ])
    spec_com.place(x=10, y=280 )
    cpec_bt = tk.Button(ws, text='Дополнить заявку', bg= 'Green', fg= 'White', width=50)
    cpec_bt.pack(side= tk.BOTTOM, fill= tk.BOTH, pady=10, padx=5)
    spec_lbl6 = tk.Label(ws, text='специалистами АРМ \n проведены следующие работы:', font= 'Arial 10')
    spec_lbl6.place(x= 50, y= 320)
    spec_text = tk.Text (ws, width=34, height= 8, bg= 'black', fg= 'white')
    spec_text.place(x= 10, y= 380)
    spec_lbl7 = tk.Label(ws, text='Ответственный специалист:', font= 'Arial 12 bold')
    spec_lbl7.place(x= 20, y= 520)
    spec_entr = tk.Entry(ws,  textvariable= spec_written, width = 33,  font = ('Arial',  '11', 'bold')) # Собственно, сами поля ввода...
    spec_entr.place(x=10 , y= 550)


lb1 = tk.Label(mwin, text='Заявки на ремонт:', fg= 'Black', font='Arial 20 bold')
lb1.place(x=120, y=20)
lb2 = tk.Label(mwin, text='Заявки на ТО:', fg= 'Black', font='Arial 20 bold')
lb2.place(x=120, y=450)
lb3 = tk.Label(mwin, text='Для заявки №', fg= 'Black', font='Arial 15 bold')
lb3.place(x=1100, y=20)

lb3 = tk.Label(mwin, text=':', fg= 'Black', font='Arial 15 bold')
lb3.place(x=1450, y=20)
lb4 = tk.Label(mwin, text='Выгрузка заявок по:', fg= 'Black', font='Arial 15 bold')
lb4.place(x=820, y=370)




fra_s = tk.Frame(mwin, width=200, height=30, bg= '#708090')
fra_s.place(x=1250,y=20)
fra_i = tk.Frame(mwin, width=250, height=60, bg= '#708090')
fra_i.place(x=1250,y=370)
global id_num
lbl_num = Label(fra_s, text= id_num, fg= 'Green', font='Arial 12 bold' ).pack()

btm= tk.Button(text = 'Заказать запчасть', width= '2', height = '1', padx='50', pady ='3', bg = 'green', fg = 'white', font ='times 12')
btm.place(x=1372, y=78)
btm1= tk.Button(text = 'Выгрузить форму', width= '2', height = '1', padx='50', pady ='3', bg = 'green', fg = 'white', font ='times 12')
btm1.place(x=1372, y=130)
btm2= tk.Button(text = 'Изменить статус', width= '2', height = '1', padx='50', pady ='3', bg = 'green', fg = 'white', font ='times 12', command= Win_status)
btm2.place(x=1372, y=180)
btm3= tk.Button(text = 'Закрыть заявку', width= '2', height = '1', padx='50', pady ='3', bg = 'green', fg = 'white', font ='times 12')
btm3.place(x=1372, y=230)
btm4= tk.Button(text = 'Начать выгрузку', width= '2', height = '1', padx='50', pady ='3', bg = 'green', fg = 'white', font ='times 12')
btm4.place(x=1250, y=440)

com_v= ttk.Combobox(font = 'times 15', width = 15, height='5', values=['дате',
                                                            'длительности ремонта',
                                                            'статусу ремонта',
                                                            'по принадлежности к ДЭУ',
                                                            'по гаражной группе'
                                                            ])
com_v.place(x=1050, y=370)
mwin.mainloop()