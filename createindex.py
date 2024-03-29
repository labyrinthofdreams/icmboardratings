import argparse
import os
import codecs
import time

try:
    import jinja2
    from common import verify_file_overwrite
except Exception, e:
    print e
    sys.exit(0)

def main():
    opts = argparse.ArgumentParser()
    opts.add_argument('userdir', help='Directory with user CSV rating files')
    opts.add_argument('saveto', help='Path to the save file')

    args = opts.parse_args()

    outfile = verify_file_overwrite(args.saveto)

    for dirname, dirnames, filenames in os.walk(args.userdir):
        users = [os.path.splitext(fn)[0].replace('.partial', '') for fn in filenames]

    env = jinja2.Environment(loader=jinja2.PackageLoader('csvtohtml'))
    tpl = env.get_template('index.html')

    # Local timestamp
    weeknum = int(time.strftime('%W')) + 1
    updated = time.strftime('%Y %B %d (week {0})'.format(weeknum))

    rendered = tpl.render(users=users, date_updated=updated)

    with codecs.open(outfile, 'wb') as f:
        f.write(rendered)

if __name__ == '__main__':
    main()