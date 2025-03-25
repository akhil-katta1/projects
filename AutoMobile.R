#1
car <- read.csv('C:\\Users\\kjs\\Downloads\\data mining\\week 3\\ToyotaCorolla.csv')
install.packages('ggplot2')
View(car)
library(ggplot2)
#3
plot(car$KM, car$Price)
# As the Number of KiloMetersdriven by the car increases, the car price decreases
#4
class(car$MetColor)
class(car$Automatic)
# Both the MetColor and Automatic are integer data types which is appropriate
# 5
unique(car$Doors)
class(car$Doors)
#There are 4 different values for Doors. Since these are categorical variables, we can use factors.
#6
lmcars.fit <- lm(Price ~ Age + KM + Fuel_Type + HP + MetColor + Automatic + Doors, data = car)
summary(lmcars.fit)
#7
#since the P values for Fuel_TypePetrol and MetColor are greater than 0.05, We can consider them as insignificant
#So, the variables - Age, KM, Fuel_TypeDiesel, HP, MetColor, Automatic, Doors are significant
#8
confint(lmcars.fit, c('Age', 'Automatic'))
#Age-> We can say that the population coefficient of age is between -144.7334 and -134.0413 with 97.5% confidence.
#This would mean that the value of the dependent variable will decrease by the absolute value of a number in the above mentioned range with a unit increase in age.
#Automatic-> We can say that the population coefficient of Automatic is between 518.4378 1189.0744 with 97.5% confidence.
#This would mean that the value of the dependent variable will increase by a number in the above mentioned range when compared to manual.
#9
#Running the summary function in line 19, we found that the r squared value of lmcar.fit is 0.835. so the model is reliable 83.5% of the time.
#10
Test <- data.frame(Age = c(23, 30, 30, 37), KM = c(71138, 64359, 11090, 27500),
            Fuel_Type = c("Diesel", "Petrol", "Petrol", "Petrol"), HP = c(69, 110,110, 97),
            MetColor = c(0, 1, 1, 0), Automatic = c(0, 0, 0, 1), Doors = c(3, 2, 3, 4))
predict(lmcars.fit, Test, interval = "confidence")
predict(lmcars.fit, Test, interval = "prediction")
