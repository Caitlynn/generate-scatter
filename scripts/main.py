import os
import json
import fileinput
import util
import multiprocessing
from emoji import UNICODE_EMOJI
import sys

flatten = lambda l: [item for sublist in l for item in sublist]

emojis = flatten([key.split(" ") if " " in key else key for key in list(UNICODE_EMOJI.keys())])
emojis = list(filter(lambda x: len(x) > 0, emojis))

def process_line(line):
    json_line = json.loads(line, encoding='utf8')
    body = json_line.get('body')
    count = 0
    for char in body:
        if char in emojis:
            count += 1
    return ",".join([
        json_line.get('id'),
        json_line.get('created_utc'),
        str(count),
	str(len(body)),
        str(json_line.get('score')),
    ])


def lines(input_file):
    with open(input_file) as f:
        for line in f:
            if line != "\n":
                yield line

@util.time_usage
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()
    data_file = args.input_file

    total_items = util.file_len(data_file)
    print('total lines: {}'.format(total_items))

    pool = multiprocessing.Pool()
    results_iterator = pool.imap_unordered(process_line, lines(data_file), chunksize=10)
    current = 0
    last_message_size = 0
    output_csv = open('./output_{}.csv'.format(os.path.split(data_file)[1]), 'w+')
    for result in results_iterator:
        current += 1
        output_csv.write(result + '\n')
        if current % 100 == 0:
            progress_message = "{}/{} --> {}%".format(
                current,
                total_items, round(current / total_items * 100)
            )
            sys.stderr.write('\b' * last_message_size)
            sys.stderr.write(progress_message)
            sys.stderr.flush()
            last_message_size = len(progress_message)
    sys.stderr.write('\b' * last_message_size)
    sys.stderr.flush()
    pool.terminate()


if __name__ == '__main__':
    main()
