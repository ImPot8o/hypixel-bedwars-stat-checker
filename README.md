# Hypixel BedWars Stats Tracker

A GUI application to view player statistics from Hypixel's BedWars game using Python, tkinter, and the Hypixel API.

## Features

- Displays BedWars stats for different modes (Solo, Doubles, 3v3v3v3, 4v4v4v4, and Overall).
- Includes a special section for Dream modes.
- User-friendly interface to input player names and view their stats.

## Dependencies

- Python 3.x
- `tkinter` for GUI (usually comes pre-installed with Python)
- `requests` for API calls

Install `requests` with:
```bash
pip install requests
```

## How to Run

1. **Clone or download the project:**
  ```bash
   git clone https://github.com/ImPot8o/hypixel-bedwars-stat-checker.git
   cd hypixel-bedwars-stat-checker
   ```

2. **Set Up Your API Key:**
   - First, obtain an API key from Hypixel by following these steps:
     1. Log into https://developer.hypixel.net/ and get your api key
     2. Place it in the code.

   - Open `main.py` or the main script file in an editor and replace `API_KEY = "YOUR API KEY"` with your own API key:
     ```python
     API_KEY = "YOUR API KEY"
     ```

3. **Run the script:**
   ```bash
   python main.py
   ```

   If you have multiple Python versions installed, you might need to use:
   ```bash
   python3 main.py
   ```

## Usage

- **Enter Player Name:** Type the Minecraft IGN (in-game name) of the player whose stats you want to view.
- **Get Stats:** Click the "Get Stats" button to retrieve and display the statistics.

## Troubleshooting

- **No Stats Displayed:** Ensure the player name is correct and the player has played BedWars. Also, check if your API key is valid and not rate-limited. You have to wait a couple minutes before requesting a players stats more than once
- **API Key Issues:** If you're encountering API key errors, verify that your key hasn't been revoked or hit the rate limit. Remember, API keys can only make a certain number of requests per minute.

## Contributing

Feel free to contribute to this project by improving the UI, adding features, or optimizing the code. 

1. Fork the repository.
2. Create a new branch for your feature (```bashgit checkout -b feature/AmazingFeature```).
3. Commit your changes (```bashgit commit -m 'Add some AmazingFeature'```).
4. Push to the branch (```bashgit push origin feature/AmazingFeature```).
5. Create a Pull Request.

## License

This project is under the MIT License - see the `LICENSE` file for details.

---

**Note:** This project is for educational purposes and to enhance your programming skills. Always ensure compliance with Hypixel's terms of service when using their API.
