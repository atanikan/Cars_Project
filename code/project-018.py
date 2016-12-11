# coding: utf-8

# #IMPORTS FOR SPARK AND OTHER PYTHON PACKAGES 

# In[914]:

#Get spark/spark home from enviroment and execute spark
import os
import sys


# In[915]:

#Change the path here
MY_PY4j_PATH = 'C:\\spark-2.0.1-bin-hadoop2.7\\python\\lib\\py4j-0.10.3-src.zip'
spark_home = os.environ.get('SPARK_HOME', None)
print(spark_home)
if not spark_home:
    raise ValueError('SPARK_HOME environment variable is not set')

sys.path.insert(0, os.path.join(spark_home,
                                
                                'python'))

## may need to adjust on your system depending on which Spark version you're using and where you installed it.
sys.path.insert(0, os.path.join(spark_home, MY_PY4j_PATH)) 

execfile(os.path.join(spark_home, 'python/pyspark/shell.py'))


# In[916]:

#change path here
#Directories
MY_VEHICLES_CSV_DATA_DIR = 'C:\\Users\\Aditya\\Desktop\\Big_Data_Analytics\\final_project\\Data\\'
vehicles_path = os.path.join(MY_VEHICLES_CSV_DATA_DIR, 'vehicles.csv')
emissions_path = os.path.join(MY_VEHICLES_CSV_DATA_DIR, 'emissions.csv')


# In[917]:

#Necessary Import
import numpy as np
import pandas as pd
import matplotlib as plt
get_ipython().magic(u'matplotlib inline')
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import pie, axis, show
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report
from collections import defaultdict


# In[918]:

import sys, getopt, pprint
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark import SparkConf
from pyspark import SparkContext
conf=(SparkConf().setMaster("local").setAppName("Cars").set("spark.executor.memory","1g"))
sqlContext = SQLContext(sc)


# # DATA EXTRACTION AND MANIPULATION

# In[919]:

vehicles = sc.textFile(vehicles_path)
print vehicles.count()


# In[920]:

header = vehicles.first()
fields = [StructField(field_name, StringType(), True) for field_name in header.split(',')]
print len(fields)


# In[921]:

#create schema
schema = StructType(fields)
#vehicles file without header
vehicleHeader = vehicles.filter(lambda l: 'barrels08' in l)
vehcilesNoHeader = vehicles.subtract(vehicleHeader)
print vehcilesNoHeader.take(1)


# In[922]:

vehicles_df = pd.read_csv(vehicles_path)
emission_df = pd.read_csv(emissions_path)


# In[923]:

#prints information about dataframe along with percentage of null values
def getDfInfo(df):
    nrow = df.shape[0]
    print "\n*****SHAPE********"
    print df.shape
    print "*****NULL PERCENTAGE*********"
    print df.isnull().sum() / nrow


# In[924]:

print getDfInfo(vehicles_df)


# # EXPLORATORY DATA ANALYSIS

# In[925]:

#deleteing columns with more than 1 NA
vehicles_df= vehicles_df.dropna(thresh=len(vehicles_df) - 1, axis=1)


# In[926]:

getDfInfo(vehicles_df)


# In[927]:

vehicle_emission_df = pd.merge(vehicles_df, emission_df[['score','scoreAlt','id']], how ='left', 
                                                      on=['id'])


# In[928]:

vehicle_emission_df.head()


# In[929]:

makecount = pd.value_counts(vehicle_emission_df['make'].values, sort=False)
makecount = makecount.to_frame().reset_index()
makecount.columns = ('make','count')
makecount = makecount[makecount['count']>500]


# In[930]:

plt.figure(figsize=(8, 8))
pie(makecount['count'], labels=makecount['make']);
show()


# In[931]:

vclass_co2_df = vehicle_emission_df[vehicle_emission_df['co2'] >= 0]
vclass_co2_df=pd.DataFrame(vclass_co2_df.groupby(vclass_co2_df['VClass'])['co2'].mean().reset_index())


# In[932]:

group_data1 = vclass_co2_df.sort('co2',ascending=False)[0:5]


# In[933]:

group_data2 = vclass_co2_df.sort('co2',ascending=True)[0:5]


# In[934]:

#5 Car vehicle class with highest CO2 emission
sns.barplot(x='VClass', y='co2', data=group_data1 , label='make')
plt.figure(figsize=(8, 8))
plt.savefig("Car_vehicle_class_highest_CO2_emission.png")


# In[935]:

