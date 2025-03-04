import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations

df = pd.read_csv('eurojackpot_draw_results.csv')

def get_sum_of_numbers(numbers):
    return sum(map(int, numbers))

def frequency_analysis(df):
    primary_counter = Counter()
    secondary_counter = Counter()

    for _, row in df.iterrows():
        primary_numbers = row['primary_numbers'].split(', ')
        secondary_numbers = row['secondary_numbers'].split(', ')

        primary_counter.update(primary_numbers)
        secondary_counter.update(secondary_numbers)

    primary_sorted = sorted(primary_counter.items(), key=lambda x: x[1], reverse=True)
    secondary_sorted = sorted(secondary_counter.items(), key=lambda x: x[1], reverse=True)

    return primary_sorted, secondary_sorted

def number_pairing_frequency(df):
    primary_pairs_counter = Counter()

    for _, row in df.iterrows():
        primary_numbers = row['primary_numbers'].split(', ')
        primary_pairs = combinations(primary_numbers, 2)
        primary_pairs_counter.update(primary_pairs)

    primary_pairs_sorted = sorted(primary_pairs_counter.items(), key=lambda x: x[1], reverse=True)

    return primary_pairs_sorted

def number_gap_analysis(df):
    last_seen = {}
    gap_data = {}

    for _, row in df.iterrows():
        date = row['date']
        primary_numbers = row['primary_numbers'].split(', ')

        for number in primary_numbers:
            if number in last_seen:
                gap = pd.to_datetime(date) - pd.to_datetime(last_seen[number])
                gap_days = gap.days
                if number in gap_data:
                    gap_data[number].append(gap_days)
                else:
                    gap_data[number] = [gap_days]

            last_seen[number] = date

    return gap_data

def sum_of_drawn_numbers(df):
    sum_of_primary = [get_sum_of_numbers(row['primary_numbers'].split(', ')) for _, row in df.iterrows()]
    return sum_of_primary

def even_odd_distribution(df):
    even_odd_data = {'even': 0, 'odd': 0}

    for _, row in df.iterrows():
        primary_numbers = row['primary_numbers'].split(', ')
        for number in primary_numbers:
            if int(number) % 2 == 0:
                even_odd_data['even'] += 1
            else:
                even_odd_data['odd'] += 1

    return even_odd_data

def high_low_distribution(df):
    high_low_data = {'high': 0, 'low': 0}

    for _, row in df.iterrows():
        primary_numbers = row['primary_numbers'].split(', ')
        for number in primary_numbers:
            if int(number) > 25:
                high_low_data['high'] += 1
            else:
                high_low_data['low'] += 1

    return high_low_data

def number_repetition(df):
    last_draw = set()
    repetition_count = 0

    for _, row in df.iterrows():
        primary_numbers = set(row['primary_numbers'].split(', '))

        if last_draw:
            repetition_count += len(last_draw.intersection(primary_numbers))

        last_draw = primary_numbers

    return repetition_count

def consecutive_numbers(df):
    consecutive_count = 0

    for _, row in df.iterrows():
        primary_numbers = sorted(map(int, row['primary_numbers'].split(', ')))

        for i in range(len(primary_numbers) - 1):
            if primary_numbers[i + 1] - primary_numbers[i] == 1:
                consecutive_count += 1

    return consecutive_count

def most_likely_winning_row(primary_sorted, secondary_sorted):
    most_likely_primary = [num for num, _ in primary_sorted[:5]]
    most_likely_secondary = [num for num, _ in secondary_sorted[:2]]

    most_likely_primary.sort(key=int)
    most_likely_secondary.sort(key=int)

    return most_likely_primary, most_likely_secondary

def plot_frequencies(primary_sorted, secondary_sorted):
    primary_df = pd.DataFrame(primary_sorted, columns=['Number', 'Frequency'])
    secondary_df = pd.DataFrame(secondary_sorted, columns=['Number', 'Frequency'])

    plt.figure(figsize=(10, 6))
    plt.bar(primary_df['Number'], primary_df['Frequency'], color='blue')
    plt.title('Primary Numbers Frequency')
    plt.xlabel('Number')
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    plt.show()

    plt.figure(figsize=(8, 4))
    plt.bar(secondary_df['Number'], secondary_df['Frequency'], color='green')
    plt.title('Secondary Numbers Frequency')
    plt.xlabel('Number')
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    plt.show()

def main():
    primary_sorted, secondary_sorted = frequency_analysis(df)

    primary_pairs_sorted = number_pairing_frequency(df)

    gap_data = number_gap_analysis(df)

    sum_of_primary = sum_of_drawn_numbers(df)

    even_odd_data = even_odd_distribution(df)

    high_low_data = high_low_distribution(df)

    repetition_count = number_repetition(df)

    consecutive_count = consecutive_numbers(df)

    most_likely_primary, most_likely_secondary = most_likely_winning_row(primary_sorted, secondary_sorted)

    print("\n--- Frequency Analysis ---")
    print(f"Most common primary numbers: {primary_sorted[:5]}")
    print(f"Most common secondary numbers: {secondary_sorted[:2]}")

    print("\n--- Number Pairing Frequency ---")
    print(f"Most common pairs: {primary_pairs_sorted[:5]}")

    print("\n--- Gap Between Draws ---")
    print(f"Example gaps for number '1': {gap_data['1'][:5] if '1' in gap_data else 'Not Available'}")

    print("\n--- Sum of Drawn Numbers ---")
    print(f"Average sum of primary numbers: {sum(sum_of_primary)/len(sum_of_primary):.2f}")

    print("\n--- Even and Odd Distribution ---")
    print(f"Even numbers: {even_odd_data['even']}, Odd numbers: {even_odd_data['odd']}")

    print("\n--- High and Low Distribution ---")
    print(f"High numbers (26-50): {high_low_data['high']}, Low numbers (1-25): {high_low_data['low']}")

    print("\n--- Number Repetition ---")
    print(f"Total numbers repeated from the previous draw: {repetition_count}")

    print("\n--- Consecutive Numbers ---")
    print(f"Total consecutive number pairs: {consecutive_count}")

    print("\n--- Most Likely Winning Row ---")
    print(f"Most likely primary numbers: {', '.join(most_likely_primary)}")
    print(f"Most likely secondary numbers: {', '.join(most_likely_secondary)}")

    plot_frequencies(primary_sorted, secondary_sorted)

if __name__ == "__main__":
    main()
