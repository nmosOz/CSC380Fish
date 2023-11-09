import pandas as pd 
import os

def html_from_csv(csv_filename):

    #this is the directory we will save the csv file to
    save_path = './FlaskTutorial/static/report_htmls'

    #read the csv file in
    df = pd.read_csv(csv_filename+".csv")

    #seperate the .csv from the file name
    file_name, file_ext = os.path.splitext(csv_filename)

    #join the file name with the file extension we want
    completeName = os.path.join(save_path, file_name+".html")

    #Open the file to write the html to it 
    with open(completeName, 'w') as f_output:
        #Write it as an html file
        df.to_html(f_output)


    