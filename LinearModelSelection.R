# Topic: Linear model selection
# Data: Happiness Index

happy.df <- read.csv('Happiness2019.csv')
happy.df <- happy.df[ ,-c(1,2)]

# 1. Import the libraries
install.packages('leaps')
library(leaps)
# 2. Use the regsubsets() to find the best models
regfit.full <- regsubsets(Score ~ ., happy.df)
reg.summary <- summary(regfit.full)
# Display the results of best subset selection
reg.summary$rsq
reg.summary$adjr2
reg.summary$cp
reg.summary$bic
# Find the model with the best performance
which.max(reg.summary$adjr2)
which.min(reg.summary$cp)

# 3. Stepwise selection
# Forward selection
reg.fwd <- regsubsets(Score ~ ., data = happy.df,
                      method = 'forward')
fwd.sum <- summary(reg.fwd)
which.max(fwd.sum$adjr2)
which.min(fwd.sum$cp)

# Backward selection
reg.bwd <- regsubsets(Score ~ ., data = happy.df,
                      method = 'backward')
bwd.sum <- summary(reg.bwd)
bwd.sum
which.max(bwd.sum$adjr2)
which.min(bwd.sum$cp)

# 
