import argparse
import time
import random
from copy import deepcopy
from collections import defaultdict
from itertools import combinations

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, default='2of12_5letter.txt', help='name of word-list file to read from')
parser.add_argument('--wsize', type=int, default=5, help='length of words to play Wordle with')
parser.add_argument('--test', '-t', required=False, action='store_true', help='run a test on every word in the file')
parser.add_argument('--profile', '-p', required=False, action='count', default= 0, help='profile the performance of the script')
parser.add_argument('--wordtest', '-wt', required=False, action='store_true', help='simulate a Wordle for a single word')
args = parser.parse_args()

WORD_SIZE = args.wsize
filename = args.file

if args.test:
    print(f"Running test on file {filename}")

letterdict = defaultdict(lambda:defaultdict(int))
locationmap = list()
lettercombo_list = dict()
for i in range(WORD_SIZE):
    locationmap.append(defaultdict(int))
    lettercombo_list[i+1] = set()
wordlist = 0
working_wordlist = 0
wordcount = 0



cur_word = ['', '', '', '', ''] #letters we know the place of
non_word = [list(), list(), list(), list(), list()] #letters we know do not have the correct place
known_letters = set() #letters we don't know the place of
non_letters = set() #letters that aren't in there
working_combo_list = dict() #working list of ONLY letter combos that are still valid

#reset all the variables we use for a new word
def reset_word():
    global cur_word
    global non_word
    global known_letters
    global non_letters
    global working_combo_list
    global working_wordlist
    
    cur_word = ['', '', '', '', '']
    non_word = [list(), list(), list(), list(), list()] 
    known_letters = set()
    non_letters = set() 
    working_combo_list = deepcopy(lettercombo_list)
    working_wordlist = deepcopy(wordlist)
    
    

#build a dictionary of nested dictionaries
def build_lettercount():
    global letterdict
    global wordlist
    global locationmap
    global lettercombo_list
    
    wordcount = 0
    
    for word in wordlist:    
        wordcount += 1
        letters = set(word.strip())
        #print(f"letters size: {len(letters)}")
        lettercombo_list[len(letters)].add(frozenset(letters))
        for letter in letters:
            for co_letter in letters:
                letterdict[letter.lower()][co_letter.lower()] += 1
        for i in range(WORD_SIZE):
            locationmap[i][word[i]] += 1
            
    """for entry in locationmap:
        print(f"{entry}")
    for entry in lettercombo_list:
        print(f"{entry}: {lettercombo_list[entry]}")"""
    return wordcount
    

#get a count of 'roughly how many words have this combination of letters'
def get_lettercount(letter_list):
    global letterdict
    if not letter_list:
        return 0
    max_values = list()
    #print(f"get_lettercount: {letter_list}")
    
    for letter in letter_list:
        l_dict = letterdict[letter]
        #print(f"letter: {letter}, l_dict: {l_dict}")
        cur_values = list()
        for l in l_dict:
            #print(f"l: {l}")
            if l in letter_list:
                cur_values.append(l_dict[l])
                #print(f"appended {l_dict[l]}")
        max_values.append(min(cur_values))
    #print(f"get_lettercount: {max(max_values)}")
    return max(max_values)
    
def compare_answer(guess, solution):
    global cur_word
    global non_word
    global non_letters
    global known_letters
    
    if not args.test:
        print(f"Comparing guess '{guess}' to solution '{solution}'")
    
    for l in guess:
        if (l in solution) and (l not in known_letters):
            known_letters.add(l)
            #print(f"Added letter '{l}' to known_letters")
        if (l not in solution) and (l not in non_letters):
            non_letters.add(l)
            #print(f"Added letter '{l}' to non_letters")
    for i in range(WORD_SIZE):
        if guess[i] == solution[i]:
            cur_word[i] = guess[i]
        else:
            non_word[i].append(guess[i])
            
    if not args.test:
        print(f"current known word: {cur_word}")
        print(f"current non_word: {non_word}")
        print(f"current known_letters: {known_letters}")
        print(f"current non_letters: {non_letters}")
    trim_working_wordlist()
    if(guess == solution):
        return True
    return False
    
def user_guess(guess):
    global cur_word
    global non_word
    global non_letters
    global known_letters
    
    
    for n in range(WORD_SIZE):
        char = guess[n]
        print(f"Character {char}:")
        isinword = ""
        while not (isinword.lower() in ["y", "n"]):
            print("Is this character in the word? (Y/N)")
            isinword = input()
        isinword = (isinword.lower() == "y")
        if isinword:
            isrightplace = ""
            while not (isrightplace.lower() in ["y", "n"]):
                print("Is this character in the right place? (Y/N)")
                isrightplace = input()
            if (isrightplace.lower() == "y"):
                cur_word[n] = char
            else:
                non_word[n].append(char)
            known_letters.add(char)
            print(f"Added {char} to known letters!")
        else:
            non_letters.add(char)
            print(f"Added {char} to non-letters!")
    print(f"Current word: {cur_word}")
    
        

