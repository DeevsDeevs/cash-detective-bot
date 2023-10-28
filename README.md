# cash-detective-bot

Cash Detective Bot is a Telegram bot designed to manage your finances. It helps track your expenses, categorize them, and analyze your financial habits through various charts.

## Core Features

1. **Adding Expenses**:
   - Users can easily add their expenses with a description, cost, and category.

2. **Managing Categories**:
   - Users can create and view categories for better organization of their expenses.

3. **Adding Funds**:
   - Users can update their balance by adding funds to their account.

4. **Viewing Balance**:
   - Users can check their current balance at any time.

5. **Financial Analysis**:
   - Users can analyze their expenses through various charts, including expense history, expense distribution by categories and weekdays, etc.

## Installation and Launch

1. Clone the repository:

```bash
git clone https://github.com/DeevsTheBest/cash-detective-bot.git
cd cash-detective-bot
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Create a .env file with the token and the path to the database:
```
BOT_TOKEN = 'your-telegram-bot-token'
STORAGE_PATH = 'storage/'
```

4. Launch the bot:

```bash
python main.py
```

Now your bot should be online and ready for use in Telegram!

## Running Tests

To run the tests, execute the following command in the project's root directory:

```bash
python tests.py
```

This will run all the tests in the `tests` directory, and you will see the testing results in the console.

## Generating Sample Data

For demonstration purposes, you can easily generate sample data using the `gen_sample_data.py` script. This script creates a set of random purchases along with a list of categories, and saves them to a file which can be used to test the bot.