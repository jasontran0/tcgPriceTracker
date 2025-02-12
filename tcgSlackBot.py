import slack
import os
from slack_sdk import WebClient
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from celery import Celery
from tasks import run_tcg_tracker_and_send, get_price_task

# load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# flask app setup
app = Flask(__name__)

# slack app setup
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

# slash command to get all prices by running our tcgPriceTracker.py script and dms the user the csv results
@app.route('/getAllPrices', methods=['POST'])
def get_all_prices():
    user_id = request.form.get('user_id')

    # Step 1: Open a DM with the user to get a valid channel_id
    dm_response = client.conversations_open(users=[user_id])
    dm_channel_id = dm_response["channel"]["id"]  # Get the correct DM channel ID

    
    # Run tcgPriceTracker.py script
    # os.system('python /Users/kyzubs/tcgPriceTracker/tcgPriceTracker.py')
    
    # Step 2: Notify user that they will receive the CSV file
    client.chat_postMessage(channel=user_id, text='Generating the price list. You will receive the CSV file shortly.')
    
    # Step 3: Queue the background job
    run_tcg_tracker_and_send.delay(user_id, dm_channel_id)

    return Response(), 200

@app.route('/getPrice', methods=['POST'])
def get_price():
    product_id = request.form.get('text')
    channel_id = request.form.get('channel_id')
    print(request.form)

    # Step 1: Notify user that they will receive the CSV file
    client.chat_postMessage(channel=channel_id, text=f'Generating the price for product ID {product_id}. You will receive the product details shortly.')

    # Step 2: Queue the background job
    get_price_task.delay(product_id, channel_id)

    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)
