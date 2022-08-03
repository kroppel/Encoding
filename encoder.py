import os
import io
from numpy import uint8, uint16, uint32, arange
import argparse

class encoder_lz78():
    def __init__(self, dictionary_table_length, alphabet):
        self.dictionary_table_length = dictionary_table_length
        self.alphabet = alphabet

    def encode(self, text):
        index = 1
        encoding = []
        prefix = ""
        dictionary_table = {}

        for symbol in text:
            if prefix + symbol in dictionary_table.keys():
                prefix += symbol            
            else:
                if prefix == "":
                    encoding.append((0, symbol))
                    if index < self.dictionary_table_length:
                        dictionary_table[symbol] = index
                    index += 1
                else: 
                    encoding.append((dictionary_table[prefix],symbol))
                    if index < self.dictionary_table_length:
                        dictionary_table[prefix+symbol] = index
                    index += 1
                    prefix = ""

        return encoding

    def decode(self, encoding):
        encoding_index = 0
        index = 1
        decoded_text = ""
        prefix = ""
        dictionary_table = {}

        while encoding_index < len(encoding):
            decoded_index = uint8(encoding[encoding_index])
            utf8_encoded_symbol = encoding[encoding_index+1]

            if utf8_encoded_symbol < 128:
                decoded_symbol = bytes(encoding[encoding_index+1:encoding_index+2]).decode("utf8")
                encoding_index += 2
            elif utf8_encoded_symbol > 193 and utf8_encoded_symbol < 224:
                decoded_symbol = bytes(encoding[encoding_index+1:encoding_index+3]).decode("utf8")
                encoding_index += 3
            elif utf8_encoded_symbol > 223 and utf8_encoded_symbol < 240:
                decoded_symbol = bytes(encoding[encoding_index+1:encoding_index+4]).decode("utf8")
                encoding_index += 4
            elif utf8_encoded_symbol > 239 and utf8_encoded_symbol < 245:
                decoded_symbol = bytes(encoding[encoding_index+1:encoding_index+5]).decode("utf8")
                encoding_index += 5
            else:
                print("UTF8 Code ungültig")
                encoding_index += 2

            if decoded_index == 0:
                if index < self.dictionary_table_length:
                    dictionary_table[index] = decoded_symbol
                decoded_text += decoded_symbol  
            else:
                decoded_text += dictionary_table[decoded_index]
                decoded_text += decoded_symbol
                if index < self.dictionary_table_length:
                    dictionary_table[index] = dictionary_table[decoded_index]+decoded_symbol

            index += 1

        return decoded_text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="path to input file")
    parser.add_argument("output_path", help="path to output file")
    parser.add_argument("-v", "--verbose", help="write results to std::out as well", action="store_true")
    parser.add_argument("-d", "--decode", help="switch from Encoding mode (default) to Decoding mode.", action="store_true")
    args = parser.parse_args()

    e = encoder_lz78(256, "")

    if not args.decode:
        if args.verbose:
            print("Starting encoding.")

        # Read input and encode
        file = open(args.input_path) 
        text = file.read()
        encoding = e.encode(text)
        file.close()

        # Write encoding to file
        file = open(args.output_path, "wb")
        for code in encoding:
            file.write(uint8(code[0]))
            file.write(code[1].encode("utf8"))
        file.close()

        if args.verbose:
            print("Encoding finished.")

    else:
        if args.verbose:
            print("Starting decoding.")

        # Read in encoding and decode
        file = open(args.input_path, "rb")
        encoding_bytes = file.read()
        decoded_text = e.decode(encoding_bytes)
        file.close()

        # Write decoded text to file
        file = open(args.output_path, "w")
        file.write(decoded_text)
        file.close()

        if args.verbose:
            print("Decoding finished with output:\n")

        if args.verbose:
            print(decoded_text)

if __name__ == "__main__":
    main()