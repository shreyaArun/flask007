import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@absdb.cygtiwji8ayl.ap-south-1.rds.amazonaws.com:3306/absdb'
#Random Comment
'''
try:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
except:
	print("Error to connect")
'''
db = SQLAlchemy(app)

class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	dt = db.Column(db.DateTime, default=datetime.utcnow)
	i1 = db.Column(db.Integer, nullable=False, default=0)
	i2 = db.Column(db.Integer, nullable=False, default=0)
	i3 = db.Column(db.Integer, nullable=False, default=0)
	i4 = db.Column(db.Integer, nullable=False, default=0)
	i5 = db.Column(db.Integer, nullable=False, default=0)
	TotalPrice = db.Column(db.Integer, nullable=True)

	def __repr__(self):
		return "Order('{}','{}','{}','{}','{}','{}','{}')".format(self.dt,self.i1,self.i2,self.i3,self.i4,self.i5,self.TotalPrice)

@app.route('/ordered', methods=['POST','GET'])
def ordered():
	print("Ordered")
	if request.method == 'POST':
		i1 = request.form.get('select_1')
		i2 = request.form.get('select_2')
		i3 = request.form.get('select_3')
		i4 = request.form.get('select_4')
		i5 = request.form.get('select_5')

		print(" ",i1," ",i2," ",i3," ",i4," ",i5)
		TP = int(i1) * 1000 + int(i2) * 800 + int(i3) * 1200 + int(i4) * 10000 + int(i5) * 5000
		data = Order(i1 = int(i1), i2 = int(i2), i3 = int(i3), i4 = int(i4), i5 = int(i5), TotalPrice = TP)
		try:
			db.session.add(data)
			db.session.commit()
		except:
			return render_template('index.html',error=2)
		return render_template('ordered.html', line=data)
	else:
		return render_template('index.html', error=True)

@app.route('/result')
def result():
	print("Result")
	# ADD DATABASE READER
	data = Order.query.order_by(Order.id).all()
	return render_template('result.html', data=data)

@app.route('/add')
def add():
	print("Add")
	return render_template('add.html')

@app.route('/Login', methods=['POST','GET'])
def test():
	print("Login Successful")
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		print("username = ",username,"\t password = ",password)
		return render_template('loggedin.html')
	else:
		return render_template('index.html',error=1)

@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html',error=0)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug = True)
