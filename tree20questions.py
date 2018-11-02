#Simple tree based quizzing program
#Pros: Dead simple implementation
#Cons: Tree unbalanced, always asks same questions, not limited to 20, limited to yes/no for accuracy
import os
import pickle

from QuizHelper import *

class QuizTree:
    def __init__(self, label, children=None):
        self.parent = None
        self.label = label
        if children is None:
            children = []
        if len(children) > 2:
            raise Exception("Too many children")
        self.children = children
        for child in children:
            child.parent = self

    @property
    def yes(self):
        return self.children[0]
    
    @property
    def no(self):
        return self.children[1]
    
    @property
    def is_leaf(self):
        return len(self.children) != 2

    def get_answer_node(self, count=0):
        if self.is_leaf:
            return self, count
        else:
            answer = ask(self.label)
            if answer == "yes":
                return self.yes.get_answer_node(count + 1)
            else:
                return self.no.get_answer_node(count + 1)
        
    def set_children(self, children):
        self.children = children
        for child in children:
            child.parent = self
    
    def already_asked(self, question):
        if question == self.label:
            return True
        if self.parent is None:
            return False
        return self.parent.already_asked(question)
    
    def all_questions(self):
        if self.is_leaf:
            return []
        return [self.label] +  self.yes.all_questions() + self.no.all_questions()
    
    def leaves(self):
        if self.is_leaf:
            return [self]
        else:
            return self.yes.leaves() + self.no.leaves()
    
    def unique_animals(self):
        return list(set([node.label for node in self.leaves()]))

    def data_dump(self):
        """ Returns all the animals in tree as columns """
        #first traverse for set of all questions
        questions = set(self.all_questions())
        print(questions)

def starter_tree():
    tree = QuizTree("Does it have four legs?", [
        QuizTree("Does it live on land?", [
            QuizTree("Dog"),
            QuizTree("Dolphin")
        ]),
        QuizTree("Is it a carnivore?", [
            QuizTree("Bear"),
            QuizTree("Koala")
        ] )
    ])
    return tree

def play_game(tree):
    print(len(tree.unique_animals()), "animals")
    questions = yield_questions()
    guess, count = tree.get_answer_node()
    print(f"I guess: {guess.label}.")
    q = ask("Is this your animal?")
    #if not, then we need to update the tree
    #enlist a new question
    if q == "yes":
        print(f"Yay! It took me {count} questions.")
        return
    else:
        new_name = cap_words(nonempty_input("What is the name of your animal? ").lower())
        old_name = guess.label
        print()
        ans_old = ans_new = None
        while ans_old == ans_new:
            try:
                new_question = next(questions)
                while guess.already_asked(new_question): #see if question is already in ancestry of guess node
                    new_question = next(questions)
            except:
                new_question = nonempty_input(
                    f"We are out of questions! Please enter a question where the answers are DIFFERENT for {new_name.upper()} and {old_name.upper()}"
                )
                with open("questions.txt", "a") as f:
                    f.write(new_question + "\n")
            ans_new = ask(f"Answer for {new_name.upper()}: {new_question}")
            ans_old = ask(f"Answer for {old_name.upper()}: {new_question}")
        guess.label = new_question #Update node label to question       
        if ans_new == "yes":
            guess.set_children([
                QuizTree(new_name), #yes
                QuizTree(old_name),
            ])
        else:
            guess.set_children([
                QuizTree(old_name),
                QuizTree(new_name), #no
            ])
        print("Gotcha, thanks!")

if __name__ == "__main__":
    pickled_filename = "tree20questions.dat"
    try:
        with open(pickled_filename, "rb") as f:
            tree = pickle.load(f)
    except Exception as e:
        tree = starter_tree()
        with open(pickled_filename, "wb") as f:
            pickle.dump(tree, f)
    play_game(tree)
    with open(pickled_filename, "wb") as f:
        pickle.dump(tree, f)