#!/usr/bin/env python3

import cgi
import cgitb
import json
import sys
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import pymysql.cursors
from flask import Flask, abort, jsonify, make_response, request, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session

import settings
# from passlib.hash import sha256_crypt


cgitb.enable()

import settings  # Our server and db settings, stored in settings.py

app = Flask(__name__, static_url_path='/static')
api = Api(app)

app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)

####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { "status": "Bad request" } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { "status": "Resource not found" } ), 404)

############################################################################################################
############################################################################################################
#.....1)
#
#			Get All Users
#
#

class Manager_getAllUsers(Resource):
	#
	def get(self):
		#
		#
		# curl -i https://cs3103.cs.unb.ca:8004/manager/users 
		# 
		#
		# Get the request data

		# Check for if manager logged in 
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'manager':
				user_type = 'manager'
			else:
				abort(403,"User is not a Manager")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)

		try:
			dbConnection = pymysql.connect(
			settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'getAllUsers'
			cursor = dbConnection.cursor()
			cursor.callproc(sql) # stored procedure, no arguments
			rows = cursor.fetchall() # get all the results
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({'users': rows}), 200) # turn set into json and return it

#####################################################################################################################
#
#
#			ADD USER
#
#
	def post(self):
		#
		#
		#
		# curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "rick","name": "rick","email": "rick@unb.ca","user_type": "customer"}' -b cookie-jar -k https://cs3103.cs.unb.ca:8004/manager/users
		#
		#

		# Check for if manager logged in 
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'manager':
				user_type = 'manager'
			else:
				abort(403,"User is not a Manager")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)


		#
		# Get the request data
		user_data = request.json

		# Validate the data
		if 'user_id' not in user_data:
			return jsonify({'error': 'user_id is required'}), 400
		if 'email' not in user_data:
			return jsonify({'error': 'email is required'}), 400
		if 'name' not in user_data:
			return jsonify({'error': 'name is required'}), 400
		if 'user_type' not in user_data:
			return jsonify({'error': 'user_type is required'}), 400

		# Create the user
		user = {
			'user_id' : user_data['user_id'],
			'name': user_data['name'],
			'email': user_data['email'],
			'user_type': user_data['user_type']
		}
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'addUser'
			cursor = dbConnection.cursor()
			sqlArgs = (user['user_id'],user['name'], user['email'], user['user_type']) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			row = cursor.fetchone()
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

		return make_response(jsonify( { "Response" : "User created successfully!" } ), 201) # successful resource creation

#############################################################################################################################################################################

#
#
#			UPDATE USER
#
#
	def put(self):
		#
		#
		#
		# curl -i -H "Content-Type: application/json" -X PUT -d '{"user_id": "z9h8f","name": "Priyanka","email": "Priyanka@gmail.com"}' -b cookie-jar -k https://cs3103.cs.unb.ca:8004/manager/users
		#
		#

		# Check for if manager logged in 
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'manager':
				user_type = 'manager'
			else:
				abort(403,"User is not a Manager")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)
		#
		user_data = request.json

		# Validate the data
		#Add code to validate input

		# Create the user
		user = {
			'user_id': user_data['user_id'],
			'name': user_data['name'],
			'email': user_data['email']
		}
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'updateUser'
			cursor = dbConnection.cursor()
			sqlArgs = (user['user_id'],user['name'], user['email']) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			row = cursor.fetchone()
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

		return make_response(jsonify( {"response_code " : "200"})) # successful resource creation


############################################################################################################
############################################################################################################
#.....2)
#
#					FETCH USER Details
#
#
class Manager_getUser(Resource):
	def get(self, userId):
		#
		#
		# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:8004/manager/users/z9h8f
		# 
		#

		# Check for if manager logged in 
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'manager':
				user_type = 'manager'
			else:
				abort(403,"User is not a Manager")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)

		try:
			dbConnection = pymysql.connect(
			settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'getUser'
			cursor = dbConnection.cursor()
			sqlArgs = (userId,)
			cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
			row = cursor.fetchone() # get the single result
			if row is None:
				abort(404)
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({"user": row}), 200) # successful
	
