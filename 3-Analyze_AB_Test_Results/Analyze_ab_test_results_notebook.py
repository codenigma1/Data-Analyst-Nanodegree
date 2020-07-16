#!/usr/bin/env python
# coding: utf-8

# ## Analyze A/B Test Results
# 
# You may either submit your notebook through the workspace here, or you may work from your local machine and submit through the next page.  Either way assure that your code passes the project [RUBRIC](https://review.udacity.com/#!/projects/37e27304-ad47-4eb0-a1ab-8c12f60e43d0/rubric).  **Please save regularly.**
# 
# This project will assure you have mastered the subjects covered in the statistics lessons.  The hope is to have this project be as comprehensive of these topics as possible.  Good luck!
# 
# ## Table of Contents
# - [Introduction](#intro)
# - [Part I - Probability](#probability)
# - [Part II - A/B Test](#ab_test)
# - [Part III - Regression](#regression)
# 
# 
# <a id='intro'></a>
# ### Introduction
# 
# A/B tests are very commonly performed by data analysts and data scientists.  It is important that you get some practice working with the difficulties of these 
# 
# For this project, you will be working to understand the results of an A/B test run by an e-commerce website.  Your goal is to work through this notebook to help the company understand if they should implement the new page, keep the old page, or perhaps run the experiment longer to make their decision.
# 
# **As you work through this notebook, follow along in the classroom and answer the corresponding quiz questions associated with each question.** The labels for each classroom concept are provided for each question.  This will assure you are on the right track as you work through the project, and you can feel more confident in your final submission meeting the criteria.  As a final check, assure you meet all the criteria on the [RUBRIC](https://review.udacity.com/#!/projects/37e27304-ad47-4eb0-a1ab-8c12f60e43d0/rubric).
# 
# <a id='probability'></a>
# #### Part I - Probability
# 
# To get started, let's import our libraries.

# In[1]:


import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
#We are setting the seed to assure you get the same answers on quizzes as we set up
random.seed(42)


# `1.` Now, read in the `ab_data.csv` data. Store it in `df`.  **Use your dataframe to answer the questions in Quiz 1 of the classroom.**
# 
# a. Read in the dataset and take a look at the top few rows here:

# In[2]:


# Read top 5 rows and store in df
df = pd.read_csv('ab_data.csv')

df.head()


# b. Use the cell below to find the number of rows in the dataset.

# In[3]:


df.shape[0]


# c. The number of unique users in the dataset.

# In[4]:


df['user_id'].nunique()


# d. The proportion of users converted.

# In[5]:


df.converted.mean()


# e. The number of times the `new_page` and `treatment` don't match.

# In[6]:


df_1 = df.query("group == 'treatment' and landing_page != 'new_page'").count()[0]

df_2 = df.query("group != 'treatment' and landing_page == 'new_page'").count()[0]

df_1 + df_2


# f. Do any of the rows have missing values?

# In[7]:


df.info()


# `2.` For the rows where **treatment** does not match with **new_page** or **control** does not match with **old_page**, we cannot be sure if this row truly received the new or old page.  Use **Quiz 2** in the classroom to figure out how we should handle these rows.  
# 
# a. Now use the answer to the quiz to create a new dataset that meets the specifications from the quiz.  Store your new dataframe in **df2**.

# In[8]:


df_new = df.query("group == 'treatment' and landing_page == 'new_page'")
df_old = df.query("group == 'control' and landing_page == 'old_page'")


# In[9]:


df2 = df_new.append(df_old, ignore_index=True)
df2.head()


# In[10]:


# Double Check all of the correct rows were removed - this should be 0
df2[((df2['group'] == 'treatment') == (df2['landing_page'] == 'new_page')) == False].shape[0]


# `3.` Use **df2** and the cells below to answer questions for **Quiz3** in the classroom.

# a. How many unique **user_id**s are in **df2**?

# In[11]:


df2.user_id.nunique()


# b. There is one **user_id** repeated in **df2**.  What is it?

# In[12]:


# we get here repeated row
df2[df2.duplicated(['user_id'], keep=False)].sort_values(by=['user_id'])


# c. What is the row information for the repeat **user_id**? 

# **user_id is** _773192_
# 
# **group is** _treatment_
# 
# **landing_page is** _new_page
# 
# **converted is** _0_

# d. Remove **one** of the rows with a duplicate **user_id**, but keep your dataframe as **df2**.

