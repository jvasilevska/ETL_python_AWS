# Instructions

### Installation
#### Requirements
* Python 3
* virtualenv 
* AWS account

#### Setup

* Copy `config.ini.example` to `config.ini` with the following command:  
```
cp config.ini.example config.ini
```

* Add your credentials for API connection and AWS account in `config.ini`
* Create new environment: `python -m venv env`
* Activate the environment: `env\Scripts\activate`
* Install requirements: `pip install -r requirements.txt`
* When done, deactivate environment: `env\Scripts\deactivate.bat`

### Running the script
`python api_to_s3.py`


After running this script a new S3 bucket will be created on AWS that will contain the .csv files with the data from the API.