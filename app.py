from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ayush@123'
app.config['MYSQL_DB'] = 'LaptopData'

mysql = MySQL(app)

@app.route('/')
def index():
    # You can include any necessary logic here
    return render_template('index.html')  # Render the index.html template

@app.route('/get_laptop_suggestions')
def get_laptop_suggestions():
    user_input = request.args.get('input')

    # Query the database for laptop name suggestions, limiting to 5 results
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT laptop_name FROM laptops WHERE laptop_name LIKE %s LIMIT 4", ('%' + user_input + '%',))
    laptop_suggestions = [row[0] for row in cur.fetchall()]
    cur.close()

    return jsonify({'suggestions': laptop_suggestions})

@app.route('/compare2L.html')
def compare2laptops():
    laptop1_name = request.args.get('laptop1')
    laptop2_name = request.args.get('laptop2')

    # Query the database for laptop information
    cur = mysql.connection.cursor()
    cur.execute("SELECT laptop_name, brand, model, colors, thickness, weight, operating_system, operating_system_type, ssd_capacity, ram, ram_type, memory_slots, expandable_memory, memory_layout, capacity, processor, graphic_processor, clockspeed, battery_type, battery_cell, power_supply, display_touchscreen, pixel_density, display_size, display_features, display_resolution, display_type, sound_technologies, video_recording, speakers, microphone_type, webcam, inbuilt_microphone, wireless_lan, bluetooth_version, bluetooth, sales_package, warranty, fingerprint_scanner, keyboard, headphone_jack, microphone_jack, image_url, score,price FROM laptops WHERE laptop_name = %s OR laptop_name = %s",(laptop1_name, laptop2_name))

    laptop_data = cur.fetchall()
    cur.close()

    if len(laptop_data) == 2:
        return render_template('compare2L.html', laptop_data=laptop_data)
    else:
        return redirect(url_for('index'))


@app.route('/compare3L.html')
def compare3laptops():
    laptop1_name = request.args.get('laptop1')
    laptop2_name = request.args.get('laptop2')
    laptop3_name = request.args.get('laptop3')

    # Query the database for laptop information
    cur = mysql.connection.cursor()
    cur.execute("SELECT laptop_name, brand, model, colors, thickness, weight, operating_system, operating_system_type, ssd_capacity, ram, ram_type, memory_slots, expandable_memory, memory_layout, capacity, processor, graphic_processor, clockspeed, battery_type, battery_cell, power_supply, display_touchscreen, pixel_density, display_size, display_features, display_resolution, display_type, sound_technologies, video_recording, speakers, microphone_type, webcam, inbuilt_microphone, wireless_lan, bluetooth_version, bluetooth, sales_package, warranty, fingerprint_scanner, keyboard, headphone_jack, microphone_jack, image_url, score,price FROM laptops WHERE laptop_name = %s OR laptop_name = %s OR laptop_name = %s",
                (laptop1_name, laptop2_name, laptop3_name))
    laptop_data = cur.fetchall()
    cur.close()

    if len(laptop_data) == 3:
        return render_template('compare3L.html', laptop_data=laptop_data)
    else:
        return redirect(url_for('index'))

@app.route('/compare4L.html')
def compare4laptops():
    laptop1_name = request.args.get('laptop1')
    laptop2_name = request.args.get('laptop2')
    laptop3_name = request.args.get('laptop3')
    laptop4_name = request.args.get('laptop4')

    # Query the database for laptop information
    cur = mysql.connection.cursor()
    cur.execute("SELECT laptop_name, brand, model, colors, thickness, weight, operating_system, operating_system_type, ssd_capacity, ram, ram_type, memory_slots, expandable_memory, memory_layout, capacity, processor, graphic_processor, clockspeed, battery_type, battery_cell, power_supply, display_touchscreen, pixel_density, display_size, display_features, display_resolution, display_type, sound_technologies, video_recording, speakers, microphone_type, webcam, inbuilt_microphone, wireless_lan, bluetooth_version, bluetooth, sales_package, warranty, fingerprint_scanner, keyboard, headphone_jack, microphone_jack, image_url, score, price FROM laptops WHERE laptop_name = %s OR laptop_name = %s OR laptop_name = %s OR laptop_name = %s",
                (laptop1_name, laptop2_name, laptop3_name, laptop4_name))
    laptop_data = cur.fetchall()
    cur.close()

    if len(laptop_data) == 4:
        return render_template('compare4L.html', laptop_data=laptop_data)
    else:
        return redirect(url_for('index'))


@app.route('/mob.html')
def mobile_page():
    return render_template('mob.html')

