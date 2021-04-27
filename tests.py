import map
import random

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

def random_coord():
    #Generate random coordinates.
    lat = random.random() * 180 - 90
    lon = random.random() * 360 - 180

    return lat,lon

def run_test(coords, causefail=False):
    #Turn coords into words, then back into coords. Return True if they match.
    #causefail will deliberately cause a test failure.

    lat = coords[0]
    lon = coords[1]

    if causefail:
        lat += 0.001

    words = map.to_words(lat, lon)
    coords_from_words = map.to_coords(words)
    checksum_pass = coords_from_words[1]
    coords_from_words = coords_from_words[0]

    if not checksum_pass:
        print("Test FAILED: Bad checksum. in=%s, out=%s, words=%s" %(coords, coords_from_words,words))
        return False

    coords = (round(coords[0],4), round(coords[1],4))
    
    if float(coords[0]) == float(coords_from_words[0]) and float(coords[1]) == float(coords_from_words[1]):
        print("Test PASSED: %s is %s" %(coords,words))
        return True

    print("Test FAILED: in=%s, out=%s, words=%s" %(coords, coords_from_words,words))
    return False

def random_test():
    #Generate random coordinates and test them. Only stop when a test fails.
    pass_count = 0
    while True:
        coords = random_coord()
        result = run_test(coords)

        if not result:
            print("A test failed. Stopping now.")
            break
        pass_count += 1
        
    print("%s tests passed" %(pass_count))


def all_test():
    #This will generate every possible coordinate and test it.
    #No optimisation (or threads) has been implemented so this will take months.
    pass_count = 0

    lat = -90
    lon = -180
    while True:
        lat += 0.0001
        if lat > 90:
            lat = -90
            lon += 0.0001
        if lon > 180:
            print("It seems like we're done")
            break

        coords = (round(lat,4),round(lon,4))
        result = run_test(coords)

        if not result:
            print("A test failed. Stopping now.")
            break

    print("%s tests passed" %(pass_count))

random_test()
#all_test()