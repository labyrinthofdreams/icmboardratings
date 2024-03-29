from __future__ import division
import csv
import argparse
import codecs
import os.path
from datetime import datetime
try:
    import jinja2
    import common
    from PIL import Image
except Exception, e:
    print e
    sys.exit(0)



class Entry:
    def __init__(self, ranking, diff, title, year, directors, mean, median, std,
                 numvoters, runtime, imdbrating, imdbvotes, titletype, genres,
                 imdbid, users):
        self.title = title
        self.directors = directors
        self.imdbrating = float(imdbrating) if imdbrating else ''
        self.runtime = int(runtime) if runtime else ''
        self.year = int(year) if year else ''
        self.genres = ', '.join([x.title().replace('_', '-') for x in genres.split(',')])
        self.imdbvotes = int(imdbvotes) if imdbvotes else ''
        self.mean = float(mean)
        self.median = float(median)
        self.std = float(std)
        self.ranking = int(ranking)
        self.numvoters = numvoters
        self.diff = int(diff) if diff else None
        self.imdbid = imdbid
        self.imgname = None
        self.imgsize = None
        self.users = users.split(',')

# UnicodeCsvReader from http://stackoverflow.com/a/6187936/110397
# Author: http://stackoverflow.com/users/412080/maxim-yegorushkin
class UnicodeCsvReader(object):
    def __init__(self, f, encoding="utf-8", **kwargs):
        self.csv_reader = csv.reader(f, **kwargs)
        self.encoding = encoding

    def __iter__(self):
        return self

    def next(self):
        # read and split the csv row into fields
        row = self.csv_reader.next()
        # now decode
        return [unicode(cell, self.encoding) for cell in row]

    @property
    def line_num(self):
        return self.csv_reader.line_num

class UnicodeDictReader(csv.DictReader):
    def __init__(self, f, encoding="utf-8", fieldnames=None, **kwds):
        csv.DictReader.__init__(self, f, fieldnames=fieldnames, **kwds)
        self.reader = UnicodeCsvReader(f, encoding=encoding, **kwds)

def parse_csv(infile, outiter):
    reader = UnicodeCsvReader(infile)
    # Skip header
    reader.next()
    for l in reader:
        e = Entry(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8], l[9],
                  l[10], l[11], l[12], l[13], l[14], l[15])
        outiter.append(e)

def get_files(directory):
    files = []
    for dirname, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            # Get image size
            im = Image.open(os.path.join(dirname, filename))
            files.append(tuple(os.path.splitext(filename) + im.size))
    return files   

def contains_imdbid(iterable, imdbid):
    for item in iterable:
        if item[0] == imdbid:
            return item
    return None

# Jinja2 filters
def add_sign(num):
    if num > 0:
        return '{0:+d}'.format(num)
    else:
        return num

def add_sep(num):
    return '{0:,}'.format(int(num))

def column_split(iterable, count):
    return [iterable[i::count] for i in range(0, count)]
    
def resize_to_width(orig_w, orig_h, new_w):
    return int(round(orig_h / orig_w * new_w)) 

def main():
    opts = argparse.ArgumentParser()
    opts.add_argument('incsv', help='Raw CSV file to convert')
    opts.add_argument('--outhtmltable', help='Filename to create HTML table')
    opts.add_argument('--outhtmlimages', nargs=2, metavar=('FILENAME', 'IMAGEDIRECTORY'),
                      help='Filename to create HTML image list')
    opts.add_argument('--outhtmlthumbs', nargs=2, metavar=('FILENAME', 'IMAGEDIRECTORY'),
                      help='Filename to create HTML thumbnail list')
    opts.add_argument('--outhtmllargeimages', nargs=2, metavar=('FILENAME', 'IMAGEDIRECTORY'),
                      help='Filename to create HTML large image list')                      
    opts.add_argument('--title', help='Title to be used in the HTML')

    args = opts.parse_args()

    entries = []
    with open(args.incsv, 'rb') as f:
        parse_csv(f, entries)

    env = jinja2.Environment(loader=jinja2.PackageLoader('csvtohtml'))
    env.filters['addsign'] = add_sign
    env.filters['addsep'] = add_sep
    env.filters['colsplit'] = column_split

    # Create HTML from CSV
    if args.outhtmltable:
        #outfile = common.verify_file_overwrite(args.outhtmltable)
        outfile = args.outhtmltable

        tpl = env.get_template('csvtohtml.html')
        rendered = tpl.render(entries=entries,
                              title=args.title)

        with codecs.open(outfile, 'wb', 'utf-8') as f:
            f.write(rendered)
            
    if args.outhtmlthumbs:
        #outfile = common.verify_file_overwrite(args.outhtmlthumbs[0])
        outfile = args.outhtmlthumbs[0]
        localfiles = get_files(args.outhtmlthumbs[1])
        
        for e in entries:
            item = contains_imdbid(localfiles, e.imdbid)
            if item:
                e.imgname = ''.join((item[0], item[1]))
                e.imgsize = (item[2], item[3])

        tpl = env.get_template('thumbs_list.html')
        rendered = tpl.render(entries=entries,
                              title=args.title)

        with codecs.open(outfile, 'wb', 'utf-8') as f:
            f.write(rendered)
            
    if args.outhtmllargeimages:
        #outfile = common.verify_file_overwrite(args.outhtmlthumbs[0])
        outfile = args.outhtmllargeimages[0]
        localfiles = get_files(args.outhtmllargeimages[1])
        
        for e in entries:
            item = contains_imdbid(localfiles, e.imdbid)
            if item:
                e.imgname = ''.join((item[0], item[1]))
                e.imgsize = (item[2], item[3])
                e.resizedsize = (400, resize_to_width(item[2], item[3], 400))

        tpl = env.get_template('large.html')
        rendered = tpl.render(entries=entries,
                              title=args.title)

        with codecs.open(outfile, 'wb', 'utf-8') as f:
            f.write(rendered)

    if args.outhtmlimages:
        #outfile = common.verify_file_overwrite(args.outhtmlimages[0])
        outfile = args.outhtmlimages[0]
        localfiles = get_files(args.outhtmlimages[1])

        with codecs.open('missing_images.html', 'ab', 'utf-8') as f:
            f.write(u'<h2>{0}</h2>'.format(args.title))
            for e in entries:
                item = contains_imdbid(localfiles, e.imdbid)
                if item:
                    e.imgname = ''.join((item[0], item[1]))
                    e.imgsize = (item[2], item[3])
                else:
                    f.write(u'<a href="http://imdb.com/title/{0}">{1}</a><br>'.format(e.imdbid, e.title))

        tpl = env.get_template('csvtohtml_images.html')
        rendered = tpl.render(entries=entries,
                              title=args.title)

        with codecs.open(outfile, 'wb', 'utf-8') as f:
            f.write(rendered)

if __name__ == '__main__':
    main()