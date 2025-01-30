# Martin's Python Portfolio
Enclosed is a portfolio of various Python scripts of varying utility I have come up with from time to time.

## Wordle Generator
My most major recent project, a script that solves New York Times Wordle puzzles through selecting guesses that narrow down words as much as possible. I went into this with 0 knowledge of information theory and found it a fun learning experience to come up with my own Wordle-solving algorithm without looking anything up. Tested on a 3,200-word list of 5-letter words, it takes an average of 3.9 or so guesses per word, and solves the Wordle (6 guesses or less) around 98.5% of the time.

### How to run it
No arguments runs the script in 'Wordle assistant' mode, where the user acts as essentially a middle man between the Wordle and the program, with the program generating guesses and the user giving feedback on what is correct or incorrect in the guess:
![image](https://github.com/user-attachments/assets/80efaca8-0402-4649-8305-248cb176a904)

Running with command line argument `-wt` or `-wordtest` runs the script in 'word test' mode, where the user inputs a solution word and the program goes through guesses until it arrives at the right answer:
![image](https://github.com/user-attachments/assets/f077295c-9d46-4be1-a805-05f2d9d8d30d)

And finally, running with command line argument `-t` or `test` runs a full stress test where the program solves a Wordle for every single word in its word list. The argument `-p` includes performance profiling on how fast it runs and can be repeated for finer detail.
![image](https://github.com/user-attachments/assets/036a903e-2963-4477-a7ce-2c564662d7b7)

### How it works

How it works is as follows. First, the script reads in a list of 5-letter words (in my case, I used the fantastic [12dicts](http://wordlist.aspell.net/12dicts-readme/) word list, specifically the '2 of 12' list) and builds a few different data structures to categorize everything:
- A list of sets of letters in words (e.g. the word 'rover' adds ['r', 'o', 'v', 'e'] to the list) called `lettercombo_list`, that is iterated over to select a set of letters from.
- A dictionary of dictionaries (`<char, <char, int>>`) called `letterdict` that acts as a co-occurrence matrix for a given letter, listing for each letter, how many times each other letter is co-located in a word with it (i.e., for the words 'bagel' and 'bread', the letter 'b' has a dictionary of `<char, int>` that looks like ['a': 2, 'e': 2, 'g': 1, 'r': 1, 'd': 1, 'l', 1]). This is used for evaluating how good a specific letter combination is.
- A dictionary of dictionaries (`<int, <char, int>>`) called `locationmap` that acts as a location count, recording for each place in the word (e.g. letters 1-5 of a 5-letter Wordle) how many times a given letter appears in this place. This is used for evaluating how good an individual word is versus another word that uses an identical set of letters - for instance, if 90% of words started with 'a', then the word 'aster' would be more useful in Wordle than 'stare'.

Once this is done building, guesses are arrived at using an algorithm that performs linear searches in `lettercombo_list` looking for the best set of letters to use, and the best valid word that uses those letters, while keeping in mind the feedback from Wordle (e.g., checking to make sure the set of letters includes any letters the script knows are in the Wordle, and does not include any letters that have been ruled out). To find the best set of letters to use, it scores a letter set based on `letterdict` from earlier, grabbing the maximum of a list of the lowest co-location counts for all the letters (confusing, I know). The higher the score, the better - for context, if the script doesn't know anything about the word, the highest-scoring set of letters for Wordle is ['a', 'e', 'r', 's', 't'].

Once this is done, it tries to find the best word that fits the letter list it's chosen - If only one word matches, it chooses it, if there are multiple words, it scores them off of `locationmap`, adding up the scores for each letter/index combination and picking the word with the highest score. For the letter set ['a', 'e', 'r', 's', 't'], there are two valid words: 'aster' and 'stare'. The latter returns a much higher score (For instance, words that start with 'S' are more common than words that start with 'A'), so the script chooses 'stare' as its starting guess.

After that, the script checks this guess - either the user inputs the feedback from Wordle or the program checks it against a solution that has already been input. It records which letters are in the correct place, which letters are in the word but in the wrong place, and which letters are not in the word at all. It forms a whitelist of letters, a blacklist of letters, a 'known word' list of letters in correct places (e.g. if the answer is 'glass' then 'stare' returns [' ', ' ', 'a', ' ', ' '], and a 'non-word' list of lists of letters that are definitely in wrong places (e.g. for 'glass' 'stare' returns [['g'], ['l'], [], ['s'], ['s']]). When the script tries again, it selects only sets of letters and words that adhere to those four pieces of information and would constitute possible answers.

### Optimizations

This script started off taking a good minute to come up with the first guess, and now does solves upwards of 40-50 complete Wordles per second. I optimized it by first removing as much nested iteration as possible, and more notably, switching the program over to using 'working list' copies of both the base wordlist and `lettercombo_list` - After every guess, the program iterates through the wordlist and removes everything that doesn't fit the Wordle (and thus isn't a viable guess), and while coming up with a viable letter set, the program trims every non-viable letter set it encounters. This results in the program quickly going from iterating through over 3,000 words at a time to only a few hundred, which really adds up for subsequent guesses.

## Tuner Shop Generator

Something much sillier than the Wordle solver, this comes from myself noticing that a lot of Japanese custom car tuning garages tend to have a very amusing naming scheme where they mix in random English nouns alongside unrelated automotive descriptors. No fancy algorithm here, it's pretty self-explanatory:

![image](https://github.com/user-attachments/assets/b99c6783-0824-4918-bfe3-bb48628f5a57)
