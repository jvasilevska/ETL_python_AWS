#Task description: 
 
The task can be broken down into the following steps:
* Investigate the API and understand how to get the required data out of it
* Write the python application which will run on Elastic Beanstalk and retrieves the data for the last game day
	* The application has to write the retrieved data into a CSV-file (‘<league>_YYYYMMDD.csv’) which will be stored in a S3 bucket (bucket name is: ‘football_games’). The following data points have to be retrieved:
	    * Date
	    * League
	    * Season
	    * Home team name
	    * Home team goals (fulltime)
	    * Away team name
	    * Away team goals (fulltime)
	* (optional) Schedule the app with a cron script
* Deploy the Elastic Beanstalk to the cloud

The code needs to be documented with comments and log statements need to be included.

Note: There is a hard cap of 10 requests/min for the API.