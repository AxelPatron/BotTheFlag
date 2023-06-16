from functools import total_ordering
from http import client
from pydoc import cli
from re import T
from xml.etree.ElementTree import tostring
from TwitterAPI import TwitterAPI
import configparser
import tweepy
import time
import flag
import operator

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
BEARER_TOKEN = ''

CONSUMER_KEY2 = ''
CONSUMER_SECRET2 = ''
ACCESS_KEY2 = ''
ACCESS_SECRET2 = ''
BEARER_TOKEN2 = ''

CONSUMER_KEY3 = ''
CONSUMER_SECRET3 = ''
ACCESS_KEY3 = ''
ACCESS_SECRET3 = ''
BEARER_TOKEN3 = ''


auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api=tweepy.API(auth)
api2 = TwitterAPI( \
        consumer_key=CONSUMER_KEY, 
        consumer_secret=CONSUMER_SECRET, 
        access_token_key=ACCESS_KEY, 
        access_token_secret=ACCESS_SECRET 
        )
config = configparser.ConfigParser()
config.read("config.ini")
client = tweepy.Client(bearer_token=BEARER_TOKEN,
                           consumer_key=CONSUMER_KEY,
                           consumer_secret=CONSUMER_SECRET,
                           access_token=ACCESS_KEY,
                           access_token_secret=ACCESS_SECRET)

client2 = tweepy.Client(bearer_token=BEARER_TOKEN2,
                           consumer_key=CONSUMER_KEY2,
                           consumer_secret=CONSUMER_SECRET2,
                           access_token=ACCESS_KEY2,
                           access_token_secret=ACCESS_SECRET2)

client3 = tweepy.Client(bearer_token=BEARER_TOKEN3,
                           consumer_key=CONSUMER_KEY3,
                           consumer_secret=CONSUMER_SECRET3,
                           access_token=ACCESS_KEY3,
                           access_token_secret=ACCESS_SECRET3)

def split(word): #split the word into a list of character
    return [char for char in word]

def get_all_index(list,word): #return the index of all the word in the list
    indices = []
    for index in range(len(list)):
        if list[index] == word:
            indices.append(index)
    return indices

def is_flag_emoji(c): #return true if c is a flag emoji
    return "\U0001F1E6\U0001F1E8" <= c <= "\U0001F1FF\U0001F1FC" or c in ["\U0001f3f3\uFE0F\u200D\u26A7\uFE0F","\U0001F3F3\uFE0F\u200D\U0001F308","\U0001F3F4\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f", "\U0001F3F4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f", "\U0001F3F4\U000e0067\U000e0062\U000e0077\U000e006c\U000e0073\U000e007f"]
def is_lgbt_emoji(c):
    return c in ["\U0001F3F3\uFE0F\u200D\U0001F308"]
def is_trans_emoji(c):
    return c in ["\U0001f3f3\uFE0F\u200D\u26A7\uFE0F"]
def is_scotland_emoji(c):
    return c in ["\U0001f3f4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f"]
def is_wales_emoji(c):
    return c in ["\U0001f3f4\U000e0067\U000e0062\U000e0077\U000e006c\U000e0073\U000e007f"]
def is_england_emoji(c):
    return c in ["\U0001f3f4\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f"]
def is_pirate_emoji(c):
    return c in ["\U0001f3f4\u200D\u2620\uFE0F"]
