# Krapollibot

Krapollibot is a Telegram bot designed to manage and analyze polls in group chats. It allows users to create polls, track answers, and analyze poll data for multiple groups.

## Features

- Create and manage polls in Telegram groups
- Track poll answers with timestamps
- Handle poll data for multiple groups
- Automatic poll closing functionality
- Analyze poll data

## Setup

### Prerequisites

- A Telegram bot token from [BotFather](https://core.telegram.org/bots#botfather)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/krapollibot.git
    cd krapollibot
    ```

2. **Install required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure your Telegram bot token**:
    - Create a file named [bot_token.py] in the project directory.
    - Add the following line to [bot_token.py]:
      ```python
      BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
      ```

### Running the Bot

1. **Start the bot**:
    ```bash
    python Sanuli_bot.py
    ```

## Usage

Add the bot to your Telegram group to start creating and managing polls. 
## Data Storage

### `answers_data.csv`
Stores poll answers with fields:
- chat_id
- poll_id
- chosen_option
- answer_timestamp
- username

### registered_groups.csv
Stores the IDs of registered groups.

### last_polls.csv
Stores the last poll IDs for each group.

### `poll_id_to_chat_id.csv`
Maps poll IDs to chat IDs.


## Acknowledgements

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [aiocron](https://github.com/gawel/aiocron)
