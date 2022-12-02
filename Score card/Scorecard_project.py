from datetime import datetime
start_time = datetime.now()
import pandas as pd
import numpy as np

dataframe_pakinnings = pd.DataFrame()
f=open("pak_inns1.txt","r")
lines=f.readlines()
f.close()
result=[]
present_bowl = []
present_bowler = []
tos = []
present_batsman = []
contents = []
for x in lines:
	if (len(x)>1):
		pres_index = 0
		if (x[3]==' '):
			pres_index = 3
			present_bowl.append(x[0:3])
		else :
			pres_index = 4
			present_bowl.append(x[0:4])
		for z in range(pres_index+1,len(x)):
			if(x[z]==' ' and x[z+1]=='t' and x[z+2]=='o'):
				present_bowler.append(x[pres_index+1:z])
				pres_index = z
				break
		for z in range(pres_index+1,len(x)):
			if(x[z]==' '):
				tos.append(x[pres_index+1:z])
				pres_index = z
				break	
		for z in range(pres_index+1,len(x)):
			if(x[z]==','):
				present_batsman.append(x[pres_index+1:z])
				pres_index = z+1
				break	
		for z in range(pres_index+1,len(x)):
			if(x[z]==','):
				contents.append(x[pres_index+1:z])
				pres_index = z
				break	
			elif (x[z]=='!'):
				contents.append(x[pres_index+1:z])
				break
dataframe_pakinnings['first'] = present_bowl
dataframe_pakinnings['second'] = present_bowler
dataframe_pakinnings['third'] = present_batsman
dataframe_pakinnings['runs'] = contents
#print(dataframe_pakinnings)
indbowlers=set(present_bowler)
#print(indbowlers)
pakbatters=set(present_batsman)
#print(pakbatters)
comruns = {}
comruns['no run'] = 0
comruns['FOUR'] = 4
comruns['SIX'] = 6
comruns['3 runs'] = 3
comruns['2 runs'] = 2
comruns['1 run'] = 1
comruns['wide'] = 1
comruns['byes'] = 1
comruns['leg byes']=1
comruns['1 wides']=2
comruns['2 wides']=3
comruns['3 wides']=4
batterstatsballs={}
for i in pakbatters:
	batterstatsballs[i]=0
batterstatsruns={}
for i in pakbatters:
	batterstatsruns[i]=0
#Here we are finding how many balls are faced by pakistani Batters
for i in pakbatters:
	for j in range(0,len(dataframe_pakinnings)):
		if(i==dataframe_pakinnings['third'][j]):
			if(dataframe_pakinnings['runs'][j]=='wide'):
				continue
			elif(dataframe_pakinnings['runs'][j]=='no ball'):
				continue
			elif(dataframe_pakinnings['runs'][j]=='byes'):
				batterstatsballs[i]+=1
			elif(dataframe_pakinnings['runs'][j]=='leg byes'):
				batterstatsballs[i]+=1
			elif(dataframe_pakinnings['runs'][j][0:10]=='out Caught'):
				batterstatsballs[i]+=1
			elif(dataframe_pakinnings['runs'][j]=='out Bowled'):
				batterstatsballs[i]+=1
			elif(dataframe_pakinnings['runs'][j]=='out Lbw'):
				batterstatsballs[i]+=1
			else:
				batterstatsballs[i]+=1
#print(batterstatsballs)
#Here we are finding how many runs are scored by pakistani Batters
fours=[]
sixes=[]
out={}
for i in pakbatters:
	out[i]=" "
