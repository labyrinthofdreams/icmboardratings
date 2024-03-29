import argparse
import csv
import copy
try:
    from common import verify_file_overwrite
    from objsort import objsort
except Exception, e:
    sys.exit(e)

class RawEntry:
    def __init__(self, ranking, diff, title, year, directors, mean, median, std,
                 numvoters, runtime, imdbrating, imdbvotes, titletype, genres,
                 imdbid, users):
        self.imdbid = imdbid
        self.title = title
        self.titletype = titletype
        self.directors = directors
        self.imdbrating = float(imdbrating) if imdbrating else None
        self.runtime = int(runtime) if runtime else None
        self.year = int(year) if year else None
        self.genres = genres
        self.imdbvotes = int(imdbvotes) if imdbvotes else None
        self.users = users
        self.mean = mean
        self.median = median
        self.std = std
        self.ranking = int(ranking)
        self.numvoters = numvoters
        self.diff = diff
    def header(self):
        """Returns a header for the output file. Order should match to_list()"""
        return ['Ranking', 'Diff', 'Title', 'Year', 'Directors', 'Mean',
                'Median', 'Std deviation', 'Num voters', 'Runtime (mins)',
                'IMDb rating', 'IMDb votes', 'Title type', 'Genres', 'IMDb id',
                'Users']
    def to_list(self):
        return [self.ranking, self.diff, self.title, self.year, self.directors,
                self.mean, self.median, self.std, self.numvoters,
                self.runtime, self.imdbrating, self.imdbvotes, self.titletype,
                self.genres, self.imdbid, self.users]

def main():
    opts = argparse.ArgumentParser()
    opts.add_argument('oldcsv', help='Path to old (raw) top list')
    opts.add_argument('newcsv', help='Path to new (raw) top list')
    opts.add_argument('newallcsv', help='Path to new (raw) top list with all entries')
    opts.add_argument('outcsv', help='Path to the output CSV file')

    args = opts.parse_args()

    outfile = verify_file_overwrite(args.outcsv)

    oldentries = []
    newentries = {}
    # Read and parse the old CSV file
    with open(args.oldcsv, 'rb') as f:
        reader = csv.reader(f)
        # Skip header
        reader.next()
        for line in reader:
            oldentries.append(line)
    # Read and parse the new CSV file
    with open(args.newcsv, 'rb') as f:
        reader = csv.reader(f)
        # Skip header
        header = reader.next()
        for line in reader:
            imdbid = line[-2]
            newentries[imdbid] = line

    dropentries = []
    for o in oldentries:
        imdbid = o[-2]
        if not newentries.has_key(imdbid):
            dropentries.append(o)

    # Read and parse the new full raw CSV file
    newallentries = {}
    with open(args.newallcsv, 'rb') as f:
        reader = csv.reader(f)
        # Skip header
        reader.next()
        for line in reader:
            imdbid = line[-2]
            newallentries[imdbid] = line

    # Get ranking differences and update old values to new values
    realdropentries = []
    for d in dropentries:
        imdbid = d[-2]
        oldentry = RawEntry(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8],
                     d[9], d[10], d[11], d[12], d[13], d[14], d[15])
        if newallentries.has_key(imdbid):
            nd = newallentries[imdbid]
            newentry = RawEntry(nd[0], nd[1], nd[2], nd[3], nd[4], nd[5], nd[6], nd[7], nd[8],
                                nd[9], nd[10], nd[11], nd[12], nd[13], nd[14], nd[15])

            diff = int(oldentry.ranking) - int(newentry.ranking)
            # This replaces all old values with values


            # Update ranking difference
            #newallentries[imdbid][1] = diff
            newentry.diff = diff

            realdropentries.append(newentry)
        else:
            # Reset diff so that there's no chance of having some old
            # value in there
            # If this gets executed it means the entry was not found
            # in the new full title list
            # Reasons may be a removed rating / user rating list
            # resulting in fewer than required ratings
            oldentry.ranking = 0
            oldentry.diff = 0
            oldentry.mean = 0.0
            oldentry.median = 0.0
            oldentry.std = 0.0
            oldentry.numvoters = 0
            realdropentries.append(oldentry)

    objsort(realdropentries, [('mean', 'd'), ('year', 'a'), ('title', 'a')])

    # Write dropped entries to output file
    with open(args.outcsv, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for e in realdropentries:
            writer.writerow(e.to_list())





if __name__ == '__main__':
    main()