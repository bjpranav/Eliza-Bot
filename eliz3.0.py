'''
Eliza by Team GAP
Team Members: Pranav Krishna SJ,Alagappan A, Ganesh Nalluru

Eliza mimics a psychatrist. It takes input from the user and replies by
spotting words and transforming sentences. The program replies something even 
if the given sentence is not recogonizable. It detects repeated inputs, empty 
strings and replies acordingly. It has a memory feature which makes the 
conversation divert to the previously discussed topic if it does not 
recognize user input. For example, it stores the reply of sentences where the keyword
my is used. I detects positive or negative emotions and replies acordingly. 
These features are inspired from the Eliza research paper by Joseph Weizanbaum.

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


'''


import re
import random
import numpy as np

#Negative words to be detected
negative = ["sad", "unhappy", "depressed", "sick","dejected","sorrow","regretful"]

#Positive words to be detected
positive = ["happy", "elated", "glad", "better","good","great"]

'''
Regular expressions for some user inputs whose responses gets stored in memory
and used when required.
'''
memoryMatchRegEx = {

    r'.* ?(my|our) (?P<keywords>\w+)': ["Lets discuss further about your replacement_text",
                                  "Tell me more about your replacement_text",
                                  "I would like to discuss more about your replacement_text"]
}


#Regular expressions dictionary for spotting words and transforming sentences.
dic = {
       
    #The regular expression below is used for matching uncertain inputs, the responses are general replies a human
    #would give to uncertain responses
    
    r'.* ?(Perhaps|Maybe|I am not sure|I don\'t know).*': ["How certain are you about this?",
                                                           "How sure are you about it?",
                                                           "How often do you respond with uncertainity?",
                                                           "Can't you be more positive"],
       
    #The regular expression below is used for matching words after key words 'I want'. When user input has
    #'I want', it is evident that the user desires something. Sentences like "How would you feel if you 
    #got something", "How badly do you want replacement_text" induces the user to talk more on the topic. 
    #Moreover, these are general questions which fit to any desire
    
    r'I want (?P<keywords>.+)': ["Do you crave replacement_text?",
                                 "Do you really want replacement_text?",
                                 "How would you feel if you got replacement_text",
                                 "How badly do you want replacement_text"],
       
    #Any reply that has the word 'Sorry' indicates an act of apology. That apology could be to 
    #eliza or about an incdient for which the user feels sorry for etc. Sentences like 
    #"Do you think there was a need for apology?", "How do you feel when somone apologizes you?"
    #would apply to any of these contexts. Therfore they are used as possible replies.
    
    r'.*Sorry ?.*': ["Do you think there was a need for apology?",
                       "How do you feel when somone apologizes you?",
                       "What would you do when you feel sorry?"],
       
    #It is more common for a person to recall about a past experience to a psychatrist. So, the keywords 
    #'I remember' is captured. Sentences transformations like "How often do you think of replacement_text?
    #and "What makes you remember replacement_text?" makes the user believe Eliza is aware of the context
    #that the user is "Thinking" of something.
    

    r'.*I Remember (?P<keywords>.+)': ["How often do you think of replacement_text?",
                                         "Does thinking of replacement_text bring anything else to mind",
                                         "What makes you remember replacement_text?",
                                         "Why do you want to remember replacement_text now?",
                                         ],
    #The key word do you remember is similar to the one discussed above. Any thing after the do you 
    #remember is captured. Sentences transformations like "How often do you think of replacement_text?
    #and "What makes you remember replacement_text?" makes the user believe Eliza is aware of the context
    #that the user is "Thinking" of something.

    r'Do you remember (?P<keywords>.+)': ["Did you think I would forget replacement_text",
                                              "Why do you think I should recall replacement_text now?",
                                              "What else do you remember?"],

    r'(?P<keywords>.+ If .+)': ['Do you think its likely that replacement_text',
                                "Do you wish that replacement_text",
                                "What do you think about replacement_text",],

    r'.* dream (?P<keywords>.+)': ["Do you like to fantasize replacement_text everytime?",
                                    "Does dreaming about that make you crazy?",
                                    "Do you think the dream has anything to do with your problem?",
                                    "Do you always dream about that?"],

   
    r'.* ?am I (?P<keywords>.+)': ["Do you believe you are replacement_text",
                                  "Would you want to be replacement_text",
                                  "You wish i would tell replacement_text",
                                  "What would it mean if you were replacement_text?"],
   
    r'I am (?P<keywords>.+)':   ["Is it because you are replacement_text you came to me?",
                                  "How long have you been replacement_text?",
                                  "Do you believe it is normal to be replacement_text?"],

    r'.* am (?P<keywords>.+)': ["Why do you say 'am'?",
                                 "I don't understand that",
                                 ],

    r'.* ?Hello ?(?P<keywords>.*)?': ["Hey! How's life?",
                                      "Hi! Nice to meet you. Please state your problem.",
                                      "Hello! Let's discuss about your problems."],

    r'.* ?are you (?P<keywords>.*)': ["Why are you interested in whether I am replacement_text or not ?",
                                      "Would you prefer if I weren't replacement_text ?",
                                      "Perhaps I am replacement_text in your fantasies",
                                      "Do you sometimes think I am replacement_text"],

    r'.* ?are they (?P<keywords>.*)': ["Did you think they might be replacement_text",
                                       "Would you like if they were not replacement_text ?",
                                       "What if they were not replacement_text ?",
                                       "Possibly they are replacement_text"],

    r' .* your (?P<keywords>.*)': ["Why are you concerned over my replacement_text ?",
                                    "What about your own replacement_text ?",
                                    "Are you worried about someone else's replacement_text ?",
                                    "Really, my replacement_text!"],

    r'I was (?P<keywords>.*)': ["Were you really replacement_text ?",
                                "Why do you tell me you were replacement_text now?"],

    r'Were you (?P<keywords>.*)': ["Would you like to believe I was replacement_text ?",
                                     "What suggests that I was replacement_text ?",
                                     "Perhaps I was replacement_text",
                                     "What if I had been"],
    r'.* You say (?P<keywords>.+)':["Can you elaborate on replacement_text ",
                              "Do you say replacement_text for some special reason",
                              "That's quite Interesting"
                              ],

    r'.* am (?P<keywords>.+)':["Why do you say 'am'?",
                              "I don't understand that",
                              "You wish I would tell you you are replacement_text"
                              ],

     r'Yes ?(?P<keywords>.*)':["How often do you reply positively?",
                              "You are sure?",
                              "I see","I Understand"
                              ],
     r'No ?(?P<keywords>.*)':["are you saying 'no' just to be negative?",
                              "you seem bit negative",
                              "why not?","why 'NO'?"
                              ],

    r'Because (?P<keywords>.+)':["Is that the reason?",
                              "Don't any other reasons come to mind?",
                              "Does that reason seem to explain anything else?",
                              "What other reasons might there be?"
                              ],

    r'Why don\'t you (?P<keywords>.+)':["Do you believe I don't replacement_text ",
                              "Perhaps I will replacement_text in good time",
                              "Should you replacement_text yourself",
                              "You want me to replacement_text"
                              ],

    r'.* ?my (?P<keywords>(mother|father|brother|sister|wife)) .*': ["What was your relationship with your replacement_text like?",
                                                                    "How do you feel about your replacement_text ?",
                                                                    "Does your relationship with your replacement_text related to your feelings today?",
                                                                    "Do you have trouble showing affection with your family?"],

    r'.* ?(you remind me of|you are) (?P<keywords>\w+)': ["What makes you think I am replacement_text?",
                                  "Does it please you to believe I am replacement_text",
                                  "Do you sometimes wish you were replacement_text",
                                  "Perhaps you would like to be replacement_text"],
         
    r'.* ?(you (?P<keywords>\w+) me)': ["Why do you think I replacement_text you?",
                                  "Do you really belive I replacement_text you?",
                                  "I don't think I replacement_text you"],
          
    r'.* ?(what ?(?P<keywords>.*))': ["That's an interesting question",
                                  "How long is this question in your mind?",
                                  "why did you ask that?",
                                  "Why are you asking that question?"], 
          
    r'.* ?(everyone|everybody|none|nobody) ?(?P<keywords>.*)': ["Can you be more specific?",
                                  "Do you have someone in mind?",
                                  "Are you talking about anyone in particular?"],
          
    r'.* ?(Always ?(?P<keywords>.*))': ["Do you have anything in particular?",
                                  "Is there any exemptions?",
                                  "Do you like to use definitive language?"],

    r'.* ?(am|is|are|was) like ?(?P<keywords>.*)': ["How sure are you about the similarity?",
                                  "Do you like to compare things??",
                                  "How did you make the connection?"],
    'negative':["I am sorry to hear you are replacement_text",
                "Do you think coming here will help you not to be replacement_text ?",
                "I'm sure its not pleasant to be replacement_text"],

    'positive':["How have I helped you to be replacement_text ?",
                "Has your treatment made you replacement_text ?",
                "What makes you replacement_text just now ?"]
}

