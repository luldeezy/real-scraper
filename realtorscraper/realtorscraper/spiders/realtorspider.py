import scrapy
import json

    # Data being pulled 
class RealtorSpider(scrapy.Spider):
    name = "realtorspider"
    start_urls = ["https://www.realtor.com/realestateandhomes-search/Madison_WI"]

    def parse(self, response):
        # Taking the embedded JSON from the webpage
        next_data_script = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        # will show error if script does not work
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
                "home type": home["description"].get("type", None),
                "posted": home.get("list_date", None),
                "home URL": home.get("permalink", None),
                "home main image": home["primary_photo"].get("href", None),
                "home status": home.get("status", None),
                "home price": home.get("list_price", None),
                "home address": home["location"]["address"].get("line", None),
                "home zipcode": home["location"]["address"].get("postal_code", None),
                "num beds": home["description"].get("beds", None),
                "num baths": home["description"].get("baths_consolidated", None),
                "Square Feet": home["description"].get("sqft", None),
            }
            yield home_data

        # Optional: Handle pagination for additional pages
        next_page_url = data.get("props", {}).get("pageProps", {}).get(
            "searchPageState", {}
        ).get("pagination", {}).get("nextUrl")

        if next_page_url:
            full_next_page_url = response.urljoin(next_page_url)
            self.logger.info(f"Following pagination to: {full_next_page_url}")
            yield scrapy.Request(url=full_next_page_url, callback=self.parse)
