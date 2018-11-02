def ask(question, valid_responses=('yes', 'no')):
    options = f"[{'/'.join(valid_responses)}]"
    print(question)
    while True:
        i = input(f"Your answer {options}? ").lower()
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

def nonempty_input(s):
    while True:
        res = input(s)
        if res:
            return res