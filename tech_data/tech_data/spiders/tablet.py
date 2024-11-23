import scrapy
import mysql.connector
import random

class TabletSpider(scrapy.Spider):
    name = "tablet"
    start_page = 1
    max_pages = 8 # Update with the actual number of pages

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ayush@123',
            database='LaptopData'  # Update the database name to match the tablet data
        )

    def closed(self, reason):
        self.conn.close()

    def start_requests(self):
        base_url = "https://tech.hindustantimes.com/tablet-finder?&page={}"

        for page_number in range(self.start_page, self.max_pages + 1):
            url = base_url.format(page_number)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Extract links to individual tablet detail pages
        tablet_links = response.css('div.overallAnchor::attr(data-metaurl)').getall()

        for tablet_link in tablet_links:
            yield response.follow(tablet_link, callback=self.parse_tablet)

        # Check if there's a "Next" page button
        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_tablet(self, response):
        # Extract tablet specifications from the individual tablet detail page
        score = response.css('div.num span::text').get()

        if score is None:
            score = str(random.randint(2, 7))  # Generate a random integer between 2 and 7 (inclusive)
        else:
            score = score.strip()

        price = response.css('div.detail.priceIcon::text').getall()[-1].strip()

        tablet_info = {
            'Image': response.css('.entry__img.lazyload::attr(src)').get(),

            'Score': score,
            'Price': price,
            # General Info
            'Tablet Name': response.css('.tooltip h1::text').get(),
            'Brand': response.css('li label:contains("Brand") + span::text').get(),
            'Model': response.css('li label:contains("Model") + span::text').get(),
            'Operating System': response.css('li label:contains("Operating System") + span::text').get(),
            'Custom UI': response.css('li label:contains("Custom UI") + span::text').get(),
            'Launch Date': response.css('li label:contains("Launch Date") + span::text').get(),

            # Battery
            'Battery Type': response.css('li label:contains("Type") + span::text').get(),
            'User Replaceable Battery': response.css('li label:contains("User Replaceable") + span::text').get(),
            'Quick Charging': response.css('li label:contains("Quick Charging") + span::text').get(),
            'USB Type-C': response.css('li label:contains("USB Type-C") + span::text').get(),
            'Battery Capacity': response.css('li label:contains("Capacity") + span::text').get(),

            # Camera
            'Camera Settings': response.css('li label:contains("Settings") + span::text').get(),
            'Camera Features': response.css('li label:contains("Camera Features") + span::text').get(),
            'Video Recording': response.css('li label:contains("Video Recording") + span::text').get(),
            'Shooting Modes': response.css('li label:contains("Shooting Modes") + span::text').get(),
            'Camera Resolution': response.css('li label:contains("Resolution") + span::text').get(),
            'Autofocus': response.css('li label:contains("Autofocus") + span::text').get(),
            'Flash': response.css('li label:contains("Flash") + span::text').get(),
            'Image Resolution': response.css('li label:contains("Image Resolution") + span::text').get(),

            # Design
            'Width': response.css('li label:contains("Width") + span::text').get(),
            'Height': response.css('li label:contains("Height") + span::text').get(),
            'Weight': response.css('li label:contains("Weight") + span::text').get(),
            'Thickness': response.css('li label:contains("Thickness") + span::text').get(),
            'Colors': response.css('li label:contains("Colors") + span::text').get() or response.css('li label:contains("Colour") + span::text').get(),

            # Display
            'Screen Protection': response.css('li label:contains("Screen Protection") + span::text').get(),
            'Screen Size': response.css('li label:contains("Screen Size") + span::text').get(),
            'Display Type': response.css('li label:contains("Display Type") + span::text').get(),
            'Touch Screen': response.css('li label:contains("Touch Screen") + span::text').get(),
            'Pixel Density': response.css('li label:contains("Pixel Density") + span::text').get(),
            'Screen to Body Ratio': response.css('li label:contains("Screen to Body Ratio") + span::text').get(),
            'Screen Resolution': response.css('li label:contains("Screen Resolution") + span::text').get(),

            # Multimedia
            'Fm Radio': response.css('li label:contains("Fm Radio") + span::text').get(),
            'Audio Features': response.css('li label:contains("Audio Features") + span::text').get(),
            'Audio Jack': response.css('li label:contains("Audio Jack") + span::text').get(),

            # Storage
            'Expandable Memory': response.css('li label:contains("Expandable Memory") + span::text').get(),
            'Internal Memory': response.css('li label:contains("Internal Memory") + span::text').get(),

            # Network & Connectivity
            'Network Support': response.css('li label:contains("Network Support") + span::text').get(),
            'USB Connectivity': response.css('li label:contains("USB Connectivity") + span::text').get(),
            'WiFi': response.css('li label:contains("WiFi") + span::text').get(),
            'Voice Calling': response.css('li label:contains("Voice Calling") + span::text').get(),
            'VoLTE': response.css('li label:contains("VoLTE") + span::text').get(),
            'Bluetooth': response.css('li label:contains("Bluetooth") + span::text').get(),
            'NFC': response.css('li label:contains("NFC") + span::text').get(),
            'Wifi Features': response.css('li label:contains("Wifi Features") + span::text').get(),

            # Performance
            'Architecture': response.css('li label:contains("Architecture") + span::text').get(),
            'Processor': response.css('li label:contains("Processor") + span::text').get(),
            'Graphics': response.css('li label:contains("Graphics") + span::text').get(),
            'RAM': response.css('li label:contains("RAM") + span::text').get(),
            'Chipset': response.css('li label:contains("Chipset") + span::text').get(),

            # Smart TV Features
            'Smart TV Camera': response.css('li label:contains("Camera") + span::text').get(),

            # Special Features
            'Fingerprint Sensor': response.css('li label:contains("Fingerprint Sensor") + span::text').get(),
            'Other Sensors': response.css('li label:contains("Other Sensors") + span::text').get(),



        }

        cursor = self.conn.cursor()
        select_query = "SELECT 1 FROM tablets WHERE tablet_name = %(Tablet Name)s LIMIT 1"
        cursor.execute(select_query, tablet_info)
        existing_record = cursor.fetchone()

        # If the record doesn't exist, insert it into the database
        if not existing_record:
            insert_query = """
               INSERT INTO tablets (
                   image_url,
                   tablet_name,
                   score,
                   price,
                   brand,
                   model,
                   colors,
                   battery_type,
                   user_replaceable_battery,
                   quick_charging,
                   usb_type_c,
                   battery_capacity,
                   camera_settings,
                   camera_features,
                   video_recording,
                   shooting_modes,
                   camera_resolution,
                   autofocus,
                   flash,
                   image_resolution,
                   width,
                   weight,
                   height,
                   thickness,
                   screen_protection,
                   screen_size,
                   display_type,
                   touch_screen,
                   pixel_density,
                   screen_to_body_ratio,
                   screen_resolution,
                   operating_system,
                   custom_ui,
                   launch_date,
                   network_support,
                   fingerprint_sensor,
                   fm_radio,
                   audio_features,
                   audio_jack,
                   usb_connectivity,
                   wifi,
                   voice_calling,
                   volte,
                   bluetooth,
                   nfc,
                   wifi_features,
                   architecture,
                   processor,
                   graphics,
                   ram,
                   chipset,
                   smart_tv_camera,
                   other_sensors,
                   expandable_memory,
                   internal_memory
                   -- Add more columns here if needed
               ) VALUES (
                   %(Image)s,
                   %(Tablet Name)s,
                   %(Score)s,
                   %(Price)s,
                   %(Brand)s,
                   %(Model)s,
                   %(Colors)s,
                   %(Battery Type)s,
                   %(User Replaceable Battery)s,
                   %(Quick Charging)s,
                   %(USB Type-C)s,
                   %(Battery Capacity)s,
                   %(Camera Settings)s,
                   %(Camera Features)s,
                   %(Video Recording)s,
                   %(Shooting Modes)s,
                   %(Camera Resolution)s,
                   %(Autofocus)s,
                   %(Flash)s,
                   %(Image Resolution)s,
                   %(Width)s,
                   %(Weight)s,
                   %(Height)s,
                   %(Thickness)s,
                   %(Screen Protection)s,
                   %(Screen Size)s,
                   %(Display Type)s,
                   %(Touch Screen)s,
                   %(Pixel Density)s,
                   %(Screen to Body Ratio)s,
                   %(Screen Resolution)s,
                   %(Operating System)s,
                   %(Custom UI)s,
                   %(Launch Date)s,
                   %(Network Support)s,
                   %(Fingerprint Sensor)s,
                   %(Fm Radio)s,
                   %(Audio Features)s,
                   %(Audio Jack)s,
                   %(USB Connectivity)s,
                   %(WiFi)s,
                   %(Voice Calling)s,
                   %(VoLTE)s,
                   %(Bluetooth)s,
                   %(NFC)s,
                   %(Wifi Features)s,
                   %(Architecture)s,
                   %(Processor)s,
                   %(Graphics)s,
                   %(RAM)s,
                   %(Chipset)s,
                   %(Smart TV Camera)s,
                   %(Other Sensors)s,
                   %(Expandable Memory)s,
                   %(Internal Memory)s
                   -- Add more values here if needed
               )
               """
            cursor.execute(insert_query, tablet_info)
            self.conn.commit()
            cursor.close()

            yield tablet_info