pronouns = {"i": "you", "me": "you",
            "you": "me","your": "my",
            "my": "your","was": "were",
            "i'll": "you will", "i've": "you have",
            "myself":"yourself", "yourself": "myself"}




def userNameValidation():
    nameExp = r'((i\s?am\s?)|(my\s?name\s?is)|(they\s?call\s?me)|(myself))?\s?(?P<fname>\w+)'
    username = input()
    username=username.strip()
    if (username.replace(" ", "") and not (set('[~!@#$%^&*()_+{}":;\']+$').intersection(username))):
        match = re.match(nameExp, username, re.IGNORECASE)
        firstName = match.group('fname')
        print("Eliza: Hi " + firstName + ", How can I help you today?")
        bot(firstName)
    else:
        print("Eliza: We are not proceeding without your name. Please type your name.")
        userNameValidation()

def memory(userinput):
    for regExpressions in memoryMatchRegEx:
        memoryMatch = re.match(regExpressions, userinput, re.IGNORECASE)
        if (memoryMatch != None):
            memoryText = memoryMatch.group('keywords')
            memoryReply = random.choice(memoryMatchRegEx[regExpressions])
            replacedMemoryText = re.sub(r'replacement_text', memoryText, memoryReply)
            return replacedMemoryText
    return userinput