###########################################################################################################    

	def delete(self, userId):
		#
		#
		#curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:8004/manager/users/z9h8f
		# 
		#

		# Check for if manager logged in 
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'manager':
				user_type = 'manager'
			else:
				abort(403,"User is not a Manager")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)

		try:
			dbConnection = pymysql.connect(
			settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			#
			sql = 'getUser'
			cursor = dbConnection.cursor()
			sqlArgs = (userId,)
			cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
			row = cursor.fetchone() # get the single result
			if row is None:
				return make_response(jsonify({"User Does Not Exist": userId}), 404)
			#	
			sql = 'deleteUser'
			cursor = dbConnection.cursor()
			sqlArgs = (userId,)
			cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
			dbConnection.commit()

		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return 204
        
        
###########################################################################################################
###########################################################################################################
#.....3)

class Manager_getAllReservations(Resource):
	#
 #
 #
 #					GET ALL RESERVATIONS
 #
 #
	def get(self):
		#
		#
		# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k https://cs3103.cs.unb.ca:8004/manager/reservations
		# 
		#

		# Check for if manager logged in 
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'manager':
				user_type = 'manager'
			else:
				abort(403,"User is not a Manager")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)

		try:
			dbConnection = pymysql.connect(
			settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'getAllReservations'
			cursor = dbConnection.cursor()
			cursor.callproc(sql) # stored procedure, no arguments
			rows = cursor.fetchall() # get all the results
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({'reservations': rows}), 200) # turn set into json and return it

	def post(self):
		#
		#
#	
#
#
#					CREATE RESERVATION
#
#
		#
		# curl -i -H "Content-Type: application/json" -X POST 
		# -d '{"timeslot": "0","reservation_date": "2023-03-15", "user_id": "10001","table_id": "4"}' 
		# https://cs3103.cs.unb.ca:8004/manager/reservations
		#
		#
		#
		# Get the request data

		# Check for if manager logged in 
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'manager':
				user_type = 'manager'
			else:
				abort(403,"User is not a Manager")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)

		reservation_data = request.json

		# Validate the data
		if 'timeslot' not in reservation_data:
			return jsonify({'error': 'timeslot is required'}), 400
		if 'reservation_date' not in reservation_data:
			return jsonify({'error': 'reservation_date is required'}), 400
		if 'user_id' not in reservation_data:
			return jsonify({'error': 'user_id is required'}), 400
		if 'table_id' not in reservation_data:
			return jsonify({'error': 'table_id is required'}), 400

		# Create the user
		reservation = {
			'timeslot': reservation_data['timeslot'],
			'reservation_date': reservation_data['reservation_date'],
			'user_id': reservation_data['user_id'],
			'table_id': reservation_data['table_id']
		}
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'addReservation'
			cursor = dbConnection.cursor()
			sqlArgs = (reservation['timeslot'], reservation['reservation_date'], reservation['user_id'], reservation['table_id']) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			row = cursor.fetchone()
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		
		return make_response(jsonify( { "Response" : "Reservation created successfully!" } ), 201) # successful resource creation

	###########################################################################################################


	def put(self):
		#
		#
		#
		# curl -i -H "Content-Type: application/json" -X PUT 
		# -d '{"timeslot": "0","reservation_date": "2023-03-15"}' 
		# https://cs3103.cs.unb.ca:8004/manager/reservations
		#
		#
		#
		# Get the request data

		# Check for if manager logged in 
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'manager':
				user_type = 'manager'
			else:
				abort(403,"User is not a Manager")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)

		reservation_data = request.json

		# Validate the data


		# Update the Reservation
		reservation = {
			'user_id' : reservation_data['user_id'],
			'reservation_id': reservation_data['reservation_id'],
			'timeslot': reservation_data['timeslot'],
			'reservation_date': reservation_data['reservation_date'],
			'table_id' : reservation_data['table_id']
		}
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'updateReservation'
			cursor = dbConnection.cursor()
			sqlArgs = (reservation['user_id'],reservation['reservation_id'], reservation['timeslot'],reservation_data['table_id'], reservation['reservation_date']) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			row = cursor.fetchone()
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

		return make_response(jsonify( { "Response_code" : 200 } )) # successful resource creation