# In[13]:


df2.drop_duplicates(subset='user_id', keep='last', inplace=True)


# `4.` Use **df2** in the cells below to answer the quiz questions related to **Quiz 4** in the classroom.
# 
# a. What is the probability of an individual converting regardless of the page they receive?

# In[14]:


df['converted'].mean()


# b. Given that an individual was in the `control` group, what is the probability they converted?

# In[15]:


df2[df2['group'] == 'control']['converted'].mean()


# c. Given that an individual was in the `treatment` group, what is the probability they converted?

# In[16]:


# this is alternate way to calculate by query
df2.query("group == 'treatment'").converted.mean()


# d. What is the probability that an individual received the new page?

# In[17]:


len(df2[df2['landing_page'] == 'new_page'])/df2.shape[0]


# e. Consider your results from parts (a) through (d) above, and explain below whether you think there is sufficient evidence to conclude that the new treatment page leads to more conversions.

# **No, the probability that the an individual received the new page is 0.5001 which is implied information proability received the old page also the half probability.**
# 
# **Furthermore, By looking individual "control" group proabaility conversion is 0.1204 whereas "treatment" group probability is 0.1188 that provide probability evidence.**
# 
# **In conclusion, the new treatment page leads to less conversions than old group page.**

# <a id='ab_test'></a>
# ### Part II - A/B Test
# 
# Notice that because of the time stamp associated with each event, you could technically run a hypothesis test continuously as each observation was observed.  
# 
# However, then the hard question is do you stop as soon as one page is considered significantly better than another or does it need to happen consistently for a certain amount of time?  How long do you run to render a decision that neither page is better than another?  
# 
# These questions are the difficult parts associated with A/B tests in general.  
# 
# 
# `1.` For now, consider you need to make the decision just based on all the data provided.  If you want to assume that the old page is better unless the new page proves to be definitely better at a Type I error rate of 5%, what should your null and alternative hypotheses be?  You can state your hypothesis in terms of words or in terms of **$p_{old}$** and **$p_{new}$**, which are the converted rates for the old and new pages.

# We assume the null hypothesis old page is better than new page unless the new page proves.
# 
# Null hypothesis:  **$$H_0: p_{new} \leq p_{old}$$**
# 
# Here, new page is better than old page. So, we reject the null hypothesis
# 
# Alternate hypothesis: **$$H_1: p_{new} > p_{old}$$**

# `2.` Assume under the null hypothesis, $p_{new}$ and $p_{old}$ both have "true" success rates equal to the **converted** success rate regardless of page - that is $p_{new}$ and $p_{old}$ are equal. Furthermore, assume they are equal to the **converted** rate in **ab_data.csv** regardless of the page. <br><br>
# 
# Use a sample size for each page equal to the ones in **ab_data.csv**.  <br><br>
# 
# Perform the sampling distribution for the difference in **converted** between the two pages over 10,000 iterations of calculating an estimate from the null.  <br><br>
# 
# Use the cells below to provide the necessary parts of this simulation.  If this doesn't make complete sense right now, don't worry - you are going to work through the problems below to complete this problem.  You can use **Quiz 5** in the classroom to make sure you are on the right track.<br><br>

# a. What is the **conversion rate** for $p_{new}$ under the null? 

# In[18]:


# Calculating p_new under the null hypothesis
p_new = df2['converted'].mean()
p_new


# b. What is the **conversion rate** for $p_{old}$ under the null? <br><br>

# In[19]:


# Calculating p_old under the null hypothesis
p_old = df2['converted'].mean()
p_old


# c. What is $n_{new}$, the number of individuals in the treatment group?

# In[20]:


n_new = df2[df2['group'] == 'treatment'].count()[0]
n_new


# d. What is $n_{old}$, the number of individuals in the control group?

# In[21]:


n_old = df2[df2['group'] == 'control'].count()[0]
n_old


# e. Simulate $n_{new}$ transactions with a conversion rate of $p_{new}$ under the null.  Store these $n_{new}$ 1's and 0's in **new_page_converted**.

# In[22]:


new_page_converted = np.random.binomial(1, p_new, n_new)
new_page_converted.mean()


# f. Simulate $n_{old}$ transactions with a conversion rate of $p_{old}$ under the null.  Store these $n_{old}$ 1's and 0's in **old_page_converted**.

# In[23]:


old_page_converted = np.random.binomial(1, p_old, n_old)
old_page_converted.mean()


