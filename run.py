#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from bean import bloom
from exps.pipelines import ErrorCounterOneFile
import math
import random
import os


def run_error_counter(expected_rate, payload_length, copy_number, stdev, hash_function_type, read_depth, root_path,
                      insertion_rate=0.00075, deletion_rate=0.00075, substitution_rate=0.0015, seed=30,
                      actual_dnas=False, digital_count=None, training_dnas=None, checking_dnas=None, training_name=None,
                      checking_name=None, filter_size=0, hash_size=0, counting_type=False, record_coverage=False, 
                      verbose=False):

    bloom_filter = bloom.Filter(inform_count=(digital_count if not actual_dnas else len(training_dnas)),
                                hash_function_type=hash_function_type)
    error_counter = ErrorCounterOneFile(bloom_filter, expected_rate, payload_length, digital_count, copy_number, stdev,
                                        read_depth, root_path, insertion_rate, deletion_rate, substitution_rate, seed,
                                        actual_dnas, training_dnas, checking_dnas, training_name, checking_name,
                                        filter_size, hash_size, counting_type, record_coverage, verbose)
    error_counter.run()
    error_counter.show_results()


def dna_file(dna_file_path, extract_count=None, seed=None):
    digital_dnas = []
    with open(dna_file_path, 'r') as file:
        lines = file.readlines()
        if extract_count:
            if seed:
                random.seed(seed)
            extract_lines = random.sample(lines, extract_count)
            for line in extract_lines:
                digital_dnas.append(line[:-1])
        else:
            for line in lines:
                digital_dnas.append(line[:-1])

    return digital_dnas


if __name__ == '__main__':
    need_counting_filter = False
    need_verbose = False
    need_coverage = False
    root_path = "./outputs/"

    yycpdf_dna = dna_file('./files/yyc_pdf.dna', extract_count=100000, seed=30)
    training_name = 'yycpdf-' + str(len(yycpdf_dna))
    checking_name = 'yycpdf-' + str(len(yycpdf_dna))

    # for hash in [['BKDR'],['AP'],['DJB'],['JS'],['SDBM'],['Murmur'],['Lookup3'],['RS']]:
    for hash in [['FNV1a']]:
        for depth in [1000]:
            print('depth = ', str(depth))
            run_error_counter(0.001, 120, 1000, 100, hash, int(depth), root_path, seed=30, actual_dnas=True,
                              training_dnas=yycpdf_dna, checking_dnas=yycpdf_dna,
                              training_name=training_name, checking_name=checking_name,
                              counting_type=need_counting_filter, record_coverage=need_coverage, verbose=need_verbose)

        for depth in list(range(10, 1000, 10)):
            print('depth = ', str(depth))
            run_error_counter(0.001, 120, 1000, 100, hash, int(depth), root_path, seed=30, actual_dnas=True,
                              training_dnas=yycpdf_dna, checking_dnas=yycpdf_dna,
                              training_name=training_name, checking_name=checking_name,
                              counting_type=need_counting_filter, record_coverage=need_coverage, verbose=need_verbose)
