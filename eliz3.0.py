import re
import random
import string

pronouns={
        "i":"you",
        "me":"you",
        "you":"me",
        "your":"my",
        "my":"your",
        "was":"were",
        "i'll":"you will",
        "i've":"you have",
        "myself": "yourself"
        
        }



dic={
     r'.* Perhaps (?P<keywords>.+)':["You aren't certain, are you?",
                              "How sure are you about it?",
                              "Why are you uncertain?"
                              "You aren't sure"
                              ],
     r'I want (?P<keywords>.+)':["Why do you want replacement_text?",
                              "What would you do if you got replacement_text?"
                              ],
     r'Sorry(?P<keywords>.*)':["It's absolutely fine.",
                                "You don't need to appologize at all.",
                                "What would you do when you feel sorry?",
                                "No need for an apology"
                                ],
     r'.*I Remember (?P<keywords>.+)':["Do you often think of replacement_text",
                                "Does thinking of replacement_text bring anything else to mind",
                                "What else do you remember?",
                                "Why do you remember replacement_text just now",
                                'What in the present situation reminds you of replacement_text'
                                ],
    r'.*Do you remember (?P<keywords>.+)':["Did you think i would forget replacement_text",
                                "Why do you think i should recall replacement_text now",
                                "What else do you remember?"
                                ],
    r'(?P<keywords>.+ If .+)':['Do you think its likely that replacement_text',
                              "Do you wish that replacement_text",
                              "What do you think about replacement_text",
                              ],
    r'.*dream (?P<keywords>.+)':['Have you ever fantasied replacement_text while you were awake',
                              "Have you dreamt replacement_text before?",
                              "Don't you believe that dream has something to do with your problem",
                              "What does that dream sugest to you?"
                              ],
    r'.*computer (?P<keywords>.+)':['Do computers worry you',
                              "Why do you mention computers",
                              "What do you think machines have to do with your problem",
                              "Don't you think computers can help people?"
                              ],
    r'.*am I (?P<keywords>.+)':['Do you believe you are replacement_text',
                              "Would you want to be replacement_text",
                              "You wish i would tell you are replacement_text",
                              "What would it mean if you were replacement_text?"
                              ],
    r'.* am (?P<keywords>.+)':["Why do you say 'am'",
                              "I don't understand that",
                              "You wish I would tell you are replacement_text?"
                              ],
    r'.*Hello (?P<keywords>.*)':["Hey! How's life?",
                              "Hi! Nice to meet you. Please state your problem.",
                              "Hello! Let's discuss about your problems."
                              ]
    }
memoryMatchRegEx={
    r'.*my (?P<keywords>\w+)':["Lets discuss further about your replacement_text"]    
        }

def userNameValidation():
    nameExp=r'((i\s?am\s?)|(my\s?name\s?is)|(they\s?call\s?me)|(myself))?\s?(?P<fname>\w+)'
    username=input()
    if(username):
        match=re.match(nameExp,username,re.IGNORECASE)
        firstName=match.group('fname')
        print("Eliza: Hi "+firstName+", How can I help you today?")
        bot(firstName)
    else:
        print("Eliza: We are not proceeding without your name. Please type your name.")
        userNameValidation()

def bot(firstName):
    x=1
    filler=["Tell me more about it "+firstName,"I see","Please go on "+firstName,"That's very interesting "+firstName+"!"]
    inputTracker=None
    while x!=0:
        userinput=input(firstName.title()+":")
        flag=0
        if(userinput==''):
            print("Eliza: Please talk something")
            continue
        if(userinput == "quit"):
            print("Eliza: I will not say goodbye to you! I`ll say see you soon!")
            break
        if(userinput==inputTracker):
            repeatResponse=["Are you testing me by repeating yourself?","Please don't repeat yourself.",
                    "What do you expect me to say by repeating yourself?"]
            print("Eliza:",random.choice(repeatResponse))
            continue
        for regExpressions in memoryMatchRegEx:
            memoryMatch=re.match(regExpressions,userinput,re.IGNORECASE)
            if(memoryMatch!=None):
                memoryText=memoryMatch.group('keywords')
                memoryReply=random.choice(memoryMatchRegEx[regExpressions])
                replacedMemoryText=re.sub(r'replacement_text',memoryText,memoryReply)
                filler.append(replacedMemoryText)
        inputTracker=userinput
        for decompose in dic:
            match=re.match(decompose,userinput,re.IGNORECASE)
            if(match!=None):
                flag=1
                matchText = match.group('keywords')
                reply = random.choice(dic[decompose])
                splits = matchText.split()
                for i in range(0,len(splits)):
                    if splits[i].lower() in pronouns:
                        splits[i]=pronouns[splits[i].lower()]
                splits = " ".join(splits)
                reply = re.sub(r'replacement_text',splits,reply)
                print("Eliza: ",reply)
                break
        if flag == 0:
            reply=random.choice(filler)
            print("Eliza: ",reply) 
        
            

if(__name__ == "__main__"):
    print("Eliza: Hi, I'm a psychotherapist. What is your name?")
    userNameValidation()
    