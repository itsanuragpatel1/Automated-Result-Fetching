🚀 Automated Result Fetching Process  🚀


I automated the entire process of fetching and saving student results from a university website. 


🔧 Technical Highlights:

➸ Selenium WebDriver : Automated the navigation of a complex web interface with dynamic content selection and program-based form submission.

➸ Captcha Recognition : Solved CAPTCHA challenges using Python’s Tesseract OCR (pytesseract), converting image-based CAPTCHAs into readable text for seamless form submission.

➸ Retry Logic : Built a robust retry mechanism to handle failures in CAPTCHA recognition, retrying up to 10 times for accuracy.

➸ Data Scraping : Extracted essential fields like student name, enrollment number, SGPA, CGPA, and result status from the dynamically generated result page.

➸ Data Storage : Efficiently wrote the scraped data into a structured CSV file using Python’s csv module, making it easy to analyze and store the results for a range of enrollment numbers.

➸ Session Handling : Implemented session reinitialization to ensure smooth scraping across multiple iterations, reloading pages and avoiding stale element exceptions.


🛠 Tools & Libraries Used:


➸ Python Selenium : For browser automation.

➸ Tesseract OCR : To decode image-based CAPTCHA.

➸ OpenCV & Requests : To retrieve and preprocess CAPTCHA images from the web.

➸ CSV Module : For efficient data storage and future scalability.


🔎 Why This Matters:


➸ Efficiency Boost : Manual tasks are now automated, saving time and increasing productivity.

➸ Accuracy : Automation minimizes human error, especially with repetitive tasks like CAPTCHA solving and data entry.

➸ Scalability : This solution can easily be extended for bulk data retrieval without breaking a sweat!
