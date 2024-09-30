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



# DRF END POINTS

based on the access token api the user role will be determined which will be used to fetch the details machine from database

1. To get access token 

use curl to import and run the api to get accesstoken

curl --location 'http://127.0.0.1:8000/api/token/' \
--header 'Content-Type: application/json' \
--data '{
	"username": "pradeep",
    "password":"pradeep"
}'

2. Fetch machine details

use curl to import and run the api to get machine details

curl --location 'http://127.0.0.1:8000/api/machines/historical-data/?axis_id=1%2C2' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI3NzIwMDI2LCJpYXQiOjE3Mjc3MTk3MjYsImp0aSI6IjY4NmQ4MmMzNGQ0ZDQ0ZWFhMjc2ZWJjOTA5ODM4NjQzIiwidXNlcl9pZCI6MX0.RUR5CBEWShnFWtgiMkdYRhLmTplEUXYe4eAOATxhx8A'