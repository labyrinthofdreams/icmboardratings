Install python2 or install anaconda and run:

conda create -n python2 python=2.7 anaconda  
conda activate python2

Create a directory called "archive/new/lists", and put the *.csv files in there

Then run:

icmboardratings.bat lists.csv old new

"lists.csv" would contain "username","imdb_ratings_url" lines but it no longer works so this doesn't do anything  
"old" should contain previously generated data  
"new" will contain new data

Dates are recommended over names like "old" and "new", e.g.:

icmboardratings.bat lists.csv 20240101 20240601
