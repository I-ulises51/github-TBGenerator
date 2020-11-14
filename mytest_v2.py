from tkinter import * 
from tkinter import ttk 
from TestbenchCreator import giveGUIinfo

def my_print(*args):
    print("\n\nAccept")
    #print ("Text Box: ",TestBench_Text.get("1.0", END))
    print ("RadioButtom: ", SecoCom.get())
    print("TimeScale: ", TimeScale_Combo.get())
    print ("#Delays: ", Delay_Combo.get())
    print ("Clks Name: ", Clk.get())
    print("Reset: ", Rst_Combo.get())
    print ("Rst's Name: ", Rst_Entry.get())
    giveGUIinfo(TestBench_Text.get("1.0", END),
                TimeScale_Combo.get(),
                Delay_Combo.get(),
                SecoCom.get(),
                Clk.get(), 
                Rst_Combo.get(),
                Rst_Entry.get()) 

    TestBench_Text.delete("1.0", END)
    TimeScale_Combo.current(0)
    Clk_Entry.delete(0, 'end')
    Rst_Combo.current(0)
    Rst_Entry.delete(0,'end')
    
def enableFrame(OnOff, childList):
    if (OnOff.get() == '1'):
        for child in childList: 
            child.configure(state = DISABLED)
    if (OnOff.get() == '0'):
        for child in childList: 
            child.configure(state = NORMAL)

def enableSeq(childList):
    ClkState.set("1")
    RstState.set("1")
    for child in childList: 
        child.configure(state = NORMAL)
        
def disableSeq(childList):
    Clk_Entry.delete(0, 'end')
    Rst_Combo.current(0)
    Rst_Entry.delete(0, 'end')
    for child in childList: 
        child.configure(state = DISABLED)
    ClkState.set("0")
    RstState.set("0")
    Clk_Entry.config(state = DISABLED)
    Rst_Entry.config(state = DISABLED)
    Rst_Combo.config(state = DISABLED)

def EraseEverything():
    TestBench_Text.delete("1.0", END)
    Delay_Combo.current(0)
    TimeScale_Combo.current(0)
    Clk_Entry.delete(0, 'end')
    Rst_Combo.current(0)
    Rst_Entry.delete(0,'end')
    

#setting up the window
root = Tk()
root.title("Testbench Template Generator")


#Entry for the txt  and root separation
TestBench_Text = Text(root)
TestBench_Text.grid(column = 0, row = 0, padx = 10, pady= 10, sticky = NSEW)
mainframe = ttk.Frame(root, padding = "10 10 10 10")
mainframe.grid(column = 0, row = 1, padx = 10, pady = 10, sticky= NSEW)
Buttonsframe = ttk.Frame(root, padding = "10 10 10 10")
Buttonsframe.grid(column = 0, row = 2, sticky = NSEW)

#frames inside mainframe
SoCframe = ttk.Frame(mainframe, padding = "10 10 10 10", borderwidth = 0.5, relief = SUNKEN)
SoCframe.grid(column = 0, row = 0, sticky =NSEW)
Timeframe = ttk.Frame(mainframe,  padding = "10 10 10 10", borderwidth = 0.5, relief = SUNKEN)
Timeframe.grid(column = 1, row = 0, sticky =NSEW)
SecOpframe = ttk.Frame(mainframe, padding = "10 10 10 10", borderwidth = 0.5, relief = SUNKEN)
SecOpframe.grid(column = 2, row = 0, sticky =NSEW)
Extframe = ttk.Frame(mainframe, padding = "10 10 10 10", borderwidth = 0.5, relief = SUNKEN)
Extframe.grid(column = 3, row = 0, sticky = NSEW)


#frames inside Extframe
Clkframe = ttk.Frame(Extframe, padding = "10 10 10 10")
Clkframe.grid(column = 0, row = 1, sticky = NSEW)
Rstframe = ttk.Frame(Extframe, padding = "10 10 10 10")
Rstframe.grid(column = 0, row = 2, sticky = NSEW)


#in case the user resize it
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)
root.rowconfigure(1, weight = 1)
root.rowconfigure(2, weight = 1)
root.rowconfigure(3, weight = 1)

