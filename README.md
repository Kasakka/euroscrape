# EuroJackpot Analysis

A Python-based project for scraping, analyzing, and predicting EuroJackpot lottery numbers. This project includes tools for historical data collection, statistical analysis, and pattern-based number prediction.

## Features

### Data Collection (`scraper.py`)
- Scrapes historical EuroJackpot lottery results from 2012 to present
- Saves data in CSV format with draw dates, primary numbers, and secondary numbers
- Includes error handling and rate limiting
- Tracks failed requests for later retry

### Statistical Analysis (`results.py`)
Performs comprehensive analysis of lottery data including:
- Number frequency analysis
- Common number pair combinations
- Gap analysis between number appearances
- Sum distribution of winning numbers
- Even/odd number distribution
- High/low number distribution
- Number repetition patterns
- Consecutive number analysis
- Visual representation of number frequencies

### Number Prediction (`mostlikely.py`)
Generates potential number combinations based on:
- Historical frequency weights
- Gap analysis scores
- Pair frequency patterns
- Even/odd balance
- High/low number distribution

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/eurojackpot-analysis.git
cd eurojackpot-analysis
```

2. Install required packages:
```bash
pip install pandas requests matplotlib
```

## Usage

1. First, collect historical data:
```bash
python scraper.py
```

2. Run statistical analysis:
```bash
python results.py
```

3. Generate number predictions:
```bash
python mostlikely.py
```

## Data Format

The script generates a CSV file (`eurojackpot_draw_results.csv`) with the following structure:
- `date`: Draw date
- `primary_numbers`: Five main numbers drawn
- `secondary_numbers`: Two supplementary numbers drawn

## Disclaimer

This project is for educational and entertainment purposes only. Lottery games are based on random chance, and past results do not guarantee future outcomes. Please gamble responsibly.

## AI Contribution Disclosure

Parts of this codebase were developed with the assistance of AI tools. In the spirit of transparency:
- Some code structures and algorithms were suggested by AI language models
- The final implementation was reviewed and verified by human developers
- All code has been tested to ensure functionality and reliability

If you're using or building upon this project, be aware that AI-generated code may require additional validation for your specific use case.
