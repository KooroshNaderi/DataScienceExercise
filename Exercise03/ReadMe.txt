Problem: Develop a simple url grabber. The program gets as input two address files,
	 one containing urls and the other one contains regular expressions. 
	 The purpose of the program is to check the urls, fetch their context and 
	 match with given regular expressions.

Files: 
- solution.py: the main file that contains the solution to the problem
- file_utils.py: utility functions for reading files
- function_utils.py: other utility functions for regular expression, time, and os
- command.txt: commands for running the solution.py
- run_command.ipynb: jupyter notebook file containing explanation for the solution 
		     and some tests. The explanation is also brought here.
- url_file.txt: the file containing the urls
- regex_file.txt: the file containing the regular expressions


Solution: To approach the problem, I have done the followings:
	* docopt is used to get as arguments two file names: url_file and regex_file
	* pandas is used to read urls assuming urls have big data
	* multi-processing is used to assign workers for finding a match string given
	  urls and regex list. 
		** To log the output, multi-threading queue is used to put a dictionary
		   as a log
		** To read the url, urllib is used to open the webpage and read its context
		** The process of assigning workers is as follows:
			1) a url is selected from database, and its context is fetched
			   if it exists
			2) as long as a worker is free, a regex is selected from list 
			   to be checked against the url
			3) go to first step if all regex list is assigned a worker, and
			   there is more url to check otherwise end
	* to handle ctrl+c, try-except is used
		first: I needed to import big library like pandas and urllib inside the
		       function. As a result, I could catch the error and log/report nice
		       print in case of ctrl+c
		second: ctrl+c might happed in the middle of reading from database and as
			a result it reported error. To avoid that I used os.kill to kill 
			the process and send ctrl+break

To run: please run the command provided in the 'command.txt' in the console