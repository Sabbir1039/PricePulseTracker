# PricePulseTracker - E-commerce Price Monitoring System
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-green?style=for-the-badge)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)

An automated system to track e-commerce product prices, receive alerts
when prices drop below a threshold, and store historical data in
Google Sheets.

## Features 
- 🛒 **Web Scraping**: Extracts product data from e-commerce sites

- 🔔 **Smart Alerts**: Email/Slack notifications when prices drop below
given threshold

- 📊 **Data Export**: Automatically logs price history to Google Sheets

- ⏰ **Scheduled Monitoring**: Runs continuously with customizable check
intervals

- 📈 **Price Trend Analysis**: Tracks historical price data for better
decision making

## Getting Started 
### Prerequisites 

- Python 3.6+
- Google account (for Sheets API)
- Email account (for alerts) or Slack workspace

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
    - Add your credentials:
        ```
        EMAIL_USER=your_email@gmail.com 
        EMAIL_PASSWORD=your_app_password
        RECEIVER_EMAIL=alert_receiver@email.com
        SLACK_TOKEN=xoxb-your-slack-token
        ```

4. Set up Google Sheets API:

    - Follow Google\'s guide to enable the API
    - Download the credentials JSON file and place it in the project root as credentials.json

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

    - Check prices every hour (configurable)
    - Send alerts when prices drop below given threshold
    - Log all data to Google Sheets

### File Structure

    PricePulseTracker/
    ├── main.py               # Main application runner
    ├── scraper.py            # Web scraping functionality
    ├── tracker.py            # Price tracking and comparison
    ├── notifier.py           # Email/Slack notification system
    ├── sheets_integration.py # Google Sheets API integration
    ├── requirements.txt      # Python dependencies
    ├── .env.example          # Environment variables template
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

2. Google Sheets permission errors:

    - Ensure your service account has edit permissions
    - Share your spreadsheet with the service account email

3. Email not sending:

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