@app.route('/get_mobile_suggestions')
def get_mobile_suggestions():
    user_input = request.args.get('input')

    # Query the database for laptop name suggestions, limiting to 5 results
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT mobile_name FROM mobiles WHERE mobile_name LIKE %s LIMIT 4", ('%' + user_input + '%',))
    mobile_suggestions = [row[0] for row in cur.fetchall()]
    cur.close()

    return jsonify({'suggestions': mobile_suggestions})
@app.route('/compare2M.html')
def compare2mobiles():
    mobile1_name = request.args.get('mobile1')
    mobile2_name = request.args.get('mobile2')

    cur = mysql.connection.cursor()
    cur.execute("SELECT mobile_name, brand, colours, operating_system, weight, fingerprint_sensor, launch_date, battery, processor, wireless_charging, rear_camera, front_camera, camera_sensor, camera_settings, image_resolution, shooting_modes, camera_features, video_recording, camera_setup, resolution, autofocus, thickness, build_material, ruggedness, waterproof, height, width, display, display_type, bezelless_display, hdr_support, touch_screen, pixel_density, brightness, screen_size, refresh_rate, aspect_ratio, screen_to_body_ratio, screen_protection, stereo_speakers, audio_features, audio_jack, loudspeaker, wifi_calling, sim_slots, sim_size, network_support, volte, bluetooth, wifi, wifi_features, usb_connectivity, gps, cpu, fabrication, chipset, graphics, architecture, ram, ram_type, internal_memory, expandable_memory,image_url,price FROM mobiles WHERE mobile_name = %s OR mobile_name = %s",(mobile1_name, mobile2_name))
    mobile_data = cur.fetchall()
    cur.close()
    if len(mobile_data) == 2:
        return render_template('compare2M.html', mobile_data=mobile_data)
    else:
        return redirect(url_for('mobile_page'))

@app.route('/compare3M.html')
def compare3mobiles():
        mobile1_name = request.args.get('mobile1')
        mobile2_name = request.args.get('mobile2')
        mobile3_name = request.args.get('mobile3')

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT mobile_name, brand, colours, operating_system, weight, fingerprint_sensor, launch_date, battery, processor, wireless_charging, rear_camera, front_camera, camera_sensor, camera_settings, image_resolution, shooting_modes, camera_features, video_recording, camera_setup, resolution, autofocus, thickness, build_material, ruggedness, waterproof, height, width, display, display_type, bezelless_display, hdr_support, touch_screen, pixel_density, brightness, screen_size, refresh_rate, aspect_ratio, screen_to_body_ratio, screen_protection, stereo_speakers, audio_features, audio_jack, loudspeaker, wifi_calling, sim_slots, sim_size, network_support, volte, bluetooth, wifi, wifi_features, usb_connectivity, gps, cpu, fabrication, chipset, graphics, architecture, ram, ram_type, internal_memory, expandable_memory,image_url,price FROM mobiles WHERE mobile_name = %s OR mobile_name = %s OR mobile_name = %s",(mobile1_name, mobile2_name, mobile3_name))
        mobile_data = cur.fetchall()
        cur.close()
        if len(mobile_data) == 3:
            return render_template('compare3M.html', mobile_data=mobile_data)
        else:
            return redirect(url_for('mobile_page'))


@app.route('/compare4M.html')
def compare4mobiles():
        mobile1_name = request.args.get('mobile1')
        mobile2_name = request.args.get('mobile2')
        mobile3_name = request.args.get('mobile3')
        mobile4_name = request.args.get('mobile4')

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT mobile_name, brand, colours, operating_system, weight, fingerprint_sensor, launch_date, battery, processor, wireless_charging, rear_camera, front_camera, camera_sensor, camera_settings, image_resolution, shooting_modes, camera_features, video_recording, camera_setup, resolution, autofocus, thickness, build_material, ruggedness, waterproof, height, width, display, display_type, bezelless_display, hdr_support, touch_screen, pixel_density, brightness, screen_size, refresh_rate, aspect_ratio, screen_to_body_ratio, screen_protection, stereo_speakers, audio_features, audio_jack, loudspeaker, wifi_calling, sim_slots, sim_size, network_support, volte, bluetooth, wifi, wifi_features, usb_connectivity, gps, cpu, fabrication, chipset, graphics, architecture, ram, ram_type, internal_memory, expandable_memory,image_url,price FROM mobiles WHERE mobile_name = %s OR mobile_name = %s OR mobile_name = %s OR mobile_name = %s",(mobile1_name, mobile2_name, mobile3_name, mobile4_name))
        mobile_data = cur.fetchall()
        cur.close()
        if len(mobile_data) == 4:
            return render_template('compare4M.html', mobile_data=mobile_data)
        else:
            return redirect(url_for('mobile_page'))

@app.route('/tab.html')
def tablet_page():
            return render_template('tab.html')

