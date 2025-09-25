#!/usr/bin/env python3

import numpy as np
import sys

def compress(uncompressed):
    dict_size = 256
    dictionary = dict((chr(i), i) for i in range(dict_size))
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
    return result

def uncompress(compressed):
    dict_size = 256
    dictionary = dict((i, chr(i)) for i in range(dict_size))
    result = []
    
    if not compressed:
        return ""
    
    # Initialize with first code
    w = chr(compressed[0])
    result.append(w)
    
    for code in compressed[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            # Special case: code not yet in dictionary
            entry = w + w[0]
        else:
            raise ValueError(f"Invalid compressed code: {code}")
        
        result.append(entry)
        
        # Add new entry to dictionary
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        
        w = entry
    
    return ''.join(result)

def main() -> int:
	# Image generation
    height, width = 100, 100
    image = np.zeros((height, width), dtype=np.uint8)
    image[20:80, 20:80] = 200
    image[40:60, 40:60] = 100
    flat_image = image.flatten()
    uncompressed = ''.join(chr(p) for p in flat_image)  # As bytes
    print(f"Approximate size without compression: {len(uncompressed)} bits")

    compressed_codes = compress(uncompressed)
    num_codes = len(compressed_codes)
    max_code = max(compressed_codes)
    bits_needed = max(9, (max_code.bit_length()))
    approx_size = (num_codes * bits_needed) // 8 + ((num_codes * bits_needed) % 8 > 0)

    print(f"Number of codes: {num_codes}")
    print(f"Approximate size with compression: {approx_size} bits")

    # Test decompression
    decompressed = uncompress(compressed_codes)
    print(f"Compression/decompression successful: {uncompressed == decompressed}")
    
    return 

if __name__ == "__main__":
    sys.exit(main())
