This is for the Website Realtor.com Homes for Sale
Created using Scrapy

On line 7 change -search/(insert any location)/pg-{page}" to customize for a location you would like , ensure you visit the url within realtor.com first to confirm url structure

Check how many pages are available and change the range needed

Change file format to .csv to get spreadsheet view

Run command in terminal        < scrapy crawl realtorspider -o results.json >      to get results (this is where you would change the file format)
