import argparse
import csv
try:
    from common import verify_file_overwrite
except Exception, e:
    sys.exit(e)

def main():
    opts = argparse.ArgumentParser()
    opts.add_argument('oldcsv', help='Path to compare against')
    opts.add_argument('cmpcsv', help='Path to raw CSV file to compare')
    opts.add_argument('outcsv', help='Path to the output CSV file')

    args = opts.parse_args()

    outfile = verify_file_overwrite(args.outcsv)

    oldentries = {}
    cmpentries = []
    # Read and parse the old CSV file
    with open(args.oldcsv, 'rb') as f:
        reader = csv.reader(f)
        # Skip header
        reader.next()
        for line in reader:
            oldentries[line[-2]] = line
    # Read and parse the new CSV file
    with open(args.cmpcsv, 'rb') as f:
        reader = csv.reader(f)
        # Skip header
        header = reader.next()
        for line in reader:
            cmpentries.append(line)

    newentries = []
    for c in cmpentries:
        if not oldentries.has_key(c[-2]):
            newentries.append(c)
    with open(outfile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(newentries)





if __name__ == '__main__':
    main()