import pandas as pd
import Stemmer
stemmer = Stemmer.Stemmer('english')
def symp_finder(text,lang):
	df=pd.read_csv('sub_app/py_templates/urdu_symptoms.csv')
	df.drop('ur_symp',axis=1,inplace=True)
	if lang=='en-US':#english
		df.drop(['roman_symp'],axis=1,inplace=True)

		df.columns=['doctor','symp']
		df.symp=df.symp.str.split(',')
		df.symp=df.symp.apply(lambda x:[stemmer.stemWord(i) for i in x])
		text=text.lower().split()
		text=[stemmer.stemWord(i) for i in text]
		print(text)
	elif lang=='en-IN':#urdu
		df.drop(['en_symp'],axis=1,inplace=True)
		df.columns=['doctor','symp']
		text=text.lower().split()
		df.symp=df.symp.str.split(',')
	try:
		
		
		print(df)
		print(text)
		df.symp=df.symp.apply(lambda x: [i.strip() for i in x])
		result=df.symp.apply(lambda x: set(x) & set(text)).dropna()
		result=df['doctor'][result.map(lambda d: len(d)) > 0]
		print('text is', list(result)[0])
		return list(result)[0]
	except: 
		return None
#print(symp_finder("mere pait mein dard horahee hai"))