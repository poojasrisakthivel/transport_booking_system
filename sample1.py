from flask import Flask,redirect, url_for,render_template,request,redirect
import mysql.connector
from fpdf import FPDF
import csv
import matplotlib.pyplot as plt
import base64
import io
app = Flask(__name__) 


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3308 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python'

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    port=app.config['MYSQL_PORT'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)


@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    
    
   # cursor = mysql.cursor()
    username = request.form['username']
    password = request.form['password']

    # Create a cursor to execute SQL queries
    cursor = mysql.cursor()

    # Example: Insert data into a 'users' table
    insert_query = "INSERT INTO login (username, password) VALUES (%s, %s)"
    data = (username, password)
    cursor.execute(insert_query, data)

    # Commit the changes and close the connection
    mysql.commit()
    cursor.close()

    #return f"User {username} successfully inserted into the database."
    return render_template('page1.html')

@app.route('/home')
def home():
    return render_template('page1.html')


@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/sumbit',methods=['POST'])
def sumbit():
    name = request.form['name']
    phone = request.form['phone']
    hours=request.form['hours']
    email=request.form['email']
    carType=request.form['carType']
    aadhar=request.form['aadhar']
    
    phone_int=int(phone)
    hours_int=int(hours)
    aadhar_int=int(aadhar)
    price=1500*hours_int


    # Create a cursor to execute SQL queries
    cursor = mysql.cursor()

    # Example: Insert data into a 'users' table
    insert_query = "INSERT INTO booking (name, phone,hours,emaill,carType,aadhar,price) VALUES (%s, %s,%s,%s,%s,%s,%s)"
    data = (name, phone,hours,email,carType,aadhar,price)
    cursor.execute(insert_query, data)

    # Commit the changes and close the connection
    mysql.commit()
    cursor.close()
    #mysql.close()
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM booking ORDER BY id DESC LIMIT 1 ")
    data = cursor.fetchone()
    cursor.close()
    return render_template('index.html', data=data)
    #return "Booking is successfull"

@app.route('/report')
def report():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM login")
    loginDetail = cursor.fetchall()
    with open('reportLogin.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Name', 'Password'])
        for username, password in loginDetail:
            csv_writer.writerow([username, password])

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=7)
    for username, password in loginDetail:
        pdf.cell(200, 10, txt=f"Username: {username}, Password: {password}", ln=True)

    # Save the PDF file
    pdf.output("reportLogin.pdf")
    

    #login
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM booking")
    loginDetail = cursor.fetchall()
    with open('reportBooking.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['id','Name', 'Phone','Hours','Email','CarType','Aadhar','Price'])
        for id, name, phone,hours,emaill,carType,aadhar,price in loginDetail:
            csv_writer.writerow([id,name, phone,hours,emaill,carType,aadhar,price])

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=7)
    for id,name, phone,hours,emaill,carType,aadhar,price in loginDetail:
        pdf.cell(200, 10, txt=f"Username: {name}, Phone: {phone},Hours: {hours},Email: {emaill},CarType: {carType},Aadhar: {aadhar},Price: {price}", ln=True)

    # Save the PDF file
    pdf.output("reportBooking.pdf")

    return 'Report generated successfully'


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/display')
def index():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM login")
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', data=data)

@app.route('/graph')
def graph():
    cursor = mysql.cursor()
    cursor.execute("SELECT hours FROM booking")
    hr = cursor.fetchall()
    cursor.execute("SELECT price FROM booking")
    pr = cursor.fetchall()

    plt.plot(hr, pr, label='Graph')
    plt.xlabel('hours')
    plt.ylabel('price')
    plt.title('Data Plot')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image as base64 and include it in the HTML response
    plot_url = base64.b64encode(img.getvalue()).decode()

    cursor.close()
    return render_template('graph.html', plot_url=plot_url)

@app.route('/hours')
def hours():
    cursor = mysql.cursor()
    cursor.execute("SELECT hours FROM booking")
    hr = cursor.fetchall()
    l=len(hr)
    le = list(range(l))

    plt.plot(le, hr, label='Graph')
    plt.xlabel('')
    plt.ylabel('hours')
    plt.title('Hours Plot')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image as base64 and include it in the HTML response
    plot_url = base64.b64encode(img.getvalue()).decode()

    cursor.close()
    return render_template('hours.html', plot_url=plot_url)

@app.route('/price')
def price():
    cursor = mysql.cursor()
    cursor.execute("SELECT price FROM booking")
    pr = cursor.fetchall()
    l=len(pr)
    le = list(range(l))

    plt.plot(le, pr, label='Graph')
    plt.xlabel('')
    plt.ylabel('Price')
    plt.title('Price Plot')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image as base64 and include it in the HTML response
    plot_url = base64.b64encode(img.getvalue()).decode()

    cursor.close()
    return render_template('price.html', plot_url=plot_url)

    
if __name__ == "__main__":
    app.run()
    

