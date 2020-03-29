Eliza mimics a psychiatrist. It takes input from the user and replies by
spotting words and transforming sentences. The program replies something even 
if the given sentence is not recognizable. It detects repeated inputs, empty
strings and replies accordingly. It has a memory feature which makes the
conversation divert to the previously discussed topic if it does not 
recognize user input. For example, it stores the reply of sentences where the keyword
'my' is used. It detects positive or negative emotions and replies accordingly.
These features are inspired from the Eliza research paper by Joseph Weizanbaum. To
the best of our knowledge, almost all the features of the research paper has been 
implemented in this program.

Reference: weizanbaum, J. (n.d.). ELIZA A Computer Program.


    
PLEASE TYPE 'quit' TO END THE PROGRAM

Algorithm:
    Requests user name and validates.
    Starts conversation.
    Loop:
        Gets user input.
        If user input is quit, the program terminates.
        Checks if input needs to be stored in memory and stores if necessary.
        Matches regular expressions with user inputs.
        If matches:
            Picks a random choice from possible replies to the expression.
            Performs necessary pronoun conversion and prints output.
        If doesn't match:
            Checks memory if anything is stored.
            If something is stored:
                Prints replies in memory or default replies by weighted probability.
                 

Few conversation examples generated through this program are given below.

Eliza: Hi, I'm a psychotherapist. What is your name?
Pranav

Eliza: Hi Pranav, How can I help you today?
Pranav:I am helpless

Eliza:  How long have you been helpless?
Pranav:Since I was born

Eliza:  Please go on Pranav
Pranav:I want help

Eliza:  Do you crave for help?
Pranav:My mother helps me

Eliza:  Does your relationship with your mother related to your feelings today?
Pranav:everytime

Eliza:  That's very interesting Pranav!
Pranav:gibberish

Eliza:  Let's hear more about you mother
Pranav:quit
