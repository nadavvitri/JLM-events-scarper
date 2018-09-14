# JLM-events-scarper
extract events from itraveljerusalem.com

## Getting started
install the following libraries:
```
easy_install pip
pip install BeautifulSoup4
```

## Running the script
Tested on ```python 3.5```
```
python3 scraper.py <calendar> [-h] [--csv]  [--all] [--scrapers SCRAPERS [SCRAPERS ...]]
```
 ```-h``` - Help how to use the scraper
 
 ```--all``` - Extract events from all scrapers (currently only <http://itraveljerusalem.com> work)
 
```--scrapers SCRAPERS [SCRAPERS ...]``` - Extract from specifics scrapers

 ```--csv``` - Export events also to file
 
 - ```--all``` and ```-scrapers``` are ambiguity and occur error message
 
 