#check if the word fits the current letter list, and if it can be a possible answer
def check_valid_word(word, letter_list):
    global cur_word
    global non_word

    if set(word) != set(letter_list):
        return False
    else:
        word_correct = True
        for i in range(WORD_SIZE):
            if (not (cur_word[i] == '') and not (cur_word[i] == word[i])) or (word[i] in non_word[i]):
                word_correct = False
        return word_correct
        
def check_can_be_answer(word):
    global cur_word
    global non_word
    word_correct = True
    for i in range(WORD_SIZE):
        if (not (cur_word[i] == '') and not (cur_word[i] == word[i])) or (word[i] in non_word[i]):
            word_correct = False
    return word_correct
                

    
def trim_working_wordlist():
    global working_wordlist
    
    if args.profile >= 3: 
        print(f"Trimming working wordlist from {len(working_wordlist)}...")
        trimtime_start = time.perf_counter()
        trimcount = len(working_wordlist)
    new_working_wordlist = [word for word in working_wordlist if check_can_be_answer(word)]
    working_wordlist = new_working_wordlist
    """for index, word in enumerate(working_wordlist):
        if not check_can_be_answer(word):
            del working_wordlist[index]
            if args.profile >= 3:
                trimcount += 1"""
    if args.profile >= 3:
        trimtime = time.perf_counter() - trimtime_start
        print(f"Trim complete, {trimcount - len(new_working_wordlist)} words trimmed, time: {trimtime}s")
    
#get a list of all words with this letter list that can possibly solve the wordle, and also remove all impossible guesses from the working wordlist
def get_all_valid_words(letter_list):
    global working_wordlist
    global cur_word
    global non_word
    
    words = list()
    new_working_wordlist = list()
    
    if not letter_list:
        return None
    for index, word in enumerate(working_wordlist):
        word = word.strip().lower()
        if check_can_be_answer(word):
            new_working_wordlist.append(word)
            if check_valid_word(word, letter_list): 
                words.append(word)
        elif args.profile >= 4:
                print(f"word {word} removed from wordlist, wordlist size {len(working_wordlist)}/{len(wordlist)}")
        #elif not check_can_be_answer(word): # trim down working_wordlist in real time
            #del working_wordlist[index]
            
    working_wordlist = new_working_wordlist

    return words
    
def get_word_score(word):
    score = 0
    for i in range(WORD_SIZE):
        score += locationmap[i][word[i]]
    return score
    
def get_best_word(letter_list):
    global working_wordlist
    
    max_score = 0
    best_word = ''
    for word in working_wordlist:
        word = word.strip().lower()
        if check_valid_word(word, letter_list):
            score = get_word_score(word)
            if args.profile >= 2:
                print(f"Score for word {word}: {score}")
            if score > max_score:
                best_word = word
                max_score = score
    if not args.test:
        print(f"Returning word {best_word} with score {max_score}")
    return best_word
            
#return the first word that is a valid answer to the wordle
def get_valid_word(letter_list):
    global working_wordlist
    global cur_word
    global non_word
    
    #print(f"letter_list: {letter_list}")
    
    if not letter_list:
        return None
    for index, word in enumerate(working_wordlist.copy()):
        word = word.strip().lower()
        if set(word) == set(letter_list):
            word_correct = True
            for i in range(WORD_SIZE):
                if not (cur_word[i] == '') and not (cur_word[i] == word[i]):
                    word_correct = False
                    break
                    #print(f"deleted {word} from working_wordlist ({len(working_wordlist)}/{len(wordlist)})")
                    #print(f"   non_word: {non_word}")
                    #print(f"   cur_word: {cur_word}")
                elif (word[i] in non_word[i]):
                    #print(f"Ruling out {word.strip()}")
                    word_correct = False
                    break
                    #print(f"deleted {word} from working_wordlist ({len(working_wordlist)}/{len(wordlist)})")
                    #print(f"   non_word: {non_word}")
                    #print(f"   cur_word: {cur_word}")
            if word_correct:
                return word
            #else:
                #del working_wordlist[index]
    return None
    

    
# is this a set of letters that has an associated word that can answer the wordle?
def check_valid_combo(letter_list):
    if args.profile >= 4:
        start_time = time.perf_counter()
    word = get_valid_word(letter_list)
    if args.profile >= 4:
        end_time = time.perf_counter() - start_time
        print(f"check_valid_combo time: {end_time}")
        
    if word:
        return True
    return False
   
