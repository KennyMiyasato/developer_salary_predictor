# mod4_project

## The Goal: Predicting Salary Based on Demographics and Developer Experience

For this project, we used multiple linear regression to predict salary based on responses from the 2019 StackOverflow Developer Survey. With our model, we were able to explain about 40% of the variance in respondents' reported salary. Our model was especially effective in predicting salaries between $50,000 and $165,000. Outside of those values, the residual errors in our model were not normally distributed, indicating that further research is needed to make the model suffeciently predictive for all respondents. 

## Predictors

The variables that informed our prediction included respondents' demographics, education, social preferences, work experience, and career satisfaction. We combined some of these feature in order to examine the effects of interaction between them. For example, we created interaction variables for gender and ethnicity to see if the combination of those two factors had an effect on salary. After fitting our multiple linear regression using 80% of the data, we eliminated variables with coeffecient p-values above .05 and Variance Influence Factors above 5. 

## The Response

