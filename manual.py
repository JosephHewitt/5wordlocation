import map
import sys

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

#map.to_words(lat,lon) will return a string of five words separated by spaces
#map.to_coords(string) will turn the previously returned string back into coordinates.

args = ' '.join(sys.argv[1:])
if args.count(' ') > 1:
    try:
        coords = map.to_coords(args)
    except ValueError:
        print("One or more of those words is invalid, try again")
        exit()
    except IndexError:
        print("Incorrect number of words.")
        exit()

    if not coords:
        print("This group of words causes a checksum error; at least one of the words must be incorrect.")
        exit()

    print("%s matches %s" %(args,coords))

else:
    args = args.replace(',',' ').replace('  ',' ')
    lat,lon = args.split(' ')
    
    words = map.to_words(lat, lon)
    print("Your five words -->  %s" %(words))