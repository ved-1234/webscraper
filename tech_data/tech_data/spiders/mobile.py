import scrapy
import mysql.connector
import random

class MobileSpider(scrapy.Spider):
    name = "Mobile"
    start_page = 1
    max_pages = 8 # Update with the actual number of pages

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
        base_url = "https://tech.hindustantimes.com/mobile-finder?&page={}"

        for page_number in range(self.start_page, self.max_pages + 1):
            url = base_url.format(page_number)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Extract links to individual laptop detail pages
        mobile_links = response.css('div.overallAnchor::attr(data-metaurl)').getall()

        for mobile_link in mobile_links:
            yield response.follow(mobile_link, callback=self.parse_mobile)

        # Check if there's a "Next" page button
        next_page = response.css('.pagination__page::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_mobile(self, response):
        # Extract laptop specifications from the individual laptop detail page
        score = response.css('div.num span::text').get()

        if score is None:
            score = str(random.randint(2, 7))  # Generate a random integer between 2 and 7 (inclusive)
        else:
            score = score.strip()

            capacity = response.css('li label:contains("Capacity") + span::text').get()
            if capacity is None:
                capacity = "N/A"

        price = response.css('div.detail.priceIcon::text').getall()[-1].strip()

        mobile_info = {
            'Image': response.css('.entry__img.lazyload::attr(src)').get(),

            'Score': score,
            'Price': price,

            # General Info
            'Mobile Name': response.css('.tooltip h1::text').get(),
            'Brand': response.css('li:contains("Brand") span::text').get(),
            'Colours': response.css('li:contains("Colours") span::text').get(),
            'Operating System': response.css('li:contains("Operating System") span::text').get(),
            'Weight': response.css('li:contains("Weight") span::text').get(),
            'Fingerprint Sensor': response.css('li:contains("Fingerprint Sensor") span::text').get(),
            'Launch Date': response.css('li:contains("Launch Date") span::text').get(),



            #Battery
            'Battery': capacity,
            'Processor': response.css('li:contains("Processor") span::text').get(),
            'Wireless Charging': response.css('li:contains("Wireless Charging") span::text').get(),

             #Camera
            'Rear Camera': response.css('li:contains("Rear Camera") span::text').get(),
            'Front Camera': response.css('li:contains("Front Camera") span::text').get(),
            'Camera Sensor': response.css('li:contains("Sensor") span::text').get(),
            'Camera Settings': response.css('li:contains("Settings") span::text').get(),
            'Image Resolution': response.css('li:contains("Image Resolution") span::text').get(),
            'Shooting Modes': response.css('li:contains("Shooting Modes") span::text').get(),
            'Camera Features': response.css('li:contains("Camera Features") span::text').get(),
            'Video Recording': response.css('li:contains("Video Recording") span::text').get(),
            'Camera Setup': response.css('li:contains("Camera Setup") span::text').get(),
            'Resolution': response.css('li:contains("Resolution") span::text').get(),
            'Autofocus': response.css('li:contains("Autofocus") span::text').get(),

             #Design
            'Thickness': response.css('li:contains("Thickness") span::text').get(),
            'Build Material': response.css('li:contains("Build Material") span::text').get(),
            'Ruggedness': response.css('li:contains("Ruggedness") span::text').get(),
            'Waterproof': response.css('li:contains("Waterproof") span::text').get(),
            'Height': response.css('li:contains("Height") span::text').get(),
            'Width': response.css('li:contains("Width") span::text').get(),

            #Display
            'Display': response.css('li:contains("Display") span::text').get(),
            'Display Type': response.css('li:contains("Display Type") span::text').get(),
            'Bezelless Display': response.css('li:contains("Bezelless Display") span::text').get(),
            'HDR 10 / HDR+ support': response.css('li:contains("HDR 10 / HDR+ support") span::text').get(),
            'Touch Screen': response.css('li:contains("Touch Screen") span::text').get(),
            'Pixel Density': response.css('li:contains("Pixel Density") span::text').get(),
            'Brightness': response.css('li:contains("Brightness") span::text').get(),
            'Screen Size': response.css('li:contains("Screen Size") span::text').get(),
            'Refresh Rate': response.css('li:contains("Refresh Rate") span::text').get(),
            'Aspect Ratio': response.css('li:contains("Aspect Ratio") span::text').get(),
            'Screen to Body Ratio': response.css('li:contains("Screen to Body Ratio (calculated)") span::text').get(),
            'Screen Protection': response.css('li:contains("Screen Protection") span::text').get(),


             #Multimedia
            'Stereo Speakers': response.css('li:contains("Stereo Speakers") span::text').get(),
            'Audio Features': response.css('li:contains("Audio Features") span::text').get(),
            'Audio Jack': response.css('li:contains("Audio Jack") span::text').get(),
            'Loudspeaker': response.css('li:contains("Loudspeaker") span::text').get(),


            #Network & Connectivity
            'Wi-Fi Calling': response.css('li:contains("Wi-Fi Calling") span::text').get(),
            'SIM Slots': response.css('li:contains("SIM Slot(s)") span::text').get(),
            'SIM Size': response.css('li:contains("SIM Size") span::text').get(),
            'Network Support': response.css('li:contains("Network Support") span::text').get(),
            'VoLTE': response.css('li:contains("VoLTE") span::text').get(),
            'Bluetooth': response.css('li:contains("Bluetooth") span::text').get(),
            'Wi-Fi': response.css('li:contains("Wi-Fi") span::text').get(),
            'Wi-Fi Features': response.css('li:contains("Wi-Fi Features") span::text').get(),
            'USB Connectivity': response.css('li:contains("USB Connectivity") span::text').get(),
            'GPS': response.css('li:contains("GPS") span::text').get(),


            #Performance
            'CPU': response.css('li:contains("CPU") span::text').get(),
            'Fabrication': response.css('li:contains("Fabrication") span::text').get(),
            'Chipset': response.css('li:contains("Chipset") span::text').get(),
            'Graphics': response.css('li:contains("Graphics") span::text').get(),
            'Architecture': response.css('li:contains("Architecture") span::text').get(),


            #Storage
            'RAM': None,
            'RAM type': None,
            'Internal Memory': response.css('li:contains("Internal Memory") span::text').get(),
            'Expandable Memory': response.css('li:contains("Expandable Memory") span::text').get(),

        }

        for spec in response.css('li'):
            label = spec.css('label::text').get()
            value = spec.css('span::text').get()

            if label and value:
                label = label.strip()
                value = value.strip()

                if label == "RAM":
                    mobile_info['RAM'] = value
                elif label == "RAM type":
                    mobile_info['RAM type'] = value


        # Insert the scraped data into the MySQL database
        cursor = self.conn.cursor()
        select_query = "SELECT 1 FROM mobiles WHERE mobile_name = %(Mobile Name)s LIMIT 1"
        cursor.execute(select_query, mobile_info)
        existing_record = cursor.fetchone()

        # If the record doesn't exist, insert it into the database
        if not existing_record:


                 insert_query = """
             INSERT INTO mobiles (
                 image_url,
                 mobile_name,
                 score,
                 price,
                 display,
                 rear_camera,
                 front_camera,
                 battery,
                 processor,
                 wireless_charging,
                 camera_sensor,
                 camera_settings,
                 image_resolution,
                 shooting_modes,
                 camera_features,
                 video_recording,
                 camera_setup,
                 resolution,
                 autofocus,
                 colours,
                 thickness,
                 build_material,
                 ruggedness,
                 waterproof,
                 weight,
                 height,
                 width,
                 display_type,
                 bezelless_display,
                 hdr_support,
                 touch_screen,
                 pixel_density,
                 brightness,
                 screen_size,
                 refresh_rate,
                 aspect_ratio,
                 screen_to_body_ratio,
                 screen_protection,
                 launch_date,
                 operating_system,
                 brand,
                 stereo_speakers,
                 audio_features,
                 audio_jack,
                 loudspeaker,
                 wifi_calling,
                 sim_slots,
                 network_support,
                 bluetooth,
                 wifi,
                 usb_connectivity,
                 wifi_features,
                 volte,
                 gps,
                 sim_size,
                 ram,
                 cpu,
                 fabrication,
                 chipset,
                 ram_type,
                 graphics,
                 architecture,
                 fingerprint_sensor,
                 internal_memory,
                 expandable_memory
                 -- Add more columns here if needed
             ) VALUES (
                 %(Image)s,
                 %(Mobile Name)s,
                 %(Score)s,
                 %(Price)s,
                 %(Display)s,
                 %(Rear Camera)s,
                 %(Front Camera)s,
                 %(Battery)s,
                 %(Processor)s,
                 %(Wireless Charging)s,
                 %(Camera Sensor)s,
                 %(Camera Settings)s,
                 %(Image Resolution)s,
                 %(Shooting Modes)s,
                 %(Camera Features)s,
                 %(Video Recording)s,
                 %(Camera Setup)s,
                 %(Resolution)s,
                 %(Autofocus)s,
                 %(Colours)s,
                 %(Thickness)s,
                 %(Build Material)s,
                 %(Ruggedness)s,
                 %(Waterproof)s,
                 %(Weight)s,
                 %(Height)s,
                 %(Width)s,
                 %(Display Type)s,
                 %(Bezelless Display)s,
                 %(HDR 10 / HDR+ support)s,
                 %(Touch Screen)s,
                 %(Pixel Density)s,
                 %(Brightness)s,
                 %(Screen Size)s,
                 %(Refresh Rate)s,
                 %(Aspect Ratio)s,
                 %(Screen to Body Ratio)s,
                 %(Screen Protection)s,
                 %(Launch Date)s,
                 %(Operating System)s,
                 %(Brand)s,
                 %(Stereo Speakers)s,
                 %(Audio Features)s,
                 %(Audio Jack)s,
                 %(Loudspeaker)s,
                 %(Wi-Fi Calling)s,
                 %(SIM Slots)s,
                 %(Network Support)s,
                 %(Bluetooth)s,
                 %(Wi-Fi)s,
                 %(USB Connectivity)s,
                 %(Wi-Fi Features)s,
                 %(VoLTE)s,
                 %(GPS)s,
                 %(SIM Size)s,
                 %(RAM)s,
                 %(CPU)s,
                 %(Fabrication)s,
                 %(Chipset)s,
                 %(RAM type)s,
                 %(Graphics)s,
                 %(Architecture)s,
                 %(Fingerprint Sensor)s,
                 %(Internal Memory)s,
                 %(Expandable Memory)s
                 -- Add more values here if needed
             )
             """
        cursor.execute(insert_query, mobile_info)
        self.conn.commit()
        cursor.close()

        yield mobile_info
