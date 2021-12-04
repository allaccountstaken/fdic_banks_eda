from tkinter import *
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
'''
Developer Notes: 
Year Range is from 2000-2020, User can determine year range within those years to create more specific charts
'''
def click():
    print("Something is happening")
###main:
def FilterDF(df, cols_keep, date_col, class_col, filter_criteria={}, start_year=2000, end_year=2020):

    # Ensure Correct Data Types
    if type(cols_keep) != list:
        cols_keep = [cols_keep]

    # Extract Desired Columns
    df_clean = df[cols_keep].copy()
    
    # Convert Date Column to DateTime
    df_clean[date_col] = pd.to_datetime(df_clean[date_col])

    # Filter Date Column To Desired Range (2000-2020 defualt)
    df_clean = df_clean.loc[(df_clean[date_col].dt.year >= start_year) & 
                            (df_clean[date_col].dt.year <= end_year)]

    # Filter Anything Not Needed
    if filter_criteria != {}:
        for key in filter_criteria.keys():
            df_clean = df_clean.loc[df_clean[key] == filter_criteria[key]]

    # Filter Class Type != Savings or Commercial
    df_clean = df_clean.loc[(df_clean[class_col] == 'Savings') |
                            (df_clean[class_col] == 'Commercial')
                            ].reset_index(drop=True)

    

    return df_clean

def CountByYear(df, class_col, date_col, count_col):

    # Count Cert IDs by Year
    df_by_year = df.groupby([class_col, df[date_col].dt.year]).count()[count_col].reset_index()
    df_by_year.columns = ['Class Type', 'Year', 'Count']

    # Fill in Missing Years
    for year in range(2000, 2021):
        temp_com = df_by_year.loc[(df_by_year['Year'] == year) &
                                  (df_by_year['Class Type'] == 'Commercial')]
        temp_sav = df_by_year.loc[(df_by_year['Year'] == year) &
                                  (df_by_year['Class Type'] == 'Savings')]
        if len(temp_com) != 1:
            df_by_year = df_by_year.append({'Class Type': 'Commercial', 'Year': year, 'Count': 0}, ignore_index=True)
        if len(temp_sav) != 1:
            df_by_year = df_by_year.append({'Class Type': 'Savings', 'Year': year, 'Count': 0}, ignore_index=True)

    # Sort DataFrame
    df_by_year = df_by_year.sort_values(by=['Class Type', 'Year']).reset_index(drop=True)

    # Reformat DataFrame
    df_by_year_reformat = pd.DataFrame(df_by_year.loc[df_by_year['Class Type'] == 'Commercial', 'Year'])
    df_by_year_reformat['Commercial'] = list(df_by_year.loc[df_by_year['Class Type'] == 'Commercial', 'Count'])
    df_by_year_reformat['Savings'] = list(df_by_year.loc[df_by_year['Class Type'] == 'Savings', 'Count'])

    return df_by_year_reformat



