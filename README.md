# Encoding

This repository contains the implementation of an encoder and decoder that uses the [LZ78 encoding method](https://de.wikipedia.org/wiki/LZ78) and encodes single characters using [UTF8](https://de.wikipedia.org/wiki/UTF-8). UTF8 encodings are assumed to be valid, invalid encodings may cause the decoding to fail.

## Usage

`python encoder [-h] [-d] [-v] input_path output_path`

positional arguments:  
- input_path: path to input file  
- output_path: path to output file  

options:  
- -h, --help: show this help message and exit  
- -v, --verbose: write results to std::out as well  
- -d, --decode: switch from Encoding mode (default) to Decoding mode. 

## Examples

The directory _examples_ contains several example input texts as well as their encodings and the decoding results. Note that the encoding/decoding output file specified under *output_path* must already exist, and by calling the encoder its content will be overwritten.
