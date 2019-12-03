# mod4_project

## The Goal: Predicting Salary Based on Demographics and Developer Experience

For this project, we used multiple linear regression to predict salary based on responses from the 2019 StackOverflow Developer Survey. With our model, we were able to explain about 40% of the variance in respondents' reported salary. Our model was especially effective in predicting salaries between $50,000 and $165,000. Outside of those values, the residual errors in our model were not normally distributed, indicating that further research is needed to make the model suffeciently predictive for all respondents. 

## Predictors

The variables that informed our prediction included respondents' demographics, education, social preferences, work experience, and career satisfaction. We combined some of these feature in order to examine the effects of interaction between them. For example, we created interaction variables for gender and ethnicity to see if the combination of those two factors had an effect on salary. After fitting our multiple linear regression using 80% of the data, we eliminated variables with coeffecient p-values above .05 and Variance Influence Factors above 5. 

## The Response

For our model, we considered any respondents that earned between $10,000 and $250,000. As mentioned, the residual errors in our model's predicted values failed to maintain a normal distribution on either extreme. This could mean that the relationship between our predictors and response is not fundamentally linear, or it could mean that there is a relationship between our predictors and response that we failed to account for. Further analysis is needed to make salary predictions with a reasonable degree of confidence. We can still use our model to understand the relative impact of certain predictors on our response. 

## Interpretation

A respondent's country proved to be the most significant predictor of salary. Out of the 25 largest predictor coeffecients (i.e. the predictors with the largest positive effect on salary), 13 of them were coeffecients associated with the respondent's country. Other significant predictors include work week wours, education level, organation size, ethnicity, and career satisfaction. 

## The Model

We started by running a multiple linear regression with 288 predictors. After cross-validating this model's performance with a train-test split of 80/20, the R^2 value for our test data proved to be slightly negative. This indicated that we were overfitting our training data. By recursively eliminating any coeffecient p-values above .05, our test R^2 drastically increased to about 70%. This left us with 117 predictors. However, after investigating multicollinearity, we removed 10 additional variables, and our R^2 fell down to about 40%. We wer able to improve performance slightly with regularization. Interestingly, the highest test R^2 was obtained by running a ridge regression on the original set of predictors that yielded a negative test R^2 for an un-penalized OLS regression. Ultamitely we decided the most approprate model was a ridge regression using the most limited subset of variables. 