#Sequential RadioButtons creation 
SecoCom = StringVar()
ComRadio = ttk.Radiobutton(SoCframe, text = "Combinational", variable = SecoCom, value = "Com", command = lambda: disableSeq(SecOpframe.winfo_children()))
SeqRadio = ttk.Radiobutton(SoCframe, text = "Secuencial", variable = SecoCom, value = "Seq", command = lambda: enableSeq(SecOpframe.winfo_children()))
ComRadio.grid(column = 0, row = 1, sticky = W)
SeqRadio.grid(column = 0, row = 2, sticky = W)
SecoCom.set("Com")

#Creation of the timescale combobox
TimeScale_Label = ttk.Label(Timeframe, text = "Timescale: ",justify = CENTER).grid(column = 0, row = 1, sticky=W)
TimeScale_Combo= ttk.Combobox(Timeframe, state = ["readonly"])
TimeScale_Combo["values"] = ["1ns/1ns", "10ns/1ns", "1ns/1ps"]
TimeScale_Combo.grid(column = 1, row = 1, sticky = NSEW)
TimeScale_Combo.current(1)

#delay entry creation
Delay_Label = ttk.Label(Timeframe, text = "#Delay Satements: ", justify = LEFT). grid(column = 0, row =3, sticky = W)
Delay_Combo= ttk.Combobox(Timeframe, state = ["readonly"])
Delay_Combo["values"] = ["1", "2", "3", "4", "5", "6", "7", "8"]
Delay_Combo.grid(column = 1, row = 3, sticky = NSEW)
Delay_Combo.current(1)

#Checkbuttons for clk and rst
ClkState = StringVar()
CheckClk = Checkbutton(SecOpframe, text = "Clk", variable = ClkState, onvalue = "0", offvalue = "1", state = DISABLED, command = lambda: enableFrame(ClkState, Clkframe.winfo_children()))
CheckClk.grid(column = 0, row = 0, sticky = W)
RstState = StringVar()
CheckRst = Checkbutton(SecOpframe, text = "Rst", variable = RstState, onvalue = "0", offvalue = "1", state = DISABLED, command = lambda: enableFrame(RstState, Rstframe.winfo_children()));
CheckRst.grid(column = 0, row = 1, sticky= W)

#Creation of the clk's name option
Clk_Label = ttk.Label(Clkframe, text = "Clk's Name: ", justify = LEFT)
Clk_Label.grid(column = 1, row =0, sticky = W)
Clk = StringVar()
Clk_Entry = ttk.Entry(Clkframe, width = 16, textvariable = Clk, justify = CENTER)
Clk_Entry.grid(column = 2, row = 0, sticky = NSEW)

#Creation of the reset combobox, for active high or active low options
Rst_Label = ttk.Label(Rstframe, text = "Reset: ", justify = LEFT)
Rst_Label.grid(column = 0, row =0, sticky = W)
Rst_Combo= ttk.Combobox(Rstframe, width = 15, justify = CENTER, state = ["readonly"])
Rst_Combo["values"] = ["", "Active High", "Active Low"]
Rst_Combo.grid(column = 1, row = 0, sticky = NSEW)
Rst_Combo.current(0)
RstName_Label = ttk.Label(Rstframe, text = "Name: ", justify = LEFT)
RstName_Label.grid(column = 0, row =2, sticky = W)
RstName = StringVar()
Rst_Entry = ttk.Entry(Rstframe, width = 16, textvariable = RstName, justify = CENTER)
Rst_Entry.grid(column = 1, row = 2, sticky = NSEW)


AcceptButton = ttk.Button(Buttonsframe, text = "Accept", command = my_print)
AcceptButton.pack(side = RIGHT)
CancelButton = ttk.Button(Buttonsframe, text = "Cancel", command = EraseEverything)
CancelButton.pack(side = RIGHT)


for child in Clkframe.winfo_children():
    child.configure(state = DISABLED)

for child in Rstframe.winfo_children():
    child.configure(state = DISABLED)

for child in Timeframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

for child in SecOpframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

for child in SoCframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)


root.mainloop()