def get_mention_id(api,since_id):
    try:
        mentions=api.mentions_timeline(count=10,since_id=since_id)       
    except:
        mentions=[]
        print("Too many Request timeline")
    reply_ids=[]
    usernames=[]
    mentions_id=[]
    not_analyse=[]
    mentions_text=[]
    analyses=["analyse ce tweet","analyse le tweet","analyse this","bottheflag thanks","analyse moi","analyse moi","analyse son tweet","analyse ca","analyse ça","bottheflag analyze","analyze this","analyze that", "bottheflag please","analyse if","analyze if","analyze this tweet","bottheflag","bottheflag analyse","analysis this"]
    for i in range(len(mentions)):
        if mentions[i].in_reply_to_status_id is not None:
            if (("render" in (mentions[i].text).lower()) or ("screenshot" in (mentions[i].text).lower()) or ("pikaso_me" in (mentions[i].text).lower())):
                try:
                    api2.request('blocks/create', {'screen_name': mentions[i].user.screen_name})
                    since_id=mentions[i].id+1
                    print(mentions[i].user.screen_name+" blocked <3")
                except:
                    pass 
            elif any(x in (mentions[i].text).lower() for x in analyses):#"analyse ce tweet" in (mentions[i].text).lower() or "analyses ce tweet" in (mentions[i].text).lower():
                reply_ids.append(mentions[i].in_reply_to_status_id)
                usernames.append(mentions[i].user.screen_name)
                mentions_id.append(mentions[i].id)
                mentions_text.append((mentions[i].text).lower())
            else:
                not_analyse.append(mentions[i].id)
                since_id=max(not_analyse)+1
                print(since_id)
        elif mentions[i].is_quote_status:
            if any(x in (mentions[i].text).lower() for x in analyses):#"analyse ce tweet" in (mentions[i].text).lower() or "analyses ce tweet" in (mentions[i].text).lower():
                reply_ids.append(mentions[i].quoted_status_id)
                usernames.append(mentions[i].user.screen_name)
                mentions_id.append(mentions[i].id)
                mentions_text.append((mentions[i].text).lower())
            else:
                not_analyse.append(mentions[i].id)
                since_id=max(not_analyse)+1
                print(since_id)
    if len(mentions)>0:
        if mentions_id:
            print(mentions_id)
            print("\n reply ids: ")
            print(reply_ids)
            since_id=max(mentions_id)+1
    return mentions_id,usernames,reply_ids,since_id,mentions_text

