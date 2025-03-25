bar.df <- read.csv('C:\\Users\\kjs\\Downloads\\data mining\\week 12\\Barcelona.csv')
View(bar.df)
names(bar.df)

#linear model
lm.fit <- lm(price ~ bedrooms + room_shared + room_private + person_capacity + superhost + multi
             + biz + cleanliness + guest_satisfaction + dist + metro_dist + attr_index + rest_index, data = bar.df)
summary(lm.fit)
# The variables bedrooms, room_sharedTRUE, room_privateTRUE, biz, dist and rest_index are significant.
install.packages('leaps')
library(leaps)

#subset selection
regfit.full <- regsubsets(price ~ ., bar.df)
reg.summary <- summary(regfit.full)
which.max(reg.summary$adjr2)
#adjusted r squared method, the model with 8 variables is the best having variables - bedrooms, room_sharedTRUE, room_privateTRUE, biz, 
#guest_satisfaction, dist, rest_index, lng.
which.min(reg.summary$cp)
#cp method, the model with 7 variables is the best having variables - bedrooms, room_sharedTRUE, room_privateTRUE, biz, 
#dist, rest_index, lng.
which.min(reg.summary$bic)
#bic method, the model with 4 variables is the best having variables - bedrooms, room_sharedTRUE, room_privateTRUE, biz.

#forward selection
reg.fwd <- regsubsets(price ~., data = bar.df,
                          method = 'forward')
fwd.summary <- summary(reg.fwd)
fwd.summary
which.max(fwd.summary$adjr2)
#adjusted r squared method, the model with 8 variables is the best having variables - bedrooms, 
#room_sharedTRUE, room_privateTRUE, biz, guest_satisfaction, dist, rest_index, lng.
which.min(fwd.summary$cp)
#cp method, the model with 7 variables is the best having variables - bedrooms, room_sharedTRUE, 
#room_privateTRUE, biz, guest_satisfaction, dist, rest_index, lng.
which.min(fwd.summary$bic)
#bic method, the model with 4 variables is the best having variables - bedrooms, room_sharedTRUE, room_privateTRUE, biz.

#backward selection
reg.bwd <- regsubsets(price ~., data = bar.df,
                      method = 'backward')
bwd.summary <- summary(reg.bwd)
bwd.summary
which.max(bwd.summary$adjr2)
#adjusted r squared method, the model with 8 variables is the best having variables - bedrooms, 
#room_sharedTRUE, room_privateTRUE, biz, guest_satisfaction, dist, rest_index, lng.
which.min(bwd.summary$cp)
#cp method, the model with 7 variables is the best having variables - bedrooms, room_sharedTRUE, 
#room_privateTRUE, biz, guest_satisfaction, dist, rest_index, lng.
which.min(bwd.summary$bic)
#bic method, the model with 4 variables is the best having variables - bedrooms, room_sharedTRUE, room_privateTRUE, biz.
