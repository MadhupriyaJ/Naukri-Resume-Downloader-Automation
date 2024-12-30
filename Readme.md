Naukri Resume Downloader Automation

This project is a Selenium-based automation script designed to scrape and download resumes from the Naukri job portal. The script automates the process of navigating job listings, opening profiles, and downloading resumes efficiently.

Features

Automated Job Tuple Processing: Iterates through job tuples on the listing page and processes them.

Profile Navigation and Download: Opens profiles in new tabs and downloads resumes.

Pagination Support: Navigates through multiple pages of profiles.

Error Handling: Skips profiles that encounter errors and logs them.

Requirements

Python 3.x

Google Chrome (installed)

ChromeDriver (matching the version of Chrome)

Selenium Python Package

Installation

Install Selenium:

pip install selenium

Download ChromeDriver:

Download the appropriate version of ChromeDriver from here.

Place it in a directory accessible by the system PATH.

Enable Remote Debugging in Chrome:

chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome-data"

Usage

Start Chrome with Remote Debugging:

chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome-data"

Run the Python Script:

python automate.py

How It Works

Connect to Chrome: The script connects to an existing Chrome session using remote debugging.

Navigate to Job Listings: Opens the Naukri job listing URL.

Process Job Tuples:

Scrolls through job listings.

Opens each job in a new tab.

Clicks to download resumes.

Pagination: The script handles pagination and processes all profiles across multiple pages.

Code Structure

connect_to_existing_chrome(): Connects to the existing Chrome session.

process_job_tuples(driver): Iterates over job tuples and processes them.

clickprofile(driver): Automates clicking profiles and downloads resumes.

downloadresume(driver): Handles resume downloads from the profile page.

main(): Coordinates the entire workflow.

Configuration

Job Listing URL:

Replace the job listing URL in the main() function with the actual URL:

job_listing_url = "https://hiring.naukri.com/hiring/job-listing"

Notes

Ensure that pop-ups and downloads are enabled in Chrome settings.

Adjust sleep times (time.sleep()) as per network speed and system performance.

Handle Captchas manually if encountered.

Troubleshooting

Connection Issues: Ensure that Chrome is running with remote debugging enabled.

Element Not Found: Increase the WebDriverWait timeout or review the XPath selectors.

Permission Errors: Run the script with administrative privileges if necessary.

Disclaimer

This script is for educational purposes only. Use it responsibly and ensure compliance with Naukri's terms of service.

