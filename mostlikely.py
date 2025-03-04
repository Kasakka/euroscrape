import pandas as pd
from collections import Counter, defaultdict
from itertools import combinations

df = pd.read_csv('eurojackpot_draw_results.csv')

def calculate_gap_scores(gap_data):
    gap_scores = defaultdict(int)
    for number, gaps in gap_data.items():
        avg_gap = sum(gaps) / len(gaps) if gaps else 0
        gap_scores[number] = avg_gap
    return gap_scores

def frequency_analysis(df):
    primary_counter = Counter()
    secondary_counter = Counter()

    for _, row in df.iterrows():
        primary_numbers = row['primary_numbers'].split(', ')
        secondary_numbers = row['secondary_numbers'].split(', ')

        primary_counter.update(primary_numbers)
        secondary_counter.update(secondary_numbers)

    return primary_counter, secondary_counter

def number_pairing_frequency(df):
    primary_pairs_counter = Counter()

    for _, row in df.iterrows():
        primary_numbers = row['primary_numbers'].split(', ')
        primary_pairs = combinations(primary_numbers, 2)
        primary_pairs_counter.update(primary_pairs)

    return primary_pairs_counter

def number_gap_analysis(df):
    last_seen = {}
    gap_data = defaultdict(list)

    for _, row in df.iterrows():
        date = row['date']
        primary_numbers = row['primary_numbers'].split(', ')

        for number in primary_numbers:
            if number in last_seen:
                gap = pd.to_datetime(date) - pd.to_datetime(last_seen[number])
                gap_days = gap.days
                gap_data[number].append(gap_days)

            last_seen[number] = date

    return gap_data

def even_odd_distribution(df):
    even_numbers = set()
    odd_numbers = set()

    for _, row in df.iterrows():
        primary_numbers = row['primary_numbers'].split(', ')
        for number in primary_numbers:
            if int(number) % 2 == 0:
                even_numbers.add(number)
            else:
                odd_numbers.add(number)

    return even_numbers, odd_numbers

def high_low_distribution(df):
    high_numbers = set()
    low_numbers = set()

    for _, row in df.iterrows():
        primary_numbers = row['primary_numbers'].split(', ')
        for number in primary_numbers:
            if int(number) > 25:
                high_numbers.add(number)
            else:
                low_numbers.add(number)

    return high_numbers, low_numbers

def most_likely_row(df):
    primary_counter, secondary_counter = frequency_analysis(df)
    primary_pairs_counter = number_pairing_frequency(df)
    gap_data = number_gap_analysis(df)
    even_numbers, odd_numbers = even_odd_distribution(df)
    high_numbers, low_numbers = high_low_distribution(df)

    gap_scores = calculate_gap_scores(gap_data)

    number_scores = defaultdict(int)

    for number, count in primary_counter.items():
        number_scores[number] += count * 1.5

        if number in gap_scores:
            number_scores[number] += gap_scores[number] * 0.5

        for pair in primary_pairs_counter:
            if number in pair:
                number_scores[number] += primary_pairs_counter[pair] * 1

    for number in number_scores:
        if number in even_numbers:
            number_scores[number] += 2
        elif number in odd_numbers:
            number_scores[number] += 2

    for number in number_scores:
        if number in high_numbers:
            number_scores[number] += 1
        elif number in low_numbers:
            number_scores[number] += 1

    sorted_numbers = sorted(number_scores.items(), key=lambda x: x[1], reverse=True)

    most_likely_primary = [num for num, _ in sorted_numbers[:5]]

    sorted_secondary = sorted(secondary_counter.items(), key=lambda x: x[1], reverse=True)
    most_likely_secondary = [num for num, _ in sorted_secondary[:2]]

    most_likely_primary.sort(key=int)
    most_likely_secondary.sort(key=int)

    return most_likely_primary, most_likely_secondary


def main():
    most_likely_primary, most_likely_secondary = most_likely_row(df)

    print("\n--- Most Likely Next Winning Row ---")
    print(f"Most likely primary numbers: {', '.join(most_likely_primary)}")
    print(f"Most likely secondary numbers: {', '.join(most_likely_secondary)}")


if __name__ == "__main__":
    main()