# g. Find $p_{new}$ - $p_{old}$ for your simulated values from part (e) and (f).

# In[24]:


new_page_converted.mean() - old_page_converted.mean()


# h. Create 10,000 $p_{new}$ - $p_{old}$ values using the same simulation process you used in parts (a) through (g) above. Store all 10,000 values in a NumPy array called **p_diffs**.

# In[25]:


p_diffs = []

for _ in range(10000):
    new_page_converted = np.random.binomial(1, p_new, n_new).mean()
    old_page_converted = np.random.binomial(1, p_old, n_old).mean()
    p_diffs.append(new_page_converted - old_page_converted)    


# i. Plot a histogram of the **p_diffs**.  Does this plot look like what you expected?  Use the matching problem in the classroom to assure you fully understand what was computed here.

# In[26]:


plt.hist(p_diffs);


# j. What proportion of the **p_diffs** are greater than the actual difference observed in **ab_data.csv**?

# In[27]:


# Calculating actual difference 
control_mean = df2.query("group == 'control'").converted.mean()
treatment_mean = df2.query("group == 'treatment'").converted.mean()

# Actual difference 
act_diffs = treatment_mean - control_mean
act_diffs


# In[28]:


plt.hist(p_diffs);
plt.axvline(x= act_diffs, color = 'r', label = 'Actual difference')
plt.legend()
plt.ylabel('Frequency')
plt.xlabel('p_diff')


# In[29]:


# compute p value
(p_diffs > act_diffs).mean()


# k. Please explain using the vocabulary you've learned in this course what you just computed in part **j.**  What is this value called in scientific studies?  What does this value mean in terms of whether or not there is a difference between the new and old pages?

# **The p-value is large than alpha level 0.05, we have evidence that our statistic was likely to come from the null hypothesis. Therefore, we failed to reject null hypothesis.**
# 
# **To sum up, the old page is better than new page for the company.**

# l. We could also use a built-in to achieve similar results.  Though using the built-in might be easier to code, the above portions are a walkthrough of the ideas that are critical to correctly thinking about statistical significance. Fill in the below to calculate the number of conversions for each page, as well as the number of individuals who received each page. Let `n_old` and `n_new` refer the the number of rows associated with the old page and new pages, respectively.

# In[30]:


import statsmodels.api as sm

convert_old = df2[(df2['landing_page'] == 'old_page') & (df2['converted'] == 1)].count()[0]
convert_new = df2[(df2['landing_page'] == 'new_page') & (df2['converted'] == 1)].count()[0]
n_old = df2[df2['landing_page'] == 'old_page'].count()[0]
n_new = df2[df2['landing_page'] == 'new_page'].count()[0]


# m. Now use `stats.proportions_ztest` to compute your test statistic and p-value.  [Here](https://docs.w3cub.com/statsmodels/generated/statsmodels.stats.proportion.proportions_ztest/) is a helpful link on using the built in.

# In[31]:


# [convert_new, convert_old]
[convert_old, convert_new]


# In[32]:


# [n_new, n_old]
[n_old, n_new]


# In[33]:


stat, p_value = sm.stats.proportions_ztest([convert_old, convert_new], [n_old, n_new], value=None, alternative='smaller', prop_var=False)
(stat, p_value)


# n. What do the z-score and p-value you computed in the previous question mean for the conversion rates of the old and new pages?  Do they agree with the findings in parts **j.** and **k.**?

# **Summary points:**
# 
# _**By comparing our p-value to our type I error threshold (α), we can make our decision about which hypothesis we will choose.**_ 
# 
# _**As showing above model p value and z value are greater than alpha level (α) =.05. That means it's failed to reject the null hypothesis again and implied conversion rate of old page is better than new page of conversion rate. So, I agree with finding the J and K part which is deduced the old control page is better than new treatment page.**_

# <a id='regression'></a>
# ### Part III - A regression approach
# 
# `1.` In this final part, you will see that the result you achieved in the A/B test in Part II above can also be achieved by performing regression.<br><br> 
# 
# a. Since each row is either a conversion or no conversion, what type of regression should you be performing in this case?

# **Applying the logistic regression is a regression approach used to predict only two possible outcomes. Here we are predicting whether the new page conversion is better or not. That means anything like I want to predict with only two outcomes. In short, I want to predict one of two possible outcomes.**

