Copernicus Mapping Data
-----------------------

Scripts used to extract [Copernicus](http://www.copernicus.eu/) [Emergency Management Service Mappings](http://emergency.copernicus.eu/mapping/ems/emergency-management-service-mapping).

### Download Shapefiles

The first step is to download the individual shapefiles from Copernicus.  As of this writing there are about 500 files to download.  A web scraper is provided to automate this process in `Copernicus-Mapping-DB/scraper/scraper.py`.  The scraper depends on the Chrome webdriver for selenium.  [This](http://stackoverflow.com/questions/28307469/chrome-driver-needs-to-be-available-in-the-path-error-on-mac) StackOverflow answer has some instructions on how to setup the Chrome driver.  Alternatively, you can alter the script to use a different driver (Safari, Firefox, etc...).

Files will be downloaded to whatever your browser's default download folder is.  On my computer this is `~/Downloads`.  To avoid confusion, it is best to clean out this folder prior to running the script.

To run, simply:

1. `pip install -r requirements.txt`
2. `./scraper.py`

This will fire up a browser instance and automatically download all files

### Generate the SQL Script

##### Dependencies:

- [`geojson2postgres`](https://github.com/ArnholdInstitute/geojson2postgres) - `npm install -g geojson2postgres`
- `ogr2ogr` - `brew install gdal`

##### Instructions

1. Create a directory called `./files` in the root of the Copernicus-Mapping-DB directory
2. `./to_sql.py`
3. `cat script.sql | psql <db_name`






