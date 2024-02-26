in# Data: Accounting Fraud from Bao et al (2020)
# Topic: ridge and lasso regression

# Import
fraud.df <- read.csv('C:\\Users\\kjs\\Downloads\\data mining\\week10\\AccountingFraud.csv')
View(fraud.df)
# It may take sometime to import

# 1. Data preparation
# 1.1 Check for missing values
sapply(fraud.df, function(x) sum(is.na(x)))
# We decide to drop observations with missing values.
# 1.2 Drop missing values
fraud.df <- na.omit(fraud.df)
fraud.df$misstate <- as.factor(fraud.df$misstate)

# 2. Data partition
# The natural split of training and validation dataset is to
# use time. We train the model using data from 1990-2010
# and the 2011-2014 as validation.
install.packages("dplyr")
install.packages("glmnet")
library(dplyr)
library(glmnet)
train.df <- filter(fraud.df, fyear < 2011)
valid.df <- filter(fraud.df, fyear >= 2011)
View(train.df)
# Drop fyear from the dataset
train.df <- train.df[,-1]
valid.df <- valid.df[,-1]
# 4. Prepare X and y for ridge/lasso regression
y <- train.df$misstate
X <- model.matrix(misstate ~., train.df)
X <- X[,-1]
View(X)
#ridge regression...............................................................
# 5
#train.df
ridge.mod <- glmnet(X, y, alpha = 0, family = 'binomial')
dim(coef(ridge.mod))
plot(ridge.mod)
# 6
set.seed(1)
cv.ridge <- cv.glmnet(X, y, alpha = 0, family='binomial', type.measure = 'class')
plot(cv.ridge)
ridgelam <- cv.ridge$lambda.min
ridgelam
#for valid.df...................................................................
# 7
X1 <- model.matrix(misstate ~., valid.df)
X1 <- X1[,-1]
ridge.pred <- predict(ridge.mod, s = ridgelam, newx = X1)
ridge.pred
# 8
#lasso regression...............................................................
#Train.df
lasso.mod <- glmnet(X, y, alpha = 1, family='binomial')
plot(lasso.mod)
coef(lasso.mod)[,20]
#the variables from the above code that have the coefficients which are not zero are considered as important and the values with zero as 
#coefficient are considered as not important.
lasso.mod$lambda[20]
# 9
lasso.out <- cv.glmnet(X, y, alpha = 1, family='binomial', type.measure = 'class')
plot(lasso.out)
lassolam <- lasso.out$lambda.min
lassolam

lasso.pred <- predict(lasso.mod, s = lassolam, newx = X1)
lasso.pred

