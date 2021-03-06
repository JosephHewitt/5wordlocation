# 5wordlocation
Turn any location on Earth into 5 words. This was created in around 8 hours as a programming challenge. This system gives approximately 11 meters of precision and uses a checksum so many mistakes will be detected.

This project doesn't have an "official" name yet and probably never will. Feel free to fork it and make it something great.

## Usage
`map.py` can be called directly and should print 10 coordinates and their 5-word counterparts as an example.

You may use `import map` in your own Python script to get the following two functions:

`map.to_words(lat,lon)` - convert a latitude and longitude into 5 words. Returns a single string with the words separated by spaces.

`map.to_coords(string)` - convert a string generated by the previous function into a coordinates tuple and a boolean to indicate if the checksum passed or not.

This repository also includes `manual.py` which allows you to do lookups on the command line. It accepts either 5 words or a latitude and longitude. For example:

`./manual.py 40.6892, -74.0445` returns `Your five words -->  cent limit frame choice install`

`./manual.py cent limit frame choice install` returns `cent limit frame choice install matches (40.6892, -74.0445), Good checksum=True`

These scripts have only been tested with Python 3.9.4, older Python versions may not work correctly.

## Details

Latitude/Longitude coordinates are split up into 4 numbers which are used as indices for a word list. The integer part of the latitude in addition to one digit after the decimal make up the first word; the same thing is done for longitude to make the second word. This means that the first 2 words alone represent coordinates with a single decimal digit of precision (eg, around 11km of precision).

The second two words are generated in a similar way using digits 2,3, and 4 (after the decimal). This means with 4 words the precision is around 11 meters. The fifth word is a checksum of the previous 4 and doesn't alter the precision.

## Reliability?

Included in this repository is `tests.py`. If you run it, coordinates will be randomly generated, turned into words, and turned back into coordinates again. The script will only stop running if a mismatch is found. So far, no mismatches have been found.

This system should be reliable but the word list may not be. Some "problematic" words might remain despite me removing some obvious issues. For example, both "color" and "colour" *were* in the list; this would have made it hard to communicate the 5 words using spoken words. I expect some pairs of words like these may still remain. Words which are pronounced the same (eg, there and their) **may** remain; you need to carefully check the word list before using this system for anything serious.

I'm not aware of any bugs which cause bad data to be returned unless bad data was given as an input. Assuming properly formatted strings/coordinates are provided, the return values should always be consistent.

## Wordlist

The wordlist is stored at `words.txt` and can be modified freely. You can't decode words generated with different wordlists; this means all changes you make will prevent you from decoding old strings reliably.

As long as the wordlist has 3700+ **unique** words, everything should work correctly.