# b. The goal is to use **statsmodels** to fit the regression model you specified in part **a.** to see if there is a significant difference in conversion based on which page a customer receives. However, you first need to create in df2 a column for the intercept, and create a dummy variable column for which page each user received.  Add an **intercept** column, as well as an **ab_page** column, which is 1 when an individual receives the **treatment** and 0 if **control**.

# In[34]:


df2[['no_ab_page', 'ab_page']] = pd.get_dummies(df2['group'])
df2.drop(['no_ab_page'], axis=1, inplace=True)
df2['intercept'] = 1
df2.head()


# c. Use **statsmodels** to instantiate your regression model on the two columns you created in part b., then fit the model using the two columns you created in part **b.** to predict whether or not an individual converts. 

# In[35]:


# instantiate the model

logit_mod = sm.Logit(df2['converted'], df2[['intercept', 'ab_page']])
result = logit_mod.fit()
result.summary2()


# d. Provide the summary of your model below, and use it as necessary to answer the following questions.

# In[36]:


# In the linear regression we converted above coeffient value into exponential by mathmatical logic
np.exp(-0.0150)


# In[37]:


# Whenever you see the exponential result less than 1 bascially need to convert into reciprocal i,e 1/np.exp(-1.4637)
1/np.exp(-0.0150)


# if 1 unit descrease from the ab_page treatment, the conversion rate will be 1.01 less likely than no_ab_page of control group, holding all other variable constant. Therefore, the old page is better than new page.

# e. What is the p-value associated with **ab_page**? Why does it differ from the value you found in **Part II**?<br><br>  **Hint**: What are the null and alternative hypotheses associated with your regression model, and how do they compare to the null and alternative hypotheses in **Part II**?

# **The p_value is 0.1899 which is higher than alpha level 0.05. So we failed to reject the null hypothesis as likewise in part 2. However it is pretty less than part2.**
# 
# **Why we get p_value is different? because of In part 2 we compute p_value on Bootstrapping is any test or metric that uses random sampling with replacement, and falls under the broader class of resampling methods.This technique allows estimation of the sampling distribution of almost any statistic using random sampling methods.**
# 
# **In part 3, we predicting the value of the indivisual increase the point by Linear Regression is a machine learning algorithm based on supervised learning. It performs a regression task. Regression models a target prediction value based on independent variables. ... When training the model – it fits the best line to predict the value of y for a given value of x.**
# 
# **Therefore, we get different p_value in part 2 and part 3.**

# **In part 2, we have one tailed test. However, In part 3, we observed the two tailed test as following:**

# $$H_0: p_{new} = p_{old}$$
# 
# $$H_1: p_{new} \neq p_{old}$$

# f. Now, you are considering other things that might influence whether or not an individual converts.  Discuss why it is a good idea to consider other factors to add into your regression model.  Are there any disadvantages to adding additional terms into your regression model?

# **The disadvantages of Logist regression as followng:**
# 
# 1) linear regression technique outliers can have huge effects on the regression and boundaries are linear in this technique.
# 
# 2) Mulitcolinearity 
# 
# 3) Non-linearity of the response predictor releationship

# g. Now along with testing if the conversion rate changes for different pages, also add an effect based on which country a user lives in. You will need to read in the **countries.csv** dataset and merge together your datasets on the appropriate rows.  [Here](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.join.html) are the docs for joining tables. 
# 
# Does it appear that country had an impact on conversion?  Don't forget to create dummy variables for these country columns - **Hint: You will need two columns for the three dummy variables.** Provide the statistical output as well as a written response to answer this question.

# In[38]:


countries_df = pd.read_csv('countries.csv')
countries_df.head()


# In[39]:


countries_df.info()


# In[40]:


countries_df.groupby('country').count()


# In[41]:


df_new = df2.set_index('user_id').join(countries_df.set_index('user_id'))


# In[42]:


df_new[['US', 'UK', 'CA']] = pd.get_dummies(df_new['country'])
df_new.drop(['CA'], axis=1, inplace=True)
df_new.head()


# In[43]:


df_new['intercept'] = 1
logit_ob = sm.Logit(df_new['converted'], df_new[['intercept', 'ab_page', 'US', 'UK']])
result = logit_ob.fit()
result.summary2()


# In[44]:


np.exp(-0.0408), np.exp(0.0099)


# In[45]:


# US less than one that need to take receprical
1/np.exp(-0.0408)


# p_values of all independent variable is greater than 0.05 alpha level. We again failed to reject null hypothesis. So, the country factor not impact on conversion page

