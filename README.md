# ScoreNotifier - Improved Security and Reliability

## Security and Reliability Improvements

This version includes several important improvements:

### 🔒 Security Enhancements
- **Environment Variables**: Tokens are now loaded from environment variables instead of hardcoded values
- **Sensitive Data Protection**: No more hardcoded tokens in source code

### 🛡️ Error Handling
- **Network Request Error Handling**: Proper handling of HTTP requests failures
- **JSON Parsing Protection**: Safe handling of malformed JSON responses
- **API Data Validation**: Validation of API response structure
- **File Loading Safety**: Graceful handling of missing or corrupted target.json

### ⚡ Performance Improvements
- **Async Function Optimization**: Replaced blocking `time.sleep()` with `await asyncio.sleep()`
- **Discord Channel Validation**: Improved channel existence checking

## Setup

### Environment Variables

Set the following environment variables before running the application:

```bash
# Required
export DISCORD_TOKEN="your_discord_bot_token_here"
export DISCORD_CHANNEL_ID="123456789012345678"

# Optional (for Line notifications)
export LINE_NOTIFY_TOKEN="your_line_notify_token_here"
```

### Installation

```bash
# Install required dependencies
pip install nextcord requests

# Run the application
python3 main.py
```

### Docker Usage (Example)

```bash
# Run with environment variables
docker run -e DISCORD_TOKEN="your_token" \
           -e DISCORD_CHANNEL_ID="your_channel_id" \
           -e LINE_NOTIFY_TOKEN="your_line_token" \
           your-scorenotifier-image
```

## Configuration

The application reads target score names from `target.json`:

```json
{
    "targets": [
        "20 ธันวาคม 2567 - ม.ต้น",
        "23 ธันวาคม 2567 - ม.ปลาย",
        "ผลการประเมิน GPA ม.3"
    ]
}
```

## Error Messages

The improved version provides clear error messages:

- `❌ DISCORD_TOKEN environment variable not set` - Missing required Discord token
- `⚠️ LINE_NOTIFY_TOKEN not set` - Line notifications disabled
- `❌ Discord channel not found` - Invalid channel ID or insufficient permissions
- `❌ Network error` - API connection issues
- `❌ JSON parsing error` - Invalid API response format
- `⚠️ Invalid item structure` - Malformed API data

## Testing

Run the included test suite:

```bash
python3 test_main.py
```

This will validate all the security and reliability improvements.