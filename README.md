
# fdic_banks_eda

# Project Proposal

### INTRODUCTION
The project will provide explanatory data analysis (EDA) of banking industry historical evolution. It seems that the industry is going through a rapid consolidation as a number of regulated entities declined from 8,500 to roughly 5,000 in the last 20 years. 

From a preliminary survey, it appears that only 500 banks actually failed during these years, and consequently, 3,500 disappeared due to other reasons, such as mergers, charter changes and voluntary liquidation. The main objective of the EDA is to create visual explanations of this consolidation, i.e. historical trends and drivers. 

![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/Screen%20Shot%202021-10-21%20at%204.01.44%20PM.png)

### THE DATA
Federal Deposit Insurance Corporation (FDIC) is a United States government agency that examines and supervises the majority of commercial and savings banks (https://en.wikipedia.org/wiki/Federal_Deposit_Insurance_Corporation). The Corporation collects and maintains granular datasets describing the industry as a whole, as well as individual regulated entities. ![GUI_FileDownloaded](https://user-images.githubusercontent.com/32313952/144724028-a0729a0f-99ae-41f9-9e00-4716e2d43018.png)


Statutory Reports of Condition and Income (Call reports) are provided by the Examination Council via SOUP API: 
- https://cdr.ffiec.gov/public/ManageFacsimiles.aspx. 

General data are available to the public via REST API: 
- https://banks.data.fdic.gov/bankfind-suite/. 

Detailed Swagger documentation is available here: 
- https://banks.data.fdic.gov/docs/swagger.yaml. 
 
Moreover, FDIC web sites contain numerous HTML tables with aggregated information that can be obtained programmatically with Python requests library.

Insights we are aiming to produce are important because credit institutions are critical for community development and economic growth. Moreover, costs of financial restructuring, although are not directly endured by tax payers, are still unproductive and avoidable. Finally, understanding consolidation drivers can help inform direct fintech innovation and future  product development. 

### EXPERIMENTAL DESIGN
The data will be obtained from the official FDIC databases. Historical events will be queried using REST API and statutory reports will be obtained using SOAP connection. It is anticipated that two separated Python clients will be developed. Queries will be executed using report dates and unique entity identifiers, i.e. ID RSSD or FDIC Certificate Number.

It is also proposed that EDA will be following the waterfall chart pattern, https://en.wikipedia.org/wiki/Waterfall_chart, i.e. quarterly status: new entrants, mergers and spinoffs, and exits. This will require a tabular data format: rows being report dates and bank IDs, columns being event status and selected financial metrics. Expected format of the resulting table is provided below:

![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/Screen%20Shot%202021-11-21%20at%208.46.59%20PM.png)

### PROJECT MANAGEMENT
![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/Screen%20Shot%202021-11-21%20at%208.47.24%20PM.png) 

### RESULTS
It is anticipated that the summary plot will allow for visual querying of the dataset, i.e. what entities were added and removed from the set during a specific time period. Alternatively, command line interface will allow for manual examination of the dataset. 
![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/waterfall_example.png)

### TESTING
![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/Screen%20Shot%202021-11-21%20at%208.48.00%20PM.png)

### OUTCOME
The final product will provide a unique big picture view of the banking industry, what will help general public better understand trends and drivers of the recent consolidation. Moreover, it is anticipated that users will enjoy extensive filtering functionality and easy to understand visuals. Finally, the resulting dataset can be used for multi-class classifications because it will contain labels describing historical events as well as relevant financial metrics. 


# GUI
## GUI Dependencies: 
The GUI is not able to be run in a jupyter notebook. The dependencies of the GUI are
* tkinter
* matplotlib
* pandas

To install Tkinter using pip, use the command 

```pip install tk```

For additional assitance installing Tkinter: 
https://www.tutorialspoint.com/how-to-install-tkinter-in-python
## Directory:
For the program to run, ensure the program is running in the parent folder.

``` fdic_banks_eda/```
## Using the GUI

Below is a video demonstration of the GUI:

https://user-images.githubusercontent.com/32313952/144725567-918a2779-cffe-48d8-80b3-13e3aca28b4f.mp4


The GUI takes no command line arguments, it should run right away. 
When the GUI starts, this is the first window you will see:

![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/GUI_Pre_Input.png)

The interface has two text boxes, four buttons to generate visuals, and one button to download the data. 

To generate a view, enter the desired minimum and maximum years into the text boxes, and select the button for your desired view. This will generate the corresponding plot. 

Below is a view of all bank Liquidations from 2000-2015:

![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/GUI_Liquidations.png)

If you would like to download the data for a corresponding view, select the DOWNLOAD DATA button at the bottom of the chart. A confirmation message will appear below the title of the GUI to inform the user that the data has been downloaded. Below is an example of a confirmation for New Banks from 2000-2015:

![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/GUI_FileDownloaded.png)

Clicking this button will download a CSV file of the relevant data to the folder /fdic_bank_eda/data/data_outputs 

The naming convention of the file is:
```changetype_MinYear_to_MaxYear.csv```

Where change type is:
* New Banks (NewInstitutions)
* Liquidated Banks (Liquidations)
* Failed Banks (Failures)
* Combined Banks (Combinations) 

and min and max year are the years indicated by the user. 

For example, the file generated by this view is saved as:
```NewInstitutions_2000_to_2015.csv```

![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/GUI_ExcelFiles.png)
This file can then be opened in excel like any standard CSV.

![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/GUI_DataInExcel.png)


The program will continue to run, generating and downloading different views based on the user inputs, until the program is closed by the user. It is not necessary to restart the program to generate a new view. 

## Error Handling in the GUI
The GUI relies on user input to generate views. We have methods to handle incorrect user input to ensure the GUI works as intended. When a user generates an error, an error message will appear in red under the title, prompting the user the correct course of action to fix the error. 

Below is a video that demonstrates the error handling capabilities of the GUI:

https://user-images.githubusercontent.com/32313952/144725534-5bd1e8df-3905-4350-b507-cc93a05bee9b.mp4


### Type Error

If a user enters a non-integer value for the year, the GUI will prompt the user for a correct input. 

![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/GUI_NonInteger.png)

### Value Error

If a user inputs years outside of the range of the data set, the GUI will prompt the user for a correct input.

![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/GUI_Out_Of_Range.png)

If a user inputs a minimum year that is larger than the maximum year, the GUI will prompt the user for a correct input.

![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/GUI_Min_Greater_Max.png)

### Downloading Data with No Data Generated

If a user selects the DOWNLOAD DATA button before generating a plot, the GUI will prompt the user to generate a plot before downloading data. 

![](https://github.com/allaccountstaken/fdic_banks_eda/blob/main/results/GUI_Download_Error.png)

