from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

import re
import pytesseract as Pyt
import cv2
import numpy as np
import requests
import time
import csv

# Set the Tesseract executable path
Pyt.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Setup Chrome options to enable incognito mode
chrome_options = Options()
chrome_options.add_argument("--incognito")  # Add incognito mode option

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)  # Pass options

# Base enrollment number
base_enrollment_num = "0301CS2310"

# Loop through enrollment numbers
for i in range(1, 80):
    enrollment_num = base_enrollment_num + f"{i:02d}"  # Create enrollment number

    # Retry counter
    retry_count = 0
    result_found = False

    # Loop for up to 10 attempts
    while retry_count < 10:
        
        driver.get("http://result.rgpv.ac.in/Result/ProgramSelect.aspx")
        # time.sleep(3)  # Wait for the site to load

        # click on btech
        button = driver.find_element(By.ID, 'radlstProgram_1')  
        button.click()
        time.sleep(2)  # Wait for the action to complete

        # Enter the enrollment number
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtrollno').send_keys(enrollment_num)

        # Select the semester
        def select_semester(sem):
            semester_dropdown = Select(driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_drpSemester'))
            semester_dropdown.select_by_value(str(sem))

        select_semester(2)

        # Get the captcha image element and its src attribute
        captcha_image = driver.find_element(By.XPATH, "//img[@alt='Captcha']")
        captcha_src = captcha_image.get_attribute('src')

        # Print the full captcha image URL
        print("Captcha Image URL:", captcha_src)

        # Fetch the captcha image
        image_url = captcha_src

        # Function to get an image from a URL
        def get_image_from_url(url):
            response = requests.get(url)
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            return img

        # Fetch the image from the URL
        img = get_image_from_url(image_url)

        # Extract text using pytesseract
        text = Pyt.image_to_string(img)
        result = re.sub(r"\s+", "", text.upper())  # Remove whitespace and convert to uppercase
        print("Extracted Text:", result)

        # Send the captcha text to the input field
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_TextBox1').send_keys(result)
        time.sleep(2)

        # Click the button to view results
        button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnviewresult')
        button.click()
        time.sleep(1)

        #  Check if the result data appears
        try:
            # Attempt to extract result data
            student_name = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lblNameGrading').text
            enrollment_number = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lblRollNoGrading').text
            sgpa = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lblSGPA').text
            cgpa = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lblcgpa').text
            ResultDes = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lblResultNewGrading').text

            # Print extracted result data
            print(f"Student Name: {student_name}")
            print(f"Enrollment Number: {enrollment_number}")
            print(f"SGPA: {sgpa}")
            print(f"CGPA: {cgpa}")
            print(f"Result Des. : {ResultDes}")

            # Prepare data for CSV
            data_to_insert = [student_name, enrollment_number, sgpa, cgpa, ResultDes]

            # Write data to CSV file
            with open("results.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(data_to_insert)

            print("Result data has been saved to CSV file!")
            result_found = True  # Mark that result has been found
            break  # Exit the retry loop if successful

        except Exception as e:
            print(f"Attempt {retry_count + 1}: Result not found for {enrollment_num}. Retrying...")
            retry_count += 1  # Increment the retry count

    if not result_found:
        print(f"Failed to retrieve results for {enrollment_num} after 10 attempts.")

    # Close the current tab
    driver.close()
    # Reopen a new tab and start the process again
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Re-initialize the driver

# Quit the driver after all iterations
driver.quit()
