@ECHO OFF
:: CSV List is a CSV file with user,imdburl\n pairs to download CSV files from
SET csvlist=%1
:: Base Dir is the dir where the generated ratings files are saved
SET basedir=archive\%2
:: CSV List Dir is the dir where the CSV rating lists are saved
SET csvlistdir=%basedir%\lists

IF NOT EXIST %basedir% (
    MKDIR %basedir%
    MKDIR %csvlistdir%
)

ECHO ---------------------
ECHO Downloading CSV files
ECHO ---------------------
:: python imdb_csv.py %csvlist% %csvlistdir%

ECHO ---------------------------------
ECHO Generating CSV Rating files
ECHO ---------------------------------
                                                                                   
ECHO Generating Top 1000
python ratings.py %csvlistdir% %basedir%\top1000combined.raw.csv --limit-entries 1000 ^
--limit-voters-min 5 --limit-titletype feature docu short tvmovie --sort-by dmean ayear atitle
python csv_strip.py %basedir%\top1000combined.raw.csv %basedir%\top1000combined.csv                                                                                   
                                                                                                                                                                      
ECHO Generating Top 1000 Feature films
python ratings.py %csvlistdir% %basedir%\top1000features.raw.csv --limit-entries 1000 ^
--limit-voters-min 5 --limit-titletype feature --sort-by dmean ayear atitle 
python csv_strip.py %basedir%\top1000features.raw.csv %basedir%\top1000features.csv

ECHO Generating Top 1001-2000 Feature films
python ratings.py %csvlistdir% %basedir%\top1001-2000features.raw.csv --limit-entries 2000 ^
--limit-voters-min 5 --limit-titletype feature --sort-by dmean ayear atitle  --discard 1000
python csv_strip.py %basedir%\top1001-2000features.raw.csv %basedir%\top1001-2000features.csv

ECHO Generating Top 200 Documentaries
python ratings.py %csvlistdir% %basedir%\top200docus.raw.csv --limit-entries 200 ^
--limit-voters-min 5 --limit-titletype docu --sort-by dmean ayear atitle 
python csv_strip.py %basedir%\top200docus.raw.csv %basedir%\top200docus.csv

ECHO Generating Top 200 Short films
python ratings.py %csvlistdir% %basedir%\top200shorts.raw.csv --limit-entries 200 ^
--limit-voters-min 5 --limit-titletype short --sort-by dmean ayear atitle 
python csv_strip.py %basedir%\top200shorts.raw.csv %basedir%\top200shorts.csv

ECHO Generating Bottom 100 Feature films
python ratings.py %csvlistdir% %basedir%\bottom100features.raw.csv --limit-entries 100 ^
--limit-voters-min 5 --limit-titletype feature --sort-by amean dyear dtitle 
python csv_strip.py %basedir%\bottom100features.raw.csv %basedir%\bottom100features.csv

ECHO Generating 2-4 votes list
python ratings.py %csvlistdir% %basedir%\2votes.raw.csv --limit-entries 200 ^
--limit-voters-min 2 --limit-voters-max 4 --limit-titletype feature --sort-by dmean ayear atitle
python csv_strip.py %basedir%\2votes.raw.csv %basedir%\2votes.csv

ECHO Generating Full lists for diffs
python ratings.py %csvlistdir% %basedir%\combined-all-asc.csv --limit-voters-min 5 --limit-titletype feature docu short tvmovie --sort-by dmean ayear atitle 
python ratings.py %csvlistdir% %basedir%\features-all-asc.csv --limit-voters-min 5 --limit-titletype feature --sort-by dmean ayear atitle 
python ratings.py %csvlistdir% %basedir%\features-all-desc.csv --limit-voters-min 5 --limit-titletype feature --sort-by amean dyear dtitle
python ratings.py %csvlistdir% %basedir%\docus-all-asc.csv --limit-voters-min 5 --limit-titletype docu --sort-by dmean ayear atitle 
python ratings.py %csvlistdir% %basedir%\shorts-all-asc.csv --limit-voters-min 5 --limit-titletype short --sort-by dmean ayear atitle

ECHO Generating below limit lists
python ratings.py %csvlistdir% %basedir%\features-full-asc.csv --limit-voters-max 4 --limit-titletype feature --sort-by dmean ayear atitle
python ratings.py %csvlistdir% %basedir%\docus-full-asc.csv --limit-voters-max 4 --limit-titletype docu --sort-by dmean ayear atitle
python ratings.py %csvlistdir% %basedir%\shorts-full-asc.csv --limit-voters-max 4 --limit-titletype short --sort-by dmean ayear atitle

ECHO Generating database
python ..\csv_to_sqlite\csv_to_sqlite.py %basedir%\features-all-asc.csv %basedir%\db.db films --clear
python ..\csv_to_sqlite\csv_to_sqlite.py %basedir%\shorts-all-asc.csv %basedir%\db.db films
python ..\csv_to_sqlite\csv_to_sqlite.py %basedir%\docus-all-asc.csv %basedir%\db.db films
python ..\csv_to_sqlite\csv_to_sqlite.py %basedir%\features-full-asc.csv %basedir%\db.db missing --clear
python ..\csv_to_sqlite\csv_to_sqlite.py %basedir%\shorts-full-asc.csv %basedir%\db.db missing
python ..\csv_to_sqlite\csv_to_sqlite.py %basedir%\docus-full-asc.csv %basedir%\db.db missing

ECHO ----------------------
ECHO Generating HTML Tables
ECHO ----------------------