def plot(liquidations, new_institutions, combinations, failures, last_generated):
    def newInstitutions():
        GenerateHistogram(ni2_cnts, 'New Institutions')
        last_generated[0] = 'NewInstitutions'
    def liquidInstitutions():
        GenerateHistogram(li2_cnts, 'Liquidations')
        last_generated[0] = 'Liquidations'
    def combInstitutions():
        GenerateHistogram(co2_cnts, 'Combinations')
        last_generated[0] = 'Combinations'
    def failInstitutions():
        GenerateHistogram(fa2_cnts, 'Failures')
        last_generated[0] = 'Failures'
    def GenerateHistogram(df, category):
        min = int(minyear.get())
        max = int(maxyear.get())
        # Generate Figure
      
        fig, axis = plt.subplots(figsize=(12, 5))

        # Filter Year to Desired Time Frame
        df = df.loc[(df['Year'] >= min) & (df['Year'] <= max)
                ].reset_index(drop=True).copy()

        # Plot
        df.plot(kind='bar', x='Year', ax=axis)

        # Label Plot
        axis.set_ylabel(f'Count of {category}', size=10)
        axis.set_xlabel('Year', size=10)
        axis.set_title(f'{category} by Year', size=15)
        axis.tick_params(axis='x', labelsize=7, labelrotation=0)
        axis.tick_params(axis='y', labelsize=7)
        axis.legend(fontsize=10)

        # Write Counts Above Bars
        for i, v in enumerate(df['Commercial']):
            axis.text(i-0.123, 1.01*v, str(v), color='blue', fontweight='bold', horizontalalignment='center', size=8)
        for i, v in enumerate(df['Savings']):
            axis.text(i+0.123, 1.01*v, str(v), color='chocolate', fontweight='bold', horizontalalignment='center', size=8)

        # Show Figure
      
        canvas = FigureCanvasTkAgg(fig,
                               master = window)  
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, column=6, sticky=W)


    def download():
        verisonToDownload = last_generated[0]
        if verisonToDownload == 'NewInstitutions':
            df = ni2.copy()
        elif verisonToDownload == "Liquidations":
            df = li2.copy()
            df = df[df.columns[0:3]]
        elif verisonToDownload == "Combinations":
            df = co2.copy()
        elif verisonToDownload =="Failures":
            df = fa2.copy()
        else:
            print("tbd")
        df.columns = ['Cert_ID', 'Class_Type', 'Effective_Date']
        df['Change_Type'] = verisonToDownload
       
        min = int(minyear.get())
        max = int(maxyear.get())
        df = df.loc[(df['Effective_Date'].dt.year >= min) & (df['Effective_Date'].dt.year <= max)].reset_index(drop=True)
        df = df.sort_values(by=['Effective_Date']).reset_index(drop = True)
        df.to_csv(f'data/data_outputs/{verisonToDownload}_{min}_to_{max}.csv')
    
    def definitions():
        textOutput = "New Bank: A New Bank is a bank that has been created in the corresponding year. New banks have xyz.\n Failed Bank: A failed bank is a bank that has failed.\nLiquidated Bank: A bank that has been liquidated means that everyone inside has been turned into a giant smoothie to give to Jeff Besos to drink."
        output.insert(END, textOutput)
    #create label
    #include image
    #photo1 = PhotoImage(file="brand.gif")
    #Label(window, image=photo1, bg = "black").grid(row=0, column=0, sticky=E)
    ni2 = FilterDF(new_institutions, ['CERT', 'FRM_CLASS_TYPE_DESC', 'EFFDATE'], 'EFFDATE', 'FRM_CLASS_TYPE_DESC')
    li2 = FilterDF(liquidations, ['CERT', 'FRM_CLASS_TYPE_DESC', 'EFFDATE', 'CHANGECODE_DESC'], 'EFFDATE', 
            'FRM_CLASS_TYPE_DESC', filter_criteria={'CHANGECODE_DESC': 'FINANCIAL DIFFICULTY - PAYOFF'})
    co2 = FilterDF(combinations, ['CERT', 'ACQ_CLASS_TYPE_DESC', 'EFFDATE'], 'EFFDATE', 'ACQ_CLASS_TYPE_DESC')
    fa2 = FilterDF(failures, ['CERT', 'ACQ_CLASS_TYPE_DESC', 'EFFDATE'], 'EFFDATE', 'ACQ_CLASS_TYPE_DESC')

    ni2_cnts = CountByYear(ni2, 'FRM_CLASS_TYPE_DESC', 'EFFDATE', 'CERT')
    li2_cnts = CountByYear(li2, 'FRM_CLASS_TYPE_DESC', 'EFFDATE', 'CERT')
    co2_cnts = CountByYear(co2, 'ACQ_CLASS_TYPE_DESC', 'EFFDATE', 'CERT')
    fa2_cnts = CountByYear(fa2, 'ACQ_CLASS_TYPE_DESC', 'EFFDATE', 'CERT')
    
    window = Tk()
    window.title("FDIC Data - DS5100")

    #create entry for years
    Label(window, text= "Min Year:", bg="white", fg = "black", font="none 12 bold").grid(row=3,  column=2, sticky=W)
    minyear = Entry(window, width = 10, bg = "white")
    minyear.grid(row=3, column = 3, sticky =W)

    Label(window, text= "Max Year:", bg="white", fg = "black", font="none 12 bold").grid(row=3,  column=4, sticky=W)
    maxyear = Entry(window, width = 10, bg = "white")
    maxyear.grid(row=3, column = 5, sticky =W) 

    #------NEW INSTITUITONS------#
    Button(window, text="NEW BANKS", width = 15, command=newInstitutions).grid(row=7, column = 3, sticky = W)
    #create label for text
    #Label(window, text= "See New Banks:", bg="white", fg = "black", font="none 12 bold").grid(row=6,  column=2, sticky=W)
   
   #---------FAILED BANKS--------#
    #Label(window, text= "See Failed Banks:", bg="white", fg = "black", font="none 12 bold").grid(row=6,  column=4, sticky=W)
    Button(window, text="FAILED BANKS", width = 15, command=failInstitutions).grid(row=7, column = 5, sticky = W)


    #------LIQUIDATED BANKS-----#
    #Label(window, text= "See Liquidated Banks:", bg="white", fg = "black", font="none 12 bold").grid(row=6,  column=6, sticky=W)
    Button(window, text="LIQUIDATED BANKS", width = 15, command=liquidInstitutions).grid(row=7, column = 7, sticky = W)

    #-----Combination Banks-----#
    #Label(window, text= "See Liquidated Banks:", bg="white", fg = "black", font="none 12 bold").grid(row=6,  column=6, sticky=W)
    Button(window, text="COMBINED BANKS", width = 15, command=combInstitutions).grid(row=7, column = 9, sticky = W)

    #Label(window, text = "Definitions",bg="white", fg = "black", font="none 12 bold").grid(row=9,  column=6, sticky=W) 
    #Button(window, text="DEFINITIONS HELP", command=definitions).grid(row=10, column = 6, columnspan=2, sticky = W)

    #output = Text(window, width=75, height=6, wrap = WORD, background = "white")

    #output.grid(row=11, column=6, columnspan=2, sticky=W)
    
    #-------Download Data Button---------#
    Button(window, text="DOWNLOAD DATA", width = 15, command =download).grid(row=10, column = 7, sticky = W)

    window.mainloop()

def main(): 
    #Read in the CSV files 
    liquidations = pd.read_csv('data/Liquidations_10_21_2021.csv')
    new_institutions = pd.read_csv("data/New_Institutions_10_21_2021.csv")
    combinations = pd.read_csv('data/Business_Combinations_10_21_2021.csv')
    failures = pd.read_csv('data/Business_Combinations_-_Failures_10_21_2021.csv')
    last_generated = ['test']
    
    plot(liquidations, new_institutions, combinations, failures, last_generated)
main()