#5 Car vehicle class with lowest CO2 emission
sns.barplot(x='VClass', y='co2', data=group_data2)
plt.figure(figsize=(8, 8))
plt.savefig("Car_vehicle_class_with_lowest_CO2_emission.png")


# In[936]:

make_co2_df = vehicle_emission_df[vehicle_emission_df['co2'] >= 0]
make_co2_df=pd.DataFrame(make_co2_df.groupby(make_co2_df['make'])['co2'].mean().reset_index())


# In[937]:

group_data1 = make_co2_df.sort('co2',ascending=False)[0:5]


# In[938]:

group_data2 = make_co2_df.sort('co2',ascending=True)[0:5]


# In[939]:

#5 Car vehicle class with highest CO2 emission
sns.barplot(x='make', y='co2', data=group_data1 , label='make')
plt.figure(figsize=(8, 8))
plt.savefig("Car_vehicle_make_highest_CO2_emission.png")


# In[940]:

#5 Car vehicle class with lowest CO2 emission
sns.barplot(x='make', y='co2', data=group_data2)
plt.figure(figsize=(8, 8))
plt.savefig("Car_vehicle_make_with_lowest_CO2_emission.png")


# In[941]:

fuel_type_co2_df = vehicle_emission_df[vehicle_emission_df['co2'] >= 0]
fuel_type_co2_df=pd.DataFrame(fuel_type_co2_df.groupby(fuel_type_co2_df['fuelType'])['co2'].mean().reset_index())



# In[942]:

group_data1 = fuel_type_co2_df.sort('co2',ascending=False)[0:5]
group_data2 = fuel_type_co2_df.sort('co2',ascending=True)[0:5]


# In[943]:

#5 Car vehicle fuel type with highest CO2 emission
sns.barplot(x='fuelType', y='co2', data=group_data1 , label='Fuel Type')
plt.savefig("Car_vehicle_fuel_type_highest_CO2_emission.png")


# In[944]:

#5 Car vehicle fuel type with lowest CO2 emission
sns.barplot(x='fuelType', y='co2', data=group_data2)
plt.savefig("Car_vehicle_fuel_type_with_lowest_CO2_emission.png")


# In[945]:


#How You save spend has varied over years

sns.factorplot(data=vehicle_emission_df, x="year", y="fuelCost08",size=4, aspect=2,label = 'FuelCost vs Year')  
plt.savefig("fuelCostOvertheYears.png")


# In[946]:

sns.factorplot(data=vehicle_emission_df, x="year", y="co2TailpipeGpm",size=4, aspect=2,label = 'co2TailPipe vs Year')  
plt.savefig("co2OvertheYears.png")


# In[947]:

#As score ranges from 1 to 10 remove rows having -2 and -12
vehicle_emission_df_save_spend  = vehicle_emission_df[vehicle_emission_df.score>0]
sns.factorplot(data=vehicle_emission_df_save_spend, x="year", y="youSaveSpend",size=4, aspect=2,label = 'SaveSpend vs Year')
plt.savefig("youSaveSpendOverYears.png")


# # FEATURE EXTRACTION FOR MODELLING

# In[948]:

#Modelling Data to predict 

#Feature Selection 
#removing columns with NA and replacing -1 with 0 i.e. missing data
vehicle_emission_df= vehicle_emission_df.dropna(axis=0)
vehicle_emission_df = vehicle_emission_df.replace(-1,0)


# In[949]:

#prints information about dataframe along with percentage of null values
def getDfZeroInfo(df):
    nrow = df.shape[0]
    print "\n*****SHAPE********"
    print df.shape
    print "*****Zero PERCENTAGE*********"
    print (df.shape[0] - df.astype(bool).sum(axis=0))/nrow
getDfZeroInfo(vehicle_emission_df)


# In[950]:

#Selecting columns with less than 30% of zeroes in their data 
columns_to_select = (vehicle_emission_df.shape[0] - vehicle_emission_df.astype(bool).sum(axis=0))/vehicle_emission_df.shape[0]
columns_to_select = np.where(columns_to_select.values<0.30,columns_to_select.index,None)
columns_to_select = columns_to_select[columns_to_select != np.array(None)]
print columns_to_select


# In[951]:

#Removing ids and dates as they do not contribute to our prediction
vehicle_emission_df = vehicle_emission_df[['barrels08', 'city08', 'co2TailpipeGpm' ,'comb08'
, 'fuelCost08' ,'fuelType' ,'fuelType1' ,'highway08','make',
 'model' ,'UCity' ,'UHighway' ,'VClass' ,'year', 'youSaveSpend', 'score']]


# In[952]:

