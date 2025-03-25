# Topic: Resampling - Cross validation and Bootstrap
# Dataset: Smarket.csv
# Date: March 20, 2023

# Import the dataset
Smarket.df <- read.csv('Smarket.csv', stringsAsFactors = TRUE)
# Check the dimensions of the dataset
dim(Smarket.df)
# Basic statistics of the variables
summary(Smarket.df)
# Correlation plots
pairs(Smarket.df) # Error: Direction is not numerical
Smarket.df[,c(1,2,3)] # Slicing example
Smarket.df[,-9] # Exclude the last variable
pairs(Smarket.df[,-c(1,9)])
# Turn Direction into a factor variable
Smarket.df$Direction <- as.factor(Smarket.df$Direction)

names(Smarket.df)
glm.fit <- glm(Direction ~ Lag1 + Lag2 + Lag3 + Lag4 + Lag5 + Volume,
               data = Smarket.df,
               family = binomial)
summary(glm.fit)

# Using boot package to do cross-validation
install.packages('boot')
library(boot)
set.seed(1)
cv.err <- cv.glm(Smarket.df, glm.fit, K = 10)
cv.err$delta[1]
# The two numbers in the delta vector 
# contain the cross-validation results.

glm.fit.2 <- glm(Direction ~ Lag1 + Lag2 + Volume,
                 data = Smarket.df,
                 family = binomial)
cv.err.2 <- cv.glm(Smarket.df, glm.fit.2, K = 10)
cv.err.2$delta[1]

# Using caret package to implement cross-validation
install.packages('caret')
library(caret)

# Using trainControl() to specify cv parameters

myctrl <- trainControl(method = 'cv', number = 10)

lg_model <- train(Direction ~ Lag1 + Lag2 + Volume,
                  data = Smarket.df,
                  method = 'glm',
                  family = 'binomial',
                  trControl = myctrl)
lg_model

lda_model <- train(Direction ~ Lag1 + Lag2 + Volume,
                   data = Smarket.df,
                   method = 'lda',
                   trControl = myctrl)
lda_model

# Bootstrap example
# boot(data = the dataset to bootstrap, 
#             statistics = the value we estimate, 
#             R = how many bootstrap samples we want)

# How to define a function in R

# A simple sum function
add_two <- function(x, y){
  x + y
}
add_two(2,5)

# To define a function that takes a dataset and give a
# random sample of given percentage

sampling_perc <- function(sdata, perc){
  v <- sample(nrow(sdata), nrow(sdata)*perc)
  sdata[v,]
 }
Smarket.df_sample <- sampling_perc(Smarket.df, 0.4)

# This is the function to calculate alpha of the example
# in our textbook
alpha.fn <- function(data, index) {
  X <- data$X[index]
  Y <- data$Y[index]
  (var(Y) - cov(X, Y)) / (var(X) + var(Y) - 2 * cov(X, Y))
}

boot(Portfolio, alpha.fn, R = 1000)