#return a word that cuts the probability space in half
def cut_in_half():
    global cur_word
    global known_letters
    global non_letters
    global letterdict
    
    result = None
    r = WORD_SIZE + 1 #- len(known_letters)
    while (result == None):
        r = r-1
        if not args.test:
            print(f"Trying combinations of {r} letters...")
        if args.profile >= 2:
            start_time = time.perf_counter()
        result = find_halfset(r)
        if args.profile >= 2:
            end_time = time.perf_counter() - start_time
            print(f"find_halfset time: {end_time}")
    
    if args.profile >= 2:
            start_time = time.perf_counter()
    bestword = get_best_word(result)
    if args.profile >= 2:
            end_time = time.perf_counter() - start_time
            print(f"get_best_word time: {end_time}")
    
    return bestword
    #return get_valid_word(list(result.keys()))
    
#return a set of letters that cuts the current word space by ~50%
def find_halfset(r):
    global wordcount
    global letterdict
    global known_letters
    global non_letters
    global lettercombo_list
    global working_combo_list
    
    target_count = wordcount / 2
    
    closest_set = list()
    closest_count = 0
    closest_words = list()
    closest_wordscore = 0

            
    if args.profile >= 3:
        start_time = time.perf_counter()
    
    combos = []
    
    if r in working_combo_list and len(working_combo_list[r]) > 0:
        for lettercombo in working_combo_list[r].copy(): #lettercombo_list[r]:
            if lettercombo.intersection(non_letters) or known_letters.difference(lettercombo):
                working_combo_list[r].remove(lettercombo)
            else:
                combos.append(lettercombo)
                
    if args.profile >= 3:
        end_time = time.perf_counter() - start_time
        print(f"filling out combos time: {end_time}, combos size: {len(combos)}")
        
        print(f"working_combo_list size: {len(working_combo_list[r])}/{len(lettercombo_list[r])}")
            
    if args.profile >= 3 and len(combos) > 0:
        start_time = time.perf_counter()
        total_lettercount_time = 0
        total_checkvalid_time = 0
        total_checkvalid_calls = 0
        total_checkvalid_false = 0
        total_getallvalid_time = 0
        total_getallvalid_calls = 0
        
        
    for combo in combos:
        if args.profile >= 4:
            combo_time = time.perf_counter()
        
        new_set = dict()
        
        for letter in combo:
            new_set[letter] = letterdict[letter]
            
        if args.profile >= 3:
            lettercount_time_start = time.perf_counter()
        new_count = get_lettercount(new_set.keys())
        if args.profile >= 3:
            total_lettercount_time += time.perf_counter() - lettercount_time_start
            
        #case for finding two 'equal' letter sets:
        #pick the one with more words to its name
        if new_count == closest_count: 
            if args.profile >= 3:
                total_getallvalid_calls += 1
                getallvalid_time_start = time.perf_counter()
                
            new_words = get_all_valid_words(new_set.keys())
            
            if args.profile >= 3:
                total_getallvalid_time += time.perf_counter() -getallvalid_time_start
            new_wordscore = 0
            for word in new_words:
                new_wordscore += get_word_score(word)
            if new_wordscore > closest_wordscore:
                if not args.test:
                    print(f"new closest set: {new_set.keys()} with score {new_wordscore}")
                closest_wordscore = new_wordscore
                closest_words = new_words
                closest_set = new_set
        if abs(new_count - target_count) < abs(closest_count - target_count):
        
            if args.profile >= 3:
                checkvalid_time_start = time.perf_counter()
                total_checkvalid_calls += 1
            isvalid = check_valid_combo(list(new_set.keys()))
            if args.profile >= 3:
                total_checkvalid_time += time.perf_counter() - checkvalid_time_start
                
            if not isvalid:
                if args.profile >= 3:
                    total_checkvalid_false += 1
                continue
            closest_set = new_set
            closest_count = new_count
        if args.profile >= 4:
            combo_end_time = time.perf_counter() - combo_time
            print(f"analyze 1 combo time:{combo_end_time}")
                
    if args.profile >= 3 and len(combos) > 0:
        end_time = time.perf_counter() - start_time
        print(f"picking combo time: {end_time}, time per combo: {end_time/len(combos)}")
        print(f"   time spent in get_lettercount: {total_lettercount_time}")
        print(f"   time spent in check_valid_combo: {total_checkvalid_time} ({total_checkvalid_calls} calls, {total_checkvalid_false} false)")
        print(f"   time spent in get_all_valid_words: {total_getallvalid_time}, {total_getallvalid_calls} calls")
    

            
    if len(closest_set) == 0:
        if not args.test:
            print(f"No new set found!")
        return None
    if not args.test:
        print(f"Trying set: {list(closest_set.keys())} with count of {closest_count}...")
    return closest_set.keys()
    