python csv_to_html.py %basedir%\top1000combined.raw.csv --outhtmltable %basedir%\top1000combined.html ^
--outhtmlthumbs %basedir%\top1000combined.screens.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top1000combined.screens.large.html F:\ICM_Highest_Rated\Screenshots --title "Top 1000"

python csv_to_html.py %basedir%\top1000features.raw.csv --outhtmltable %basedir%\top1000features.html ^
--outhtmlthumbs %basedir%\top1000features.screens.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top1000features.screens.large.html F:\ICM_Highest_Rated\Screenshots --title "Top 1000 Feature films"
python csv_to_html.py %basedir%\top1000features.new.raw.csv --outhtmltable %basedir%\top1000features.new.html ^
--outhtmlthumbs %basedir%\top1000features.screens.new.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top1000features.screens.new.large.html F:\ICM_Highest_Rated\Screenshots --title "New in Top 1000 Feature films"
python csv_to_html.py %basedir%\top1000features.dropped.raw.csv --outhtmltable %basedir%\top1000features.dropped.html ^
--outhtmlthumbs %basedir%\top1000features.screens.dropped.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top1000features.screens.dropped.large.html F:\ICM_Highest_Rated\Screenshots --title "Dropped from Top 1000 Feature films"

python csv_to_html.py %basedir%\top1001-2000features.raw.csv --outhtmltable %basedir%\top1001-2000features.html ^
--outhtmlthumbs %basedir%\top1001-2000features.screens.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top1001-2000features.screens.large.html F:\ICM_Highest_Rated\Screenshots --title "Top 1001-2000 Feature films"
python csv_to_html.py %basedir%\top1001-2000features.new.raw.csv --outhtmltable %basedir%\top1001-2000features.new.html ^
--outhtmlthumbs %basedir%\top1001-2000features.screens.new.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top1001-2000features.screens.new.large.html F:\ICM_Highest_Rated\Screenshots --title "New in Top 1001-2000 Feature films"
python csv_to_html.py %basedir%\top1001-2000features.dropped.raw.csv --outhtmltable %basedir%\top1001-2000features.dropped.html ^
--outhtmlthumbs %basedir%\top1001-2000features.screens.dropped.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top1001-2000features.screens.dropped.large.html F:\ICM_Highest_Rated\Screenshots --title "Dropped from Top 1001-2000 Feature films"

python csv_to_html.py %basedir%\bottom100features.raw.csv --outhtmltable %basedir%\bottom100features.html ^
--outhtmlthumbs %basedir%\bottom100features.screens.html F:\ICM_Highest_Rated\Screenshots_thumbs --title "Bottom 100 Feature films"
python csv_to_html.py %basedir%\bottom100features.new.raw.csv --outhtmltable %basedir%\bottom100features.new.html ^
--outhtmlthumbs %basedir%\bottom100features.screens.new.html F:\ICM_Highest_Rated\Screenshots_thumbs --title "New in Bottom 100 Feature films"
python csv_to_html.py %basedir%\bottom100features.dropped.raw.csv --outhtmltable %basedir%\bottom100features.dropped.html ^
--outhtmlthumbs %basedir%\bottom100features.screens.dropped.html F:\ICM_Highest_Rated\Screenshots_thumbs --title "Dropped from Bottom 100 Feature films"

python csv_to_html.py %basedir%\top200docus.raw.csv --outhtmltable %basedir%\top200docus.html ^
--outhtmlthumbs %basedir%\top200docus.screens.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top200docus.screens.large.html F:\ICM_Highest_Rated\Screenshots --title "Top 200 Documentaries"
python csv_to_html.py %basedir%\top200docus.new.raw.csv --outhtmltable %basedir%\top200docus.new.html ^
--outhtmlthumbs %basedir%\top200docus.screens.new.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top200docus.screens.new.large.html F:\ICM_Highest_Rated\Screenshots --title "New in Top 200 Documentaries"
python csv_to_html.py %basedir%\top200docus.dropped.raw.csv --outhtmltable %basedir%\top200docus.dropped.html ^
--outhtmlthumbs %basedir%\top200docus.screens.dropped.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top200docus.screens.dropped.large.html F:\ICM_Highest_Rated\Screenshots --title "Dropped from Top 200 Documentaries"

python csv_to_html.py %basedir%\top200shorts.raw.csv --outhtmltable %basedir%\top200shorts.html ^
--outhtmlthumbs %basedir%\top200shorts.screens.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top200shorts.screens.large.html F:\ICM_Highest_Rated\Screenshots --title "Top 200 Short films"
python csv_to_html.py %basedir%\top200shorts.new.raw.csv --outhtmltable %basedir%\top200shorts.new.html ^
--outhtmlthumbs %basedir%\top200shorts.screens.new.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top200shorts.screens.new.large.html F:\ICM_Highest_Rated\Screenshots --title "New in Top 200 Short films"
python csv_to_html.py %basedir%\top200shorts.dropped.raw.csv --outhtmltable %basedir%\top200shorts.dropped.html ^
--outhtmlthumbs %basedir%\top200shorts.screens.dropped.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top200shorts.screens.dropped.large.html F:\ICM_Highest_Rated\Screenshots --title "Dropped from Top 200 Short films"

python csv_to_html.py %basedir%\2votes.raw.csv --outhtmltable %basedir%\2votes.html ^
--outhtmlthumbs %basedir%\top200obscure.screens.html F:\ICM_Highest_Rated\Screenshots_thumbs ^
--outhtmllargeimages %basedir%\top200obscure.screens.large.html F:\ICM_Highest_Rated\Screenshots --title "Top 200 Obscure Feature films - 2-4 votes"

python createindex.py %csvlistdir% %basedir%\index.html

ECHO Done.
