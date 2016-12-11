Project: How Far have Cars driven the Nature!

author: F16-IG-3020, Aditya Tanikanti, atanikan@iu.edu   
author: F16-IG-3005, Amruta Chavan, amchavan@iu.edu

Project Type: Analytics

Problem:This project will throw light on how much and how badly are automobiles affecting the environment and causing Global Warming. 
        We will try to find some fuel efficient cars and features of cars which cause pollution such as CO2 emission over the years. 
        We will also explore other important relationships we found in the data and model it so as to predict the smog score of a vehicle given its features.
        
Abstract: This project provides an insight into the fuel consumption and carbon emission by different car models driven in the US. 
          It analyses and compares performance of different types of cars based on types,brands and other specifications.
          The project will throw light on how much and how badly are automobiles affecting the environment and causing global warming by releasing CO2 and smog. 
          It tries to find some fuel efficient cars and/or alternate solutions to avoid further damage to nature. 
          Other important relationships and correlations between the various features will be explored through the built model and thus eventually predict smog rating given car features. 
          
References: https://gitlab.com/cloudmesh_fall2016/project-018/blob/master/report/references.bib

Deliverables:

    Environment: Python
    Requirements and Running:
            1) Download data either from website links provided below or data folder in repository ((Updated Data: Tuesday November 22 2016))
               The data is not huge hence is placed in the data folder.
            
               https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip
               https://www.fueleconomy.gov/feg/epadata/emissions.csv.zip
               
            2) System Requirements to run the project
            	Java SE Development Kit(7+)
            	Scala Build Tool(optional)
            	Spark 2.0.1(optional)
            	Python 2.7
            	Jupyter Notebook
            
            3) We have integrated pyspark for parallel processing however it's an optional feature. To download it properly in windows follow
            
            	https://www.dataquest.io/blog/pyspark-installation-guide/
            
            4) Download packages for python on anaconda by running which is found code folder
                
               pip install requirements.txt
            
            5) To run the code go to the code folder ,look or find the comment "change path here" in project-018.py or project-018.pynb file and paste the path of the location where you downloaded the data.

            6) The code/markdown folder has all the images and a project-018.md file which highlights the code from ipython notebook
            
            7) All other images are in the code/images folder

            
    Environment: D3
    Requirements and Running:
            1) Download all files from code/D3_HTML_FILES location( including the csv file as it's responsible for generating one of the visualization) all into the 
               same local drive
            
            2) To get d3 visualizations to run in windows first run the command below from a location where you downloaded the files using cmd(windows) or equivalent
            
            	'python -m SimpleHTTPServer 8888 &' 
            	
            	This starts server and helps in connecting browser to local files
            	
            3)	These links will trigger the html files and will generate the interactive visuals
            	
            	http://localhost:8888/files/type_emission_per_year.html
            	http://localhost:8888/files/make_emission.html
            
            4) The folder code/D3_HTML_FILES also has images which denote how the visualization looks.
            	

            
    Environment: R
    Requirements and Running:
            1) Install and/or include library packages namely: tidyverse,ggplot2,stat.
            
            2) Load CSV files mentioned below:
                a) Vehicles.csv
                b) FuelEconomyData.csv
                c) co2_fuel_aggr.csv
                
            Note: FuelEconomyData.csv and co2_fuel_aggr.csv and clean, consolidated and derived datasets from the original dataset for better data analysis and visualization.
            
            3) Find all the images and visualizations in the images folder.
            
            4) DescriptiveAnalysis.R can run without RMArkdown supporting packages.
            
            5) R Markdown file which consolidates all the R code and Plots is also included alongwith its PDF output.(To Execute R Markdown file RMarkdown and Tex packages are required)