###########################################################################################################
###########################################################################################################
#.....4)

class Manager_getReservationsByUserId(Resource):
	#
	def get(self, userId):
		#
		#
		# curl -i https://cs3103.cs.unb.ca:8004/manager/reservations/g7vfx
		# 
		#

		# Check for if manager logged in 
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'manager':
				user_type = 'manager'
			else:
				abort(403,"User is not a Manager")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)

		try:
			dbConnection = pymysql.connect(
			settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'getReservation'
			cursor = dbConnection.cursor()
			sqlArgs = (userId,)
			cursor.callproc(sql,sqlArgs) # stored procedure, userId arguement
			row = cursor.fetchall() # get all results
			if row is None:
				return make_response(jsonify({"No Reservations found for userId" : userId}))
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({"reservations": row}), 200) # successful
		####################################################################################

	# def put(self):
        
	# 	user_data = request.json

	# 	# Validate the data
	# 	#Add code to validate input

	# 	# Create the user
	# 	user = {
	# 		'user_id': user_data['user_id'],
	# 		'name': user_data['name'],
	# 		'email': user_data['email']
	# 	}
	# 	try:
	# 		dbConnection = pymysql.connect(settings.DB_HOST,
	# 		settings.DB_USER,
	# 		settings.DB_PASSWD,
	# 		settings.DB_DATABASE,
	# 		charset='utf8mb4',
	# 		cursorclass= pymysql.cursors.DictCursor)
	# 		sql = 'updateUser'
	# 		cursor = dbConnection.cursor()
	# 		sqlArgs = (user['user_id'],user['name'], user['email']) # Must be a collection
	# 		cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
	# 		row = cursor.fetchone()
	# 		dbConnection.commit() # database was modified, commit the changes
	# 	except:
	# 		abort(500) # Nondescript server error
	# 	finally:
	# 		cursor.close()
	# 		dbConnection.close()
	# 	uri = 'https://'+settings.APP_HOST+':'+str(settings.APP_PORT)
	# 	uri = uri+str(request.url_rule)+'/'+str(row['LAST_INSERT_ID()'])
	# 	return make_response(jsonify( { "uri" : uri } ), 201) # successful resource creation

###########################################################################################################
###########################################################################################################



class Manager_deleteReservationsByUserId(Resource):

	def delete(self,userId,reservationId):
		#
		#
		#curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:8004/manager/<userid>/reservations/<reservationid> 
		# 
		#

		# Check for if manager logged in 
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'manager':
				user_type = 'manager' #dummy statement 
			else:
				abort(403,"User is not a Manager")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)

				#
		try:
			dbConnection = pymysql.connect(
			settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			#
			sql = 'cancelReservation'
			cursor = dbConnection.cursor()
			sqlArgs = (userId,reservationId)
			cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
			row = cursor.fetchone() # get the single result	
			dbConnection.commit()

		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return 204


###########################################################################################################
###########################################################################################################

#.....5)

class User_getReservationsByUserId(Resource):
	def get(self):
		#
		#
		# curl -i https://cs3103.cs.unb.ca:8004/user/reservations
		# 
		#

		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'customer':
				user_type = 'customer'
			else:
				abort(403,"User is not a Customer")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)
		

		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getReservation'
			cursor = dbConnection.cursor()
			# To be edited to be fetched from the session 
			sqlArgs = (username,)
			cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
			rows = cursor.fetchall() # get all the results
			if len(rows) == 0:
				abort(404)
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({'reservations': rows}), 200) # turn set into json and return it

	def post(self):
		#
		#
		#
		# curl -i -H "Content-Type: application/json" -X POST -d '{"timeslot": "0","reservation_date": "2023-03-26","table_id": "4"}'  -c cookie-jar -k https://cs3103.cs.unb.ca:8004/user/reservations
		#
		#

		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'customer':
				user_type = 'customer'
			else:
				abort(403,"User is not a Customer")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)

		#
		# Get the request data
		reservation_data = request.json

		# Validate the data
		if 'timeslot' not in reservation_data:
			return jsonify({'error': 'timeslot is required'}), 400
		if 'reservation_date' not in reservation_data:
			return jsonify({'error': 'reservation_date is required'}), 400
		if 'table_id' not in reservation_data:
			return jsonify({'error': 'table_id is required'}), 400

		# Create the user
		reservation = {
			'timeslot': reservation_data['timeslot'],
			'reservation_date': reservation_data['reservation_date'],
			'user_id': session['username'],
			'table_id': reservation_data['table_id']
		}
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'addReservation'
			cursor = dbConnection.cursor()
			sqlArgs = (reservation['timeslot'], reservation['reservation_date'], reservation['user_id'], reservation['table_id']) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			row = cursor.fetchone()
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

		return make_response(jsonify( { "Response" : "Reservation created successfully!" } ), 201) # successful resource creation


	####################################################################################
	def put(self):
		#
		#						UPDATE RESERVATION
		#
		# curl -i -H "Content-Type: application/json" -X PUT -d '{"timeslot": "0","reservation_date": "2023-03-15","reservation_id" : "<your_reservation_id>"}' https://cs3103.cs.unb.ca:8004/user/reservations
		#
		#

		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'customer':
				user_type = 'customer'
			else:
				abort(403,"User is not a Customer")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)

		#
		# Get the request data
		reservation_data = request.json

		# Validate the data


		# Update the Reservation
		reservation = {
			'user_id' : session['username'],
			'reservation_id': reservation_data['reservation_id'],
			'timeslot': reservation_data['timeslot'],
			'reservation_date': reservation_data['reservation_date'],
			'table_id' : reservation_data['table_id']
		}
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'updateReservation'
			cursor = dbConnection.cursor()
			sqlArgs = (reservation['user_id'],reservation['reservation_id'], reservation['timeslot'],reservation_data['table_id'], reservation['reservation_date']) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			row = cursor.fetchone()
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()

		return make_response(jsonify( { "Response_code" : 200 } )) # successful resource creation