for i in pakbatters:
	fourscount=0
	sixescount=0
	for j in range(0,len(dataframe_pakinnings)):
		if(i==dataframe_pakinnings['third'][j]):
			if(dataframe_pakinnings['runs'][j]=='wide'):
				continue
			elif(dataframe_pakinnings['runs'][j]=='no ball'):
				continue
			elif(dataframe_pakinnings['runs'][j]=='byes'):
				continue
			elif(dataframe_pakinnings['runs'][j][0:10]=='out Caught'):
				outstats="c "+dataframe_pakinnings['runs'][j][14:]+" b "+dataframe_pakinnings['second'][j]
				out[i]=outstats
				continue
			elif(dataframe_pakinnings['runs'][j]=='out Bowled'):
				outstats="b "+dataframe_pakinnings['second'][j]
				out[i]=outstats
				continue
			elif(dataframe_pakinnings['runs'][j]=='out Lbw'):
				outstats="lbw "+"b "+dataframe_pakinnings['second'][j]
				out[i]=outstats
				continue
			else:
				batterstatsruns[i]+=comruns[dataframe_pakinnings['runs'][j]]
				if(dataframe_pakinnings['runs'][j]=='FOUR'):
					fourscount=fourscount+1
				if(dataframe_pakinnings['runs'][j]=='SIX'):
					sixescount=sixescount+1
	fours.append(fourscount)
	sixes.append(sixescount)
for i in out:
	if(out[i]==" "):
		out[i]="notout"
print(out)
#print(batterstatsruns)
print(fours)
print(sixes)
pakbatterss=[]
text="Batsmen"
for i in range(0,36):
	text=text+" "
text=text+'\t'+'\t'+'\t'+"Runs"
text=text+'\t'
text=text+"Balls"+'\t'
text=text+"Strikerate"+'\t'
text=text+"FOURS"+'\t'+"SIXES"+'\n'
pakbatters=list(pakbatters)
for i in pakbatters:
	space=40-len(i)
	spaceextra=""
	for j in range(0,space):
		spaceextra=spaceextra+" "
	pakbatterss.append(i+spaceextra)
batterstatsballslist=[]
for i in batterstatsballs:
	batterstatsballslist.append(batterstatsballs[i])
#print(batterstatsballslist)
batterstatsrunslist=[]
for i in batterstatsruns:
	batterstatsrunslist.append(batterstatsruns[i])
#print(batterstatsrunslist)
strikerate=[]
for i in range(0,len(batterstatsruns)):
	sr=round((batterstatsrunslist[i]/batterstatsballslist[i])*100,2)
	strikerate.append(sr)
score1=0
for i in batterstatsrunslist:
	score1=score1+i
outlist=[]
for i in pakbatters:
	outlist.append(out[i])
for i in range(0,len(pakbatterss)):
	#cricktxt=indbowlers[i]+spaceextra
	text=text+pakbatterss[i]+spaceextra+'\t'+str(batterstatsrunslist[i])+'\t'+str(batterstatsballslist[i])+'\t'+str(strikerate[i])+'\t'+'\t'+str(fours[i])+'\t'+str(sixes[i])+'\t'+outlist[i]+'\n'
	if(i==len(pakbatterss)-1):
		text=text+'\n'+'\n'+'\n'+'\n'+'\n'
with open("Scorecard.txt",'w') as file:
	file.write(text)
bowlerstatsballs={}
for i in indbowlers:
	bowlerstatsballs[i]=0
#print(bowlerstatsballs)
extras=0
bowlerstatsruns={}
for i in indbowlers:
	bowlerstatsruns[i]=0
#print(bowlerstatsruns)
#Here we are counting no of valid balls bowled by the bowler
for i in indbowlers:
	for j in range(0,len(dataframe_pakinnings)):
		if(i==dataframe_pakinnings['second'][j]):
			if(dataframe_pakinnings['runs'][j]=='wide'):
				extras=extras+1
			elif(dataframe_pakinnings['runs'][j]=='no ball'):
				extras=extras+1
			elif(dataframe_pakinnings['runs'][j]=='byes'):
				extras=extras+1
				bowlerstatsballs[i]+=1
			elif(dataframe_pakinnings['runs'][j]=='leg byes'):
				extras=extras+1
				batterstatsballs[i]+=1
			else:
				bowlerstatsballs[i]+=1
