import argparse
import pandas
from library.statistics import *
from library.data import *
from library.math import *
import os

def main():
    parser = argparse.ArgumentParser(description='Attempts to decrypt mono alpha ciphers.')
    parser.add_argument('CipherFile',
                        help='The cipher file to decrypt.')
    parser.add_argument("-s", "--spaces", action='store_true',
                        help="Counts spaces as a valid cipher character instead of ignoring them."
                             "", required=False)
    parser.add_argument("-p", "--punctuation", action='store_true',
                        help="Counts punctuation as valid cipher characters instead of ignoring them."
                             "", required=False)

    args = parser.parse_args()

    cipherfile = args.CipherFile

    with open(cipherfile, 'r') as cf:
        ciphertext = cf.read()

    totalletters, cipherlettercounts, cipherletterprobs = build_monogram_probabilities(ciphertext,
                                                                                       args.spaces,
                                                                                       args.punctuation)
    totaldigrams, cipherdigramcounts, cipherdigramprobs = build_digram_probabilities(ciphertext,
                                                                                     args.spaces,
                                                                                     args.punctuation)
    # totaltrigrams, ciphertrigramcounts, ciphertrigramprobs = build_trigram_probabilities(ciphertext,
    #                                                                                      args.spaces,
    #                                                                                      args.punctuation)

    cipherdigrammatrix = calculatedprob_to_matrix(cipherdigramprobs)

    ngram1 = pandas.read_csv(os.path.join('data','ngrams1.csv'), keep_default_na=False, na_values=['_'])
    ngram2 = pandas.read_csv(os.path.join('data','ngrams2.csv'), keep_default_na=False, na_values=['_'])
    ngram3 = pandas.read_csv(os.path.join('data','ngrams3.csv'), keep_default_na=False, na_values=['_'])

    ngram1 = ngram1[['1-gram','*/*']]
    ngram1sorted = ngram1_to_ordered_dict(ngram1)

    print(ngram1sorted)
    print(cipherletterprobs)

    ngram2 = ngram2[['2-gram','*/*']]
    ngram2matrix = ngram2_data_to_matrix(ngram2)

    error = ngram2_matrix_error(ngram2matrix, cipherdigrammatrix)
    print(error)

    print("Cipher Text:")
    print("")
    print(ciphertext)

    ciphertoplain = fit_characters_sorted_probabilities(ngram1sorted, cipherletterprobs)

    print(ciphertoplain)

    print("Plain Text: \n")

    plaintext = ""
    for c in ciphertext:
       if c in ciphertoplain:
           plaintext += ciphertoplain[c]
       else:
           plaintext += c

    print(plaintext)

    currtotaldigrams, currplaindigramcounts, currplaindigramprobs = build_digram_probabilities(plaintext,
                                                                                               args.spaces,
                                                                                               args.punctuation)
    currplaindigrammatrix = calculatedprob_to_matrix(currplaindigramprobs)

    error = ngram2_matrix_error(ngram2matrix, currplaindigrammatrix)
    print(error)


if __name__ == "__main__":
    main()
