# PricePulseTracker - E-commerce Price Monitoring System
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?logo=Selenium&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-green?style=for-the-badge)

An automated system to track e-commerce product prices, receive alerts
when prices drop below a threshold, and store historical data in
json and csv files.

## Features 
- 🛒 **Web Scraping**: Extracts product data from e-commerce sites
- 🔔 **Smart Alerts**: Email notifications when prices drop below
given threshold
- 📊 **Data Export**: Automatically logs price history to json and csv files
- 📈 **Price Trend Analysis**: Tracks historical price data for better
decision making

## Getting Started 
### Prerequisites 

- Python 3.6+
- selenium 4.3+
- Email account (for alerts)

### Installation 
1. Clone the repository:

    ```
    git clone https://github.com/Sabbir1039/PricePulseTracker.git
    cd PricePulseTracker
    ```

2. Install required packages:

    ```
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    - Create a .env file in the root directory
    - Add credentials:
        ```
        EMAIL_USER=your_email@gmail.com 
        EMAIL_PASSWORD=your_app_password
        RECEIVER_EMAIL=alert_receiver@email.com
        SLACK_TOKEN=xoxb-your-slack-token
        ```

### Usage 
1. Configure products to track in **main.py**:

    ```
    python PRODUCTS_TO_TRACK = { 
        "https://www.amazon.com/dp/B08N5KWB9H": 300.00, # Product URL: Threshold price
        "https://www.bestbuy.com/site/some-product": 199.99 
    }
    ```

2. Run the tracker:

    ```
    python main.py
    ```

3. The system will:

    - Send alerts when prices drop below given threshold
    - Log all data to Google Sheets

### File Structure

    PricePulseTracker/
    ├── main.py               # Main application runner
    ├── scraper.py            # Web scraping functionality
    ├── tracker.py            # Price tracking and comparison
    ├── notifier.py           # Email/Slack notification system
    ├── export_to_csv.py      # Convert product data json to csv
    ├── requirements.txt      # Python dependencies
    ├── .env                  # Environment variables template
    ├── tracked_products.json # Product data storage
    └── README.md             # This documentation


### Customization Options

- **Change check interval**: Modify the time.sleep() value in main.py
- **Add more retailers**: Extend scraper.py with additional parsing logic
- **Customize alerts**: Edit message templates in notifier.py
- **Add more notification channels**: Implement additional services like Discord or SMS

### Troubleshooting 
#### Common Issues 

1. Scraping blocked:

    - Try changing the User-Agent header in **scraper.py**
    - Add delays between requests
    - Consider using proxies

2. Email not sending:

    - Verify app passwords are enabled for your email
    - Check spam folders

### Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create your feature branch (**git checkout -b feature/AmazingFeature**)
3. Commit your changes (**git commit -m \'Add some AmazingFeature\'**)
4. Push to the branch (**git push origin feature/AmazingFeature**)
5. Open a Pull Request

### License
Distributed under the MIT License. See **LICENSE** for more
information.

### Contact
For inquiries or support:

- Email: sabbirmd31948@gmail.com

- Project Link: https://github.com/Sabbir1039/PricePulseTracker
