#### Race Results Crawler for [roadraceresults.com](http://www.roadraceresults.com/default.php)
---

#### Setting up

+ Install project requirements
```python
pip install -r requirements.txt
```

+ Set Environment Variables
  + Create a `.env` file in the root of the outer `race_results` directory
  + Add the following keys to the file
  ```python
	displayname=<your roadraceresults display name>
	email=<your roadraceresults email>
	uid=<your roadraceresults uid>
	uidcode=<your roadraceresults uidcode>
	uresultgroup=<your roadraceresults uresultgroup>
	accounttype=<your roadraceresults accounttype>
	code=<your roadraceresults code>
  ```
  + Your structure should look something like this
  ```python
	race_results
		no_scrapy/
		race_results/
		__init__.py
		.env
		.gitignore
		proxies.txt
		README.md
		requirements.txt
		run_crawler.sh
		scrapy.cfg
  ```

+ Running the crawler
	+ First we, need to get a list of links to all the race results.
	+ Get this by running this in your terminal
	```python
	scrapy crawl rrl
	
	# rrl is simply an abbreviation for `race result links`
	```
	+ This woud create a file named `links_with_results.csv` in the root dir.
	+ If you inspect this file, you'd see urls to all the race results from 1998 to 2017 (of course the year range can be easily customized)
	+ We'd referece this file in the next step
	+ To get the actual race results, I decided not to use scrapy as some data are being lost in the way it parses the response body
	+ I built a custom scraper which does a better job at this. You can run this by simply running
	```python
	python no_scrapy/main.py
	```
	+ This would crawl each link in the `links_with_results.csv` file and write the output to a new csv file `race_results.csv`
	+ And there you have it.
