## P6: Make Effective Data Visualization
by Yuheng Cai

### Summary
The sinking of the RMS Titanic is one of the most infamous shipwrecks in history.  On April 15, 1912, during her maiden voyage, the Titanic sank after colliding with an iceberg, killing 1502 out of 2224 passengers and crew. This sensational tragedy shocked the international community and led to better safety regulations for ships.  

This data Visualization shows the demographics and passenger information between those passengers who survived and those who died. The Titanic dataset is downloaded from [Kaggle](https://www.kaggle.com/c/titanic).

### Design
##### Story to Tell - Findings from Exploratory Data Analysis  
* Female passengers had higher chance to survive
* Higher class passengers were more likely to survive

Details of the EDA can be found from:  
[Udacity Data Analyst Nanodegree - P2 Titanic Dataset Analysis by Yuheng Cai](https://github.com/waldlecai/Udacity-Data-Analyst/blob/master/p2_data_analysis_Python/P2_Investigate_a_Dataset.html)

##### Initial Design Decision
index_0.html reflects the initial design decision in order to convey the key findings mentioned above.

* Bar chart type is selected to compare between passengers who survived and died.  
* Multiple bar charts will be needed and grouped based on categorical variables (i.e. PassengerClass, Sex) in order to drill down the comparison in each category.
* Color will be used for differentiating survived and died only; but not for categorical variables since grouping should do the job.  
* Labels for legend and axis should be kept concise

### Feedback
After initial design (index_0.html) was completed, three reviewers were interviewed, each of which was briefly introduced to the overview of the project and Titanic tragedy. After the briefing, reviewers had the chance to interact with the data Visualization and provided following Feedback.  

##### Feedback 1
"This bar chart is quite different from what I normally see. It took a while for me to understand the meaning of grouped bar. But after interacting with visualization, the tool tip when hovering on the bar explains well."  

##### Feedback 2
"The legend in '1'/'0' is weird. I had to ask what that means. But once that definition is explained, the message of the whole chart becomes clear."  

##### Feedback 3
"The legend is certainly not right coz it's not self explained with '1'/'0' representing passengers who survived or died. Font size of legend and axis labels is too small compared with the overall chart size. The grouping of bars make a lot of sense"  

##### Design Revision
While the use of 'grouped bar' takes the reviewers a while to interpret the comparison, but once they got that the grouping and color really make the key finding of data stand out. So I sticked to the grouped bar. The horizontal orientation receives positive feedback too.

The final revision made on the visualization is all around labels:
* font size was made bigger for both legend and axis  
* Legend labels '1'/'0' was changed to 'survived'/'Died' respectively for easier interpretation

### Resource
- [Udacity Data Analyst Nanodegree - P2 Titanic Dataset Analysis](https://github.com/waldlecai/Udacity-Data-Analyst/blob/master/p2_data_analysis_Python/P2_Investigate_a_Dataset.html)
- [dimple.js Documentation](http://dimplejs.org/)
