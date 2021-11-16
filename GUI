from tkinter import *
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

def click():
    print("Something is happening")
###main:

def plot():
    def plot_new():
        min = int(minyear.get())
        max = int(maxyear.get())
        
        new_institutions = pd.read_csv("data/New_Institutions_10_21_2021.csv")
        new_x = new_institutions[['EFFYEAR', "CLASS_TYPE", 'CERT']]
        new_x = new_x[new_x['EFFYEAR']>=min]
        new_x = new_x[new_x['EFFYEAR']<=max]
     
        comb_new_by_year = new_x.groupby(['CLASS_TYPE', 'EFFYEAR']).count()['CERT'].reset_index()
        comb_new_by_year.columns = ['Class Type', 'Effective Year', 'Count']
        for year in range(min, max):
            temp_com = comb_new_by_year.loc[(comb_new_by_year['Effective Year'] == year) &
                                                (comb_new_by_year['Class Type'] == 'C')]
            temp_sav = comb_new_by_year.loc[(comb_new_by_year['Effective Year'] == year) &
                                                (comb_new_by_year['Class Type'] == 'S')]
            if len(temp_com) != 1:
                comb_new_by_year = comb_new_by_year.append({'Class Type': 'C', 'Effective Year': year, 'Count': 0}, ignore_index=True)
            if len(temp_sav) != 1:
                comb_new_by_year = comb_new_by_year.append({'Class Type': 'S', 'Effective Year': year, 'Count': 0}, ignore_index=True)

        comb_new_by_year = comb_new_by_year.sort_values(by=['Class Type', 'Effective Year']).reset_index(drop=True)

        comb_new_by_year_reformat = pd.DataFrame(comb_new_by_year.loc[comb_new_by_year['Class Type'] == 'C', 'Effective Year'])
        comb_new_by_year_reformat['C'] = list(comb_new_by_year.loc[comb_new_by_year['Class Type'] == 'C', 'Count'])
        comb_new_by_year_reformat['S'] = list(comb_new_by_year.loc[comb_new_by_year['Class Type'] == 'S', 'Count'])
        
        
        fig, axis = plt.subplots(figsize=(10, 5))

        comb_new_by_year_reformat.plot(kind='bar', x='Effective Year', ax=axis)

        axis.set_ylabel('Count of New Institutions', size=8)
        axis.set_xlabel('Effective Year', size=8)
        axis.set_title('New Institutions by Year', size=11)

        axis.tick_params(axis='x', labelsize=7, labelrotation=0)
        axis.tick_params(axis='y', labelsize=7)

        axis.legend(fontsize=8)

        for i, v in enumerate(comb_new_by_year_reformat['C']):
            axis.text(i-0.13, v+1, str(v), color='blue', fontweight='bold', horizontalalignment='center')
        for i, v in enumerate(comb_new_by_year_reformat['S']):
            axis.text(i+0.13, v+1, str(v), color='orange', fontweight='bold', horizontalalignment='center')


   

        canvas = FigureCanvasTkAgg(fig,
                               master = window)  
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, column=6, sticky=W)
        # placing the canvas on the Tkinter window


    def definitions():
        textOutput = "New Bank: A New Bank is a bank that has been created in the corresponding year. New banks have xyz.\n Failed Bank: A failed bank is a bank that has failed.\nLiquidated Bank: A bank that has been liquidated means that everyone inside has been turned into a giant smoothie to give to Jeff Besos to drink."
        output.insert(END, textOutput)
    #create label
    #include image
    #photo1 = PhotoImage(file="brand.gif")
    #Label(window, image=photo1, bg = "black").grid(row=0, column=0, sticky=E)
    window = Tk()
    window.title("FDIC Data - DS5100")

    #create entry for years
    Label(window, text= "Min Year:", bg="white", fg = "black", font="none 12 bold").grid(row=3,  column=2, sticky=W)
    minyear = Entry(window, width = 10, bg = "white")
    minyear.grid(row=3, column = 3, sticky =W)

    Label(window, text= "Max Year:", bg="white", fg = "black", font="none 12 bold").grid(row=3,  column=4, sticky=W)
    maxyear = Entry(window, width = 10, bg = "white")
    maxyear.grid(row=3, column = 5, sticky =W) 
    Button(window, text="NEW BANKS", width = 15, command=plot_new).grid(row=7, column = 3, sticky = W)
    #create label for text
    Label(window, text= "See New Banks:", bg="white", fg = "black", font="none 12 bold").grid(row=6,  column=2, sticky=W)
   
    Label(window, text= "See Failed Banks:", bg="white", fg = "black", font="none 12 bold").grid(row=6,  column=4, sticky=W)
    Button(window, text="FAILED BANKS", width = 15, command=click).grid(row=7, column = 5, sticky = W)
    Label(window, text= "See Liquidated Banks:", bg="white", fg = "black", font="none 12 bold").grid(row=6,  column=6, sticky=W)
    Button(window, text="LIQUIDATED BANKS", width = 15, command=click).grid(row=7, column = 7, sticky = W)


    Label(window, text = "Definitions",bg="white", fg = "black", font="none 12 bold").grid(row=9,  column=6, sticky=W) 
    Button(window, text="DEFINITIONS HELP", width = 30, command=definitions).grid(row=10, column = 6, columnspan=2, sticky = W)

    output = Text(window, width=75, height=6, wrap = WORD, background = "white")
    output.grid(row=11, column=6, columnspan=2, sticky=W)
    window.mainloop()

def main(): 

    plot()
main()
