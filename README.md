# ControlAnalyzer
This project works with a merged excel sheet and searches for files within a directory to pair together the results and format it all into a user friendly spreadsheet

To start:

Our lab was not aware that its technicians were possibly plating their plate samples wrong, so we wanted to analyze the results that we were getting each week. Our robot generates hundreds of CSV files each week that contain the results of treatment and control plates. This program deals with handling the files, taking the necessary data, and pairing it with a master file that the program uses.

This "master" file contains the cell lines that were plated that week, which technicians plated them, the dates, drugs tested, and barcodes associated with each sample plate. 

The main.py first takes the master file and extracts the necessary data from it and puts it into a couple of dictionaries for the day1 controls and the day7 controls. This is a nested dictionary that goes as such ... Technician: { Date : { Barcode : [list of cell lines]}}
The different functions were created so that it can work with the funky formatting of the excel sheet the data was coming from. For this project, I used the openpyxl library to deal with the excel data.

Now that the necessary information is stored, I was able to use that to search a directory of files for those robot-generated CSV files. 

The first function in the FileFinder.py file "control_avg_function" loops through the either the d1 control dictionary or the d7 control dictionary, as well as the directory within the program. If the current iteration, a barcode, matches one within that directory, it will go inside the CSV result file and take the average of the results for the desired cell lines. These CSV files are all the same, and are formatted in a way that is familiar to me. There will be an example of this sheet located in the 'results' directory so you can see what I am talking about.

Once the file is found, depending on how many cell lines were associated with the barcode, the program will extract the data that is needed.
All I really need is one column, and this column could represent up to 8 different cell lines. But as specified before, it ranges from 1-8 cell lines. 
So, the averaged results are then associated with the cell lines that were stored into the control dictionaries I mentioned earlier. These cell lines and results are then stored into another dictionary where I can access it later.
I wrote pretty much everything (all results, cell lines, techinicans, dates) into a not-so-important .txt file, but this was purely for my own records and for the lab to analyze with if necessary.

The end results are then written into another excel file (lab preference) where the cell line, d1 barcodes, d1 results, d7 barcodes, d7 results, the difference in growth from start to finish, and the increase factor are stored.

In the near future, I'd like to upgrade this program into a locally-hosted website where we can visualize the data better, have a page for each cell line, and have a graph to go along with it that displays plot points that show the difference each week.

This will require basically creating a database to store the info that I need. TBD how to accomplish this, however I am confident I can figure it out.
