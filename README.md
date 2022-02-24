# SAPHETOR REST API ASSIGNMENT
## ASSIGNMENT
Generate a REST API (over HTTP) that will manipulate data based on the contents of a VCF File (attached with the project - the first 5 “CHROM, POS,ID,REF,ALT“ fields available on the VCF may be selected for the purpose of the project). 

Try to provide back an implementation that, as closely as possible, covers the requested functionality. There is no restriction in using 3rd party  python libraries to cover the requested functionality. Pay attention though to balance between providing a partial implementation of all the  requirements or a “proper” implementation of a part of the requirements if the available time to complete the project is an issue.  

---

## SETUP AND EXECUTION
Python 3.10.1 is used (preferrably install Python 3.9+ due to the return types applied to the methods)
A requirements.txt is provided with all the essential libraries used to build the REST API
### Setup and execution steps
- Clone the project
- Install the virtualenv library in order to build the virtual environment that is needed to run the project
- Install the requirements as instructed below
- Create a .env file inside the src/config folder and write the following line:
	`SECRET_KEY=ANY_SECRET_KEY_YOU_LIKE`
	This will be used for the authentication required for the POST request
- Place the vcf.gz file provided in the assignment email inside the src/static folder. This is our dataset for all the requests that will be performed 		upon the execution. No extraction needed.

```
# change directory into the project root and install the libraries
pip install -r requirements.txt
# activate the virtual environment (Windows is my OS)
python venv/Scripts/activate
```

In order to run the project you have to be inside the project root folder and have already activated the virtual environment. Then, execute this:
`python src/app.py`

A running server output will be printed.

I personally used Insomnia client to perform the requests. I will provide the endpoints, headers and data needed to perform the requests
- **GET:** 
	- **without pagination**: `http://localhost:5000/saphetor/getRow/DESIRED_ID`
	- **with pagination:** `http://localhost:5000/saphetor/getPaginatedData?page=1&per_page=10`
	- **header (optional, anything between these or no header applied at all):** `header=Response-Type, value=application/xml | application/json | */* `
- **POST:** 
	- **URL:** `http://localhost:5000/saphetor/addRow`
	- **data:** 
		```
		{
	    "CHROM": "chr1",
	    "POS": 1002,
	    "ALT": "A",
	    "REF": "C",
	    "ID": "rs123456789"
		}
		```
	- **headers:**
		- `header=Content-Type, value=application/json`
		- `header=X-Access-Token, value=ANY_KEY_YOU_HAVE_IN_THE_ENV_FILE`
- **PUT**
	- **URL:** `http://localhost:5000/saphetor/updateRow/DESIRED_ID`
	- **data:** 
		```
		{
		"CHROM": "chrXY",
		"POS": 11,
		"ALT": "ABC",
		"REF": "CDEffff"
		}
		```
	- **headers:**
		- `header=Content-Type, value=application/json`
		- `header=X-Access-Token, value=ANY_KEY_YOU_HAVE_IN_THE_ENV_FILE`
- **DELETE:**
	- **URL:** `http://localhost:5000/saphetor/deleteRow/DESIRED_ID`
	- **headers:** `header=X-Access-Token, value=ANY_KEY_YOU_HAVE_IN_THE_ENV_FILE`
---