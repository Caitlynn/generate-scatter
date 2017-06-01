from datetime import datetime
import csv

def per_hour_stats():
    d = {}
    with open("combined_output.csv") as f:
        r = csv.reader(f, delimiter=",")
        for row in r:
            date = datetime.fromtimestamp(int(row[1]))
            day = date.strftime('%Y-%m-%d')
            hour = date.strftime('%H')
            key = day + 'T' + hour
            d.setdefault(key, []).append(row)
    output_csv_lines = []
    for key, values in d.items():
        emoji_counts = list(map(lambda row: int(row[2]), values))
        total_emojis = sum(emoji_counts)
        average_emojis = total_emojis / len(emoji_counts)
        scores = list(map(lambda row: int(row[3]), values))
        total_scores = sum(scores)
        average_scores = total_scores / len(scores)
        sentiments = list(map(lambda row: float(row[4]), values))
        average_sentiments = sum(sentiments) / len(sentiments)
        day, hour = key.split('T')
        csv_line = ','.join([
            key,
            day,
            hour,
            str(total_emojis),
            str(average_emojis),
            str(total_scores),
            str(average_scores),
            str(average_sentiments),
        ])
        output_csv_lines.append(csv_line)

    with open('per_hour_stats.csv', 'w+') as newfile:
        newfile.write('\n'.join(output_csv_lines))
        newfile.flush()

if __name__ == "__main__":
    per_hour_stats()