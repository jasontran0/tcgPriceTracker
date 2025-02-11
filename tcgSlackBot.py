import slack
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']


client.chat_postMessage(channel='#tcgbot', text='Hello World!')

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
    file_name = 'tcg_price_data.csv'
    file_size = os.path.getsize(file_path)  # Get file size in bytes

    # Step 1: Request an upload URL from Slack
    # response = client.api_call('files.getUploadURLExternal')
    # print(response)
    # print("hi")
        # Step 1: Request an upload URL from Slack
    upload_response = client.api_call(
        "files.getUploadURLExternal",
        params={
            "filename": file_name,
            "length": file_size
        }
    )

    if not upload_response["ok"]:
        client.chat_postMessage(channel=user_id, text="Failed to get upload URL from Slack.")
        return Response(), 500

    upload_url = upload_response["upload_url"]
    file_id = upload_response["file_id"]
    # upload_response = client.files_getUploadURLExternal(filename=file_name, length=file_size)
    # upload_url = upload_response["upload_url"]
    # file_id = upload_response["file_id"]

    # Step 2: Upload the file to the provided URL
    with open(file_path, 'rb') as file_data:
        requests.put(upload_url, data=file_data, headers={'Content-Type': 'application/octet-stream'})

    # Step 3: Complete the upload
    # client.files.completeUploadExternal(
    #     file_id=file_id,
    #     channel_id=user_id,
    #     title='TCG Prices',
    #     initial_comment='Here is the latest price list.'
    # )

    # Step 3: Complete the upload
    print("Completing the upload")
    complete_response = client.api_call(
        "files.completeUploadExternal",
        json={  # Use `json=` to properly format the request
            "files": [{"id": file_id}],  # <-- This fixes the missing `files` error
            "channel_id": channel_id,
            "title": "TCG Prices",
            "initial_comment": "Here is the latest price list."
        }
    )

    if not complete_response["ok"]:
        client.chat_postMessage(channel=user_id, text="Failed to complete file upload.")
        return Response(), 500

    # message: "<user_id> Here is the latest price list."
    # target: user_id
    # title: "TCG Prices"
    # data:
    #     file:
    #         path: file_path
    print("All done")
    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True)
