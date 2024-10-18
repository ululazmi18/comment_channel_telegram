# 🌟 Auto Comment Telegram Script

## 📖 Description

This script automatically comments on messages in Telegram channels using multiple accounts. You can set delays between comments and account switches according to your needs.

## ✨ Features

- Automatic commenting on Telegram channels.
- Adjustable delays for comments and account switches.
- Support for sending text and media.

## 🚀 Installation

### Additional Steps for Termux
  
  1. **Update Packages**
     ```bash
     pkg update && pkg upgrade
     ```
  
  2. **Install Required Packages**
     ```bash
     pkg install python git
     ```
  
  3. **Allow Storage Access**
     Run the following command to grant storage access:
     ```bash
     termux-setup-storage
     ```
     Select "Allow" when prompted.
  
  4. **Access Internal Folder**
     ```bash
     cd /storage/emulated/0
     ```
  
  5. **Set Up Git for Security**
     To allow Git operations in Termux, run:
     ```bash
     git clone https://github.com/ululazmi18/comment_channel_telegram.git
     cd comment_channel_telegram
     git config --global --add safe.directory /storage/emulated/0/comment_channel_telegram
     ```

### 1. Preparation

- **Python**: Ensure Python is installed on your system. Download it from [python.org](https://www.python.org/downloads/).
- **Pip**: Pip usually comes with the Python installation. Ensure pip is up to date:
  ```bash
  python -m pip install --upgrade pip
  ```

### 2. Clone the Repository

Clone this repository to your local directory using the following command:

```bash
git clone https://github.com/ululazmi18/comment_channel_telegram.git
cd comment_channel_telegram
```

### 3. Install Dependencies

Once you're in the repository directory, install the required dependencies:

```bash
pip install -r requirements.txt
```

## ⚙️ How to Use

This script uses the following arguments:

```bash
python main.py --api API_ID API_HASH --cdelay COMMENT_DELAY_MIN COMMENT_DELAY_MAX --sdelay SWITCH_DELAY_MIN SWITCH_DELAY_MAX --limit LIMIT --add PHONE_NUMBER
```

### 🛠️ Arguments

- `--api API_ID API_HASH`: Your Telegram application's API ID and API Hash.
- `--cdelay COMMENT_DELAY_MIN COMMENT_DELAY_MAX`: Minimum and maximum delay for comments (in seconds).
- `--sdelay SWITCH_DELAY_MIN SWITCH_DELAY_MAX`: Minimum and maximum delay for account switching (in seconds).
- `--limit LIMIT`: Number of messages to fetch from each channel (default: 2).
- `--add PHONE_NUMBER`: New phone number to add (format: +123456789).

### 💡 Usage Examples

1. **Adding a new account:**
   ```bash
   python main.py --api 12345678 your_api_hash --add +123456789
   ```

2. **Setting delays and message limit:**
   ```bash
   python main.py --cdelay 1 5 --sdelay 300 600 --limit 5
   ```

## 🔧 Configuration

If the `config.json` file does not exist, the script will create it with default settings. You can manually edit `config.json` if needed.

## ⚠️ Note

- Ensure you do not violate Telegram's usage policies while using this script.
- Use this script wisely and in accordance with the applicable rules.
