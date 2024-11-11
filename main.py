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

Pyt.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

chrome_options = Options()

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)  # Pass options

base_enrollment_num = "0301CS2310"

for i in range(1, 80):
    enrollment_num = base_enrollment_num + f"{i:02d}" 

    retry_count = 0
    result_found = False

    while retry_count < 10:
        
        driver.get("http://result.rgpv.ac.in/Result/ProgramSelect.aspx")
        # time.sleep(3) #adjust acording to yourself 
        
        button = driver.find_element(By.ID, 'radlstProgram_1')  
        button.click()
        time.sleep(2)  #adjust acording to yourself 

        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtrollno').send_keys(enrollment_num)

        def select_semester(sem):
            semester_dropdown = Select(driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_drpSemester'))
            semester_dropdown.select_by_value(str(sem))

        select_semester(2)

        captcha_image = driver.find_element(By.XPATH, "//img[@alt='Captcha']")
        captcha_src = captcha_image.get_attribute('src')

        print("Captcha Image URL:", captcha_src)
        
        image_url = captcha_src

        def get_image_from_url(url):
            response = requests.get(url)
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            return img

        img = get_image_from_url(image_url)

        text = Pyt.image_to_string(img)
        result = re.sub(r"\s+", "", text.upper())  # Remove whitespace and convert to uppercase
        print("Extracted Text:", result)
        time.sleep(2)  #adjust acording to yourself 

        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_TextBox1').send_keys(result)
        time.sleep(2)   #adjust acording to yourself 

        button = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnviewresult')
        button.click()
        time.sleep(1) #adjust acording to yourself 
        
        try:
            student_name = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lblNameGrading').text
            enrollment_number = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lblRollNoGrading').text
            sgpa = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lblSGPA').text
            cgpa = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lblcgpa').text
            ResultDes = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lblResultNewGrading').text

            print(f"Student Name: {student_name}")
            print(f"Enrollment Number: {enrollment_number}")
            print(f"SGPA: {sgpa}")
            print(f"CGPA: {cgpa}")
            print(f"Result Des. : {ResultDes}")

            data_to_insert = [student_name, enrollment_number, sgpa, cgpa, ResultDes]

            with open("results.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(data_to_insert)

            print("Result data has been saved to CSV file!")
            result_found = True 
            break  

        except Exception as e:
            print(f"Attempt {retry_count + 1}: Result not found for {enrollment_num}. Retrying...")
            retry_count += 1  # Increment the retry count

    if not result_found:
        print(f"Failed to retrieve results for {enrollment_num} after 10 attempts.")

    driver.close()
    driver = webdriver.Chrome(service=service, options=chrome_options)

driver.quit()