getDfInfo(vehicle_emission_df)


# In[953]:

#5 Distribution of Class variable
count_of_class_df=pd.DataFrame(vehicle_emission_df.groupby(vehicle_emission_df['score']).count().reset_index())
sns.barplot(x='score', y='make', data=count_of_class_df , label='Count of Scores')
plt.savefig("Distribution_of_Scores.png")


# In[954]:

#preprocessing data
#converting all categorical to discrete
vehicle_emission_df = vehicle_emission_df[vehicle_emission_df['score']>0]
d = defaultdict(preprocessing.LabelEncoder)
vehicle_emission_encoded_df = vehicle_emission_df[['fuelType' ,'fuelType1','make',
 'model' ,'VClass' ,'year']].apply(lambda x: d[x.name].fit_transform(x))

vehicle_emission_encoded_df_full = vehicle_emission_encoded_df.join(vehicle_emission_df[['barrels08', 'city08', 'co2TailpipeGpm' ,'comb08'
, 'fuelCost08' , 'highway08', 'UCity' ,'UHighway' , 'youSaveSpend','score']])

vehicle_emission_encoded_df_full.head()
# Inverse the encoded
#fit.apply(lambda x: d[x.name].inverse_transform(x))

# Using the dictionary to label future data
#df.apply(lambda x: d[x.name].transform(x))



# # DATA MODELING

# In[955]:

#train test split
vehicle_emission = vehicle_emission_encoded_df_full.ix[:,0:15]
vehicle_emission_score = vehicle_emission_encoded_df_full.ix[:,15:16]
X_train, X_test, y_train, y_test = train_test_split(vehicle_emission, vehicle_emission_score, test_size=0.2, random_state=0)
X_train.shape


# In[956]:

#normalizing the data on X_train and X_test
min_max=preprocessing.MinMaxScaler()
X_train_minmax=min_max.fit_transform(X_train[['barrels08', 'city08', 'co2TailpipeGpm' ,'comb08'
, 'fuelCost08' , 'highway08', 'UCity' ,'UHighway' , 'youSaveSpend']])
X_test_minmax=min_max.fit_transform(X_test[['barrels08', 'city08', 'co2TailpipeGpm' ,'comb08'
, 'fuelCost08' , 'highway08', 'UCity' ,'UHighway' , 'youSaveSpend']])
X_train_minmax


# In[957]:

#let's consider the base class
y_train.score.value_counts()/y_train.score.count() 


# In[958]:

#KNN on MultiClass
knn=KNeighborsClassifier(n_neighbors=10)
y_pred = knn.fit(X_train_minmax,y_train.values.ravel()).predict(X_test_minmax)
print accuracy_score(y_test,y_pred)
print classification_report(y_test, y_pred) 


# In[959]:

#Multinomial NB
mnb = MultinomialNB()
y_pred = mnb.fit(X_train_minmax, y_train.values.ravel()).predict(X_test_minmax)
print '********Multinomial Naive Bayes***********'
print accuracy_score(y_test,y_pred)
print classification_report(y_test, y_pred) 


# In[960]:

#Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100)
y_pred = clf.fit(X_train_minmax, y_train.values.ravel()).predict(X_test_minmax)
print '********Random Forest Classifier***********'
print accuracy_score(y_test,y_pred)
print classification_report(y_test, y_pred)


# In[961]:

#Logistic Regression
lg = LogisticRegression(multi_class = 'multinomial',solver='newton-cg')
y_pred = lg.fit(X_train_minmax, y_train.values.ravel()).predict(X_test_minmax)
print '********Logistic Regression Classifier***********'
print accuracy_score(y_test,y_pred)
print(classification_report(y_test, y_pred))


# In[962]:

#Support Vector Machines
svc = SVC()
y_pred = svc.fit(X_train_minmax, y_train.values.ravel()).predict(X_test_minmax)
print '********Support Vector Machines Classifier***********'
print accuracy_score(y_test,y_pred)
print(classification_report(y_test, y_pred))


# In[963]:

#Decision Tree Classifier
dc = DecisionTreeClassifier()
y_pred = dc.fit(X_train_minmax, y_train.values.ravel()).predict(X_test_minmax)
print '********Decision Tree Classifier***********'
print accuracy_score(y_test,y_pred)
print(classification_report(y_test, y_pred))


# # Exporting Data for Visualizations using D3.js  

# In[ ]:

make_emission = pd.DataFrame(vehicle_emission_df.groupby(['make'])['co2TailpipeGpm'].sum())
make_emission.to_csv('make_emission.csv')


# In[ ]:



