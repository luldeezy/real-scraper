import scrapy
import json

    # Data being pulled from site from pages in range (), this can be changed to page numbers avaliable
class RealtorSpider(scrapy.Spider):
    name = "realtorspider"
    start_urls = [f"https://www.realtor.com/realestateandhomes-search/Wisconsin/pg-{page}"
    for page in range (1, 206)
]        
    # Taking the embedded JSON from the webpage
    def parse(self, response):
        next_data_script = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        # will show error if pulling json does not work
        if not next_data_script:
            self.logger.error("Failed to find __NEXT_DATA__ script on the page")
            return

        # Load JSON data
        try:
            data = json.loads(next_data_script)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON: {e}")
            return

        # Extract homes data from the JSON structure
        homes = data.get('props', ).get('pageProps', ).get('properties', )

        for home in homes:
            home_data = {
                "Home Type": home["description"].get("type", None),
                "Posted": home.get("list_date", None),
                "URL": ("https://www.realtor.com/realestateandhomes-detail/" + home.get("permalink", "") ),
                "Home Status": home.get("status", None),
                "Home Price": home.get("list_price", None),
                "Home City": home["location"]["address"].get("city", None),
                "Home Address": home["location"]["address"].get("line", None),
                "Home Zipcode": home["location"]["address"].get("postal_code", None),
                "Lat": home["location"]["address"]["coordinate"].get("lat", None),
                "Lon": home["location"]["address"]["coordinate"].get("lon", None),
                "Num Beds": home["description"].get("beds", None),
                "Num Baths": home["description"].get("baths_consolidated", None),
                "Square Feet": home["description"].get("sqft", None),
                "Brokered by": home.get("branding")[0].get("name", None),
                # "image_urls": home.get('photos', []) Images are appearing very small need to fix this issue             
            }
            yield home_data