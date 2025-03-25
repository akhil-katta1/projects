# Topic: Tree-based methods
# Dataset: Carseats.csv

# 1. Import the dataset
seats.df <- read.csv('Carseats.csv', stringsAsFactors = TRUE)
# 2. Generate a factor variables based on sales
mean(seats.df$Sales)
median(seats.df$Sales)
# The cutoff for high/low sales: 8
# We can create a variable 'High' to indicate
# whether the sale is in the high range
seats.df$High <- factor(ifelse(seats.df$Sales > 8, 'Yes', 'No'))
# 3. Build a decision tree model
# The package we use is 'tree'
install.packages('tree')
library(tree)

seats.tree <- tree(High ~.-Sales, data = seats.df)
summary(seats.tree)

plot(seats.tree)
text(seats.tree, pretty = 0)
# Display the nodes
seats.tree
# R displays the split criterion (e.g. Price < 92.5),
# the number of observations in that branch, 
# the deviance, 
# the overall prediction for the branch (Yes or No),
# and the fraction of observations in that
# branch that take on values of Yes and No. 
# Branches that lead to terminal nodes are indicated using asterisks.

# 4. Making predictions using the tree
# Let's practice the process of using training and testing dataset
set.seed(2)
train.v <- sample (nrow(seats.df), 200)
test.df <- seats.df[-train.v, ]
High.test <- seats.df$High[-train.v]
tree.train <- tree(High ~ . - Sales, seats.df,
                        subset = train.v)
# Prediction function
tree.pred <- predict(tree.train, test.df,
                       type = "class")
table(tree.pred , High.test)
(104 + 50)/200

# 5. prune tree using cv.tree(). it uses c.v. to find optimal tree size.
#FUN = prune.missclassification will use missclassification rate as the performance metric for the pruning.

set.seed(7)
cv.seats <- cv.tree(tree.train, FUN = prune.misclass)
cv.seats
#size = size of tree
#dev = no. of cv errors
#k = cost-complexity parameter. It indicates how much weight we put on the size of the tree
# 9-leaf tree has the least $dev(errors) which is 74

par(mfrow = c(1,2))
plot(cv.seats$size, cv.seats$dev, type = 'b')
plot(cv.seats$k, cv.seats$dev, type = 'b')
prune.seats <- prune.misclass(tree.train, best = 9)
plot(prune.seats)
text(prune.seats, pretty = 0)
# predictions based on pruned tree and compare the performance
prune.pred <- predict(prune.seats, test.df, type = 'class')
table(prune.pred, High.test)
(97+58)/200

# II Ensembled tree: bagging, random forest and boosting
# 1. Bagging and random forests
install.packages('randomForest')
library(randomForest)
#randonForest()  function can be used for both for bagging and random forest
#bagging is just a special case in random forest with m = p

#bagging
bag.seats <- randomForest(High ~. - Sales, seats.df,
                           subset = train.v,
                           mtry = 10,
                           importance = TRUE)
#mtry specifies m variables to build trees
#m = b is bagging; default value is sqrt(p) for classification
# p-3 for regression
#importance = TRUE will asses importance of predictors
bag.seats
#output is a confusion matrix
#let's evaluate the performance of bagged tree
bag.pred <- predict(bag.seats, test.df, type = 'class')
table(bag.pred, High.test)
(104+61)/200

#random forest
ran.seats <- randomForest(High ~. - Sales, seats.df,
                          subset = train.v,
                          importance = TRUE)
ran.seats
ran.pred <- predict(ran.seats, test.df, type = 'class')
table(ran.pred, High.test)
(109+59)/200
# to examine the importance of variables
imp <- importance(ran.seats)
View(imp)
# To plot
varImpPlot(ran.seats)
#III Boosting: gradient boosting
install.packages('gbm')
library(gbm)
seats.df$High.n <- ifelse(seats.df$Sales > 8,1,0)
boost.seats <- gbm(High.n ~ . -Sales -High, data = seats.df[train.v, ],
                   distribution = 'bernoulli',
                   n.trees = 5000,
                   shrinkage = 0.01,
                   interaction.depth = 2)
summary(boost.seats)
#summary() produces relative influence plot
#impact of individual variables can alsio be plotted
plot(boost.seats, i = 'Price')
plot(boost.seats, i = 'ShelveLoc') 
