import http.client
import json
import csv
import glob
import configparser
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from requests.exceptions import Timeout, TooManyRedirects, RequestException, HTTPError
import socket
import logging



def get_matches(x_auth_token):
    try:
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = { 'X-Auth-Token': x_auth_token }
        connection.request('GET', '/v2/matches', None, headers )
        response = json.loads(connection.getresponse().read().decode())['matches'] #this is a dictionary
        return response
    except ConnectionError as connErr:
        logging.error(connErr)
    except Timeout as toerr:
        logging.error(toErr)
    except TooManyRedirects as redirErr:
        logging.error(redirErr)
    except RequestException as reqErr:
        logging.error(reqErr)
    except HTTPError as httpErr:
        logging.error(httpErr)
    except socket.gaierror as socErr:
        logging.error(socErr)


def filenames(response):
    return [i['competition']['name'] + '_' + i['utcDate'][:10] for i in response]


def save_file(files,response):
    try:
    	for filename in files:
    		with open(filename + '.csv', 'w+', encoding='utf-8', newline='') as file:  # Use 'file' to refer to the file object
    			f = csv.writer(file)
    			f.writerow(["utcDate", "name", "season", "home_team", "home_team_goals", "away_team", "away_team_goals"])
    			for match in response:
    				if filename == match['competition']['name'] + '_' + match['utcDate'][:10]:
    				    f.writerow([match['utcDate'],
    				                match["competition"]["name"],
    				                match["season"]['startDate'][:4] + '/' + match['season']['endDate'][:4],
    				                match["homeTeam"]["name"],
    				                match["score"]["fullTime"]["homeTeam"],
    				                match["awayTeam"]["name"],
    				                match["score"]["fullTime"]["awayTeam"]])
    except IOError as ioErr:
        logging.error(ioErr)


def create_bucket(bucket_name, access_key, secret_key, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3', aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region, aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def prepare_files():
	return glob.glob("*.csv")


def upload_to_aws(local_file, bucket, access_key, secret_key, s3_file=None):
    s3 = boto3.client('s3', aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
    if s3_file is None:
        s3_file = local_file
    try:
    	for filename, s3_filename in zip(local_file, s3_file):
    		s3.upload_file(filename, bucket, s3_filename)
    	print("Upload Successful")
    	return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False



if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    response=get_matches(config['api_access']['x_auth_token'])
    files=filenames(response)
    save_file(files,response)
    create_bucket(config['s3_access']['bucket_name'], config['aws_access']['access_key'], config['aws_access']['secret_key'])
    csv_files=prepare_files()
    upload_to_aws(csv_files, config['s3_access']['bucket_name'], config['aws_access']['access_key'], config['aws_access']['secret_key'])
