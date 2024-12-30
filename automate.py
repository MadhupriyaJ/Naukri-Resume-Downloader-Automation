from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


import time


# Function to connect to an existing Chrome session
def connect_to_existing_chrome():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Connect to remote debugger
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def process_job_tuples(driver):
    processed_ids = set()  # Keep track of processed tuples by their unique IDs
    skipped_ids = set()  # Keep track of skipped tuples

    while True:
        try:
            # Wait for all tuples to be loaded
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "mjrTupleTitleText")))

            # Find all job tuples
            tuples = driver.find_elements(By.CLASS_NAME, "mjrTupleTitleText")

            if not tuples:
                print("No more tuples found.")
                break

            # Iterate over the tuples and process unprocessed ones
            for job_tuple in tuples:
                try:
                    # Get the unique ID of the tuple (from its parent element)
                    parent = job_tuple.find_element(By.XPATH, "./ancestor::div[@data-mjrtuple-id]")
                    tuple_id = parent.get_attribute("data-mjrtuple-id")

                    if tuple_id in processed_ids or tuple_id in skipped_ids:
                        continue  # Skip already processed or skipped tuples

                    print(f"Clicking tuple with ID {tuple_id}...")

                    # Scroll the job tuple into view (to ensure it's clickable)
                    driver.execute_script("arguments[0].scrollIntoView();", job_tuple)
                    time.sleep(1)  # Wait briefly to ensure it's visible

                    # Open the job tuple in a new tab
                    job_tuple.send_keys(webdriver.common.keys.Keys.CONTROL + webdriver.common.keys.Keys.RETURN)
                    time.sleep(2)  # Wait for the new tab to open

                    # Switch to the newly opened tab
                    driver.switch_to.window(driver.window_handles[-1])

                    # Wait for the navigated page to load (e.g., resumes page)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="checkbox"]')))
                    print(f"Processing tuple with ID {tuple_id}...")

                    # Call function to download resumes here (you can integrate this part)
                     # Call the download function
                    clickprofile(driver)

                    # Close the current tab
                    # driver.close()

                    # Switch back to the original tab (job listing page)
                    driver.switch_to.window(driver.window_handles[0])

                    # Mark this tuple as processed
                    processed_ids.add(tuple_id)

                    # Break out of the loop to refresh the list of tuples
                    break

                except Exception as e:
                    print(f"Error processing tuple with ID {tuple_id}: {type(e).__name__} - {e.msg}")
                    skipped_ids.add(tuple_id)  # Mark this tuple as skipped
                    continue

        except Exception as e:
            print(f"Error processing tuples: {e}")
            break


        # Log summary
    print(f"Processed tuples: {processed_ids}")
    print(f"Skipped tuples: {skipped_ids}")
    # Log skipped tuples
    # if skipped_ids:
    #     print(f"Skipped the following tuples due to errors: {skipped_ids}")
def clickprofile(driver):
    # Activate the "All" tab
    all_tab = driver.find_element(By.XPATH, "//span[text()='All']")
    all_tab.click()
    print("Activated 'All' tab.")
    time.sleep(2)

    # Click the dropdown arrow and select "160"
    down_arrow = driver.find_element(By.XPATH, "//i[@data-testid='downArrow']")
    down_arrow.click()
    print("Dropdown arrow clicked.")
    time.sleep(1)

    option_160 = driver.find_element(By.XPATH, "//li[text()='160']")
    option_160.click()
    print("Selected '160' from the dropdown.")
    time.sleep(2)

    # Paginate through all pages
    while True:  # Loop through all pages
        # Find all profile links on the current page
        profile_links = driver.find_elements(By.XPATH, "//a[contains(@class, 'customLink ')]")
        original_window = driver.current_window_handle

        for index, link in enumerate(profile_links):
            try:
                print(f"Processing profile {index + 1} on this page...")
                ActionChains(driver).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                time.sleep(2)

                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                # Download the resume
                downloadresume(driver)

                # Switch back to the original window
                driver.switch_to.window(original_window)

            except Exception as e:
                print(f"Error processing profile {index + 1}: {e}")

        print("All profiles on this page processed successfully.")

        # Navigate to the next page
        try:
            next_button = driver.find_element(By.XPATH, "//i[contains(@class, 'next') and not(contains(@class, 'disabled'))]")
            next_button.click()
            print("Navigating to the next page...")
            time.sleep(3)
        except Exception as e:
            print("No more pages to process or an error occurred.")
            break  # Exit the `while` loop if no more pages are found

    # Return to the job listing page
    print("Returning to the job listing page...")
    # driver.get("https://hiring.naukri.com/hiring/job-listing")
    time.sleep(2)

# def clickprofile(driver):
#       # Activate the "All" tab by finding and clicking the tab element
#     all_tab = driver.find_element(By.XPATH, "//span[text()='All']")
    
#     # Click on the "All" tab
#     all_tab.click()
#     print("Activated 'All' tab.")
    
#     # Wait for the content to update after clicking the tab (if necessary)
#     time.sleep(2)  # Adjust this sleep duration based on how long it takes to load

#     # Click the dropdown arrow to show options
#     down_arrow = driver.find_element(By.XPATH, "//i[@data-testid='downArrow']")
#     down_arrow.click()
#     print("Dropdown arrow clicked.")
    
#     # Wait for the dropdown options to appear
#     time.sleep(1)  # Adjust this based on the rendering time of the dropdown

#     # Select the "160" option from the dropdown
#     option_160 = driver.find_element(By.XPATH, "//li[text()='160']")
#     option_160.click()
#     print("Selected '160' from the dropdown.")
    
#     # Wait for the page to update (if necessary) after changing the selection
#     time.sleep(2)
#     # Find all profile links in the table
#     profile_links = driver.find_elements(By.XPATH, "//a[contains(@class, 'customLink ')]")
#     original_window = driver.current_window_handle  # Store the current window handle

#     for index, link in enumerate(profile_links):
#         try:
#             print(f"Processing profile {index}...")

#             # Open link in a new tab using ActionChains
#             ActionChains(driver).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
#             time.sleep(2)  # Allow time for the new tab to open

#             # Switch to the new tab
#             driver.switch_to.window(driver.window_handles[-1])

#             # Wait for the page to load completely
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

#             # Call the resume download function
#             downloadresume(driver)

#             # Close the current tab and switch back to the original window
#             # driver.close()
#             driver.switch_to.window(original_window)

#         except Exception as e:
#             print(f"Error processing profile {index}: {e.msg}")

#     print("All profiles processed successfully.")
    


def downloadresume(driver):
    """
    Automates the process of downloading the resume from the profile page.
    """
    try:
        # Locate the download button (using its class and the text within the span element)
        download_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "actionItems") and contains(., "Download")]'))
        )

        # Click the download button
        download_button.click()
        print("Download started.")
        time.sleep(3)  # Wait for the download to start

        driver.close()

        # Optionally, add a wait time for the download to complete (this may vary based on your environment)
        time.sleep(5)  # Wait for the download to complete

    except TimeoutException:
        print("Download button not found.")
    except Exception as e:
        print(f"Error in downloadresume: {e.msg}")



# Main execution
def main():
    # Connect to the existing Chrome session
    driver = connect_to_existing_chrome()
    
    # Navigate to the job listing page
    job_listing_url = "https://hiring.naukri.com/hiring/job-listing"  # Replace with the actual URL
    driver.get(job_listing_url)
    
    try:
        # Process each job tuple on the job listing page
        process_job_tuples(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
