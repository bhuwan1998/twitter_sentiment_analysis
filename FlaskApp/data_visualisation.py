# Flask Web App for Displaying the project 

from flask import Flask, render_template 
import pandas as pd 
import matplotlib.pyplot as plt 
from io import BytesIO
import base64

app = Flask(__name__)

csv_data = "../Data/Final_Merged_Data.csv"

# Function to generate the graph and return it as a base64 encoded image 
def generate_plot(): 
    df = pd.read_csv(csv_data)
    # finish the plot later 


@app.route("/") # Home Page 
def index(): 
    csv_table = pd.read_csv(pd.compat.StringIO(csv_data)).to_html(classes='table table-striped')
    plot = generate_plot()
    return render_template('index.html', csv_table=csv_table, plot=plot)

if __name__ == '__main__': 
    app.run(debug=True) 
