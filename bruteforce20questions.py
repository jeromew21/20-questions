import csv
import numpy as np
from QuizHelper import *

DATA_FILENAME = "tree20_data.csv"

lookup = {
    '': 0,
    'yes': 1,
    'no': -1,
    'sometimes': 0,
}

def convert_from_answer(a):
    return lookup.get(a, -1)

def get_and_convert_data(filename=DATA_FILENAME):
    result = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            result.append(row)
    questions, answers = result[0][1:], result[1:]
    arrays = [(res[0], np.array([convert_from_answer(a) for a in res[1:]])) for res in answers]
    return questions, arrays

questions, data = get_and_convert_data()

def diff(arr1, arr2):
    d = arr1 - arr2
    return sum(d*d)

def ordered_by_diff(pairs, input_arr):
    #Mask each pair to only questions answered in input_arr
    masked_pairs = [(label, np.copy(p)) for label, p in pairs]
    for pair in masked_pairs:
        for i in range(len(input_arr)):
            if input_arr[i] == 0:
                pair[1][i] = 0
    triples = [(label, arr, diff(arr, input_arr)) for label, arr in masked_pairs]
    return [(k[0], k[2]) for k in sorted(triples, key=lambda t: t[2])]

def get_input_arr():
    result = np.array([0 for i in questions])
    diffs = ordered_by_diff(data, result)

    print(f"There are {len(questions)} questions.")
    for index, question in enumerate(questions):
        ans = ask(question)
        result[index] = lookup.get(ans, -1)
        diffs = ordered_by_diff(data, result)
        print(f"Current guess: {diffs[0][0]}")
        
get_input_arr()