#print(bowlerstatsballs)
#print(extras)
indbowlers=list(indbowlers)
#Here we are finding out no of runs conceded by the bowler
for i in indbowlers:
	for j in range(0,len(dataframe_pakinnings)):
		if(i==dataframe_pakinnings['second'][j]):
			if(dataframe_pakinnings['runs'][j] in comruns):
				if(dataframe_pakinnings['runs'][j]=='byes'):
					continue
				else:
					bowlerstatsruns[i]+=comruns[dataframe_pakinnings['runs'][j]]
#print(bowlerstatsruns)

bowlerwickets={}
for i in indbowlers:
	bowlerwickets[i]=0
#print(bowlerwickets)
#Find no of wickets took ny the bowler
for i in indbowlers:
	for j in range(0,len(dataframe_pakinnings)):
		if(i==dataframe_pakinnings['second'][j]):
			if(dataframe_pakinnings['runs'][j][0:10]=='out Caught'):
				bowlerwickets[i]+=1
			elif(dataframe_pakinnings['runs'][j]=='out Bowled'):
				bowlerwickets[i]+=1
			elif(dataframe_pakinnings['runs'][j]=='out Lbw'):
				bowlerwickets[i]+=1
#print(bowlerwickets)
dataframe_indbowlers = pd.DataFrame()
bowlerstatsballslist=[]
for i in bowlerstatsballs:
	bowlerstatsballslist.append(bowlerstatsballs[i])
#print(bowlerstatsballslist)
bowlerstatsballslistpoint=[]
for i in bowlerstatsballslist:
	x=int(i/6)
	y=i%6
	z=str(x)+"."+str(y)
	bowlerstatsballslistpoint.append(z)
print(bowlerstatsballslistpoint)
bowlerstatsrunslist=[]
for i in bowlerstatsruns:
	bowlerstatsrunslist.append(bowlerstatsruns[i])
#print(bowlerstatsrunslist)
bowlerwicketslist=[]
for i in bowlerwickets:
	bowlerwicketslist.append(bowlerwickets[i])
#print(bowlerwicketslist)
wicket1=0
for i in bowlerwicketslist:
	wicket1=wicket1+i
#This shall be the last lines of the code.
#print('Duration of Program Execution: {}'.format(end_time - start_time))
dataframe_pakinnings.to_excel("xyz.xlsx",index=False)
text="Bowler"
for i in range(0,36):
	text=text+" "
text=text+'\t'+'\t'+'\t'+"Balls"
text=text+'\t'
text=text+"Runs"+'\t'
text=text+"Wickets"+'\n'
indbowlerss=[]
for i in indbowlers:
	space=40-len(i)
	spaceextra=""
	for j in range(0,space):
		spaceextra=spaceextra+" "
	indbowlerss.append(i+spaceextra)
for i in range(0,len(indbowlerss)):
	#cricktxt=indbowlers[i]+spaceextra
	text=text+indbowlerss[i]+spaceextra+"\t"+str(bowlerstatsballslistpoint[i])+'\t'+str(bowlerstatsrunslist[i])+'\t'+str(bowlerwicketslist[i])+'\n'
	if(i==len(indbowlerss)-1):
		text=text+'\n'+'\n'
p="Extras"+"   -   "+str(extras)
text=text+p+'\n'+'\n'
text=text+"PAK  -     "+str(score1+extras)+"/"+str(wicket1)
text=text+'\n'+'\n'+'\n'+'\n'+'\n'
score1=score1+extras
with open("Scorecard.txt",'a') as file:
	file.write(text)


