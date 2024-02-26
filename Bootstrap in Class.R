# Topic: Bootstrap
# Example: Estimate the standard deviation of predicted probability
# Data: Smarket.csv

# Import the dataset
Smarket.df <- read.csv('Smarket.csv', stringsAsFactors = TRUE)

# 1. Import the library for bootstrap
library(boot)

# 2. Define a boot function that generate the predicted
# probability
boot_func <- function(myData, indices){
  glm.fit <- glm(Direction ~ Lag1 + Lag2 + Volume,
                 data = myData[indices,],
                 family = binomial
                 )
  predProb <- predict(glm.fit, newdata = myData[indices,],
                      type = 'response')
  return(predProb)
}

# 3. boot() function to bootstrap
# boot(dataset, boot.fn, R = number of bootstrap samples)
boot.result <- boot(Smarket.df, boot_func, R = 1000)
# Display different components using $
boot.result

# To generate a random sample with replacement
Smarket.df[sample(1250, 1250, replace = T), ]

#### How to do bootstrap for one prediction ####

# We first need to create an empty vector to save the estimates
# of B number of bootstrap samples

# Let's set B to 1000; This way if we want to change the number of bootstrap
# sample, we can only change B, not the bootstrap code
B <- 1000

# The vector holds the predicted probability. So, the data type of
# the items needs to be numeric. We can use the numeric() function to do
# that, specifying length = B.
v.predProb <- numeric(length = B)

# Bootstrap means that we need to repeat the following process 
# B (now it is 1000) times.
# 1. Generate a random sample with replacement
# 2. Fit the model
# 3. Make the prediction for one observation and save it to the vector
# 4. Caculate the standard deviation
for (i in 1:B) {
  # Sample with replacement from the original dataset to create a bootstrap sample
  index <- sample(nrow(Smarket.df), replace = TRUE)
  Smarket.boot <- Smarket.df[index, ]
  
  # Fit the logistic regression model on the bootstrap sample
  fit.boot <- glm(Direction ~ Lag1 + Lag2 + Volume, 
                  data = Smarket.boot, family = binomial)
  
  # Use the fitted model to predict the value of interest for each observation in the bootstrap sample
  v.predProb[i] <- predict(fit.boot, newdata = Smarket.df[1,], type = "response")
}

# Calculate the standard deviation of the bootstrap estimates
sd.boot <- sd(v.predProb)

# Print the estimated standard deviation of the predicted value
print(sd.boot)
