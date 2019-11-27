import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
import sklearn.preprocessing as preprocessing


def sm_OLS(x_values,y_values):
    x_values = sm.add_constant(x_values)
    model = sm.OLS(y_values,x_values)
    results = model.fit()
    results_summary = results.summary()
    results_as_html = results_summary.tables[1].as_html()

    model_performance = {}
    model_performance['MSE'] = results.mse_model
    model_performance['MSE_resid'] = results.mse_resid
    model_performance['RMSE'] = results.mse_resid**.5
    model_performance['R^2'] = results.rsquared
    model_performance['R^2_adjusted'] = results.rsquared_adj
    model_performance['F-stat'] = results.fvalue
    model_performance['AIC'] = results.aic
    model_performance['BIC'] = results.bic

    model_performance = pd.DataFrame.from_dict(model_performance,orient='index',columns=['Value'])

    #print(results.summary())
    variables_as_html = results_summary.tables[1].as_html()
    variables = pd.read_html(results_as_html, header=0, index_col=0)[0]

    outcomes = {}
    outcomes['Observed_values'] = y_values
    outcomes['Predicted_values'] = results.predict()
    outcomes['Residuals'] = results.resid

    #outcomes['Conf']

    outcomes = pd.DataFrame(outcomes)
    #print(results.summary())
    return model_performance,variables,outcomes

def train_test(model,x,y):
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    #train_errors, val_errors = [],[]

    #interaction = PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
    #X_train = interaction.fit_transform(X_train)

    preprocessing.StandardScaler()
    model.fit(X_train,y_train,)

    y_pred = model.predict(X_test)

    intercept = pd.Series(data=model.coef_)
    intercept.name = 'Intercept'

    #print('Intercept: \n', model.intercept_)
    #print('Coefficients: \n', model.coef_)

#     train_errors = mean_squared_error(y_train_predict,y_train)
#     val_errors = mean_squared_error(y_val_predict,y_val)

    #plt.plot(y_train_predict,y_val_predict)

    df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

    df['difference']=df.apply(lambda x: x['Actual']-x['Predicted'],axis=1)
    df['difference_squared'] = df.apply(lambda x: x['difference']**2,axis=1)
    obsv_avg = df['Actual'].mean()
    df['actual_v_mean'] = df.apply(lambda x: (x['Actual']-obsv_avg)**2,axis=1)

    variables = pd.DataFrame(data=model.coef_,index=x.columns,columns=['Coefficient'])
    predictor_means = [X_test[x].mean() for x in list(variables.index)]
    variables['Observed_avg'] = predictor_means

    #variables.loc['Intercept'] = model.intercept_

    performance = {}
    performance['RSS'] = df['difference_squared'].sum()
    performance['TSS'] = df['actual_v_mean'].sum()
    performance['F-Stat'] = ((performance['TSS']-performance['RSS'])/len(x.columns)/
                             (performance['RSS']/len(X_test)-len(x.columns)-1)
                            )
    performance['RSE'] = ((1/(len(X_test)-len(x.columns)))*performance['RSS'])**.5
    performance['MSE'] = mean_squared_error(y_test,y_pred)
    performance['R^2'] = model.score(X_test,y_test)
    performance['observed_mean'] = obsv_avg
    performance['pred_mean'] = df['Predicted'].mean()

    variables['Observed_avg'] = predictor_means
    #variables['Observed-Observed_avg'] = [(X_test[x]-variables.loc[x]['Observed_avg']) for x in list(variables.index)]


    #print(X_test['Respondent']-variables.loc['Respondent']['Observed_avg'])
#     print(X_test.describe())
#     print(predictor_means)
#     for predictor in list(variables.index):
#         print(predictor)
        #print([value - variables.loc[predictor]['Observed_avg'] for value in X_test[predictor]].sum()/len(X_test))
    #print(X_test['Respondent'])
    return df,variables,performance
