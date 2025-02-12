import os
from celery import Celery
from slack_sdk import WebClient
from dotenv import load_dotenv
from pathlib import Path

# load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# slack client setup
client = WebClient(token=os.environ['SLACK_TOKEN'])

# celery -A tasks.celery worker --pool=solo --loglevel=info

# celery setup
celery = Celery(__name__, broker=os.environ['CELERY_BROKER_URL'])
celery.conf.update(result_backend=os.environ['CELERY_RESULT_BACKEND'])

# 🔹 Asynchronous Task: Runs in Background
@celery.task
def run_tcg_tracker_and_send(channel_id):
    """Background job to run TCG script and send the file."""
    file_path = "/Users/kyzubs/tcgPriceTracker/tcg_price_data.csv"
    
    # Run tcgPriceTracker.py script
    os.system(f'python -u /Users/kyzubs/tcgPriceTracker/tcgPriceTracker.py')

    # Upload the CSV file to the user's DM
    response = client.files_upload_v2(
        channels=channel_id,
        file=file_path,
        title="TCG Prices",
        initial_comment="Here is the latest price list."
    )
    response.get("file")  # returns the full metadata of the uploaded file

@celery.task
def get_price_task(product_id, channel_id):
    """Background job to get the price of a product and send the file."""
    file_path = f"/Users/kyzubs/tcgPriceTracker/{product_id}_price.csv"
    
    # Run tcgPriceTracker.py script with product_id
    os.system(f'python -u /Users/kyzubs/tcgPriceTracker/tcgPriceTracker.py {product_id}')

    # Upload the CSV file to the user's DM
    response = client.files_upload_v2(
        channels=channel_id,
        file=file_path,
        title=f"Price for Product ID {product_id}",
        initial_comment=f"Here is the latest price for product ID {product_id}."
    )
    response.get("file")  # returns the full metadata of the uploaded file