# If each 1 unit decrease from the new page conversion, old control ab page 1.015 more likely, holding all variable constant.

# User from the Canada 1.041 more likely converted than users from United States (US), holding all other variable constant

# User from the UK 1.0099 more likely converted than users from Canada(CA), holding all other variable constant.

# h. Though you have now looked at the individual factors of country and page on conversion, we would now like to look at an interaction between page and country to see if there significant effects on conversion.  Create the necessary additional columns, and fit the new model.  
# 
# Provide the summary results, and your conclusions based on the results.

# In[46]:


df_new['US_ab_page'] = df_new['US'] * df_new['ab_page']
df_new['UK_ab_page'] = df_new['UK'] * df_new['ab_page']


# In[47]:


# Instiantiating the model
logit_ob2 = sm.Logit(df_new['converted'], df_new[['intercept', 'ab_page', 'US', 'UK', 'US_ab_page', 'UK_ab_page']])
result = logit_ob2.fit()
result.summary2()


# **Similarly, the p_value of US_ab_page and UK_ab_page is higher than alpha level .05.
# Adding the country factor with interaction web page which is not significant effect on the conversion. So, we failed to reject the null hypothesis.**

# In[56]:


np.exp(-0.0469)


# In[54]:


# US_ab_page take receiprocal
1/np.exp(-0.0469)


# if an indivisual user from canada, conversion 1.048 more likely interaction with web page than if the user from the United states, holding all variable constant.

# In[57]:


# UK_ab_page
np.exp(0.0314)


# if an indivisual user from United Kingdom, conversion 1.032 more likely interaction with web page than if the user from the Canada, holding all variable constant.

# In[62]:


# US and UK dummy variable receiprocal
1/np.exp(-0.0175), 1/np.exp(-0.0057)


# If each one unit decrease from the United states conversion rate, User from the Canada 1.0176 more likely converted, holding all other variable constant
# 
# If each one unit decrease from the United Kingdom conversion rate, User from the Canada 1.0176 more likely converted, holding all other variable constant

# ## Conclusion 

# We have gone through three parts of for A/B testing for launching whether new page or old page of the e-commerce company website.
# 
# We found the probabiity of indivisual control group conversion is higher than treatement group conversion. Then, we performed A/B testing through bootstrapping and calculate p_value which higher than alpha level .05. So, we failed to reject the null hypothesis. Furthermore, we calculate the p_value again by the stats.proportions_ztest and linear regression model that also failed to reject the null hypothesis.
# 
# Finally, we add an effect based on which country a user lives in dataset. However, we haven't found strong influnece on convertsion rate in the regression model.
# 
# Therefore, e-commerce company should not launched the new page for the website.

# <a id='conclusions'></a>
# 
# ## Resource:
# 
# > Finding duplicate data 
# 
# > https://stackoverflow.com/questions/14657241/how-do-i-get-a-list-of-all-the-duplicate-items-using-pandas-in-python
# 
# > Finding sort data 
# 
# > https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
# 
# > Drop duplicate row
# 
# > https://stackoverflow.com/questions/13035764/remove-rows-with-duplicate-indices-pandas-dataframe-and-timeseries

# <a id='conclusions'></a>
# ## Finishing Up
# 
# > Congratulations!  You have reached the end of the A/B Test Results project!  You should be very proud of all you have accomplished!
# 
# > **Tip**: Once you are satisfied with your work here, check over your report to make sure that it is satisfies all the areas of the rubric (found on the project submission page at the end of the lesson). You should also probably remove all of the "Tips" like this one so that the presentation is as polished as possible.
# 
# 
# ## Directions to Submit
# 
# > Before you submit your project, you need to create a .html or .pdf version of this notebook in the workspace here. To do that, run the code cell below. If it worked correctly, you should get a return code of 0, and you should see the generated .html file in the workspace directory (click on the orange Jupyter icon in the upper left).
# 
# > Alternatively, you can download this report as .html via the **File** > **Download as** submenu, and then manually upload it into the workspace directory by clicking on the orange Jupyter icon in the upper left, then using the Upload button.
# 
# > Once you've done this, you can submit your project by clicking on the "Submit Project" button in the lower right here. This will create and submit a zip file with this .ipynb doc and the .html or .pdf version you created. Congratulations!

# In[50]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Analyze_ab_test_results_notebook.ipynb'])

