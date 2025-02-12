import slack
import os
import requests
from slack_sdk import WebClient
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
# app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# # Start your app
# if __name__ == "__main__":
#     SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

# slash command to get all prices by running our tcgPriceTracker.py script and dms the user the csv results
@app.route('/getAllPrices', methods=['POST'])
def get_all_prices():
    user_id = request.form.get('user_id')

    # Step 1: Open a DM with the user to get a valid channel_id
    dm_response = client.conversations_open(users=[user_id])
    channel_id = dm_response["channel"]["id"]  # Get the correct DM channel ID

    
    # Run tcgPriceTracker.py script
    # os.system('python /Users/kyzubs/tcgPriceTracker/tcgPriceTracker.py')
    
    # Notify user that they will receive the CSV file
    client.chat_postMessage(channel=user_id, text='Generating the price list. You will receive the CSV file shortly.')
    
    # Assuming the script generates a file named 'tcg_price_data.csv' in the same directory
    file_path = '/Users/kyzubs/tcgPriceTracker/tcg_price_data.csv'

    # Upload the csv file to the user's DM
    response = client.files_upload_v2(
        channels=channel_id,
        file=file_path,
        title='TCG Prices',
        initial_comment='Here is the latest price list.'
    )
    response.get("file")  # returns the full metadata of the uploaded file
    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True)
