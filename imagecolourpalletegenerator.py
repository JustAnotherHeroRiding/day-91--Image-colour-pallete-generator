#One of my favourite websites to go to when I'm 
# designing anything is a colour palette website called 
# Flat UI Colors.
#https://flatuicolors.com/palette/defo
#It's a really simple static website that shows a bunch of 
# colours and their HEX codes. I can copy the HEX codes and
# use it in my CSS or any design software.
#On day 76, you learnt about image processing with NumPy. 
# Using this knowledge and your developer skills 
# (that means Googling), build a website where a user 
# can upload an image and you will tell them what are the 
# top 10 most common colours in that image.
#This is a good example of this functionality:
#http://www.coolphptools.com/color_extract#demo


#An image is a numpy array with 3 dimensions with rgb values
#I guess we can look for the most common rgb values and print those out from the picture
#The website should have an upload image file
#I'll do it with flask if i run into Javascript Problems
#Uploading the file should be a post request with a form
#Let me choose how many colors i want to see
#Get the hex code from the rgb values

import numpy as np
from PIL import Image # for reading image files
import cv2 as cv
from flask import Flask, jsonify, render_template, request,redirect,url_for,flash,abort
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import dotenv,os
dotenv.load_dotenv()



#Gives rgb values from the given image file
def top_10_rgbs(file_path):
    my_img = Image.open(file_path)
    img_array = np.array(my_img)
    unique, counts = np.unique(img_array.reshape(-1, 3), axis=0, return_counts=True)
    sorted_indices = np.argsort(counts)[::-1]
    sorted_unique = unique[sorted_indices]
    top_10_unique = sorted_unique[:10]
    return top_10_unique

def percentages(file_path,numberofcolors):
    colors={}
    # Load the image into a NumPy array
    img = Image.open(file_path)
    img_array = np.array(img)

    # Flatten the image array to a 1D array
    try:
        flat_array = img_array.reshape(-1, 3)
    except ValueError:
        img_array = img_array[:, :, :3]
        flat_array = img_array.reshape(-1, 3)

    # Find the unique elements and their counts
    unique, counts = np.unique(flat_array, axis=0, return_counts=True)

    # Sort the counts array in descending order and get the sorted indices
    sorted_indices = np.argsort(counts)[::-1]

    # Sort the unique elements array using the sorted indices
    sorted_unique = unique[sorted_indices]

    # Calculate the percentage of each color
    total_pixels = flat_array.shape[0]
    percentages = counts[sorted_indices] / total_pixels * 100

    # Select the top 10 elements
    top_10_colors = sorted_unique[:numberofcolors]
    top_10_percentages = percentages[:numberofcolors]
    hex_codes = ['#%02x%02x%02x' % tuple(color) for color in top_10_colors]


    # Print the RGB values and percentages of the top 10 colors
    #for color, percentage in zip(top_10_colors, top_10_percentages):
        #print(f'Color: {color}, Percentage: {percentage:.2f}%')
        #colors[str(color)] = percentage
        
    for hex_code, percentage in zip(hex_codes, top_10_percentages):
        #print(f'Hex code: {hex_code}, Percentage: {percentage:.2f}%')
        colors[hex_code] = f"{percentage:.5f}"
    return colors
        
    
#TO DO
#Turn the rgb values into hex codes DONE
#Find the percentage this color covers(probably counting number of rows for color vs total rows) DONE
#Try to search for how many times the rgb values appear(aka the row)in the entire reshaped array DONE
#NEW TASKS
#Make the upload button work and run the get the top 10 hex values from the upload picture
    
#print(top_10_rgbs('salzburgimage.jpg'))
#for k,v in percentages('redrock.jpg').items():
#    print(f"{k}:{v}")


import os
from werkzeug.utils import secure_filename
import ast

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
  """Check if a file is an allowed file type"""
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("APIKEY")
app.config['UPLOAD_FOLDER'] = 'images'

defaultcolors = 10
default = percentages('static/images/topartists.png',defaultcolors)

@app.route("/", methods=["GET", "POST"])
def home():
    #if os.path.exists('/tmp'):
        #print('The /tmp directory exists')
    #else:
        #print('The /tmp directory does not exist')
    if request.args.get('percentages') and request.args.get('src'):
        percentages = request.args.get('percentages')
        #print(percentages)
        #print(type(percentages))
        percentages = ast.literal_eval(percentages)
        src = request.args.get('src')
        return render_template('index.html', percentages=percentages, src=src)
    else:
        return render_template("index.html", percentages = default, src = 'static/images/topartists.png')


@app.route('/process', methods=['POST'])
def process():
  # Get the file from the POST request
  file = request.files['photo']
  # Check if the file is an allowed image type
  if file and allowed_file(file.filename):
    # Make the filename safe and save the file to a temporary location
    filename = secure_filename(file.filename)
    #file_path = os.path.join('/tmp', filename)
    
    file_path = os.path.join('static', f"images/{filename}")

    file.save(file_path)
    
    numberofcolors = int(request.form.get('number'))
    #print(numberofcolors)
    #print(type(numberofcolors))
    # Run the percentages function and get the color percentages
    color_percentages = percentages(file_path, numberofcolors)
    # Render a template with the color percentages
    return redirect(url_for('home', percentages=color_percentages, src=file_path))
  return 'Error: Invalid file type'

#Need to figure out how to show the images DONE
# aswell and style the table and image to be smaller DONE
#Make the upload form better and not clip DONE
#Added input for number of colors



if __name__ == '__main__':
    app.run(debug=True)



