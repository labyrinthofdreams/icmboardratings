"""Strip and re-order columns from a raw CSV file"""
import argparse
import csv

try:
    from common import verify_file_overwrite
except Exception, e:
    print e
    sys.exit(0)

def extract(iterable, *idx):
    """Extract values from iterable by indexes in given order"""
    return [iterable[i] for i in idx]

def main():
    opts = argparse.ArgumentParser()
    opts.add_argument('incsv', help='CSV file to strip')
    opts.add_argument('outcsv', help='CSV file to save to')

    args = opts.parse_args()

    outfile = verify_file_overwrite(args.outcsv)

    with open(args.incsv, 'rb') as inf, open(outfile, 'wb') as outf:
        reader = csv.reader(inf)
        writer = csv.writer(outf)
        for line in reader:
            writer.writerow(extract(line, 0, 1, 2, 3, 4, 5, 8, 10, 11, 9, 13, -2))


if __name__ == '__main__':
    main()
