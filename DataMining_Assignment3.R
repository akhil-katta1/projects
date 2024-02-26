
# Topic: Accounting Fraud
# The purpose of this project is to predict potential accounting fraud
# in US public companies. The data is from Bao et al. (2020) article.

# 1.	Open the R script you download.
# Opened the downloaded R script

# 2.	Run the pre-written code to import the data and delete missing values.
# Import
fraud.df <- read.csv('C:\\Users\\kjs\\Downloads\\data mining\\week 6\\AccountingFraud.csv')
# It may take sometime to import

# 1. Data preparation
# 1.1 Check for missing values
sapply(fraud.df, function(x) sum(is.na(x)))
# A couple of variables have missing values. We decide to drop them.
# Drop missing values
fraud.df <- na.omit(fraud.df)
View(fraud.df)
library(dplyr)

# 4.
train.df <- filter(fraud.df, fyear < 2011)
test.df <- filter(fraud.df, fyear >= 2011)

# 3.
train.fyear <- as.factor(train.df$fyear)
test.fyear <- as.factor(test.df$fyear)

class(train.fyear) 
class(train.fyear) 

# 5.
train.lgfit <- glm(misstate ~., data = train.df, family = 'binomial')

# 6.
summary(train.lgfit)

# 7.
exp(train.lgfit$coefficients["reoa"])
#with a positive value of 1.234371, the reao will have a positive affect in misstate. And with a p value < 0.05, it is significant.
#An increase in the unit value of reoa will also increase the misstate.

# 8.	
pred.lgprob <- predict(train.lgfit, newdata = test.df, type = 'response')

# 9.
pred.lgclass <- ifelse(pred.lgprob > 0.5, 'Yes', 'No')
pred.lgclass

# 10.	

glm.cm = table(predict = pred.lgclass, actual = test.df$misstate)
rownames(glm.cm) <- c("Actual Negative", "Actual Positive")
colnames(glm.cm) <- c("Predicted Negative", "Predicted Positive")
print(glm.cm)
accurateLG <- sum(diag(glm.cm)) / sum(glm.cm)
print(accurateLG)
glm.sensitivity <- (glm.cm[1,1]) / (glm.cm[1,1] + glm.cm[1,2])
print(glm.sensitivity)

#Percentage accuracy = 99.6%
#LDA
library(MASS)
# Fit an LDA model
lda.fit <- lda(misstate ~., data = train.df)
# Show the estimates
lda.fit
# Make predictions
lda.pred <- predict(lda.fit, newdata = test.df)
lda.pred$class[1:10] # The classification of Y
lda.pred$posterior[1:10,] # Posterior probability of Y in class Yes/No.
# The confusion matrix for the LDA model
lda.cm <- table(lda.pred$class,test.df$misstate)
length(train.df$misstate)
accurateLDA <- sum(diag(lda.cm)) / sum(lda.cm)
#Fit a QDA model

qda.fit <- qda(misstate ~., data = train.df)
# Show the estimate
qda.fit
# Make predictions
qda.pred <- predict(qda.fit, newdata = test.df)
qda.pred$class[1:10] # The classification of Y
qda.pred$posterior[1:10,] # Posterior probability of Y in class Yes/No.
# The confusion matrix for the LDA model
qda.cm <- table(qda.pred$class,test.df$misstate)
accurateQDA <- sum(diag(qda.cm)) / sum(qda.cm)
#Naive Bayes
# The library is e1071.
library(e1071)
# Fit the model
nb.fit <- naiveBayes(misstate ~., data = train.df)
# Show the results
nb.fit
# predict() requires argument of 'newdata'
nb.class <- predict(nb.fit, newdata = train.df)
nb.class[1:10]
# predict() with type = 'raw'
nb.pred <- predict(nb.fit, newdata = test.df, type = 'raw')
nb.pred[1:10,]
# The confusion matrix
nb.cm <- table(Predicted = nb.class, Actual = train.df$misstate)
accurateNB <- sum(diag(nb.cm)) / sum(nb.cm)
print(accurateLG)
print(accurateLDA)
print(accurateQDA)
print(accurateNB)
#6 The best accuracy rate is given by glm(99.666%) followed by LDA (98.63%)
#7 Type 2 error
#8 a model with higher sensitivity is considered better while trying to avoid type 2 error
library(caret)
print(glm.sensitivity)
sensitivity(lda.cm)
sensitivity(qda.cm)
sensitivity(nb.cm)
#With a sensitivity of 0.9970989, glm is considered a the the best option 
#followed by LDA with 0.9889706 sensitivity