def get_likers_flags(api,tweet_id,since_id) :
    paginator=0
    paginator1=1
    total_users=[]
    too_many=0
    succes=0
    try:
        while paginator!=paginator1 and len(total_users)<5000:
            if paginator==0:
                users=client.get_liking_users(id=tweet_id)
            else:
                users=client.get_liking_users(id=tweet_id,pagination_token=paginator)                
            #print(users)
            paginator=users[3]['next_token']
            total_users=total_users+users[0]
            succes=1
    except:
        print("Too many Request first")
        too_many=1
    if too_many==1:
        try:
            while paginator!=paginator1 and len(total_users)<5000:
                if paginator==0:
                    users=client2.get_liking_users(id=tweet_id)
                else:
                    users=client2.get_liking_users(id=tweet_id,pagination_token=paginator)
                #print(users)
                paginator=users[3]['next_token']
                total_users=total_users+users[0]
                succes=1
        except:
            print("Too many Request both")
            too_many=2
    if too_many==2:
        try:
            while paginator!=paginator1 and len(total_users)<2000:
                if paginator==0:
                    users=client3.get_liking_users(id=tweet_id)
                else:
                    users=client3.get_liking_users(id=tweet_id,pagination_token=paginator)
                #print(users)
                paginator=users[3]['next_token']
                total_users=total_users+users[0]
                succes=1
        except:
            print("Too many Request all three")
            too_many=3
            config.read("config.ini")
            config.set("GENERAL",'since_id',str(since_id+1))
        with open("config.ini", 'w') as configfile:
            config.write(configfile)
    flags=[]
    try:   
        nbr_likes=len(total_users)
        print("Nbr likes : "+str(nbr_likes))    
        for i in range(len(total_users)):
            caracters=total_users[i].name.split()
            for c in range(len(caracters)):
                if is_trans_emoji(caracters[c]):
                    flags.append("\U0001f3f3\uFE0F\u200D\u26A7\uFE0F")
                elif is_lgbt_emoji(caracters[c]):
                    flags.append("\U0001F3F3\uFE0F\u200D\U0001F308")
                if is_scotland_emoji(caracters[c]):
                    flags.append("\U0001f3f4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f")
                if is_wales_emoji(caracters[c]):
                    flags.append("\U0001f3f4\U000e0067\U000e0062\U000e0077\U000e006c\U000e0073\U000e007f")
                if is_england_emoji(caracters[c]):
                    flags.append("\U0001f3f4\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f")
                if is_pirate_emoji(caracters[c]):
                    flag.append("\U0001f3f4\u200D\u2620\uFE0F")
                elif not flag.dflagize(caracters[c])==flag.flagize(caracters[c]):
                    if len(caracters[c])==2:
                        if caracters[c]==flag.flagize(":CP:") or caracters[c]==flag.flagize(":MF:"):
                            flags.append(flag.flagize(":FR:"))
                        elif caracters[c]==flag.flagize(":EA:"): #Ceuta y Melilla
                            flags.append(flag.flagize(":FR:"))
                        elif caracters[c]==flag.flagize(":UM:"): #USA
                            flags.append(flag.flagize(":US:"))
                        else:
                            flags.append(caracters[c])
                    else:
                        a=flag.dflagize(caracters[c])
                        a=split(a)
                        index=get_all_index(a,":")
                        for j in index:
                            try:   #Some Flags are multiple because of depandecies but look exactly the same
                                if a[j]==a[j+3]:
                                    if a[j+1]=='C' and a[j+2]=='P': #Turn Cliperton Island Flag into French Flag
                                        a[j+1]='F'
                                        a[j+2]='R'
                                        #print("".join(a[j:j+4]))
                                        #print(flag.flagize("".join(a[j:j+4])))
                                    if a[j+1]=='M' and a[j+2]=='F': #Flag of Saint-Martin into French Flag
                                        a[j+1]='F'
                                        a[j+2]='R'
                                        #print("".join(a[j:j+4]))
                                        #print(flag.flagize("".join(a[j:j+4])))
                                    if a[j+1]=='U' and a[j+2]=='M': #Turn the Outlying islands into US flags
                                        a[j+1]='U'
                                        a[j+2]='S'
                                        #print("".join(a[j:j+4]))
                                        ###print(flag.flagize("".join(a[j:j+4])))
                                    if a[j+1]=='E' and a[j+2]=='A':  #Turn Ceuta & Melilla Flag to ES flag
                                        a[j+1]='E'
                                        a[j+2]='S'
                                        ##print("".join(a[j:j+4]))
                                        #print(flag.flagize("".join(a[j:j+4])))
                                    if is_flag_emoji(flag.flagize("".join(a[j:j+4]))):
                                        flags.append(flag.flagize("".join(a[j:j+4])))
                            except:
                                continue
    except:
        nbr_likes=0
        print("except nbr_likes")               
                    
    drapeau=[]
    nbr_drapeau=[]
    drapeau_sort=[]
    nbr_drapeau_sort=[]
    try:
        for i in range(len(flags)):
            if not flags[i] in drapeau:
                drapeau.append(flags[i])
                nbr_drapeau.append(flags.count(flags[i]))
    except:
        pass
    try:
    	enumerate_drapeau = enumerate(nbr_drapeau)
    	sorted_drapeau = sorted(enumerate_drapeau, key=operator.itemgetter(1)) #sort the list of drapeau by number of likes
    	sorted_indices = [index for index, element in sorted_drapeau] #get the indices of the sorted drapeau
    	for i in reversed(sorted_indices):
        	drapeau_sort.append(drapeau[i])
        	nbr_drapeau_sort.append(nbr_drapeau[i])
    except:
        pass
    return drapeau_sort,nbr_drapeau_sort,nbr_likes,too_many,succes
            

 