###########################################################################################################    

class User_deleteReservationsByUserId(Resource):

	def delete(self,userId,reservationId):
		#
		#
		#curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:8004/user/<userid>/reservations/<reservationid> 
		# 
		#

		# Check for if manager logged in 
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'customer':
				user_type = 'customer' #dummy statement 
				if userId == username:
					user_type = 'customer' #dummy statement 
				else:
					abort(403,"Please use valid reservation id")
			else:
				abort(403,"User is not a Customer")
		else:
			response = {'Response': 'User not Logged in'}
			responseCode = 403
			abort(responseCode,response)

				#
		# Get the request data
		reservation_data = request.json

		try:
			dbConnection = pymysql.connect(
			settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			#
			sql = 'cancelReservation'
			cursor = dbConnection.cursor()
			sqlArgs = (userId,reservationId)
			cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
			row = cursor.fetchone() # get the single result	
			dbConnection.commit()

		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return 204
        
        


###########################################################################################################
###########################################################################################################
	#.....6)
class User_updateUser(Resource):
	def put(self):
		#
		#
		#
		# curl -i -H "Content-Type: application/json" -X PUT 
		# -d '{"name": "Nisper","email": "Nisper@gmail.com", "password": "password132"}' 
		# https://cs3103.cs.unb.ca:8004/user
		#
		#

		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
			if session['user_type'] == 'customer':
				user_type = 'customer'
			else:
				abort(403,"User is not a Customer")
		else:
			response = {'Response': 'User Not logged in!'}
			responseCode = 403
			abort(responseCode,response)

		#
		#
		user_data = request.json

		# Validate the data
		#Add code to validate input

		# Create the user
		user = {
			'user_id': session['username'],
			'name': user_data['name'],
			'email': user_data['email']
		}
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'updateUser'
			cursor = dbConnection.cursor()
			sqlArgs = (user['user_id'],user['name'], user['email']) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			row = cursor.fetchone()
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify( {"response_code " : "200"})) # successful resource creation


