# Bin Collection Alexa Skill

This project makes an Alexa skill that tells you when your bins will be collected. It covers rubbish, recycling, and garden waste based on where you live. The skill gets up-to-date info by scraping a council website and then answers your questions on any Alexa device.

---

## Disclaimer

This repo is mostly a brain dump since it started as a fun learning project, so apologies for the million unnecessary modules. I found setting up web scraping on AWS Lambda a tad tricky because you need to create an S3 bucket, add a Lambda layer, and sometimes Chromedriver just doesn’t cooperate. So instead, I run the scraping on a Raspberry Pi and then upload the results to AWS Lambda using the AWS CLI at scheduled intervals.

---

## What the Project Does

The Bin Collection Alexa Skill has two main parts:

1. A web scraping script that grabs the bin collection dates from the council website
2. A Lambda function that uses the scraped data to answer Alexa questions

---

## How It Works

First, the web scraper uses Selenium to pull rubbish, recycling, and garden waste collection dates from the council webpage. It then formats this data into a Python script that works with the Alexa skill.

Next, the Alexa skill, built with the ask\_sdk\_core library, uses that scraped data to respond when you ask about bin collection days.

Finally, the data gets saved to a Python file called lambda\_function.py, which you upload to AWS Lambda. Alexa calls this Lambda function whenever you ask for your bin collection info.

---

## Parts of the Project

### 1. Web Scraping Script (lambda\_function\_script.py)

This script uses Selenium to pull the bin dates from the council website.

* Runs Chrome in headless mode so it works without opening a browser window
* Waits for the webpage to load fully before scraping
* Gets rubbish, recycling, and garden waste collection dates
* Outputs the data in the right format for the Alexa Lambda function

You’ll need:

* Selenium installed in Python
* Chromium and the matching ChromeDriver
* The script uses wait methods so it doesn’t scrape too early before the page loads

How it works: it sets up a headless Chrome session, goes to the council’s page, waits for the data to appear, pulls the dates, and then creates a Python file you can upload to AWS Lambda.

---

### 2. Alexa Skill (Lambda Function) (lambda\_function.py)

This is the main Alexa skill script you put in AWS Lambda.

* When you open the skill it says hello and welcomes you
* When you ask about bin dates, it uses the scraped data to tell you when rubbish, recycling, or garden waste will be collected and also tells you today's date for reference.
* It gives clear, easy-to-understand answers that Alexa reads out loud

It works by listening for the launch request to greet you, and then handling the bin date intent by responding with the info. It’s wrapped so AWS Lambda can run it.

---

## How to Set It Up

### What You Need First

* Python 3.7 or above
* An AWS Lambda account to put the skill on
* Selenium installed via pip
* ChromeDriver that matches your version of Chromium or Chrome
* An Amazon Developer account to create and manage your Alexa skill

---

### Step 1: Install the Required Libraries

Open your terminal and run:

```bash
pip install selenium ask-sdk-core
```

---

### Step 2: Run the Web Scraping Script

Run this command to scrape the latest bin dates and make the Lambda script:

```bash
python lambda_function_script.py
```

This will make a new file called lambda\_function.py that you can upload to AWS Lambda.

---

### Step 3: Deploy the Skill to AWS Lambda

* Go to the AWS Lambda Console
* Create a new Lambda function and upload the lambda\_function.py file
* Give it the right permissions by assigning an IAM role
* In the Amazon Developer Console, link your Lambda function to the Alexa skill and set up intents and sample phrases

---

### Step 4: Try Out Your Alexa Skill

You can test your skill using the Alexa simulator in the Amazon Developer Console. Just ask something like:

"When is my next rubbish collection?"