dataframe_indinnings = pd.DataFrame()
f=open("india_inns2.txt","r")
lines=f.readlines()
f.close()
result=[]
present_bowl = []
present_bowler = []
tos = []
present_batsman = []
contents = []
for x in lines:
	if (len(x)>1):
		pres_index = 0
		if (x[3]==' '):
			pres_index = 3
			present_bowl.append(x[0:3])
		else :
			pres_index = 4
			present_bowl.append(x[0:4])
		for z in range(pres_index+1,len(x)):
			if(x[z]==' ' and x[z+1]=='t' and x[z+2]=='o'):
				present_bowler.append(x[pres_index+1:z])
				pres_index = z
				break
		for z in range(pres_index+1,len(x)):
			if(x[z]==' '):
				tos.append(x[pres_index+1:z])
				pres_index = z
				break	
		for z in range(pres_index+1,len(x)):
			if(x[z]==','):
				present_batsman.append(x[pres_index+1:z])
				pres_index = z+1
				break	
		for z in range(pres_index+1,len(x)):
			if(x[z]==','):
				contents.append(x[pres_index+1:z])
				pres_index = z
				break	
			elif (x[z]=='!'):
				contents.append(x[pres_index+1:z])
				break
dataframe_indinnings['first'] = present_bowl
dataframe_indinnings['second'] = present_bowler
dataframe_indinnings['third'] = present_batsman
dataframe_indinnings['runs'] = contents
#print(dataframe_indinnings)
pakbowlers=set(present_bowler)
#print(pakbowlers)
indbatters=set(present_batsman)
#print(indbatters)
batterstatsballs={}
for i in indbatters:
	batterstatsballs[i]=0
batterstatsruns={}
for i in indbatters:
	batterstatsruns[i]=0
#Finding no of balls faced by the batsmen
for i in indbatters:
	for j in range(0,len(dataframe_indinnings)):
		if(i==dataframe_indinnings['third'][j]):
			if(dataframe_indinnings['runs'][j]=='wide'):
				continue
			elif(dataframe_indinnings['runs'][j]=='1 wides'):
				continue
			elif(dataframe_indinnings['runs'][j]=='2 wides'):
				continue
			elif(dataframe_indinnings['runs'][j]=='3 wides'):
				continue
			elif(dataframe_indinnings['runs'][j]=='no ball'):
				continue
			elif(dataframe_indinnings['runs'][j]=='byes'):
				batterstatsballs[i]+=1
			elif(dataframe_indinnings['runs'][j]=='leg byes'):
				batterstatsballs[i]+=1
			elif(dataframe_indinnings['runs'][j][0:10]=='out Caught'):
				batterstatsballs[i]+=1
			elif(dataframe_indinnings['runs'][j]=='out Bowled'):
				batterstatsballs[i]+=1
			elif(dataframe_indinnings['runs'][j]=='out Lbw'):
				batterstatsballs[i]+=1
			else:
				batterstatsballs[i]+=1
#print(batterstatsballs)
#Finding no of runs scored by the batsmen
fours=[]
sixes=[]
out={}
for i in indbatters:
	out[i]=" "
for i in indbatters:
	fourscount=0
	sixescount=0
	for j in range(0,len(dataframe_indinnings)):
		if(i==dataframe_indinnings['third'][j]):
			if(dataframe_indinnings['runs'][j]=='wide'):
				continue
			elif(dataframe_indinnings['runs'][j]=='no ball'):
				continue
			elif(dataframe_indinnings['runs'][j]=='byes'):
				continue
			elif(dataframe_indinnings['runs'][j][0:10]=='out Caught'):
				outstats="c "+dataframe_indinnings['runs'][j][14:]+" b "+dataframe_indinnings['second'][j]
				out[i]=outstats
				continue
			elif(dataframe_indinnings['runs'][j]=='out Bowled'):
				outstats="b "+dataframe_indinnings['second'][j]
				out[i]=outstats
				continue
			elif(dataframe_indinnings['runs'][j]=='out Lbw'):
				outstats="lbw "+"b "+dataframe_indinnings['second'][j]
				out[i]=outstats
				continue
			elif(dataframe_indinnings['runs'][j]=='leg byes'):
				continue
			elif(dataframe_indinnings['runs'][j]=='1 wides'):
				continue
			elif(dataframe_indinnings['runs'][j]=='2 wides'):
				continue
			elif(dataframe_indinnings['runs'][j]=='3 wides'):
				continue
			else:
				batterstatsruns[i]+=comruns[dataframe_indinnings['runs'][j]]
				if(dataframe_indinnings['runs'][j]=='FOUR'):
					fourscount=fourscount+1
				if(dataframe_indinnings['runs'][j]=='SIX'):
					sixescount=sixescount+1
	fours.append(fourscount)
	sixes.append(sixescount)
