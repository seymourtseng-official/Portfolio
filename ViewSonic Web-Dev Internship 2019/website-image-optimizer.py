# Project Name: spider_webimagetracer (ver 1.0)
# Programmer: Seymour Tseng, Brea Olinda High School
# License: pending...
# Language: Python 3.7
# Date of Completion: 07/11/2019
# Last Revision Date: 07/11/2019

# Note: This python script is written for the author's internship at ViewSonic Corp., Brea CA, in the year of 2019
# Purpose: To crawl the company's sitemap and look for images that are over-sized, then optimize these files

# ---START OF PROGRAM---

# INITIALIZATION
import subprocess
import sys
# This uses system terminal to install python modules
subprocess.call([sys.executable, "-m", "pip", "install", 'requests'])
subprocess.call([sys.executable, "-m", "pip", "install", 'urllib3'])
subprocess.call([sys.executable, "-m", "pip", "install", 'XlsxWriter'])
subprocess.call([sys.executable, "-m", "pip", "install", 'beautifulsoup4'])
subprocess.call([sys.executable, "-m", "pip", "install", 'requests'])
subprocess.call([sys.executable, "-m", "pip", "install", 'wget'])
subprocess.call([sys.executable, "-m", "pip", "install", 'tinify'])

# LIBRARY
# The following modules are necessary to run the script
import requests                 # 'requests' is used to access the internet
import urllib.request           # 'urllib' is used to obtain information from a given url
import xlsxwriter               # 'xlsxwriter' is a module used to write excel files
from bs4 import BeautifulSoup   # 'Beautifulsoup' is popularly used to parse HTML & XML files
import wget                     # 'wget' is used to download file from an url quickly
import os                       # 'os' is used to modify or create directories within the project
import time                     # 'time' is used to compile the run time of the program
import tinify                   # 'tinify' is used to compress image size
import logging                  # 'logging' is used to log events

# EVENT LOG
# This uses the 'logging' module to log events
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename='logfile.log', filemode='w', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info("Started Program")

# INPUTS
# This obtains necessary information from users through reading terminal inputs
sitemap_address = input('' + '\n' + 'ENTER SITEMAP LINK (ex. https://viewsonic/sitemap.xml): ')
min_threshold = input('ENTER IMAGE SIZE THRESHOLD [KB-default] (ex. 100): ')
tinify_api = input('ENTER TINIFY API KEY (ex. qeiEMagIn9OyhUgFoquHjIf8KpZYClPr): ')
tinify.key = tinify_api
print('' + '\n' + 'Please wait patiently. . . The program will automatically notify when completed' + '\n' + '')
logging.info("Inputs Detected")

# This starts the timer of the program
start = time.time()


