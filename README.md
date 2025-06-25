# TCG Price Tracker + Slack Bot

A comprehensive price tracking system for TCG Player products with automated Slack bot integration. Built with Python, Flask, and Celery for real-time price monitoring and historical data analysis of Pokémon TCG Prismatic Evolutions products.

## 🌟 Features

- **Price Tracking**: Automated scraping and monitoring of TCG Player product prices
- **Historical Analysis**: Price change calculations with percentage tracking over time
- **Slack Integration**: Real-time notifications and CSV file delivery through Slack commands
- **Asynchronous Processing**: Background task processing using Celery and Redis
- **CSV Export**: Detailed product data export with pricing history
- **Individual Product Queries**: Get specific product information by ID
- **REST API Integration**: Seamless data fetching from TCG Player APIs

## 🛠️ Technologies Used

- **Python 3.13**: Core programming language
- **Flask**: Web framework for Slack bot endpoints
- **Celery**: Distributed task queue for background processing
- **Redis**: Message broker and result backend
- **Slack SDK**: Slack bot integration and file uploads
- **Requests**: HTTP library for API calls
- **CSV**: Data export and storage
- **python-dotenv**: Environment variable management

## 📁 Project Structure

```
tcgPriceTracker/
├── tcgPriceTracker.py     # Main price tracking script
├── tcgSlackBot.py         # Flask app with Slack endpoints
├── tasks.py               # Celery background tasks
├── tcg_price_data.csv     # Historical price data storage
├── .env                   # Environment variables
└── README.md              # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- Redis server
- Slack App with Bot Token
- TCG Player API access

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/tcgPriceTracker.git
cd tcgPriceTracker
```

2. Install required dependencies:
```bash
pip install flask slack-sdk celery redis requests python-dotenv slackeventsapi
```

3. Set up environment variables in `.env`:
```properties
SLACK_TOKEN=your_slack_bot_token
SIGNING_SECRET=your_slack_signing_secret
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

4. Start Redis server:
```bash
redis-server
```

5. Start Celery worker:
```bash
celery -A tasks.celery worker --pool=solo --loglevel=info
```

6. Run the Flask application:
```bash
python tcgSlackBot.py
```

## 🎯 Usage

### Standalone Price Tracking

```bash
# Track all products
python tcgPriceTracker.py

# Track specific product by ID
python tcgPriceTracker.py 610383
```

### Slack Bot Commands

- `/getAllPrices` - Generates complete price list CSV and sends via DM
- `/getPrice [product_id]` - Gets specific product price data

### API Endpoints

- `POST /getAllPrices` - Triggers full price tracking job
- `POST /getPrice` - Triggers single product price lookup

## 📊 Data Features

The system tracks the following data points for each product:
- Product ID and name
- Image URL and product URL
- Number of listings
- Lowest price with shipping
- Current market price
- Price change percentage
- Last change timestamp

### Sample Data Output

```csv
product_id,name,imageURL,url,num_listings,lowest_price_with_shipping,market_price,latestChange,priceChange
593294,Prismatic Evolutions Booster Pack,https://...,https://...,59.0,12.49,12.27,2025-02-12 02:01:35,2.25%
```

## 🔧 Configuration

### Slack Bot Setup

1. Create a Slack App at [api.slack.com](https://api.slack.com)
2. Add Bot Token Scopes: `chat:write`, `files:write`, `conversations:read`
3. Install app to workspace and copy Bot User OAuth Token
4. Set up Event Subscriptions and Slash Commands
5. Update `.env` with your tokens

### Celery Configuration

The system uses Redis as both message broker and result backend. Ensure Redis is running on default port 6379.

## 🚀 Background Processing

The application uses Celery for asynchronous task processing:

- **Price Tracking Jobs**: Run in background to avoid blocking Slack responses
- **File Generation**: CSV creation happens asynchronously
- **Slack Uploads**: File uploads processed in background tasks

## 📱 Slack Integration

Features include:
- Direct message delivery of CSV files
- Real-time status updates
- Error handling and user notifications
- Support for both channel and direct message contexts

## 🔗 API Integration

Integrates with multiple TCG Player endpoints:
- Product catalog API for bulk data
- Individual product detail API for specific queries
- Price and listing information APIs

## 🤝 Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📧 Contact

For questions or support regarding this TCG Price Tracker system, please reach out through GitHub issues or direct contact.

## 📈 Performance

- Tracks 100+ products in under 2 minutes
- Handles concurrent Slack requests
- Efficient data storage and retrieval
- Historical price trend analysis
- Real-time price change monitoring
