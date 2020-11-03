import pandas as pd



def symp_finder(text):
	#gist_file = open("sub_app/py_templates/stopwords.txt", "r")
	gist_file = open("sub_app/py_templates/stopwords.txt", "r")
	try:
	    content = gist_file.read()
	    stopwords = content.split(",")
	finally:
	    gist_file.close()

	stopwords=[i.replace('"',"").strip() for i in stopwords]
	#df2=pd.read_csv('sub_app/py_templates/final.csv')

	df2=pd.read_csv('sub_app/py_templates/final.csv')
	df2['doctor']=df2['doctor'].str.title()
	df2['Disease']=df2['Disease'].str.title()
	df2=df2.groupby(['Disease','doctor'])['Symptoms'].apply(list).reset_index()
	df2['Symptoms']=df2['Symptoms'].apply(lambda x:[str(i).split() for i in x] )
	df2['Symptoms']=df2['Symptoms'].apply(lambda x:[item for sublist in x for item in sublist])


	text=[i for i in text.lower().split() if i not in stopwords]
	print(text)
	df3=df2.copy()
	df3['match']=df3['Symptoms'].apply(lambda x:list( set(x) & set(text)))
	df3['match_len']=df3['match'].apply(lambda x:len(x))
	df3=df3[df3['match_len']!=0]
	df3=df3.sort_values(by=['match_len'],ascending=False)

	df3['diff']=df3['match_len'].diff()
	df3.reset_index(drop=True,inplace=True)
	for i in range(len(df3)):
	    if df3['diff'][i]<0:
	        break
	        
	return df3.iloc[0:i-1,0:2]