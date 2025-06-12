from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
from datetime import date

# Set the Chromedriver service path for Snap
service = Service("/snap/bin/chromium.chromedriver")

# Instantiate a Chrome options object
options = webdriver.ChromeOptions()

# Set Chrome to run in headless mode
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Today's date
today = date.today()
formatted_date = today.strftime('%B %d')

try:
    # Initialize the Chromedriver with the specified service and options
    driver = webdriver.Chrome(service=service, options=options)

    # Visit your Council site
    driver.get("")

    # Wait for the specific element containing bin information to be loaded
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bindaysearch-widget-refuse-info"))
    )
    print("Page loaded successfully")

    # Additional wait for Javascript to load completely
    time.sleep(5)

    # Extracting dates and links for Rubbish, Recycling, and Garden Waste
    rubbish_date = driver.find_element(By.XPATH, "//div[contains(@class, 'bindaysearch-widget-refuse-info')]//span").text
    recycling_date = driver.find_element(By.XPATH, "//div[contains(@class, 'bindaysearch-widget-recycling-info')]//span").text
    garden_waste_date = driver.find_element(By.XPATH, "//div[contains(@class, 'bindaysearch-widget-gardenWaste-info')]//span").text

    # Print the information
    print("\nWaste Collection Dates and Calendar Links:")
    print("=" * 50)
    print(f"\033[1mRubbish Bin:\033[0m {rubbish_date}")
    print("-" * 50)
    print(f"\033[1mRecycling Bin:\033[0m {recycling_date}")
    print("-" * 50)
    print(f"\033[1mGarden Waste Bin:\033[0m {garden_waste_date}")
    print("=" * 50)

    # Prepare the output script
    output = f'''from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response

sb = SkillBuilder()

# LaunchRequest Handler
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Welcome to Bin Collection. You can ask for rubbish, recycling, or garden waste dates."
        return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

# GetBinDatesIntent Handler
class GetBinDatesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GetBinDatesIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Your next rubbish collection is on {rubbish_date} and the recycling is on {recycling_date}. Today's date is {formatted_date}"
        return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response

# Register handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetBinDatesIntentHandler())

# Lambda Handler
lambda_handler = sb.lambda_handler()
'''

    # Write the output to a .py file
    with open("lambda_function.py", "w") as file:
        file.write(output)

except Exception as e:
    print("Error occurred:", e)

finally:
    # Release the resources allocated by Selenium and shut down the browser
    if 'driver' in locals():
        driver.quit()
        print("The results have been written to 'lambda_function.py'.")
