# ---
# jupyter:
#   kernelspec:
#     display_name: Python 3
#     name: python3
# ---

# %% [markdown]
# # Cross-validation framework
#
# Let's review the basics of model evaluation:
# * **Training error:** Error on the data used to train the model. A model can memorize the data, yielding a misleadingly low training error.
# * **Testing error (generalization error):** Error on unseen data. This tells us how the model performs in reality.
#
# Basic evaluation involves:
# 1. splitting data into training and testing sets
# 2. fitting the model on the training set
# 3. computing both training and testing errors
#
# ```{mermaid}
# flowchart LR
#     A[Dataset] --> B[Training Set]
#     A --> C[Testing Set]
# ```
#
# Let's fetch our dataset and split it.

# %%
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

housing = fetch_california_housing(as_frame=True)
data, target = housing.data, housing.target

# Transform the prices from the 100 (k$) range to the thousand dollars (k$) range.
target *= 100

data_train, data_test, target_train, target_test = train_test_split(
    data, target, random_state=0
)

# %% [markdown]
# ## Training error vs testing error
#
# We will use a decision tree regressor. Let's train our model on the training set.

# %%
from sklearn.tree import DecisionTreeRegressor

regressor = DecisionTreeRegressor(random_state=0)
regressor.fit(data_train, target_train)

# %% [markdown]
# Finally, we estimate the different types of errors. Let's start by computing
# the training error.

# %%
from sklearn.metrics import mean_absolute_error

target_predicted = regressor.predict(data_train)
score = mean_absolute_error(target_train, target_predicted)
print(f"The training error of our model is {score:.2f} k$")

# %% [markdown]
# Our model memorized the training set (0 error). Let's see how it performs on unseen testing data:

# %%
target_predicted = regressor.predict(data_test)
score = mean_absolute_error(target_test, target_predicted)
print(f"The testing error of our model is {score:.2f} k$")

# %% [markdown]
# ## Stability of cross-validation estimates
#
# A single train-test split might be lucky or unlucky. **Cross-validation** gives us a better 
# estimate of a model's true performance variability by repeatedly splitting the data.
#
# We will use "shuffle-split": randomly shuffle, split, train, and test. We'll repeat this 40 times.
#
# ![Cross-validation diagram](../figures/shufflesplit_diagram.png)
#
# Let's run `cross_validate` with a `ShuffleSplit` object:

# %%
from sklearn.model_selection import cross_validate
from sklearn.model_selection import ShuffleSplit

cv = ShuffleSplit(n_splits=40, test_size=0.3, random_state=0)
cv_results = cross_validate(
    regressor, data, target, cv=cv, scoring="neg_mean_absolute_error"
)

# %% [markdown]
# We'll convert the results dictionary into a pandas dataframe for easier analysis.

# %%
import pandas as pd

cv_results = pd.DataFrame(cv_results)
cv_results

# %% [markdown]
# Note that scikit-learn uses scores (where higher is better), so we passed `neg_mean_absolute_error`. 
# We revert the negation to get the actual error and preview the results:

# %%
cv_results["test_error"] = -cv_results["test_score"]
cv_results.head(5)

# %% [markdown]
# Let's visualize the distribution of testing errors across our 40 splits to understand 
# the model's reliability.

# %%
import matplotlib.pyplot as plt

cv_results["test_error"].plot.hist(bins=10, edgecolor="black")
plt.xlabel("Mean absolute error (k$)")
_ = plt.title("Test error distribution")

# %% [markdown]
# We observe that the testing error is clustered around 47 k\$ and ranges from
# 43 k\$ to 50 k\$.

# %%
print(
    "Cross-validated testing error: "
    f"{cv_results['test_error'].mean():.2f} ± {cv_results['test_error'].std():.2f} k$"
)

# %% [markdown]
# Is this an acceptable error? Let's contrast it with the natural variability of house prices in our dataset.

# %%
target.plot.hist(bins=20, edgecolor="black")
plt.xlabel("Median House Value (k$)")
_ = plt.title("Target distribution")
print(f"Target standard deviation: {target.std():.2f} k$")

# %% [markdown]
# The target ranges from 0 to 500 k\$. An error of ~47 k\$ might seem okay for a 500 k\$ house, 
# but it's massive for a 50 k\$ house. Let's calculate the Mean Absolute Percentage Error (MAPE) 
# on the test set to evaluate relative error.

# %%
from sklearn.metrics import mean_absolute_percentage_error
mape = mean_absolute_percentage_error(target_test, target_predicted)
print(f"Mean Absolute Percentage Error (MAPE): {mape:.1%}")

# %% [markdown]
# A MAPE of over 20% indicates that our predictions are, on average, off by more than 20% of the true house value! 
# Using a relative metric like MAPE gives us a much clearer picture of the model's practical limitations.
#
# ## Getting the fitted models
#
# You can retrieve the models fitted during cross-validation by setting `return_estimator=True`. 
# This is useful if you want to inspect each model's internal parameters.

# %%
cv_results = cross_validate(regressor, data, target, return_estimator=True)
cv_results["estimator"]

# %% [markdown]
# If you only care about the scores (and not training times or estimators), you can use `cross_val_score`:

# %%
from sklearn.model_selection import cross_val_score

scores = cross_val_score(regressor, data, target)
scores

# %% [markdown]
# ## Summary
#
# We demonstrated:
# * Splitting data into train/test sets to evaluate generalization
# * Training vs. Testing error
# * Using cross-validation to estimate the variability of a model's performance
# * Using code (like `mean_absolute_percentage_error`) to clearly check relative errors
