# Topic: Accounting Fraud
# The purpose of this project is to predict potential accounting fraud
# in US public companies. The data is from Bao et al. (2020) article.

# Import
fraud.df <- read.csv('C:\\Users\\kjs\\Downloads\\data mining\\week10\\AccountingFraud.csv')
# It may take sometime to import
View(fraud.df)
  # 1. Data preparation
# 1.1 Check for missing values
sapply(fraud.df, function(x) sum(is.na(x)))
# A couple of variables have missing values. We decide to drop them.
# Drop missing values
fraud.df <- na.omit(fraud.df)
fraud.df <- subset(fraud.df, select = -c(fyear))
fraud.df$misstate <- as.factor(fraud.df$misstate)
class(fraud.df$misstate)
install.packages('caret')
library(caret)
names(fraud.df)
myctrl <- trainControl(method = 'cv', number = 10)
lg_model <- train(misstate ~.,  
                  data = fraud.df,
                  method = 'glm',
                  family = 'binomial',
                  trControl = myctrl,
                  metric = 'Accuracy')
print(lg_model)
lda_model <- train(misstate ~., 
                   data = fraud.df,
                   method = 'lda',
                   family = 'binomial',
                   trControl = myctrl,
                   metric = 'Accuracy')
print(lda_model)
qda_model <- train(misstate ~., 
                   data = fraud.df,
                   method = 'qda',
                   family = 'binomial',
                   trControl = myctrl,
                   metric = 'Accuracy')
print(qda_model)
#with an accuracy of 99.27658%, the log model is the most accurate model.
