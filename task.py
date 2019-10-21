'''
The following script was created for the coding exercise: Model Risk Management & Control
Author: Anamaria Bernal
October 18th, 2019
'''

# Import packages
import pandas
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
import numpy

# Task 1: Replication of Results

print("Coding Exercise - Model Risk Management and Control  \n"
      "Author: Anamaria Bernal \n"
      "October 18th, 2019 \n\n"
      "Task 1: Replication of Results\n\n")

# Read data
macro = pandas.read_csv('input/data.txt', sep='|')

# Calculate first difference from time series
diff_macro = macro.iloc[:, 1:].diff().iloc[1:, :]
diff_macro.index = range(len(diff_macro))

# Split features and target for regression
X = diff_macro[['dpi', 'unemp']]
Y = diff_macro['consumption']

# Train linear regression
X = sm.add_constant(X)
mod = sm.OLS(Y, X)
res = mod.fit()
print(res.summary(), '\n')

print("Above you can observe the computed coefficients, standard error, t-statistics and p-values. "
      "Based on the results we can see that the independent variables are statistically significant (p-values < 0.05),"
      " therefore the coefficients represent the mean change in the dependent variable given a one-unit shift in the"
      " independent variables. Nevertheless, if we take a look at the R-squared we see that the percentage of "
      "the variance in the dependent variable that the independent variables explain"
      " is only of 0.3 which may affect in case we want to obtain precise predictions.\n")

# Task 2: Outlier Detections

print("Task 2: Outlier Detections\n\n")

# Calculate residuals
residuals = res.resid

# Implement Tukey's test to identify residuals
Q1 = residuals.quantile(0.25)
Q3 = residuals.quantile(0.75)
IQR = Q3 - Q1
out_detect = pandas.DataFrame((residuals < (Q1 - 1.5 * IQR)) | (residuals > (Q3 + 1.5 * IQR)))
total_out = len(out_detect[out_detect[0] == 1])

print("Using Tukey's test there were detected {} outliers.\n"
      "Since these were not excluded before fitting the regression, "
      "this may affect model. It is advice to exclude outliers before fitting a linear"
      "model or use a more robust method.\n".format(total_out))

# Test 3: Autocorrelation of Residuals

print("Test 3: Autocorrelation of Residuals\n\n")

# Get Durbin Watson statistic for the residuals
dw = durbin_watson(residuals)

print("As shown before, the Durbin-Watson (DW) statistic of the residuals is {}. "
      "The DW statistic indicates that there is a positive autocorrelation detected in the sample."
      "Which means that a positive error in one period carries over into the a positive error for "
      "the following period.\n".format(dw))

# Task 4: Bootstrapping of Standard Errors

print("Task 4: Bootstrapping of Standard Errors\n\n")

# Initialize and set variables
T = 65
n_samples = 10000
beta_boot = bse_boot = pandas.DataFrame(columns=['const', 'dpi', 'unemp'])
i = 0

while i < n_samples+1:

      # Select samples
      samples = numpy.random.choice(diff_macro.index, T)
      diff_macro_sampled = diff_macro.iloc[samples]

      # Split features and target for regression
      X_sample = diff_macro_sampled[['dpi', 'unemp']]
      Y_sample = diff_macro_sampled['consumption']

      # Train linear regression
      X_sample = sm.add_constant(X_sample)
      mod_s = sm.OLS(Y_sample, X_sample)
      res_sample = mod_s.fit()

      # Get coefficients and standard error
      beta_boot = beta_boot.append(pandas.DataFrame(data={'const': [res_sample.params[0]],
                                                          'dpi': [res_sample.params[1]],
                                                          'unemp': [res_sample.params[2]]}))
      bse_boot = bse_boot.append(pandas.DataFrame(data={'const': [res_sample.bse[0]],
                                                        'dpi': [res_sample.bse[1]],
                                                        'unemp': [res_sample.bse[2]]}))

      # Update i
      i += 1

# Get initial estimates
print("Initial estimated coefficients:\n{}\n".format(res.params))
print("Initial standard error:\n{}\n".format(res.bse))

# Get bootstrapped estimate statistics
print("Statistics from the Bootstrapped estimated coefficients:\n", beta_boot.describe(), '\n')
print("Statistics from the Bootstrapped standard error:\n", bse_boot.describe(), '\n')

# Print interpretation
print("By comparing the bootstrapped results with the initial estimates we can observe that the mean of the"
      " bootstrapped estimated coefficients is really close to the initial estimates, nevertheless when we compare it"
      " with the standard deviation we see that the coefficient of variation is relatively high.\n"
      "The results obtained from the bootstrapped standard error not so close to the initial estimates and "
      "the coefficient of variation are really high, which means that the obtained are spread out around the mean.\n"
      "The utilization of methods such as bootstrapping or cross-validation are useful get more accurate estimates.\n")
