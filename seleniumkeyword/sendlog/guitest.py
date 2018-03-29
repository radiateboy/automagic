# -*- coding: utf-8 -*-
__author__ = 'Ray'

"""
GUI 设计.
mail：tsbc@vip.qq.com
2016-05-05
http://blog.csdn.net/jcodeer?viewmode=contents
"""

from Tkinter import *
import tkFileDialog
from ttk import *
import syslogc
import time
root = Tk()

root.title("GUI-SendingTool-Ray")
root.geometry('600x450')
root.resizable(width=False, height=True)
#警告
label = Label(root, foreground='red')
label.grid(row=12, column=0, columnspan=12, sticky=W)

radio_var = IntVar()
radio_var.set(1)
def sel_radio():
    """Radiobutton 实现协议选择"""
    v = radio_var.get()
    label.config(text='')
    if v == 1:
        return v
    else:
        label.config(text = "SNMP协议暂时不可用！")
Label(root, text='协议：').grid(row=0, sticky=E)
Radiobutton1 = Radiobutton(root, text='Syslog', variable=radio_var, value=1, command=sel_radio)
Radiobutton1.grid(row=0, column=1, sticky=W)
Radiobutton2 = Radiobutton(root, text='SNMP', variable=radio_var, value=2, command=sel_radio)
Radiobutton2.grid(row=0, column=2, sticky=W)


#使用sticky参数  默认的空间会在网格中居中显示。你可以使用sticky选项去指定对齐方式，可以选择的值有：N/S/E/W，分别代表上/下/左/右。
value = True
def sendlog():
    """按钮发送功能"""
    global value
    if sel_radio() == 1:
        while True:
            if value:
                time.sleep(1)
                syslogc.test()
            else:
                print 'stop'
                return 0
    elif sel_radio() == 2:
        print "暂不可用！"
    else:
        print "GG!"

def stopsend():
    global value
    value = False
Sendbtn = Button(root, text='发送', command= sendlog)
Sendbtn.grid(row=0, column=6, rowspan=1, sticky=W+E+S+N, padx=5, pady=5)
Sendbtn = Button(root, text='停止', command= stopsend)
Sendbtn.grid(row=0, column=8, rowspan=1, sticky=W+E+S+N, padx=5, pady=5)
#分割线...
Label(root, text='__'*56, foreground='gray').grid(row=1, column=0, columnspan=12)
Label(root, text='消息设置：').grid(row=2, column=0, columnspan=1, sticky=E)

def sel_filetype(event):
    """下拉框选择日志读取格式"""
    print filetypeCombo.get()
filetype_index = 0
filetypeCombo = Combobox(root, state='readonly')
filetypeCombo['values'] = ['从文件选择', '从文本框选择']
filetypeCombo.grid(row=2, column=1, columnspan=4, sticky=W)
filetypeCombo.current(filetype_index)
filetypeCombo.bind('<<ComboboxSelected>>', sel_filetype)


def sel_logtype(event):
    """下拉框选择日志类型样本"""
    print logtypeCombo.get()

Label(root, text='选择日志样本：').grid(row=2, column=4, sticky=E)
logtype_index = 0
logtypeCombo = Combobox(root, state='readonly')
logtypeCombo['values'] = ['Jump漏动扫描', 'Jump信息审计', 'JumpIPS', 'Jump防火墙', 'Jump上网行为', 'Jump主机审计', 'Cisco路由器', 'H3C交换机']
logtypeCombo.grid(row=2, column=5, columnspan=10, sticky=W)
logtypeCombo.current(filetype_index)
logtypeCombo.bind('<<ComboboxSelected>>', sel_logtype)
Label(root, text=' ').grid(row=3, column=0, sticky=E)
e = StringVar()

#文件路径文本框
filepath = Entry(root, textvariable=e, width=65, foreground='gray', state='readonly')
e.set('请选择日志文件')
filepath.grid(row=4, column=0, columnspan=8, sticky=W)

def checkfile():
    """选择syslog样例文件"""
    filename = tkFileDialog.askopenfilename()
    e.set(filename)
    print filename
    return filename
checkbtn = Button(root, text='. . .', command=checkfile)
checkbtn.grid(row=4, column=8)

#日样例文本域
Label(root, text='文本域：').grid(row=5,sticky=W)
Text(root, width=80, height=8).grid(row=6, column=0, columnspan=10, sticky=W)

#接收地址配置
Label(root, text='目的端设置：').grid(row=7, column=0, sticky=W)


# """选中listbox中一行"""
# def print_item(event):
#     print lb.get(lb.curselection())
list = Treeview(height="4", columns=("ID","IP","PORT"), selectmode="extended")
list.heading('#1', text='ID', anchor='center')
list.heading('#2', text='IP', anchor='center')
list.heading('#3', text='端口', anchor='center')
list.column('#1', stretch=NO, minwidth=0, width=100)
list.column('#2', stretch=NO, minwidth=0, width=200)
list.column('#3', stretch=NO, minwidth=0, width=140)
list.column('#0', stretch=NO, minwidth=0, width=0) #width 0 to not display it
list.grid(row=8, column=0, rowspan=3, columnspan=7, sticky='w')

def add_btn():
    addtl = Toplevel()
    addtl.title('添加接收地址')
    addtl.geometry('400x100')
    addtl.resizable(width=False, height=False)
    firstline = Label(addtl, text='  ')
    firstline.grid(row=0)
    iplabel = Label(addtl, text='IP地址：')
    iplabel.grid(row=1, column=0, sticky=W)
    ipvalue = Entry(addtl)
    ipvalue.grid(row=1, column=1)
    protlabel = Label(addtl, text='端口：')
    protlabel.grid(row=1, column=2, sticky=W)
    protvalue = Entry(addtl)
    protvalue.grid(row=1, column=3)
    ok = Button(addtl, text='确定')
    ok.grid(row=2, column=0, columnspan=2, sticky=E)
    cancel = Button(addtl, text='取消', command=addtl.destroy)
    cancel.grid(row=2, column=3, columnspan=4, sticky=W)

addbtn = Button(root, text='添加', command=add_btn)
addbtn.grid(row=8, column=8, rowspan=1, sticky=W+E+S+N, padx=5, pady=5)
addbtn = Button(root, text='编辑')
addbtn.grid(row=9, column=8, rowspan=1, sticky=W+E+S+N, padx=5, pady=5)
addbtn = Button(root, text='删除')
addbtn.grid(row=10, column=8, rowspan=1, sticky=W+E+S+N, padx=5, pady=5)

# lb.bind('<buttonrelease-1>', print_item)
# list_item = [1,2,3,4,5,6,7,8,9,0]x
# for item in list_item:
#     lb.insert(end, item)
# scrl = scrollbar(root)
# scrl.pack(side=right, fill=y)
# lb.configure(yscrollcommand = scrl.set)
# lb.pack(side=left, fill=both)
# scrl['command'] = lb.yview

root.mainloop()

#选择目录
# dirname=tkFileDialog.askdirectory()
#选择文件
# fname = tkFileDialog.askopenfilename()
# print fname
# print dirname