# FUNCTION
# This creates a function to crawl the sitemap
def image_spider():

    # This creates folders(or, in python diction, "directories") within the same folder as the script
    try:
        os.makedirs('CORE FILES')
    except Exception as error_code:
        print(error_code)
        logging.error(error_code)
    try:
        os.makedirs('IMAGES')
    except Exception as error_code:
        print(error_code)
        logging.error(error_code)
    try:
        os.makedirs('IMAGES/ORIGINAL')
    except Exception as error_code:
        print(error_code)
        logging.error(error_code)
    try:
        os.makedirs('IMAGES/COMPRESS')
    except Exception as error_code:
        print(error_code)
        logging.error(error_code)
    try:
        os.makedirs('DATABASE')
    except Exception as error_code:
        print(error_code)
        logging.error(error_code)

    try:
        # This downloads the sitemap file from the given url
        wget.download(sitemap_address, 'CORE FILES/sitemap.xml')
    except Exception as error_code:
        input("The link address to the sitemap is invalid. Press any key to exit now. . .")
        logging.info('Closed Program')
        print(error_code)
        logging.critical(error_code)
        sys.exit()

    # This indicates the file to open, in this case, "sitemap.xml'
    sitemap = 'CORE FILES/sitemap.xml'
    source_code = open(sitemap, 'r')
    # This tells the computer to convert the xml file into plain text
    plain_text = source_code.read()
    # This uses the 'BeautifulSoup' module  to parse the xml file
    soup = BeautifulSoup(plain_text, 'xml')
    # This calculates the number of a specific tag in the document. in this case, the 'loc' tag,
    # for which the number is stored as an integer variable
    url_count = len(soup.find_all('loc'))
    # This declares a list element to separate and store parsed links
    link_list = []

    # MICROSOFT EXCEL DATABASE
    # This creates an excel book and add a sheet named "default", then writes text in the first row and column
    # Using the 'xlsxwriter' module, the method for writing in the excel grids is (row, column, text)
    outbook = xlsxwriter.Workbook('analytics.xlsx')
    # This adds format to the excel file elements
    bold = outbook.add_format({'bold': True})
    italic = outbook.add_format({'italic': True})
    images_sheet = outbook.add_worksheet('images')
    statistics_sheet = outbook.add_worksheet('statistics')
    benchmark_sheet = outbook.add_worksheet('benchmark')

    # The 'images' sheet stores image size and corresponding url
    images_sheet.write(0, 0, 'Original Size', bold)
    images_sheet.set_column(0, 0, 17)
    images_sheet.write(0, 1, 'Compress Size', bold)
    images_sheet.set_column(0, 1, 17)
    images_sheet.write(0, 2, 'File Name', bold)
    images_sheet.set_column(0, 2, 50)
    images_sheet.write(0, 3, 'URL', bold)
    images_sheet.set_column(0, 3, 140)

    # The 'statistics' sheet tracks the results of the program
    statistics_sheet.write(0, 0, 'Number of Links Retrieved', bold)
    statistics_sheet.set_column(0, 0, 50)
    statistics_sheet.write(0, 1, 'Total Images Downloaded', bold)
    statistics_sheet.set_column(0, 1, 50)
    statistics_sheet.write(0, 2, 'Original Collective File Size', bold)
    statistics_sheet.set_column(0, 2, 50)
    statistics_sheet.write(0, 3, 'Compressed Collective File Size', bold)
    statistics_sheet.set_column(0, 3, 50)
    statistics_sheet.write(0, 4, 'Optimization Freed Space', bold)
    statistics_sheet.set_column(0, 4, 50)

    # The 'benchmark' sheet stores data tracing the performance
    benchmark_sheet.write(0, 0, 'Program Execution Time', bold)
    benchmark_sheet.set_column(0, 0, 50)
    benchmark_sheet.write(0, 1, 'Proxy Denied Requests', bold)
    benchmark_sheet.set_column(0, 1, 170)
    benchmark_sheet.write(0, 2, 'Broken URL (404 Not Found)', bold)
    benchmark_sheet.set_column(0, 2, 170)
    benchmark_sheet.write(0, 3, 'Unsupported Media Type', bold)
    benchmark_sheet.set_column(0, 3, 170)
    benchmark_sheet.write(0, 4, 'Other Skipped Links', bold)
    benchmark_sheet.set_column(0, 4, 170)

    # These are local varables
    images_row = 0
    proxy_row = 0
    brokenurl_row = 0
    media_row = 0
    otherlinks_row = 0
    link_counter = 0
    image_counter = 0
    collectivesize_before = 0
    collectivesize_after = 0

    # FOR LOOP
    # This creates a for loop to search through the xml file
    for i in range(0, 10):  # The values in the range expression represent the number of tags

        try:

            # This uses the 'BeautifulSoup' module to find all the 'loc' tags in the xml file
            # Collecting plain text between the opening and closing tags, in this case, '<loc>' and '</loc>"
            url = soup.findAll("loc")[i].text
            # This adds each of the collected links into the list
            link_list.append(url)

            # For recoding purposes, this prints the url in the list and write it to the created excel file
            print(' ' + '\n' + 'Page URL: ' + link_list[i])
            images_sheet.merge_range(images_row + 1, 0, images_row + 1, 3, '')
            images_sheet.write(images_row + 1, 0, link_list[i], italic)
            images_row += 1
            link_counter += 1
            logging.info('Page URL: ' + link_list[i])

            # This conditional statement separates the two type of links: image and website
            # Direct image urls include file types (determined by the above string variables), while website urls do not

            # CONDITIONAL STATEMENT
            media_filetype = ['.jpg', '.jpeg', '.png', 'gif', 'tif', 'tiff', 'bmp', 'svg', 'webp', 'heic', 'heif']
            website_filetype = ['.html', '.phtml', '.htm']

            # PART(1/2): If the link pertains to an image file, download the image directly and record it
            if any(media_item in link_list[i] for media_item in media_filetype):
                # This uses the 'urllib' module to open each link
                d = urllib.request.urlopen(link_list[i])

                # This obtains information and specifies the type of properties wanted, in this case, 'Content-Length'
                original_str = d.info()['Content-Length']  # 'Content-Length' is another word for file original_size

                # This converts the default unit from b (bytes) to kb (kilobytes)
                original_size = int(original_str) / 1000

                # This collects images of a file original_size above a threshold
                # <--INPUT VALUE ADJUSTS THE THRESHOLD--> (recommended minimum file original_size: 80kb )
                # Images greater than 80 kb are considered large and will require longer time to load,
                # thus slowing down website traffic and resulting in a lower Search Engine Ranking
                if int(min_threshold) < original_size:
                    if original_size < 1000:
                        # This converts the default unit from b (bytes) to kb (kilobytes)
                        original_size = int(original_str) / 1000
                        collectivesize_before += original_size
                        original_unit = ' KB '

                    # This outputs the unit of images greater than 1000 kb as 1 mb
                    # Though images are unlikely to exceed 1 gb, the next level can be created with the same logic
                    elif original_size > 1000:
                        # For recoding purposes, this prints the url in the list and write it to the created excel file
                        original_size = int(original_str) / 1000000
                        collectivesize_before += (original_size * 1000)
                        original_unit = ' MB '

                    # This downloads the images
                    wget.download(link_list[i], 'IMAGES/ORIGINAL')
                    logging.info('Image Downloaded: ' + link_list[i])

                    # This uses the 'tinify' module to compress images
                    saved = tinify.from_url(link_list[i])
                    name = os.path.basename(link_list[i])
                    location = 'IMAGES/COMPRESS/' + name
                    saved.to_file(str(location))
                    compressed_str = os.path.getsize(str(location))
                    compressed_size = int(compressed_str) / 1000
                    logging.info('Image Compressed: ' + location)

                    if compressed_size < 1000:
                        # This converts the default unit from b (bytes) to kb (kilobytes)
                        compressed_size = int(compressed_str) / 1000
                        collectivesize_after += compressed_size
                        compressed_unit = ' KB '

                    # This outputs the unit of images greater than 1000 kb as 1 mb
                    # Though images are unlikely to exceed 1 gb, the next level can be created with the same logic
                    elif compressed_size > 1000:
                        compressed_size = int(compressed_str) / 1000000
                        collectivesize_after += (compressed_size * 1000)
                        compressed_unit = ' MB '

                    # For recoding purposes, this prints the url in the list and write it to the created excel file
                    print(' ' + '\n' + 'Original Size: ' + str(original_size) + original_unit + link_list[i])
                    print('Compressed Size: ' + str(compressed_size) + compressed_unit + link_list[i])
                    logging.info('Original Size: ' + str(original_size) + original_unit + link_list[i])
                    logging.info('Compressed Size: ' + str(compressed_size) + compressed_unit + link_list[i])
                    images_sheet.write(images_row + 1, 0, str(original_size) + original_unit)
                    images_sheet.write(images_row + 1, 1, str(compressed_size) + compressed_unit)
                    images_sheet.write(images_row + 1, 2, name)
                    images_sheet.write(images_row + 1, 2, link_list[i])
                    images_row += 1
                    image_counter += 1

            # PART(2/2): If the link pertains to a website, parse its HTML source code,
            # search for the images, find them, then download and record them
            elif any(website_item in link_list[i] for website_item in website_filetype):

                # This uses the 'requests' module to access the link
                html_code = requests.get(link_list[i])
                # This stores the plain text of the HTML file
                raw_text = html_code.text
                # This uses the 'BeautifulSoup' module to parse the HTML document
                webs = BeautifulSoup(raw_text, 'html.parser')
                # This calculates the number of a specific tag in the document. in this case, the 'img' tag,
                # for which the number is stored as an integer variable
                img_count = len(webs.div.find_all('img'))

                # This creates a for loop to search through the HTML file
                for k in range(0, img_count):  # The values in the range expression represent the number of tags

                    try:

                        # This uses the 'BeautifulSoup' module to find all the 'img' tags and retrieve its 'src' path
                        directory = webs.findAll('img')[k].get('src')
                        # These string variables will be used the following conditional statement
                        tag = 'https://www.viewsonic.com'
                        # If the link contains specific error-incurring text stored in the above string variables,
                        # or if the link does not have a complete url address, take certain actions
                        # (1/2) If the link is healthy, store it in the 'src' string variable
                        if tag in directory:
                            src = directory
                        # (2/2) If the link is missing the website domain (being abbreviated with only the file path),
                        # then add the text in the 'tag' variable to the 'src' string variable
                        else:
                            src = tag + directory

                        # This uses the 'urllib' module to open each link
                        d = urllib.request.urlopen(src)
                        # This obtains information and specifies the type of properties wanted, in this case, 'Content-Length'
                        original_str = d.info()['Content-Length']  # 'Content-Length' is another word for file original_size
                        # This converts the default unit from b (bytes) to kb (kilobytes)
                        original_size = int(original_str) / 1000

                        # This collects images of a file original_size above a threshold, in this case, 100 kb
                        # <--CHANGE THE VALUES TO ADJUST THE THRESHOLD--> (recommended minimum file original_size: 80kb )
                        # Images greater than 80 kb are considered large and will require longer time to load,
                        # thus slowing down website traffic and resulting in a lower Search Engine Ranking
                        if int(min_threshold) < original_size:
                            if original_size < 1000:
                                # This converts the default unit from b (bytes) to kb (kilobytes)
                                original_size = int(original_str) / 1000
                                collectivesize_before += original_size
                                original_unit = ' KB '
                            # This outputs the unit of images greater than 1000 kb as 1 mb
                            # Though images are unlikely to exceed 1 gb, the next level can be created with the same logic
                            elif original_size > 1000:
                                # For recoding purposes, this prints the url in the list and write it t+o the created excel file
                                original_size = int(original_str) / 1000000
                                collectivesize_before += (original_size * 1000)
                                original_unit = ' MB '

                            # This downloads the images
                            wget.download(src, 'IMAGES/ORIGINAL')
                            logging.info('Image Downloaded: ' + src)

                            # This uses the 'tinify' module to compress the images
                            saved = tinify.from_url(src)
                            name = os.path.basename(src)
                            location = 'IMAGES/COMPRESS/' + name
                            saved.to_file(str(location))
                            compressed_str = os.path.getsize(str(location))
                            compressed_size = int(compressed_str) / 1000
                            logging.info('Image Compressed: ' + location)

                            if compressed_size < 1000:
                                # This converts the default unit from b (bytes) to kb (kilobytes)
                                compressed_size = int(compressed_str) / 1000
                                collectivesize_after += compressed_size
                                compressed_unit = ' KB '

                            # This outputs the unit of images greater than 1000 kb as 1 mb
                            # Though images are unlikely to exceed 1 gb, the next level can be created with the same logic
                            elif compressed_size > 1000:
                                compressed_size = int(compressed_str) / 1000000
                                collectivesize_after += (compressed_size * 1000)
                                compressed_unit = ' MB '

                            # For recoding purposes, this prints the url in the list and write it to the created excel file
                            print(' ' + '\n' + 'Original Size: ' + str(original_size) + original_unit + src)
                            print('Compress Size: ' + str(compressed_size) + compressed_unit + src)
                            logging.info('Original Size: ' + str(original_size) + original_unit + src)
                            logging.info('Compress Size: ' + str(compressed_size) + compressed_unit + src)
                            images_sheet.write(images_row + 1, 0, str(original_size) + original_unit)
                            images_sheet.write(images_row + 1, 1, str(compressed_size) + compressed_unit)
                            images_sheet.write(images_row + 1, 2, name)
                            images_sheet.write(images_row + 1, 2, src)
                            images_row += 1
                            image_counter += 1

                    except Exception as error_code:
                        if '403' in str(error_code):
                            benchmark_sheet.write(proxy_row + 1, 1, src)
                            print('Proxy Denied Requests: ' + src)
                            logging.error('Proxy Denied Requests: ' + src)
                            proxy_row += 1
                        elif '404' in str(error_code):
                            benchmark_sheet.write(brokenurl_row + 1, 2, src)
                            print('Broken URL (404 Not Found): ' + src)
                            logging.error('Broken URL (404 Not Found): ' + src)
                            brokenurl_row += 1
                        elif '415' in str(error_code):
                            benchmark_sheet.write(media_row + 1, 3, src)
                            print('Unsupported Media Type: ' + src)
                            logging.error('Unsupported Media Type: ' + src)
                            media_row += 1
                        elif '429' in str(error_code):
                            print(error_code)
                            input("The program could not continue due to a fatal error. Press any key to exit now. . .")
                            logging.info('Closed Program')
                            logging.critical(error_code)
                            sys.exit()
                        elif '401' in str(error_code):
                            input("You're tinify API key is invalid. Press any key to exit now. . .")
                            logging.info('Closed Program')
                            print(error_code)
                            logging.critical(error_code)
                            sys.exit()
                        else:
                            benchmark_sheet.write(otherlinks_row + 1, 4, src)
                            print('Other Skipped Links: ' + src)
                            logging.error('Other Skipped Links: ' + src)
                            otherlinks_row += 1
                        print(str(error_code))
                        pass

        except Exception as error_code:
            if '403' in str(error_code):
                benchmark_sheet.write(proxy_row + 1, 1, link_list[i])
                print('Proxy Denied Requests: ' + link_list[i])
                logging.error('Proxy Denied Requests: ' + link_list[i])
                proxy_row += 1
            elif '404' in str(error_code):
                benchmark_sheet.write(brokenurl_row + 1, 2, link_list[i])
                print('Broken URL (404 Not Found): ' + link_list[i])
                logging.error('Broken URL (404 Not Found): ' + link_list[i])
                brokenurl_row += 1
            elif '415' in str(error_code):
                benchmark_sheet.write(media_row + 1, 3, link_list[i])
                print('Unsupported Media Type: ' + link_list[i])
                logging.error('Unsupported Media Type: ' + link_list[i])
                media_row += 1
            elif '429' in str(error_code):
                input("The program could not continue due to a fatal error. Press any key to exit now. . .")
                logging.info('Closed Program')
                print(error_code)
                logging.critical(error_code)
                sys.exit()
            elif '401' in str(error_code):
                input("You're tinify API key is invalid. Press any key to exit now. . .")
                logging.info('Closed Program')
                print(error_code)
                logging.critical(error_code)
                sys.exit()
            else:
                benchmark_sheet.write(otherlinks_row + 1, 4, link_list[i])
                print('Other Skipped Links: ' + link_list[i])
                logging.error('Other Skipped Links: ' + link_list[i])
                otherlinks_row += 1
            print(str(error_code))
            pass

    # This writes all the data to the excel sheet
    statistics_sheet.write(1, 0, str(link_counter))
    print(' ' + '\n' + 'Number of Links Retrieved: ' + str(link_counter))
    statistics_sheet.write(1, 1, str(image_counter))
    print('Total Images Downloaded: ' + str(image_counter))
    if int(collectivesize_before) < 1000000:
        statistics_sheet.write(1, 2, str(collectivesize_before) + ' KB ')
        print('Original Collective File Size: ' + str(collectivesize_before) + ' KB')
    elif 1000000 < int(collectivesize_before) < 1000000000:
        statistics_sheet.write(1, 2, str(collectivesize_before / 1000) + ' MB ')
        print('Original Collective File Size: ' + str(collectivesize_before / 1000) + ' MB')
    elif int(collectivesize_before) > 1000000000:
        statistics_sheet.write(1, 2, str(collectivesize_before / 1000000) + ' GB ')
        print('Original Collective File Size: ' + str(collectivesize_before / 1000000) + ' GB')
    if int(collectivesize_after) < 1000000:
        statistics_sheet.write(1, 3, str(collectivesize_after) + ' KB ')
        print('Compressed Collective File Size: ' + str(collectivesize_after) + ' KB')
    elif 1000000 < int(collectivesize_after) < 1000000000:
        statistics_sheet.write(1, 3, str(collectivesize_after / 1000) + ' MB ')
        print('Compressed Collective File Size: ' + str(collectivesize_after / 1000) + ' MB')
    elif int(collectivesize_after) > 1000000000:
        statistics_sheet.write(1, 3, str(collectivesize_after / 1000000) + ' GB ')
        print('Compressed Collective File Size: ' + str(collectivesize_after / 1000000) + ' GB')
    freed_space = int(collectivesize_before) - int(collectivesize_after)
    if int(freed_space) < 1000000:
        statistics_sheet.write(1, 4, str(freed_space))
        print('Optimization Freed Space: ' + str(int(freed_space)) + ' KB')
    elif 1000000 < int(freed_space) < 1000000000:
        statistics_sheet.write(1, 4, str(freed_space / 1000) + ' MB ')
        print('Optimization Freed Space: ' + str(freed_space / 1000) + ' MB')
    elif int(freed_space) > 1000000000:
        statistics_sheet.write(1, 4, str(freed_space / 1000000) + ' GB ')
        print('Optimization Freed Space: ' + str(freed_space / 1000000) + ' GB')

    # This ends the timer
    end = time.time()
    # This outputs the total run time of the program
    total_time = (end - start) / 60
    benchmark_sheet.write(1, 0, str(total_time) + ' min.')
    print('Program Execution Time: ' + str(total_time) + ' min.')


# This calls the function
image_spider()

# This notify and give users further directions after closing the program
print('' + '\n' + 'Here is the locations of where the files are stored:' + '\n' + 'CORE FILES  -->  ' + 'sitemap.xml, logfile.log' + '\n' + 'IMAGES      -->  ' + 'ORIGINAL: uncompressed images, COMPRESS: compressed images' + '\n' + 'DATABASE    -->  ' + 'analytics.xlsx: images, statistics, benchmark' + '\n' + 'SYSTEM      -->  ' + 'script root files (modification not recommended)' + '\n' + '')
input("Thank you for using the program. You're all set! Press any key to exit now. . .")
logging.info('Closed Program')


# ---END OF PROGRAM---