def eliza_reply(matchText,reference):
    reply = random.choice(dic[reference])
    splits = matchText.split()
    for i in range(0, len(splits)):
        if splits[i].lower() in pronouns:
            splits[i] = pronouns[splits[i].lower()]
    splits = " ".join(splits)
    return re.sub(r'replacement_text', splits, reply)


def matchdic(userinput):
    for decompose in dic:
        match = re.match(decompose, userinput, re.IGNORECASE)
        if (match != None):
            flag = 1
            try:
                match.group("keywords")
                matchText = match.group('keywords')

                if matchText in negative:
                    reference="negative"
                    reply = eliza_reply(matchText,reference)
                    print("Eliza: ", reply)
                elif matchText in positive:
                    reference = "positive"
                    reply = eliza_reply(matchText,reference)
                    print("Eliza: ", reply)
                else:
                    reference = decompose
                    reply = eliza_reply(matchText, reference)
                    print("Eliza: ", reply)

            except IndexError:
                reply = random.choice(dic[decompose])
                print("Eliza: ", reply)
            return flag

    flag = 0
    return flag

def bot(firstName):
    x = 1
    filler = ["Tell me more about it " + firstName, "I see", "Please go on " + firstName,
              "That's very interesting " + firstName + "!"]
    memorydic=[]
    inputTracker = None

    while x != 0:
        userinput = input(firstName.title() + ":")
        flag = 0
        if (userinput == ''):
            print("Eliza: Please say something")
            continue
        if (userinput.lower() == "quit"):
            print("Eliza: I will not say goodbye to you! See you soon!")
            break
        if (userinput == inputTracker):
            repeatResponse = ["Are you testing me by repeating yourself?", "Please don't repeat yourself.",
                              "What do you expect me to say by repeating yourself?"]
            print("Eliza:", random.choice(repeatResponse))
            continue

        text=memory(userinput)

        if(text!=userinput):
            memorydic.append(text)


        inputTracker = userinput

        flag = matchdic(userinput)

        if (flag == 0 and len(memorydic)==0):
            reply = np.random.choice(filler,replace=False)
            print("Eliza: ", reply)
        elif (len(memorydic)>0 and flag == 0):
            combinedList=[memorydic,filler]
            listChoice = np.random.choice(len(combinedList),replace=False,p=[0.6,0.4])
            reply=np.random.choice(combinedList[listChoice],replace=False)
            print("Eliza: ", reply)

if (__name__ == "__main__"):
    print("Eliza: Hi, I'm a psychotherapist. What is your name?")
    userNameValidation()
