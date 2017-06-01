import csv

def main():
    d = {}
    with open("combined_output.csv") as f:
        r = csv.reader(f, delimiter=",")
        for row in r:
            d.setdefault(row[2], []).append(int(row[3]))
    for key, value in d.items():
        avg = sum(value)/len(value)
        d[key] = avg

    with open('count_score.csv', 'w+') as newfile:
        writer = csv.writer(newfile)
        for key, value in d.items():
            writer.writerow([key, value])

if __name__ == "__main__":
    main()
