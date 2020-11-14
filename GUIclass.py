import tkinter as tk 
from tkinter import ttk 
from TestbenchCreator import giveGUIinfo

LARGEFONT =("Verdana", 35)
class TBApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) 
          
        # creating a container 
        container = tk.Frame(self)   
        container.pack(side = "top", fill = "both", expand = True)  
   
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 
   
        # initializing frames to an empty array 
        self.frames = {}   
   
        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (StartPage, ResultsPage): 
   
            frame = F(container, self) 
   
            # initializing frame of that object from 
            # startpage, page1, page2 respectively with  
            # for loop 
            self.frames[F] = frame  
   
            frame.grid(row = 0, column = 0, sticky ="nsew") 
   
        self.show_frame(StartPage) 
   
    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise() 

class StartPage(tk.Frame):

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller 
        #Entry for the txt  and root separation
        self.TestBench_Text = tk.Text(self)
        self.TestBench_Text.grid(column = 0, row = 0, padx = 10, pady= 10, sticky = "nsew")
        self.mainframe = ttk.Frame(self, padding = "10 10 10 10")
        self.mainframe.grid(column = 0, row = 1, padx = 10, pady = 10, sticky= "nsew")
        Buttonsframe = ttk.Frame(self, padding = "10 10 10 10")
        Buttonsframe.grid(column = 0, row = 2, sticky = "nsew")

        #frames inside mainframe
        SoCframe = ttk.Frame(self.mainframe, padding = "10 10 10 10", borderwidth = 0.5, relief = "sunken")
        SoCframe.grid(column = 0, row = 0, sticky = "nsew")
        self.Timeframe = ttk.Frame(self.mainframe,  padding = "10 10 10 10", borderwidth = 0.5, relief = "sunken")
        self.Timeframe.grid(column = 1, row = 0, sticky ="nsew")
        SecOpframe = ttk.Frame(self.mainframe, padding = "10 10 10 10", borderwidth = 0.5, relief = "sunken")
        SecOpframe.grid(column = 2, row = 0, sticky = "nsew")
        Extframe = ttk.Frame(self.mainframe, padding = "10 10 10 10", borderwidth = 0.5, relief = "sunken")
        Extframe.grid(column = 3, row = 0, sticky = "nsew")


        #frames inside Extframe
        Clkframe = ttk.Frame(Extframe, padding = "10 10 10 10")
        Clkframe.grid(column = 0, row = 1, sticky  = "nsew")
        Rstframe = ttk.Frame(Extframe, padding = "10 10 10 10")
        Rstframe.grid(column = 0, row = 2, sticky = "nsew")


        #in case the user resize it
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)

        #Sequential RadioButtons creation 
        self.SecoCom = tk.StringVar()
        ComRadio = ttk.Radiobutton(SoCframe, text = "Combinational", variable = self.SecoCom, value = "Com", command = lambda: self.disableSeq(SecOpframe.winfo_children()))
        SeqRadio = ttk.Radiobutton(SoCframe, text = "Secuencial", variable = self.SecoCom, value = "Seq", command = lambda: self.enableSeq(SecOpframe.winfo_children()))
        ComRadio.grid(column = 0, row = 1, sticky ="w")
        SeqRadio.grid(column = 0, row = 2, sticky ="w")
        self.SecoCom.set("Com")

        #Creation of the timescale combobox
        TimeScale_Label = ttk.Label(self.Timeframe, text = "Timescale: ",justify = "center").grid(column = 0, row = 1, sticky="w")
        self.TimeScale_Combo= ttk.Combobox(self.Timeframe, state = ["readonly"])
        self.TimeScale_Combo["values"] = ["1ns/1ns", "10ns/1ns", "1ns/1ps"]
        self.TimeScale_Combo.grid(column = 1, row = 1, sticky = "nsew")
        self.TimeScale_Combo.current(1)

        #delay entry creation
        Delay_Label = ttk.Label(self.Timeframe, text = "#Delay Satements: ", justify = "left"). grid(column = 0, row =3, sticky ="w")
        self.Delay_Combo= ttk.Combobox(self.Timeframe, state = ["readonly"])
        self.Delay_Combo["values"] = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.Delay_Combo.grid(column = 1, row = 3, sticky = "nsew")
        self.Delay_Combo.current(1)

        #Checkbuttons for clk and rst
        self.ClkState = tk.StringVar()
        CheckClk = tk.Checkbutton(SecOpframe, text = "Clk", variable = self.ClkState, onvalue = "0", offvalue = "1", state = "disabled", command = lambda: self.enableFrame(self.ClkState, Clkframe.winfo_children()))
        CheckClk.grid(column = 0, row = 0, sticky ="w")
        self.RstState = tk.StringVar()
        CheckRst = tk.Checkbutton(SecOpframe, text = "Rst", variable = self.RstState, onvalue = "0", offvalue = "1", state = "disabled", command = lambda: self.enableFrame(self.RstState, Rstframe.winfo_children()));
        CheckRst.grid(column = 0, row = 1, sticky="w")

        #Creation of the clk's name option
        Clk_Label = ttk.Label(Clkframe, text = "Clk's Name: ", justify = "left")
        Clk_Label.grid(column = 1, row =0, sticky ="w")
        self.Clk = tk.StringVar()
        self.Clk_Entry = ttk.Entry(Clkframe, width = 16, textvariable = self.Clk, justify = "center")
        self.Clk_Entry.grid(column = 2, row = 0, sticky = "nsew")

        #Creation of the reset combobox, for active high or active low options
        Rst_Label = ttk.Label(Rstframe, text = "Reset: ", justify = "left")
        Rst_Label.grid(column = 0, row =0, sticky ="w")
        self.Rst_Combo= ttk.Combobox(Rstframe, width = 15, justify = "center", state = ["readonly"])
        self.Rst_Combo["values"] = ["", "Active High", "Active Low"]
        self.Rst_Combo.grid(column = 1, row = 0, sticky = "nsew")
        self.Rst_Combo.current(0)
        RstName_Label = ttk.Label(Rstframe, text = "Name: ", justify = "left")
        RstName_Label.grid(column = 0, row =2, sticky ="w")
        self.RstName = tk.StringVar()
        self.Rst_Entry = ttk.Entry(Rstframe, width = 16, textvariable = self.RstName, justify = "center")
        self.Rst_Entry.grid(column = 1, row = 2, sticky = "nsew")


        AcceptButton = ttk.Button(Buttonsframe, text = "Accept", command = self.TBGenerator)
        AcceptButton.pack(side = "right")
        CancelButton = ttk.Button(Buttonsframe, text = "Cancel", command = self.EraseEverything)
        CancelButton.pack(side = "right")

        for child in Clkframe.winfo_children():
            child.configure(state = "disabled")

        for child in Rstframe.winfo_children():
            child.configure(state = "disabled")

        for child in self.Timeframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        for child in SecOpframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        for child in SoCframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)


    def enableFrame(self, OnOff, childList):
        if (OnOff.get() == '1'):
            for child in childList: 
                child.configure(state = "disabled")
        if (OnOff.get() == '0'):
            for child in childList: 
                child.configure(state = "normal")

    def enableSeq(self, childList):
        self.ClkState.set("1")
        self.RstState.set("1")
        for child in childList: 
            child.configure(state = "normal")
            
    def disableSeq(self, childList):
        self.Clk_Entry.delete(0, 'end')
        self.Rst_Combo.current(0)
        self.Rst_Entry.delete(0, 'end')
        for child in childList: 
            child.configure(state = "disabled")
        self.ClkState.set("0")
        self.RstState.set("0")
        self.Clk_Entry.config(state = "disabled")
        self.Rst_Entry.config(state = "disabled")
        self.Rst_Combo.config(state = "disabled")

    def EraseEverything(self):
        self.TestBench_Text.delete("1.0", "end")
        self.Delay_Combo.current(0)
        self.TimeScale_Combo.current(0)
        self.Clk_Entry.delete(0, 'end')
        self.Rst_Combo.current(0)
        self.Rst_Entry.delete(0,'end')

    def TBGenerator(self):
        print("\n\nAccept")
        #print ("Text Box: ",TestBench_Text.get("1.0", END))
        print ("RadioButtom: ",self. SecoCom.get())
        print("TimeScale: ", self.TimeScale_Combo.get())
        print ("#Delays: ", self.Delay_Combo.get())
        print ("Clks Name: ", self.Clk.get())
        print("Reset: ", self.Rst_Combo.get())
        print ("Rst's Name: ", self.Rst_Entry.get())
        self.TestBench_Text.delete("1.0", 'end')
        self.TimeScale_Combo.current(0)
        self.Clk_Entry.delete(0, 'end')
        self.Rst_Combo.current(0)
        self.Rst_Entry.delete(0,'end')
        self.controller.show_frame(ResultsPage)


# second window frame page1  
class ResultsPage(tk.Frame): 

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        #Entry for the txt  and root separation
        TestBench_Text = tk.Text(self)
        TestBench_Text.pack(side = "top", padx= 10, pady= 10, fill = "both", expand = True)
        Buttonsframe = ttk.Frame(self, padding = "10 10 10 10")
        Buttonsframe.pack(side = "bottom", fill = "x", expand = True)
    
       

        AcceptButton = ttk.Button(Buttonsframe, text = "Accept")
        AcceptButton.pack(side = "right")
        CancelButton = ttk.Button(Buttonsframe, text = "Cancel", command = lambda : controller.show_frame(StartPage))
        CancelButton.pack(side = "right")

    

# Driver Code 
app = TBApp() 
app.mainloop() 