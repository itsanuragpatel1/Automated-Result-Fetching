## 📹 Demo Video

[Watch the demo video here (linkedin post) ](https://www.linkedin.com/posts/itsanuragpatel_python-automation-selenium-activity-7247300251018022914-_7pY/)

# 🚀 Automated Result Fetching Process 🚀

This project automates the process of fetching and saving student results from a university website. The automation handles CAPTCHA solving, dynamic form submissions, and data extraction for multiple students efficiently.

## 🔧 Technical Highlights

- **Selenium WebDriver**: Automated the navigation of a complex web interface, handling dynamic content selection and form submission programmatically.
- **Captcha Recognition**: Solved CAPTCHA challenges using Python’s Tesseract OCR (`pytesseract`), converting image-based CAPTCHAs into readable text for smooth form submissions.
- **Retry Logic**: A robust retry mechanism was implemented, retrying up to 10 times to handle failures in CAPTCHA recognition.
- **Data Scraping**: Extracted essential fields such as student name, enrollment number, SGPA, CGPA, and result status from the dynamically generated result page.
- **Data Storage**: Scraped data is efficiently written to a structured CSV file using Python’s `csv` module, making it easy to analyze and store results across a range of enrollment numbers.
- **Session Handling**: Implemented session reinitialization to handle multiple iterations without encountering stale element exceptions, ensuring smooth scraping.

## 🛠 Tools & Libraries Used

- **Python Selenium**: For browser automation and dynamic form submission.
- **Tesseract OCR**: To decode image-based CAPTCHA.
- **OpenCV & Requests**: For retrieving and preprocessing CAPTCHA images from the web.
- **CSV Module**: For efficient data storage and future scalability.

## 🔎 Why This Matters

- **Efficiency Boost**: Automation of repetitive tasks saves time and increases productivity.
- **Accuracy**: Reduces human error, especially in CAPTCHA solving and data entry.
- **Scalability**: The solution can be extended to retrieve bulk data with minimal changes.


## 🛠 Tesseract OCR Setup

You can find Tesseract OCR setup files [here](https://drive.google.com/drive/folders/1W41RBeEXmEh_hzge_NUNYtWeMb6yfnZk?usp=sharing).
