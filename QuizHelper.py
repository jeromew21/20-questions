import sys

def safe_input(s):
    try:
        r = input(s)
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")
        sys.exit()
    return r

def ask(question, valid_responses=('yes', 'no')):
    options = f"[{'/'.join(valid_responses)}]"
    print(question)
    while True:
        i = safe_input(f"Your answer {options}? ").lower()
        if not i:
            print(f"Please enter a response. The question is: {question}")
            continue
        for r in valid_responses:
            if i == r or i[0] == r:
                print()
                return r
        print("Did not understand that.")

def yield_questions():
    with open("questions.txt", "r") as f:
        line = f.readline()
        while line:
            yield line.strip()
            line = f.readline()

def cap_words(s):
    return ' '.join([word.capitalize() for word in s.split(" ")])

def nonempty_input(s):
    while True:
        res = safe_input(s)
        if res:
            return res

def combine_answers(*args):
    if len(args) == 2:
        if args[0] == args[1]:
            return args[0]
        if args[0] == "yes" and args[1] == "no" or args[1] == "yes" and args[0] == "no":
            return "sometimes"
        return args[0] + args[1]