for i in out:
	if(out[i]==" "):
		out[i]="notout"
print(out)
#print(batterstatsruns)
indbatterss=[]
text="Batsmen"
for i in range(0,36):
	text=text+" "
text=text+'\t'+'\t'+'\t'+"Runs"
text=text+'\t'
text=text+"Balls"+'\t'
text=text+"Strikerate"+'\t'
text=text+"FOURS"+'\t'+"SIXES"+'\n'
indbatters=list(indbatters)
for i in indbatters:
	space=40-len(i)
	spaceextra=""
	for j in range(0,space):
		spaceextra=spaceextra+" "
	indbatterss.append(i+spaceextra)
batterstatsballslist=[]
for i in batterstatsballs:
	batterstatsballslist.append(batterstatsballs[i])
#print(batterstatsballslist)
batterstatsrunslist=[]
for i in batterstatsruns:
	batterstatsrunslist.append(batterstatsruns[i])
#print(batterstatsrunslist)
strikerate=[]
for i in range(0,len(batterstatsruns)):
	sr=round((batterstatsrunslist[i]/batterstatsballslist[i])*100,2)
	strikerate.append(sr)
score2=0
for i in batterstatsrunslist:
	score2=score2+i
outlist=[]
for i in indbatters:
	outlist.append(out[i])
for i in range(0,len(indbatterss)):
	#cricktxt=indbowlers[i]+spaceextra
	text=text+indbatterss[i]+spaceextra+'\t'+str(batterstatsrunslist[i])+'\t'+str(batterstatsballslist[i])+'\t'+str(strikerate[i])+'\t'+'\t'+str(fours[i])+'\t'+str(sixes[i])+'\t'+outlist[i]+'\n'
	if(i==len(indbatterss)-1):
		text=text+'\n'+'\n'+'\n'+'\n'+'\n'
with open("Scorecard.txt",'a') as file:
	file.write(text)
bowlerstatsballs={}
for i in pakbowlers:
	bowlerstatsballs[i]=0
#print(bowlerstatsballs)
extras=0
bowlerstatsruns={}
for i in pakbowlers:
	bowlerstatsruns[i]=0
#print(bowlerstatsruns)
#Here we are counting no of valid balls bowled by the bowler
for i in pakbowlers:
	for j in range(0,len(dataframe_indinnings)):
		if(i==dataframe_indinnings['second'][j]):
			if(dataframe_indinnings['runs'][j]=='wide'):
				extras=extras+1
			elif(dataframe_indinnings['runs'][j]=='no ball'):
				extras=extras+1
			elif(dataframe_indinnings['runs'][j]=='byes'):
				extras=extras+1
				bowlerstatsballs[i]+=1
			elif(dataframe_indinnings['runs'][j]=='leg byes'):
				extras=extras+1
				bowlerstatsballs[i]+=1
			elif(dataframe_indinnings['runs'][j]=='1 wides'):
				extras=extras+comruns[dataframe_indinnings['runs'][j]]
			elif(dataframe_indinnings['runs'][j]=='2 wides'):
				extras=extras+comruns[dataframe_indinnings['runs'][j]]
			elif(dataframe_indinnings['runs'][j]=='3 wides'):
				extras=extras+comruns[dataframe_indinnings['runs'][j]]
			else:
				bowlerstatsballs[i]+=1
