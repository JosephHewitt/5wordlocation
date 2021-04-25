#!/usr/bin/env python3

"""
Copyright 2021 Joseph Hewitt (@jhewitt_net)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

#to_words(lat,lon) will return a string of five words separated by spaces
#to_coords(string) will turn the previously returned string back into coordinates.

import hashlib
import logging

words = []

with open('words.txt', 'r') as filereader:
	for line in filereader:
		line = line.strip().lower()
		if line.startswith("#"): continue
		words.append(line.strip().lower())

logging.debug("%s words loaded" % len(words))

def make_checksum(tochecksum):
	#This checksum is used as an index to determine the 5th word; this means it can't be higher than len(words).

	tochecksum = tochecksum.strip()
	fullhash = hashlib.md5(tochecksum.encode()).digest()
	toreturn = fullhash[0] + fullhash[1] * 256 & -1+2**11

	logging.debug("Checksum %s was generated" %(toreturn))

	#The return value is capped to len(words)-1 to ensure it will always work as a word index directly.
	if toreturn >= len(words):
		logging.warn("A checksum higher than the maximum(%s) was generated and capped" %(len(words)))
		return len(words)-1
	return toreturn

def to_coords(wordstr):
	wordlist = wordstr.lower().strip().split(' ')

	latm = str(words.index(wordlist[0])).rjust(4,'0')
	lonm = str(words.index(wordlist[1])).rjust(4,'0')

	latfd = latm[-1:]
	lonfd = lonm[-1:]

	latm = int(latm[:-1])
	lonm = int(lonm[:-1])

	lats = str(words.index(wordlist[2])).rjust(3,'0')
	lons = str(words.index(wordlist[3])).rjust(3,'0')

	lats = (latfd + lats)
	lons = (lonfd + lons)

	lat_out = str(latm) + '.' + str(lats)
	lon_out = str(lonm) + '.' + str(lons)

	input_cs = -1
	missing_checksum = False
	try:
		input_cs = int(words.index(wordlist[4]))
	except:
		logging.warn("A checksum word was not provided")
		missing_checksum = True

	cs = make_checksum(' '.join(wordlist[:-1]))

	lat_out = round(float(lat_out) - 90,4)
	lon_out = round(float(lon_out) - 180,4)

	if input_cs == cs:
		return (lat_out, lon_out)

	logging.error("Checksum mismatch: %s != %s. Coordinates using just 4 words = %s,%s" %(cs,input_cs,lat_out,lon_out))
	return False


def to_words(lat, lon):
	#This makes all coordinates positive. This needs to be subtracted again later.
	lat = str(round(float(lat) + 90,4))
	lon = str(round(float(lon) + 180,4))

	if '.' not in lat:
		lat += '.0'
	if '.' not in lon:
		lon += '.0'

	lat = lat.ljust(10,'0')
	lon = lon.ljust(10,'0')

	latm = lat.split('.')[0]
	lonm = lon.split('.')[0]

	latm += lat.split('.')[1][:1]
	lonm += lon.split('.')[1][:1]

	output_words = words[int(latm)] + ' ' + words[int(lonm)] + ' '

	lats = int(lat.split('.')[1][1:4])
	lons = int(lon.split('.')[1][1:4])

	output_words += words[lats] + ' ' + words[lons] + ' '

	try:
		latt = lat.split('.')[1][3:4]
	except:
		latt = '0'

	try:
		lont = lon.split('.')[1][3:4]
	except:
		lont = '0'

	cs = str(make_checksum(output_words))
	finaln = int(cs)

	output_words += words[finaln]

	return output_words

def main():
	print("This script is designed to be included in another, see tests.py and manual.py")
	if len(words) < 1000:
		print("Your word list appears to contain %s words which isn't enough. 1000 is the minimum. 4000 is recommended." %(len(words)))
		exit()
	print("Some examples of what this software can do:\n")

	interesting_coords = [
	(51.5013, -0.1419),
	(48.8583, 2.2944),
	(38.8976, -77.0365),
	(37.3317, -122.03),
	(27.1751, 78.0421),
	(41.8901, 12.4922),
	(-33.8567, 151.2152),
	(-22.9519, -43.2104),
	(29.9791, 31.1342),
	(53.8158, -3.0552)
	]
	for coord in interesting_coords:
		words_from_coords = to_words(coord[0], coord[1])
		print("%s, %s ---> %s" %(coord[0], coord[1], words_from_coords))

	print("\nAny location on Earth can be represented as 4 words; the 5th word is optional and verifies you didn't make a mistake.")


if __name__ == "__main__":
    main()