def word_test():
    global cur_word
    global non_word
    global known_letters
    global non_letters

    print("Enter solution word:")
    solution = input()
    
    print(f"First guess (leave empty for default):")
    next_guess = input()
    if not next_guess:
        reset_word()
        next_guess = cut_in_half()

    guess_count = 0
    keep_guessing = "Y"

    while True:
        #result = cut_in_half()
        guess_count += 1
        print(f"Guess #{guess_count}: {next_guess}")
        if(compare_answer(next_guess, solution)):
            print(f"Successful guess found: {next_guess}! Number of guesses: {guess_count}")
            break
        else:
            print("Enter next guess (leave empty for auto-generated):")
            next_guess = input()
            if not next_guess:
                next_guess = cut_in_half()
        
    
def auto_test(first_guess):
    global wordcount
    global wordlist
    
    global cur_word
    global non_word
    global known_letters
    global non_letters
    
    guess_count = 0
    word_tally = 0
    
    fail_count = 0
    worst_fail = 0
    worst_words = list()
    
    total_time = 0
    for word in wordlist:
        word_tally += 1
        
        reset_word()
        
        word_guesscount = 1
        
        guess = first_guess
        if args.profile >= 2:
                print(f"Guess # {word_guesscount}: {guess}")
                
        if args.profile:
            start_time = time.perf_counter()
            
        while True:
            if(compare_answer(guess, word.strip().lower())):
                break
            
            guess = cut_in_half()
            word_guesscount += 1
            if args.profile >= 2:
                print(f"Guess # {word_guesscount}: {guess}, working wordlist: {len(working_wordlist)}/{len(wordlist)}")
        if args.profile:  
            guess_time = time.perf_counter() - start_time
            total_time += guess_time
        print(f"Word {word_tally}/{wordcount}: {word.strip().lower()}, guesses: {word_guesscount}", end='')
        if args.profile:
            guess_time =  "%.4f" % guess_time
            print(f", time: { guess_time}s", end='')
        if word_guesscount > 6:
            print(f" (Fail!)", end='')
            fail_count += 1
            if word_guesscount == worst_fail:
                worst_word.append(word.strip())
            elif word_guesscount > worst_fail:
                worst_fail = word_guesscount
                worst_word = [word.strip()]
        print(f"")
        guess_count += word_guesscount
            
    print(f"Test cycle complete!")
    if args.profile:
        print(f"Total time: {total_time}")
        print(f"Avg. time per guess: {total_time/wordcount}")
    print(f"Words tested: {wordcount}")
    print(f"Total number of guesses: {guess_count}")
    print(f"Average number of guesses per word: {guess_count/wordcount}")
    print(f"First word used to guess: {first_guess}")
    print(f"Number of wordle failures (> 6 guesses): {fail_count}")
    print(f"Worst words: {worst_word} ({worst_fail} guesses!)")
    

def word_game():
    global wordcount
    global wordlist
    
    global cur_word
    global non_word
    global known_letters
    global non_letters
    
    solution = random.choice(wordlist)
    if (args.profile >= 1):
        print(f"Word chosen: {solution}")
        
    keep_guessing = "Y"
    while (keep_guessing == "Y") or (not keep_guessing):
        guess = ""
        print("Enter guess or leave blank for autogenerated guess:")
        guess = input()
        while not ((guess == "") or (len(guess.strip()) == WORD_SIZE)):
            print("Enter a 5 letter word or leave blank!")
            guess = input()
        if guess == "":
            guess = cut_in_half()
        if guess == solution:
            print("Correct!")
            break
        print(f"Trying guess: {guess}...")
        user_guess(guess)
    
    

with open(filename, 'r') as file:
    wordlist = file.readlines()
    working_wordlist = deepcopy(wordlist)
    
wordcount = build_lettercount()

lettercombo_count = 0
for letterset in lettercombo_list:
    lettercombo_count += len(lettercombo_list[letterset])

print(f"File {filename} loaded, wordcount: {wordcount}, number of unique letter sets: {lettercombo_count}")

if args.wordtest:
    reset_word()
    word_test()
elif args.test:
    print(f"Auto test cycle. First guess (leave empty for default):")
    first_guess = input()
    if not first_guess:
        reset_word()
        first_guess = cut_in_half()
    auto_test(first_guess)
else:
    reset_word()
    word_game()




    