#print(bowlerstatsballs)
#print(extras)
pakbowlers=list(pakbowlers)
#Finding runs conceded by the bowler
for i in pakbowlers:
	for j in range(0,len(dataframe_indinnings)):
		if(i==dataframe_indinnings['second'][j]):
			if(dataframe_indinnings['runs'][j] in comruns):
				if(dataframe_indinnings['runs'][j]=='byes'):
					continue
				elif(dataframe_indinnings['runs'][j]=='leg byes'):
					continue
				elif(dataframe_indinnings['runs'][j]=='wide'):
					bowlerstatsruns[i]+=comruns[dataframe_indinnings['runs'][j]]
				elif(dataframe_indinnings['runs'][j]=='1 wides'):
					continue
				elif(dataframe_indinnings['runs'][j]=='2 wides'):
					bowlerstatsruns[i]+=comruns[dataframe_indinnings['runs'][j]]
					continue
				elif(dataframe_indinnings['runs'][j]=='3 wides'):
					bowlerstatsruns[i]+=comruns[dataframe_indinnings['runs'][j]]
					continue
				else:
					bowlerstatsruns[i]+=comruns[dataframe_indinnings['runs'][j]]
#print(bowlerstatsruns)
bowlerwickets={}
for i in pakbowlers:
	bowlerwickets[i]=0
#print(bowlerwickets)
#Finding the no of wickets took by the bowler
for i in pakbowlers:
	for j in range(0,len(dataframe_indinnings)):
		if(i==dataframe_indinnings['second'][j]):
			if(dataframe_indinnings['runs'][j][0:10]=='out Caught'):
				bowlerwickets[i]+=1
			elif(dataframe_indinnings['runs'][j]=='out Bowled'):
				bowlerwickets[i]+=1
			elif(dataframe_indinnings['runs'][j]=='out Lbw'):
				bowlerwickets[i]+=1
#print(bowlerwickets)
bowlerstatsballslist=[]
for i in bowlerstatsballs:
	bowlerstatsballslist.append(bowlerstatsballs[i])
#print(bowlerstatsballslist)
bowlerstatsballslistpoint=[]
for i in bowlerstatsballslist:
	x=int(i/6)
	y=i%6
	z=str(x)+"."+str(y)
	bowlerstatsballslistpoint.append(z)
print(bowlerstatsballslistpoint)
bowlerstatsrunslist=[]
for i in bowlerstatsruns:
	bowlerstatsrunslist.append(bowlerstatsruns[i])
#print(bowlerstatsrunslist)
bowlerwicketslist=[]
for i in bowlerwickets:
	bowlerwicketslist.append(bowlerwickets[i])
#print(bowlerwicketslist)
wicket2=0
for i in bowlerwicketslist:
	wicket2=wicket2+i
text="Bowler"
for i in range(0,36):
	text=text+" "
text=text+'\t'+'\t'+'\t'+"Balls"
text=text+'\t'
text=text+"Runs"+'\t'
text=text+"Wickets"+'\n'
pakbowlerss=[]
for i in pakbowlers:
	space=40-len(i)
	spaceextra=""
	for j in range(0,space):
		spaceextra=spaceextra+" "
	pakbowlerss.append(i+spaceextra)
for i in range(0,len(pakbowlerss)):
	#cricktxt=indbowlers[i]+spaceextra
	text=text+pakbowlerss[i]+spaceextra+'\t'+str(bowlerstatsballslistpoint[i])+'\t'+str(bowlerstatsrunslist[i])+'\t'+str(bowlerwicketslist[i])+'\n'
	if(i==len(pakbowlerss)-1):
		text=text+'\n'+'\n'
p="Extras"+"   -   "+str(extras+1)
text=text+p+'\n'+'\n'
text=text+"IND  -     "+str(score2+extras+1)+"/"+str(wicket2)+'\n'+'\n'
score2=score2+extras
if(score1>score2):
	text=text+"PAK won the match"
else:
	text=text+"IND won the match"
with open("Scorecard.txt",'a') as file:
	file.write(text)

end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))