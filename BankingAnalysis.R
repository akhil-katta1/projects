bank.df <- read.csv('Bank.csv')
View(bank.df)
#4
bank.df <- bank.df[,-c(1,5)]
View(bank.df)
bank.df$Personal.Loan <-as.factor(bank.df$Personal.Loan)
bank.df$Education <-as.factor(bank.df$Education)
#5
set.seed(1)
train.v <- sample(nrow(bank.df), nrow(bank.df)*0.60)
train.df <- bank.df[train.v,]
View(train.df)
test.df <- bank.df[-train.v,]
#6
install.packages('tree')
library(tree)
?tree
train.tree <- tree(Personal.Loan ~. - Personal.Loan, train.df)
train.tree
plot(train.tree)
text(train.tree)
#income is the first split variable
#7
library(caret)
predTrain <- predict(train.tree, train.df, type = "class")
confusionMatrix(predTrain, train.df$Personal.Loan)$overall['Accuracy']
#missclassification rate is 1-0.9866667 = 0.0133333 and the first split variable is income.
test.tree <- tree(Personal.Loan ~. - Personal.Loan, test.df)
plot(test.tree)
text(test.tree)
predTest <- predict(train.tree, test.df, type = "class")
confusionMatrix(predTest, test.df$Personal.Loan)$overall['Accuracy']
#Missclassification rate is 1-0.981= 0.019
#8
cv.bank <- cv.tree(train.tree, FUN = prune.misclass)
cv.bank
# tree with size 9, 7 have the same minimum error of 44. So, we choose the one with the minimal model complexity i.e. 7
#9
prune <- prune.misclass(train.tree, 7)
plot(prune)
text(prune, pretty = 0)
#10
predPrune <- predict(prune, test.df, type = 'class')
confusionMatrix(predPrune, test.df$Personal.Loan)$overall['Accuracy']
#missclassification rate is 1 - 0.9755 = 0.0245

