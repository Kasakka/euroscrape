import requests
import pandas as pd
import time
from datetime import datetime, timedelta

def get_week_year(date):
    return date.strftime("%Y-W%U"), date.year

def fetch_data(week):
    url = f"get-the-url-youself/{week}" #URL removed because not sure if it's allowed to be shared
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data for {week}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data for {week}: {str(e)}")
        return None

def parse_results(data):
    results = []
    for draw in data:
        primary = draw['results'][0]['primary']
        secondary = draw['results'][0].get('secondary', [])
        draw_date = datetime.fromtimestamp(draw['drawTime'] / 1000).strftime('%Y-%m-%d')
        results.append({
            'date': draw_date,
            'primary_numbers': ', '.join(primary),
            'secondary_numbers': ', '.join(secondary)
        })
    return results

def save_results_to_csv(results, filename='eurojackpot_draw_results.csv'):
    df = pd.DataFrame(results)
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)
    print(f"  Results saved to {filename}")

def save_failed_weeks(week, filename='failed_weeks.txt'):
    with open(filename, 'a') as f:
        f.write(f"{week}\n")
    print(f"  Failed week {week} saved to {filename}")


def main():
    results_filename = 'eurojackpot_draw_results.csv'
    failed_weeks_filename = 'failed_weeks.txt'

    start_date = datetime(2024, 12, 14)
    end_date = datetime(2012, 3, 23)

    week_count = 0
    previous_year = start_date.year

    start_time = time.time()

    try:
        while start_date >= end_date:
            week_year, current_year = get_week_year(start_date)

            if "W00" in week_year:
                print(f"Skipping invalid week: {week_year}")
                start_date -= timedelta(weeks=1)
                continue

            print(f"Fetching data for week {week_year} (processing week {week_count + 1})...")

            data = fetch_data(week_year)
            if data:
                weekly_results = parse_results(data)
                save_results_to_csv(weekly_results, results_filename)
                print(f"  Successfully fetched data for {week_year}")
            else:
                print(f"  No data found for {week_year}")
                save_failed_weeks(week_year, failed_weeks_filename)

            start_date -= timedelta(weeks=1)
            week_count += 1

            if current_year < previous_year:
                print(f"\nCompleted all weeks for {previous_year}. Taking a 30-second break...\n")
                time.sleep(30)
                previous_year = current_year

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nScript interrupted manually.")

    finally:
        end_time = time.time()
        total_runtime = end_time - start_time
        minutes, seconds = divmod(total_runtime, 60)
        print(f"\nScript completed. Total runtime: {int(minutes)} minutes and {int(seconds)} seconds.")


if __name__ == "__main__":
    main()
