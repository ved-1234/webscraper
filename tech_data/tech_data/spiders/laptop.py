import scrapy
import mysql.connector
import random

class LaptopSpider(scrapy.Spider):
    name = "laptop"
    start_page = 1
    max_pages = 800 # Update with the actual number of pages

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ayush@123',
            database='LaptopData'
        )

    def closed(self, reason):
        self.conn.close()

    def start_requests(self):
        base_url = "https://tech.hindustantimes.com/laptop-finder?&page={}"

        for page_number in range(self.start_page, self.max_pages + 1):
            url = base_url.format(page_number)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Extract links to individual laptop detail pages
        laptop_links = response.css('div.overallAnchor::attr(data-metaurl)').getall()

        for laptop_link in laptop_links:
            yield response.follow(laptop_link, callback=self.parse_laptop)

        # Check if there's a "Next" page button
        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_laptop(self, response):
        # Extract laptop specifications from the individual laptop detail page
        score = response.css('div.num span::text').get()

        if score is None:
            score = str(random.randint(2, 7))  # Generate a random integer between 2 and 7 (inclusive)
        else:
            score = score.strip()
            price = response.css('div.detail.priceIcon::text').getall()[-1].strip()
        laptop_info = {
            'Image': response.css('.entry__img.lazyload::attr(src)').get(),
            'Laptop Name': response.css('.tooltip h1::text').get(),
            'Score': score,
            'Price': price,
            # General Info
            'Brand': response.css('li label:contains("Brand") + span::text').get(),
            'Model': response.css('li label:contains("Model") + span::text').get(),
            'Colors': response.css('li label:contains("Colors") + span::text').get() or response.css('li label:contains("Colour") + span::text').get(),
            'Dimensions': response.css('li label:contains("Dimensionswxdxh") + span::text').get() or response.css('li label:contains("Dimensions(WxDxH") + span::text').get(),
            'Thickness': response.css('li label:contains("Thickness") + span::text').get(),
            'Weight': response.css('li label:contains("Weight") + span::text').get(),
            'Operating System': None,
            'Operating System Type': response.css('li label:contains("Operating System Type") + span::text').get(),

            # Storage

            'SSD Capacity': response.css('li label:contains("SSD Capacity") + span::text').get(),

            # Memory

            'RAM': response.css('li label:contains("RAM") + span::text').get(),
            'RAM Type': response.css('li label:contains("RAM type") + span::text').get(),
            'Memory Slots': response.css('li label:contains("Memory Slots") + span::text').get(),
            'Expandable Memory': response.css('li label:contains("Expandable Memory") + span::text').get(),
            'Memory Layout': response.css('li label:contains("Memory Layout") + span::text').get(),
            'Capacity': response.css('li label:contains("Capacity") + span::text').get(),

            # Processor
            'Processor': None,
            'Graphic Processor': None,
            'Clockspeed': response.css('li label:contains("Clockspeed") + span::text').get(),

            # Battery

            'Battery Type': response.css('li label:contains("Battery type") + span::text').get(),
            'Battery Cell': response.css('li label:contains("Battery Cell") + span::text').get(),
            'Power Supply': response.css('li label:contains("Power Supply")+ span::text').get(),

            # Display Details

            'Display Touchscreen': response.css(
                'li label:contains("Display Touchscreen") + span::text').get() or response.css(
                'li label:contains("Touchscreen") + span::text').get(),
            'Pixel Density': response.css('li label:contains("Pixel Density") + span::text').get(),
            'Display Size': response.css('li label:contains("Display Size") + span::text').get(),
            'Display Features': response.css('li label:contains("Display Features") + span::text').get(),
            'Display Resolution': response.css('li label:contains("Display Resolution") + span::text').get(),
            'Display Type': response.css('li label:contains("Display Type") + span::text').get(),

            # Multimedia

            'Sound Technologies': response.css('li label:contains("Sound Technologies") + span::text').get(),
            'Video Recording': response.css('li label:contains("Video Recording") + span::text').get(),
            'Speakers': response.css('li label:contains("Speakers") + span::text').get(),
            'Microphone Type': response.css('li label:contains("Microphone Type") + span::text').get(),
            'Webcam': response.css('li label:contains("Webcam") + span::text').get(),
            'Inbuilt Microphone': response.css('li label:contains("Inbuilt Microphone") + span::text').get(),

            # Networking

            'Wireless LAN': response.css('li label:contains("Wireless LAN") + span::text').get(),
            'Bluetooth Version': response.css('li label:contains("Bluetooth Version") + span::text').get(),
            'Bluetooth': response.css('li label:contains("Bluetooth") + span::text').get(),

            # Others

            'Sales Package': response.css('li label:contains("Sales Package") + span::text').get(),
            'Warranty': response.css('li label:contains("Warranty") + span::text').get(),

            # Peripheral

            'Fingerprint Scanner': response.css('li label:contains("Fingerprint Scanner") + span::text').get(),
            'Keyboard': response.css('li label:contains("Keyboard") + span::text').get(),

            # Ports

            'Headphone Jack': response.css('li label:contains("Headphone Jack") + span::text').get(),

            'Microphone Jack': response.css('li label:contains("Microphone Jack") + span::text').get(),
        }

        # For Operating System
        os_values = response.css('li:contains("Operating System") span::text').getall()
        os_values = [value for value in os_values if "64-bit" not in value]

        # Assign values to the fields
        if os_values:
            laptop_info['Operating System'] = os_values[0]

        # For Processor and Graphic Processor
        for spec in response.css('li'):
            label = spec.css('label::text').get()
            value = spec.css('span::text').get()

            if label and value:
                label = label.strip()
                value = value.strip()

                if label == "Processor":
                    laptop_info['Processor'] = value
                elif label == "Graphic Processor":
                    laptop_info['Graphic Processor'] = value




        # Insert the scraped data into the MySQL database
        cursor = self.conn.cursor()
        select_query = "SELECT 1 FROM laptops WHERE laptop_name = %(Laptop Name)s LIMIT 1"
        cursor.execute(select_query, laptop_info)
        existing_record = cursor.fetchone()

        # If the record doesn't exist, insert it into the database
        if not existing_record:



                insert_query = """
             INSERT INTO laptops (
                 image_url,
                 laptop_name,
                 score,
                 price,
                 brand,
                 model,
                 colors,
                 dimensions,
                 thickness,
                 weight,
                 operating_system,
                 operating_system_type,
                 ssd_capacity,
                 ram,
                 ram_type,
                 memory_slots,
                 expandable_memory,
                 memory_layout,
                 capacity,
                 processor,
                 graphic_processor,
                 clockspeed,
                 battery_type,
                 battery_cell,
                 power_supply,
                 display_touchscreen,
                 pixel_density,
                 display_size,
                 display_features,
                 display_resolution,
                 display_type,
                 sound_technologies,
                 video_recording,
                 speakers,
                 microphone_type,
                 webcam,
                 inbuilt_microphone,
                 wireless_lan,
                 bluetooth_version,
                 bluetooth,
                 sales_package,
                 warranty,
                 fingerprint_scanner,
                 keyboard,
                 headphone_jack,
                 microphone_jack
             ) VALUES (
                 %(Image)s,
                 %(Laptop Name)s,
                 %(Score)s,
                 %(Price)s,
                 %(Brand)s,
                 %(Model)s,
                 %(Colors)s,
                 %(Dimensions)s,
                 %(Thickness)s,
                 %(Weight)s,
                 %(Operating System)s,
                 %(Operating System Type)s,
                 %(SSD Capacity)s,
                 %(RAM)s,
                 %(RAM Type)s,
                 %(Memory Slots)s,
                 %(Expandable Memory)s,
                 %(Memory Layout)s,
                 %(Capacity)s,
                 %(Processor)s,
                 %(Graphic Processor)s,
                 %(Clockspeed)s,
                 %(Battery Type)s,
                 %(Battery Cell)s,
                 %(Power Supply)s,
                 %(Display Touchscreen)s,
                 %(Pixel Density)s,
                 %(Display Size)s,
                 %(Display Features)s,
                 %(Display Resolution)s,
                 %(Display Type)s,
                 %(Sound Technologies)s,
                 %(Video Recording)s,
                 %(Speakers)s,
                 %(Microphone Type)s,
                 %(Webcam)s,
                 %(Inbuilt Microphone)s,
                 %(Wireless LAN)s,
                 %(Bluetooth Version)s,
                 %(Bluetooth)s,
                 %(Sales Package)s,
                 %(Warranty)s,
                 %(Fingerprint Scanner)s,
                 %(Keyboard)s,
                 %(Headphone Jack)s,
                 %(Microphone Jack)s
             )
             """

        cursor.execute(insert_query, laptop_info)
        self.conn.commit()
        cursor.close()

        yield laptop_info