###########################################################################################################
###########################################################################################################
class SignUp(Resource):
	def post(self):
	#
	#
	#
	# curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "<your_id>","name": "<your_name>","email": "<your_email>"}' https://cs3103.cs.unb.ca:8004/signup
	#
	#
	#
		# Get the request data
		user_data = request.json
		
		
		# Validate the data
		if 'user_id' not in user_data:
			return jsonify({'error': 'user_id is required'}), 400 
		if 'email' not in user_data:
			return jsonify({'error': 'email is required'}), 400
		if 'name' not in user_data:
			return jsonify({'error': 'name is required'}), 400


		user = {
			'user_id' : user_data['user_id'],
			'name': user_data['name'],
			'email': user_data['email'],
			'user_type': "customer"
		}
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
			settings.DB_USER,
			settings.DB_PASSWD,
			settings.DB_DATABASE,
			charset='utf8mb4',
			cursorclass= pymysql.cursors.DictCursor)
			sql = 'addUser'
			cursor = dbConnection.cursor()
			sqlArgs = (user['user_id'],user['name'], user['email'], user['user_type']) # Must be a collection
			cursor.callproc(sql,sqlArgs) # stored procedure, with arguments
			row = cursor.fetchone()
			dbConnection.commit() # database was modified, commit the changes
		except:
			abort(500) # Nondescript server error
		finally:
			cursor.close()
			dbConnection.close()
		
		return make_response(jsonify( { "Response" : "User created successfully!" } ), 201) # successful resource creation

###########################################################################################################
###########################################################################################################
class SignIn(Resource):
	#
	# Set Session and return Cookie
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "<your_id>", "password": "<your_pass>"}' -c cookie-jar -k https://cs3103.cs.unb.ca:8004/signin
	#

	def get(self):
		success = False
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)	

###########################################################################################################

	def post(self):

		user_data = request.json
		
		if not request.json:
			abort(400) # bad request

		# Parse the json
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request
		if user_data['username'] in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				ldapServer = Server(host=settings.LDAP_HOST)
				ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+user_data['username']+', ou=People,ou=fcs,o=unb',
					password = user_data['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
				# At this point we have sucessfully authenticated.

				session['username'] = user_data['username']
			# Stuff in here to find the esiting userId or create a use and get the created userId
				responseCode = 201

				dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
				sql = 'getUser'
				cursor = dbConnection.cursor()
				sqlArgs = (user_data['username'],)
				cursor.callproc(sql,sqlArgs) # stored procedure, no arguments
				row = cursor.fetchone() # get the single result
				if row is None:
					return make_response(jsonify({"User Not Registered, Please SignUp" : user_data['username']}))
				else:
					#print(row)
					session['user_type']=row['user_type']
					#print(session.get('username'),session.get('user_type'))
					return make_response(jsonify({"Login Successful": row['user_id'],"User-type" : row['user_type'],"username": session['username']}), 201) # successful

			except LDAPException:
				response = {'status': 'Access denied'}
				print(response)
				responseCode = 403
			finally:
				ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)

	# GET: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:8004/signin



###########################################################################################################
###########################################################################################################


class SignOut(Resource):
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k https://cs3103.cs.unb.ca:8004/signout

	def delete(self):
		if 'username' in session:
			session.pop('username', None) # Remove the 'username' key from the session
			session.pop('user_type', None)
			response =  {'status': 'Logged out successfully' }
			responseCode = 200
			return make_response(jsonify(response), responseCode)
		else:
			response = {'status': 'User not logged in!'}
			responseCode = 403
		return make_response(jsonify(response), responseCode)

################################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(Manager_getAllUsers, '/manager/users')
api.add_resource(Manager_getUser, '/manager/users/<string:userId>')
api.add_resource(Manager_getAllReservations, '/manager/reservations')
api.add_resource(Manager_getReservationsByUserId, '/manager/reservations/<string:userId>')
# api.add_resource(Manager_updateReservationsByUserId, '/manager/reservations/<int:reservationId>')
api.add_resource(Manager_deleteReservationsByUserId, '/manager/<string:userId>/reservations/<int:reservationId>')
api.add_resource(User_getReservationsByUserId, '/user/reservations')
api.add_resource(User_deleteReservationsByUserId, '/user/<string:userId>/reservations/<int:reservationId>')
api.add_resource(User_updateUser, '/user')
api.add_resource(SignUp, '/signup')
api.add_resource(SignIn, '/signin')
api.add_resource(SignOut, '/signout')
#############################################################################

if __name__ == "__main__":
	context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)
