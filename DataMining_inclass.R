#LINEAR MODEL SELECTION
happy.df <- read.csv('C:\\Users\\kjs\\Downloads\\data mining\\week 3\\Happiness2019.csv')
happy.df <- happy.df[ ,-c(1,2)]
View(happy.df)
install.packages('leaps')
library(leaps)
regfit.full <- regsubsets(Score ~ ., happy.df)
reg.summary <- summary(regfit.full)
reg.summary$rsq#r squared
which.max(reg.summary$adjr2)
which.min(reg.summary$cp)
which.min(reg.summary$bic)
#forward selection
reg.fwd <- regsubsets(Score ~ ., data = happy.df,
                      method = 'forward')
fwd.sum <- summary(reg.fwd)
which.max(fwd.sum$adjr2)
which.min(fwd.sum$cp)
#backword selection
reg.bck <- regsubsets(Score ~ ., data = happy.df,
                      method = 'backward')
bck.sum <- summary(reg.bck)
which.max(bck.sum$adjr2)
which.min(bck.sum$cp)

#ridge regression
install.packages('glmnet')
library(glmnet)

#generate  x and y dataframes
y <- happy.df$Score
x <- model.matrix(Score ~., happy.df)[,-1]
View(x)
grid <- 10^seq(10, -2, length = 100)

ridge.mod <- glmnet(x, y, alpha = 0, lambda = grid) 
dim(coef(ridge.mod))

#one model
coef(ridge.mod)[,50]
ridge.mod$lambda[50]
#smaller model
coef(ridge.mod)[,70]
ridge.mod$lambda[70]
#coefficient increase as lambda decreases
#to make prediction

predict(ridge.mod, s = 50, type = 'coefficients')[1:7, ]

#predict regression results
library(dplyr)
#select an observation where gdp = 1.488
new.happy <- filter(happy.df , GDP.per.capita == 1.488)
predict(ridge.mod, s = 50, newx = new.happy)
