#imported necessary modules
from platform import python_version
import re
import pandas as pd
import itertools 
from datetime import datetime
start_time = datetime.now()

# Help


def scorecard():
    inns=['pak_inns1.txt','india_inns2.txt']##text file of ind and pak
    turn=['Pakistan Innings','India Innings']
    #player of both the teams
    pak_player=['Batter','Mohammad Rizwan(w)','Babar Azam(c)','Fakhar Zaman','Iftikhar Ahmed','Khushdil Shah','Shadab Khan','Asif Ali','Mohammad Nawaz','Haris Rauf','Naseem Shah','Shahnawaz Dahani']
    ind_player=['Batter','Rohit Sharma(c)','KL Rahul','Virat Kohli','Ravindra Jadeja','Suryakumar Yadav','Hardik Pandya','Dinesh Karthik(w)','Yuzvendra Chahal','Avesh Khan','Arshdeep Singh','Bhuvneshwar Kumar']
    #dic of players mapped with original names
    match_player={'Batter':'Batter','Bowler':'Bowler','Rizwan':'Mohammad Rizwan(w)','Babar Azam':'Babar Azam(c)','Fakhar Zaman':'Fakhar Zaman','Iftikhar Ahmed':'Iftikhar Ahmed','Khushdil':'Khushdil Shah','Shadab Khan':'Shadab Khan','Asif Ali':'Asif Ali','Mohammad Nawaz':'Mohammad Nawaz','Haris Rauf':'Haris Rauf','Naseem Shah':'Naseem Shah','Dahani':'Shahnawaz Dahani','Rohit':'Rohit Sharma(c)','Rahul':'KL Rahul','Kohli':'Virat Kohli','Jadeja':'Ravindra Jadeja','Suryakumar Yadav':'Suryakumar Yadav','Hardik Pandya':'Hardik Pandya','Karthik':'Dinesh Karthik(w)','Chahal':'Yuzvendra Chahal','Avesh Khan':'Avesh Khan','Arshdeep Singh':'Arshdeep Singh','Bhuvneshwar':'Bhuvneshwar Kumar'}
    #opening the scorecard text file
    with open (r"Scorecard.txt",'w')as file1:
        for ITEAM,TURN in zip(inns,turn) :
            with open(ITEAM, 'r')as file:
                ##to decribe all the necessary information about the player playing 
                Batting={"Batter":[" ","R","B","4s","6s","SR"]}
                Bowling={"Bowler":["O","M","R","W","NB","WD","ECO"]}
                #.........................!!!
                #fun to check wheather the player has appeared or not in the dic
                def checkKey(dic, key):
                    if key in dic.keys():
                        return 1
                    else:
                        return 0
                #.......................!!!
                line=file.readlines()#reading the lines of text file
                total=0 #for total run in the inning
                Powerplay=0 #for total run in the powerplay over
                extra=0##extra runs
                wickets=0##total no of wickets
                last_bowl=0
                total_wide=0
                leg_byes=0
                byes=0
                fall_of_wickets=[]#time at which there is fall of a wicket
                for i in line:
                    # print(i)
                    
                    try:
                        sentence = (re.match(".*?,\s*(.*?),.*", i).group(1))##gives text in between first two commas
                        
                    except:
                        pass
                    #print(sentence)
                    #finding the run in byes
                    sentence1=re. findall(r"leg byes, (\d)", i)
                    sentence2=re. findall(r"leg byes, ([a-zA-Z]+)", i)
                    sentence_bye1=re. findall(r"byes, ([a-zA-Z]+)", i)
                    sentence_bye2=re. findall(r"byes, (\d)", i)
                    
                    try:
                        sentence3=(re.match(".*?\s*(.*?),.*", i).group(1))##this gives text before first comma
                        result = re.search('\d.\d (.*) to', sentence3)##curr bowl
                        Bowler_name=(result.group(1))##bowler name
                        # Bowler_name=match_player[Bowler_name]
                        # print(Bowler_name)
                        result1=re.search("to (.*)",sentence3)
                        
                        Batsman_name=result1.group(1)##batsman name
                        #Batsman_name=match_player[Batsman_name]
                        #Batsman_name=re.search(result1.group(1))
                        bowl=float(re.findall(r"\d.\d|\d\d.\d",sentence3)[0])
                    except:
                        continue
                    if(checkKey(Batting,Batsman_name)==0):
                        Batting[Batsman_name]=["not out",0,0,0,0,0]
                    if(checkKey(Bowling,Bowler_name)==0):
                        Bowling[Bowler_name]=[0,0,0,0,0,0,0]
                    try:
                        heroRegex = re.compile (Batsman_name+' b '+Bowler_name)##finding the pattern in the line
                        mo1 = heroRegex.search(i)
                        Batting[Batsman_name][0]=mo1.group()
                        Bowling[Bowler_name][3]+=1
                        wickets+=1
                        wicket_time=str(total)+'-'+str(wickets)+' ('+Batsman_name+','+str(bowl)+')'
                        fall_of_wickets.append(wicket_time)
                        # print(mo1.group())
                        #lbw b
                        
                    except:
                        pass
                    try:
                        heroRegex1 = re.compile (Batsman_name+' lbw b '+Bowler_name)##finding the pattern in the line
                        mo2 = heroRegex1.search(i)
                        Batting[Batsman_name][0]=mo2.group()
                        Bowling[Bowler_name][3]+=1 
                        wickets+=1
                        wicket_time=str(total)+'-'+str(wickets)+' ('+Batsman_name+','+str(bowl)+')'
                        fall_of_wickets.append(wicket_time)
                        #print(mo2.group())
                    except:
                        pass
                    try:
                        sentence4=(re.match(".*?,\s*out Caught by (.*?)!.*", i).group(1)) ##finding the pattern in the line
                        #print(sentence4) 
                        Batting[Batsman_name][0]="c "+sentence4+" b "+Bowler_name
                        Bowling[Bowler_name][3]+=1 
                        wickets+=1
                        wicket_time=str(total)+'-'+str(wickets)+' ('+Batsman_name+','+str(bowl)+')'
                        fall_of_wickets.append(wicket_time)
                    except:
                        pass 
                    
                        
                    
                    x = sentence.split(' ', 1)[0]#splitting the sentence for run
                    try:
                        x1=sentence.split(' ',1)[1]
                        total+=int(x)
                        if(bowl<=5.6):#for powerplay
                            Powerplay+=int(x)
                            #print(i)
                        if(x1=="wides"):#if bowl is wide
                            extra+=int(x)
                            total_wide+=int(x)
                            Bowling[Bowler_name][2]+=int(x)
                            Bowling[Bowler_name][5]+=int(x)
                            Batting[Batsman_name][2]-=1
                            Bowling[Bowler_name][0]-=1
                        if(x1=="runs" or x1=="run"):
                            Batting[Batsman_name][1]+=int(x)
                            Bowling[Bowler_name][2]+=int(x)
                    except:
                    
                # print(x)  
                        if(x=='1'or x=='2' or x=='3'):##if run taken is 1,2,3
                            total+=int(x)
                            extra+=int(x)
                            if(bowl<=5.6):
                                Powerplay+=int(x)
                                #print(i)
                        if(x=='wide'):
                            total+=1
                            extra+=1
                            total_wide+=1
                            Bowling[Bowler_name][0]-=1
                            Batting[Batsman_name][2]-=1
                            Bowling[Bowler_name][2]+=1
                            Bowling[Bowler_name][5]+=1
                            if(bowl<=5.6):
                                Powerplay+=1
                                #print(i)
                        if(x=='FOUR'):
                            total+=4
                            Batting[Batsman_name][1]+=4
                            Bowling[Bowler_name][2]+=4
                            Batting[Batsman_name][3]+=1
                            if(bowl<=5.6):
                                Powerplay+=4
                                #print(i)
                        if(x=='SIX'):
                            total+=6
                            Batting[Batsman_name][1]+=6
                            Bowling[Bowler_name][2]+=6
                            Batting[Batsman_name][4]+=1
                            if(bowl<=5.6):
                                Powerplay+=6
                             
                    if(sentence1 ):#for byes run
                        total+=int(sentence1[0])
                        extra+=int(sentence1[0])
                        leg_byes+=int(sentence1[0])
                        #Bowling[Bowler_name][2]+=int(sentence1[0])
                        if(bowl<=5.6):
                            Powerplay+=int(sentence1[0])
                            #print(i)
                    if(sentence2==['FOUR']):
                        total+=4
                        extra+=4
                        leg_byes+=4
                        #Bowling[Bowler_name][2]+=4
                        if(bowl<=5.6):
                            Powerplay+=4
                            #print(i)
                    if(sentence2==['SIX']):
                        total+=6
                        extra+=6
                        leg_byes+=6
                        #Bowling[Bowler_name][2]+=6
                        if(bowl<=5.6):
                            Powerplay+=6
                            #print(i)
                    if(sentence_bye2 and len(sentence1)==0):
                        byes+=int(sentence_bye2[0])
                        total+=int(sentence_bye2[0])
                        extra+=int(sentence_bye2[0])
                    if(sentence_bye1==['SIX'] and sentence2!=['SIX']):
                        byes+=6
                        total+=6
                        extra+=6
                    if(sentence_bye1==['FOUR'] and sentence2!=['FOUR']):
                        byes+=4
                        total+=4
                        extra+=4
                    last_bowl=bowl
                    Bowling[Bowler_name][0]+=1
                    Batting[Batsman_name][2]+=1
                    Batting[Batsman_name][5]=round((Batting[Batsman_name][1]/Batting[Batsman_name][2])*100,2)# strike rate of player
                    
                
                    
                    #print(i)   
                # print(total) 
                # print(Powerplay)
                # print(extra)
                # print(fall_of_wickets)
                #print(Batting)
                #print(Bowling)
                # print(total_wide)
                # print(total_byes)
                for key, values in Bowling.items():
                    if(key!="Bowler"):
                        if(isinstance(values, list)):
                            values[6]=round((values[2]/values[0])*6,2)#econmy of bowler
                            values[0]=(values[0]//6)+((values[0]%6)/10)##converting into over
                            
                            
                        
                #print(Bowling)
                #print(Batting) 
                
                batted=[]#player who did batting
                for key, values in Batting.items():
                    batted.append(match_player[key])
                not_batted=[]#player who did not bat
                if(TURN=='Pakistan Innings'):
                    not_batted=list(set(pak_player).symmetric_difference(set(batted)))
                if(TURN=='India Innings'):
                    not_batted=list(set(ind_player).symmetric_difference(set(batted)))
                #print(total)
                #print(not_batted)
                 ##putting the values in the scorecard text file   
                b=str(total)+'-'+str(wickets)+'('+str(last_bowl)+' Ov)'
                text_line=(f"{TURN:<93}{b}")##this is used for alignment
                file1.write(text_line+'\n')#for putting the text in new line
                for key, values in Batting.items():
                
                    if(isinstance(values,list)):
                        text_line2= (f"{match_player[key]:<20}{str(values[0]): <40}{str(values[1]):^10}{str(values[2]):^10}{str(values[3]):^10}{str(values[4]):^10}{str(values[5]):>5}")
                        file1.write(text_line2+'\n')
                file1.write(" \n")
                file1.write(f"{'Extras':<63}{str(extra)+'(b '+str(byes)+', lb '+str(leg_byes)+', w '+str(total_wide)+', nb 0, p 0)'}") 
                file1.write("\n")
                file1.write(f"{'Total':<63}{str(total)+'('+str(wickets)+' wkts,'+str(bowl)+' Ov)'}")
                file1.write('\n')
                if(len(not_batted)>0):
                    file1.write(f"{'Did not Bat':<40}{not_batted}")
                    file1.write('\n')
                file1.write("Fall of Wickets\n") 
                file1.write(str(fall_of_wickets)+'\n')
                file1.write("\n")
                
                for key, values in Bowling.items():
                
                    if(isinstance(values,list)):
                        text_line2=(f"{match_player[key]:<20}{str(values[0]): <10}{str(values[1]):^10}{str(values[2]):^10}{str(values[3]):^10}{str(values[4]):^10}{str(values[5]):^10}{str(values[6]):>5}")
                        file1.write(text_line2+'\n')
                file1.write('\n')
                file1.write(f"{'Powerplays':<30}{'Overs':^10}{'Runs':>43}")
                file1.write('\n')
                file1.write(f"{'Mandatory':<30}{'0.1-6':^10}{str(Powerplay):>43}")
                file1.write('\n'*3)
    file1.close()##closing the file1
        

# Code
ver = python_version()

if ver == "3.8.10":
    print("Correct Version Installed")
else:
    print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")


scorecard()


# This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
