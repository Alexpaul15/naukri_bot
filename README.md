# Naukri.com Job Application Bot

An automated bot for applying to jobs on Naukri.com using Selenium WebDriver.

## Features

- Automated job search based on domains and locations
- Smart job application process
- Handles multiple job cards and pages
- Saves applied jobs history
- Configurable application limits
- Anti-detection measures
- Robust error handling

## Prerequisites

- Python 3.x
- Chrome browser
- ChromeDriver (automatically managed by webdriver_manager)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/naukri_bot.git
cd naukri_bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

Edit the following parameters in `naukri_bot.py`:

- `job_domains`: List of job domains to search for
- `locations`: List of preferred locations
- `max_applications`: Maximum number of applications to submit
- `default_answers`: Default answers for application forms

## Usage

1. Run the bot:
```bash
python naukri_bot.py
```

2. When the browser opens, you'll have 60 seconds to log in to your Naukri.com account manually.

3. The bot will then automatically:
   - Search for jobs based on configured domains and locations
   - Apply to matching jobs
   - Save application history
   - Handle pagination and multiple job cards

## Features

- **Smart Job Detection**: Multiple methods to find and process job listings
- **Anti-Detection**: Measures to avoid bot detection
- **Error Recovery**: Automatic recovery from common errors
- **Application Tracking**: Saves applied jobs to prevent duplicates
- **Configurable**: Easy to modify search parameters and application settings

## Safety Features

- Skips jobs requiring external website applications
- Handles system locks and popups
- Manages browser windows and tabs safely
- Recovers from common errors and exceptions

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 