def main():
    reply_ids=[]
    usernames=[]
    flags=[]
    nbr_flags=[]
    mentions_id=[]
    nbr_likes=0
    config.read("config.ini")
    since_id=int(config["GENERAL"]['since_id'])
    text=""
    english=["this"," that","analyze","if","please","thanks"]
    liste = ["list","liste"]
    while True:
        reply_ids=[]
        usernames=[]
        too_many=0
        mentions_id,usernames,reply_ids,max_since_id,mentions_text=get_mention_id(api,since_id)
        if max_since_id>since_id:
            since_id=max(max_since_id,since_id)
            for i in range(len(reply_ids)):
                flags,nbr_flags,nbr_likes,too_many,succes=get_likers_flags(api,reply_ids[i],since_id)
                print("too_many : "+str(too_many))
                text=""
                if nbr_likes>0:
                    if not flags:
                        if any(x in mentions_text[i] for x in english):
                        	response="No flags in "+str(nbr_likes)+" usernames who liked"
                        else:
                        	response="Aucun drapeau dans "+str(nbr_likes)+" noms ayant liké"
                    else:
                        if any(x in mentions_text[i] for x in liste):
                            for j in range(len(flags)):
                                text=text+flags[j]+":"+str(nbr_flags[j])+"\n"
                        else:
                            for j in range(len(flags)):
                                text=text+flags[j]+":"+str(nbr_flags[j])+","  
                        text=text[:-1]
                        if any(x in mentions_text[i] for x in english):
                            response="Nbr of flags in "+str(nbr_likes)+" usernames who liked:\n"+text
                        else:
                            response="Nbr de drapeaux dans "+str(nbr_likes)+" noms ayant likés:\n"+text
                        if len(response)>=280:
                            response=response[:279]
                        print(text)
                        api.update_status(status=response,in_reply_to_status_id=mentions_id[i],auto_populate_reply_metadata=True)
                        client.like(mentions_id[i])
                    since_id=since_id+1
                    print("since id="+str(since_id))
                else:
                    if too_many==3:
                        print("Too many request")
                        try:
                            if nbr_likes>0:
                                if any(x in mentions_text[i] for x in english):
                                	api.update_status(status="No flags in "+str(nbr_likes)+" likes",in_reply_to_status_id=mentions_id[i],auto_populate_reply_metadata=True)
                                else:
                                    api.update_status(status="Pas de drapeaux dans "+str(nbr_likes)+" likes",in_reply_to_status_id=mentions_id[i],auto_populate_reply_metadata=True)
                            elif any(x in mentions_text[i] for x in english):
                                api.update_status(status="@"+usernames[i]+" Bot too harassed at the moment, max number of requests reached, please try again in 10-15min https://twitter.com/BotTheFlag/status/1581965889565388800",in_reply_to_status_id=mentions_id[i],auto_populate_reply_metadata=True)
                            else:
                                api.update_status(status="@"+usernames[i]+" Bot trop harcelé pour le moment, nombre de requetes max atteintes, Réessayez dans 10-15min https://twitter.com/BotTheFlag/status/1581965889565388800",in_reply_to_status_id=mentions_id[i],auto_populate_reply_metadata=True)
                        except:
                            print("tweet error haut")
                    else:
                        print("pas de likes")
                        try:
                            if nbr_likes>0:
                                if any(x in mentions_text[i] for x in english):
                                	api.update_status(status="No flags in "+str(nbr_likes)+" likes",in_reply_to_status_id=mentions_id[i],auto_populate_reply_metadata=True)
                                else:
                                    api.update_status(status="Pas de drapeaux dans "+str(nbr_likes)+" likes",in_reply_to_status_id=mentions_id[i],auto_populate_reply_metadata=True)
                            elif any(x in mentions_text[i] for x in english):
                            	api.update_status(status="@"+usernames[i]+" An error happened, please retry in 10 mins https://twitter.com/BotTheFlag/status/1581965889565388800",in_reply_to_status_id=mentions_id[i],auto_populate_reply_metadata=True)
                            else:
                                api.update_status(status="@"+usernames[i]+" Une erreur est survenue, réessayez dans 10 mins https://twitter.com/BotTheFlag/status/1581965889565388800",in_reply_to_status_id=mentions_id[i],auto_populate_reply_metadata=True)                              
                        except:
                            pass
        else:
            print("max_id<since_id= "+str(max_since_id))
        config.set("GENERAL",'since_id',str(since_id))
        with open("config.ini", 'w') as configfile:
            config.write(configfile)
        time.sleep(20) 
    
while True:
    try:
        main()
    except:
        print("error")
        time.sleep(5)