@app.route('/get_tablet_suggestions')
def get_tablet_suggestions():
    user_input = request.args.get('input')

    # Query the database for tablet name suggestions, limiting to 5 results
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT tablet_name FROM tablets WHERE tablet_name LIKE %s LIMIT 4", ('%' + user_input + '%',))
    tablet_suggestions = [row[0] for row in cur.fetchall()]
    cur.close()

    return jsonify({'suggestions': tablet_suggestions})
@app.route('/compare2T.html')
def compare2tablets():
    tablet1_name = request.args.get('tablet1')
    tablet2_name = request.args.get('tablet2')

    # Query the database for tablet information
    cur = mysql.connection.cursor()
    cur.execute("SELECT tablet_name, brand, model, operating_system, custom_ui, launch_date, "
                "battery_type, user_replaceable_battery, quick_charging, usb_type_c, battery_capacity, "
                "camera_settings, camera_features, video_recording, shooting_modes, camera_resolution, "
                "autofocus, flash, image_resolution, width, weight, height, thickness, colors, "
                "screen_protection, screen_size, display_type, touch_screen, pixel_density, "
                "screen_to_body_ratio, screen_resolution, fm_radio, audio_features, audio_jack, "
                "expandable_memory, internal_memory, network_support, usb_connectivity, wifi, "
                "voice_calling, volte, bluetooth, nfc, wifi_features, architecture, processor, "
                "graphics, ram, chipset, smart_tv_camera, other_sensors, fingerprint_sensor,image_url, score,price "
                "FROM tablets WHERE tablet_name = %s OR tablet_name = %s",
                (tablet1_name, tablet2_name))
    tablet_data = cur.fetchall()
    cur.close()

    if len(tablet_data) == 2:
        return render_template('compare2T.html', tablet_data=tablet_data)
    else:
        return redirect(url_for('tablet_page'))


@app.route('/compare3T.html')
def compare3tablets():
    tablet1_name = request.args.get('tablet1')
    tablet2_name = request.args.get('tablet2')
    tablet3_name = request.args.get('tablet3')

    # Query the database for tablet information
    cur = mysql.connection.cursor()
    cur.execute("SELECT tablet_name, brand, model, operating_system, custom_ui, launch_date, "
                "battery_type, user_replaceable_battery, quick_charging, usb_type_c, battery_capacity, "
                "camera_settings, camera_features, video_recording, shooting_modes, camera_resolution, "
                "autofocus, flash, image_resolution, width, weight, height, thickness, colors, "
                "screen_protection, screen_size, display_type, touch_screen, pixel_density, "
                "screen_to_body_ratio, screen_resolution, fm_radio, audio_features, audio_jack, "
                "expandable_memory, internal_memory, network_support, usb_connectivity, wifi, "
                "voice_calling, volte, bluetooth, nfc, wifi_features, architecture, processor, "
                "graphics, ram, chipset, smart_tv_camera, other_sensors, fingerprint_sensor,image_url, score,price "
                "FROM tablets WHERE tablet_name = %s OR tablet_name = %s OR tablet_name = %s",
                (tablet1_name, tablet2_name, tablet3_name))
    tablet_data = cur.fetchall()
    cur.close()

    if len(tablet_data) == 3:
        return render_template('compare3T.html', tablet_data=tablet_data)
    else:
        return redirect(url_for('tablet_page'))

@app.route('/compare4T.html')
def compare4tablets():
    tablet1_name = request.args.get('tablet1')
    tablet2_name = request.args.get('tablet2')
    tablet3_name = request.args.get('tablet3')
    tablet4_name = request.args.get('tablet4')

    # Query the database for tablet information
    cur = mysql.connection.cursor()
    cur.execute("SELECT tablet_name, brand, model, operating_system, custom_ui, launch_date, "
                "battery_type, user_replaceable_battery, quick_charging, usb_type_c, battery_capacity, "
                "camera_settings, camera_features, video_recording, shooting_modes, camera_resolution, "
                "autofocus, flash, image_resolution, width, weight, height, thickness, colors, "
                "screen_protection, screen_size, display_type, touch_screen, pixel_density, "
                "screen_to_body_ratio, screen_resolution, fm_radio, audio_features, audio_jack, "
                "expandable_memory, internal_memory, network_support, usb_connectivity, wifi, "
                "voice_calling, volte, bluetooth, nfc, wifi_features, architecture, processor, "
                "graphics, ram, chipset, smart_tv_camera, other_sensors, fingerprint_sensor,image_url, score,price "
                "FROM tablets WHERE tablet_name = %s OR tablet_name = %s OR tablet_name = %s OR tablet_name = %s",
                (tablet1_name, tablet2_name, tablet3_name, tablet4_name))
    tablet_data = cur.fetchall()
    cur.close()

    if len(tablet_data) == 4:
        return render_template('compare4T.html', tablet_data=tablet_data)
    else:
        return redirect(url_for('tablet_page'))









if __name__ == "__main__":
    app.run()