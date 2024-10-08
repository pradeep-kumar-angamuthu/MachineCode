# MachineCode
# Machine Data Generator

## Overview
This project is a Python script designed to generate and store machine data in a SQLite database. It simulates the operations of multiple machines across different axes, updating parameters such as tool offset, feed rate, and tool usage at specified intervals. also provided with api end points for user authentication and based on role fetching api details

## Features
- Generates random values for machine parameters based on defined constraints.
- Stores machine and axis data in a SQLite database.
- Updates data periodically to simulate real-time monitoring.

## Requirements
- Python 3.x
- SQLite3 (comes pre-installed with Python)

## Installation
1. Clone the repository:
   -bash
   git clone https://github.com/pradeep-kumar-angamuthu/MachineCode.git
   cd MachineCode



# DRF API END POINTS

based on the access token api the user role will be determined which will be used to fetch the details machine from database

**1. Register for authorization**
use curl to import and store the user with OPERATOR or SUPERADMIN or SUPERVISOR or MANAGER role

curl --location 'http://127.0.0.1:8000/api/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "deepak",
  "password": "deepak",
  "email": "deepak@gmail.com",
  "role": "SUPERADMIN"  
}
'

**2. To get access token **
use curl to import and run the api to get accesstoken

curl --location 'http://127.0.0.1:8000/api/token/' \
--header 'Content-Type: application/json' \
--data '{
	"username": "deepak",
    "password":"deepak"
}'

**3. Fetch machine details for past 15 mins data**
use curl to import and run the api to get machine details

curl --location 'http://127.0.0.1:8000/api/machines/historical-data/?axis_id=1%2C2' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI3NzIwMDI2LCJpYXQiOjE3Mjc3MTk3MjYsImp0aSI6IjY4NmQ4MmMzNGQ0ZDQ0ZWFhMjc2ZWJjOTA5ODM4NjQzIiwidXNlcl9pZCI6MX0.RUR5CBEWShnFWtgiMkdYRhLmTplEUXYe4eAOATxhx8A'

**4.  Create api for storing machine related details**
use curl to import and run the api to store machine details based on the access Role

curl --location 'http://127.0.0.1:8000/api/machines/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4NDA5NjIyLCJpYXQiOjE3Mjg0MDkzMjIsImp0aSI6IjQyNjM0YzIwMTNlZDRkMDM5Mjk1ZjVkODFkNDdjOTYzIiwidXNlcl9pZCI6MX0.XhnGEavpB90Lf2mDyThaxXv_TBQ7neWUey1jC7wvvnM' \
--data '{
  "machine_id": 81258856,
  "axis_id": 2,
  "tool_offset": 10.5,
  "feedrate": 100,
  "tool_in_use": 12
  
}'

**5. Update api for machine related details**
use curl to import and run the api to update machine details based on the machine_id

curl --location --request PUT 'http://127.0.0.1:8000/api/machines/81258856/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4NDA5NjIyLCJpYXQiOjE3Mjg0MDkzMjIsImp0aSI6IjQyNjM0YzIwMTNlZDRkMDM5Mjk1ZjVkODFkNDdjOTYzIiwidXNlcl9pZCI6MX0.XhnGEavpB90Lf2mDyThaxXv_TBQ7neWUey1jC7wvvnM' \
--data '{
  "machine_id": 81258856,
  "axis_id": 2,
  "tool_offset": 10.5,
  "feedrate": 100,
  "tool_in_use": 10
  
}'

**6. Delete api for machine details destroy**
use curl to import and run the api to delete machine details based on the machine_id

curl --location --request DELETE 'http://127.0.0.1:8000/api/machines/81258856/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4NDEwNTE1LCJpYXQiOjE3Mjg0MTAyMTUsImp0aSI6IjdhNjBiMWZmYTRmODRhMDVhYzUzYWNhOTQxNjY0MGVjIiwidXNlcl9pZCI6MX0.NZCfFpLAaTb8r5FRJVNBzcJiBQbtUPAbFhijoko98tU' \
--data ''



