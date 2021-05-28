# -*- coding: utf-8 -*-

df1 <- read.csv("adult.data.csv")
head(df1)

df2 <- read.csv("howpop_train.csv")
head(df2)

"""**1. Сколько мужчин и женщин (признак sex) представлено в этом наборе данных?**"""

table(df1$sex)

"""**2. Каков средний возраст (признак age) женщин?**"""

mean(df1[df1['sex'] == "Female", "age"])

"""**3. Какова доля граждан Германии (признак native-country)?**"""

mean(df1["native.country"] == "Germany")

"""*4-5. Каковы средние значения и среднеквадратичные отклонения возраста тех, кто получает более 50K в год (признак *salary) и тех, кто получает менее 50K в год? **"""

mean(df1[df1['salary'] == ">50K", "age"])
sd(df1[df1['salary'] == ">50K", "age"])
mean(df1[df1['salary'] == "<=50K", "age"])
sd(df1[df1['salary'] == "<=50K", "age"])

"""**6. Правда ли, что люди, которые получают больше 50k, имеют как минимум высшее образование? (признак education – Bachelors, Prof-school, Assoc-acdm, Assoc-voc, Masters или Doctorate)**"""

colnames <- df1$education == "Bachelors" | df1$education == "Prof-school" | df1$education == "Assoc-acdm" | df1$education == "Assoc-voc" | df1$education == "Masters" | df1$education == "Doctorate"

addmargins(table(df1$salary, colnames))

"""**7. Выведите статистику возраста для каждой расы (признак race) и каждого пола. Используйте groupby и describe. Найдите таким образом максимальный возраст мужчин расы Amer-Indian-Eskimo.**"""

by(df1$age, df1$race, summary)

"""**8. Среди кого больше доля зарабатывающих много (>50K): среди женатых или холостых мужчин (признак marital-status)? Женатыми считаем тех, у кого marital-status начинается с Married (Married-civ-spouse, Married-spouse-absent или Married-AF-spouse), остальных считаем холостыми.**"""

library(stringr)
df1$sex <- str_replace_all(df1$sex, fixed(" "), "")
df1$salary <- str_replace_all(df1$salary, fixed(" "), "")
df1$marital.status <- str_replace_all(df1$marital.status, fixed(" "), "")
a <- (df1$marital.status == "Married-civ-spouse" | df1$marital.status == "Married-spouse-absent" | df1$marital.status == "Married-AF-spouse") & (df1$sex == "Male") & (df1$salary == ">50K")
b <- (df1$marital.status == "Divorced" | df1$marital.status == "Widowed" | df1$marital.status == "Separated" | df1$marital.status == "Never-married") & (df1$sex == "Male") & (df1$salary == ">50K")
c <- (sum(a) / (sum(a) + sum(b)))
d <- (sum(b) / (sum(a) + sum(b)))
print(sprintf("Доля женатых среди зарабатыващих больше 50К равна %f. Доля неженатых среди зарабатыващих больше 50К равна %f", c, d))

"""**9. Какое максимальное число часов человек работает в неделю (признак hours-per-week)? Сколько людей работают такое количество часов и каков среди них процент зарабатывающих много?**"""

i <- sum(df1$hours.per.week == max(df1$hours.per.week) & df1$salary == ">50K")
i * 100 / sum(df1$hours.per.week == max(df1$hours.per.week))

"""**10. Посчитайте среднее время работы (hours-per-week) зарабатывающих мало и много (salary) для каждой страны (native-country).**"""

print(tapply(X = df1$hours.per.week, INDEX = list(df1$salary, df1$native.country), FUN = mean))

"""## 1\. В каком месяце (и какого года) было больше всего публикаций?"""

library(ggplot2)
library(readxl)
library(scales)
library(dplyr)
library(tidyverse)
df2 <- read.csv("howpop_train.csv")

df2$published = as.character(df2$published)
df2$year <- as.numeric(substring(df2$published, 1, 4))
df2$month <- as.numeric(substring(df2$published, 6, 7))
df2$day <- as.numeric(substring(df2$published, 9, 10))
df2$hour <- as.numeric(substring(df2$published, 12, 13))

y_2015 <- subset(df2, year == 2015)
y_2016 <- subset(df2, year == 2016)
y_2015_03 <- subset(y_2015, month == 3)
y_2015_04 <- subset(y_2015, month == 4)
y_2016_03 <- subset(y_2016, month == 3)
y_2016_04 <- subset(y_2016, month == 4)

m <- rbind(c(nrow(y_2015_03), nrow(y_2016_03)), c(nrow(y_2015_04), nrow(y_2016_04)))
colnames(m) <- c("march", "april")
rownames(m) <- c(2015, 2016)

barplot(m, ylab="number", legend = rownames(m), beside=TRUE, col = topo.colors(2),  border = "black")
print("Ответ: март 2015")

"""## 2\. Проанализируйте публикации в месяце из предыдущего вопроса

Выберите один или несколько вариантов:

* Один или несколько дней сильно выделяются из общей картины
* На хабре _всегда_ больше статей, чем на гиктаймсе
* По субботам на гиктаймс и на хабрахабр публикуют примерно одинаковое число статей

Подсказки: постройте график зависимости числа публикаций от дня; используйте параметр `hue`; не заморачивайтесь сильно с ответами и не ищите скрытого смысла :)
"""

library(data.table)
df2$published = as.character(df2$published)
df2$year <- as.numeric(substring(df2$published, 1, 4))
df2$month <- as.numeric(substring(df2$published, 6, 7))
df2$day <- as.numeric(substring(df2$published, 9, 10))
df2$hour <- as.numeric(substring(df2$published, 12, 13))
y_2015 <- subset(df2, year == 2015)
y_2015_03 <- subset(y_2015, month == 3)
y_2015_03_days <- y_2015_03$day
table <- data.table(y_2015_03_days)
grouped_table <- table[, .N, by = names(table)]
data <- grouped_table$N
m = rbind(c(data[1:31]))
colnames(m) = c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
rownames(m) = c("number of texts")
barplot(m, ylab=rownames(m), xlab="days", beside=TRUE, col = rainbow(31),  border = "black")

library(data.table)
df2$published = as.character(df2$published)
df2$year <- as.numeric(substring(df2$published, 1, 4))
df2$month <- as.numeric(substring(df2$published, 6, 7))
df2$day <- as.numeric(substring(df2$published, 9, 10))
df2$hour <- as.numeric(substring(df2$published, 12, 13))
y_2015 <- subset(df2, year == 2015)
y_2015_03 <- subset(y_2015, month == 3)
y_2015_03_habr <- subset(y_2015_03, domain == "habrahabr.ru")
y_2015_03_geek <- subset(y_2015_03, domain == "geektimes.ru")
y_2015_03_habr_days <- y_2015_03_habr$day
table_habr <- data.table(y_2015_03_habr_days)
grouped_table_habr <- table_habr[, .N, by = names(table_habr)]
data_habr <- grouped_table_habr$N
y_2015_03_geek_days <- y_2015_03_geek$day
table_geek <- data.table(y_2015_03_geek_days)
grouped_table_geek <- table_geek[, .N, by = names(table_geek)]
data_geek <- grouped_table_geek$N
m = rbind(c(data_geek[1:31]), c(data_habr[1:31]))
colnames(m) = c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
rownames(m) = c("geektimes.ru", "habrahabr.ru")
barplot(m, ylab="Number of texts on each site", xlab="days", beside=TRUE, legend = rownames(m), col = topo.colors(2),  border = "black")

df2$published = as.character(df2$published)
df2$year <- as.numeric(substring(df2$published, 1, 4))
df2$month <- as.numeric(substring(df2$published, 6, 7))
df2$day <- as.numeric(substring(df2$published, 9, 10))
df2$hour <- as.numeric(substring(df2$published, 12, 13))

Saturdays <- function(year, month) {
    days <- as.POSIXlt(paste(year, month, 1:31, sep="-"), format="%Y-%m-%j")
    Std <- (days[days$wday==6])
    Std[!is.na(Std)]
}
a <- (Saturdays(2015, 3))
y_2015 <- subset(df2, year == 2015)
y_2015_03 <- subset(y_2015, month == 3)
y_2015_03_habr <- subset(y_2015_03, y_2015_03$domain  == "habrahabr.ru")
y_2015_03_geek <- subset(y_2015_03, y_2015_03$domain  == "geektimes.ru")

first_saturday <- as.character(a[1])
day1 <- as.numeric(substring(first_saturday, 9, 10))

second_saturday <- as.character(a[2])
day2 <- as.numeric(substring(second_saturday, 9, 10))


third_saturday <- as.character(a[3])
day3 <- as.numeric(substring(third_saturday, 9, 10))

fourth_saturday <- as.character(a[4])
day4 <- as.numeric(substring(fourth_saturday, 9, 10))

first_saturday_habr <- nrow(subset(y_2015_03_habr, y_2015_03_habr$day == day1))
second_saturday_habr <- nrow(subset(y_2015_03_habr, y_2015_03_habr$day == day2))
third_saturday_habr <- nrow(subset(y_2015_03_habr, y_2015_03_habr$day == day3))
fourth_saturday_habr <- nrow(subset(y_2015_03_habr, y_2015_03_habr$day == day4))

first_saturday_geek <- nrow(subset(y_2015_03_geek, y_2015_03_geek$day == day1))
second_saturday_geek <- nrow(subset(y_2015_03_geek, y_2015_03_geek$day == day2))
third_saturday_geek <- nrow(subset(y_2015_03_geek, y_2015_03_geek$day == day3))
fourth_saturday_geek <- nrow(subset(y_2015_03_geek, y_2015_03_geek$day == day4))

m = rbind(c(first_saturday_geek, second_saturday_geek, third_saturday_geek, fourth_saturday_geek),
c(first_saturday_habr, second_saturday_habr, third_saturday_habr, fourth_saturday_habr))
colnames(m) = c("07.03.2015", "14.03.2015", "21.03.2015", "28.03.2015")
rownames(m) = c("geektimes.ru", "habrahabr.ru")
barplot(m, ylab="Number of texts on each site", xlab="Dates", beside=TRUE, legend = rownames(m), col = topo.colors(2),  border = "black")

"""## 3\. Когда лучше всего публиковать статью?
* Больше всего просмотров набирают статьи, опубликованные в 12 часов дня
* У опубликованных в 10 утра постов больше всего комментариев
* Больше всего просмотров набирают статьи, опубликованные в 6 часов утра
* Максимальное число комментариев на гиктаймсе набрала статья, опубликованная в 9 часов вечера
* На хабре дневные статьи комментируют чаще, чем вечерние
"""

#Больше всего просмотров набирают статьи, опубликованные в 12 часов дня и У опубликованных в 10 утра постов больше всего комментариев
df2$published = as.character(df2$published)
df2$year <- as.numeric(substring(df2$published, 1, 4))
df2$month <- as.numeric(substring(df2$published, 6, 7))
df2$day <- as.numeric(substring(df2$published, 9, 10))
df2$hour <- as.numeric(substring(df2$published, 12, 13))
df2.hour0 <- df2[df2$hour == 0, ]
df2.hour1 <- df2[df2$hour == 1, ]
df2.hour2 <- df2[df2$hour == 2, ]
df2.hour3 <- df2[df2$hour == 3, ]
df2.hour4 <- df2[df2$hour == 4, ]
df2.hour5 <- df2[df2$hour == 5, ]
df2.hour6 <- df2[df2$hour == 6, ]
df2.hour7 <- df2[df2$hour == 7, ]
df2.hour8 <- df2[df2$hour == 8, ]
df2.hour9 <- df2[df2$hour == 9, ]
df2.hour10 <- df2[df2$hour == 10, ]
df2.hour11 <- df2[df2$hour == 11, ]
df2.hour12 <- df2[df2$hour == 12, ]
df2.hour13 <- df2[df2$hour == 13, ]
df2.hour14 <- df2[df2$hour == 14, ]
df2.hour15 <- df2[df2$hour == 15, ]
df2.hour16 <- df2[df2$hour == 16, ]
df2.hour17 <- df2[df2$hour == 17, ]
df2.hour18 <- df2[df2$hour == 18, ]
df2.hour19 <- df2[df2$hour == 19, ]
df2.hour20 <- df2[df2$hour == 20, ]
df2.hour21 <- df2[df2$hour == 21, ]
df2.hour22 <- df2[df2$hour == 22, ]
df2.hour23 <- df2[df2$hour == 23, ]
hour0 <- mean(df2.hour0$views)
hour1 <- mean(df2.hour1$views)
hour2 <- mean(df2.hour2$views)
hour3 <- mean(df2.hour3$views)
hour4 <- mean(df2.hour4$views)
hour5 <- mean(df2.hour5$views)
hour6 <- mean(df2.hour6$views)
hour7 <- mean(df2.hour7$views)
hour8 <- mean(df2.hour8$views)
hour9 <- mean(df2.hour9$views)
hour10 <- mean(df2.hour10$views)
hour11 <- mean(df2.hour11$views)
hour12 <- mean(df2.hour12$views)
hour13 <- mean(df2.hour13$views)
hour14 <- mean(df2.hour14$views)
hour15 <- mean(df2.hour15$views)
hour16 <- mean(df2.hour16$views)
hour17 <- mean(df2.hour17$views)
hour18 <- mean(df2.hour18$views)
hour19 <- mean(df2.hour19$views)
hour20 <- mean(df2.hour20$views)
hour21 <- mean(df2.hour21$views)
hour22 <- mean(df2.hour22$views)
hour23 <- mean(df2.hour23$views)
sumhour0 <- sum(df2.hour0$views)
sumhour1 <- sum(df2.hour1$views)
sumhour2 <- sum(df2.hour2$views)
sumhour3 <- sum(df2.hour3$views)
sumhour4 <- sum(df2.hour4$views)
sumhour5 <- sum(df2.hour5$views)
sumhour6 <- sum(df2.hour6$views)
sumhour7 <- sum(df2.hour7$views)
sumhour8 <- sum(df2.hour8$views)
sumhour9 <- sum(df2.hour9$views)
sumhour10 <- sum(df2.hour10$views)
sumhour11 <- sum(df2.hour11$views)
sumhour12 <- sum(df2.hour12$views)
sumhour13 <- sum(df2.hour13$views)
sumhour14 <- sum(df2.hour14$views)
sumhour15 <- sum(df2.hour15$views)
sumhour16 <- sum(df2.hour16$views)
sumhour17 <- sum(df2.hour17$views)
sumhour18 <- sum(df2.hour18$views)
sumhour19 <- sum(df2.hour19$views)
sumhour20 <- sum(df2.hour20$views)
sumhour21 <- sum(df2.hour21$views)
sumhour22 <- sum(df2.hour22$views)
sumhour23 <- sum(df2.hour23$views)

m = c(sumhour1, sumhour2, sumhour3, sumhour4, sumhour5, sumhour6, sumhour7, sumhour8, sumhour9, sumhour10, sumhour11, sumhour12, sumhour13, sumhour14, sumhour15, sumhour16, sumhour17, sumhour18, sumhour19, sumhour20, sumhour21, sumhour22, sumhour23, sumhour0)

plot(m, ylab="Number of views by hour", xlab="Hours", type = "o", col = "darkblue")

#Больше всего просмотров набирают статьи, опубликованные в 6 часов утра
df2$comments_lognorm <- NULL
df2$favs_lognorm <- NULL
df2$published = as.character(df2$published)
df2$year <- as.numeric(substring(df2$published, 1, 4))
df2$month <- as.numeric(substring(df2$published, 6, 7))
df2$day <- as.numeric(substring(df2$published, 9, 10))
df2$hour <- as.numeric(substring(df2$published, 12, 13))
df2.hour0 <- df2[df2$hour == 0, ]
df2.hour1 <- df2[df2$hour == 1, ]
df2.hour2 <- df2[df2$hour == 2, ]
df2.hour3 <- df2[df2$hour == 3, ]
df2.hour4 <- df2[df2$hour == 4, ]
df2.hour5 <- df2[df2$hour == 5, ]
df2.hour6 <- df2[df2$hour == 6, ]
df2.hour7 <- df2[df2$hour == 7, ]
df2.hour8 <- df2[df2$hour == 8, ]
df2.hour9 <- df2[df2$hour == 9, ]
df2.hour10 <- df2[df2$hour == 10, ]
df2.hour11 <- df2[df2$hour == 11, ]
df2.hour12 <- df2[df2$hour == 12, ]
df2.hour13 <- df2[df2$hour == 13, ]
df2.hour14 <- df2[df2$hour == 14, ]
df2.hour15 <- df2[df2$hour == 15, ]
df2.hour16 <- df2[df2$hour == 16, ]
df2.hour17 <- df2[df2$hour == 17, ]
df2.hour18 <- df2[df2$hour == 18, ]
df2.hour19 <- df2[df2$hour == 19, ]
df2.hour20 <- df2[df2$hour == 20, ]
df2.hour21 <- df2[df2$hour == 21, ]
df2.hour22 <- df2[df2$hour == 22, ]
df2.hour23 <- df2[df2$hour == 23, ]
df2.hour0 <- as.integer(df2.hour0$comments)
df2.hour1 <- as.integer(df2.hour1$comments)
df2.hour2 <- as.integer(df2.hour2$comments)
df2.hour3 <- as.integer(df2.hour3$comments)
df2.hour4 <- as.integer(df2.hour4$comments)
df2.hour5 <- as.integer(df2.hour5$comments)
df2.hour6 <- as.integer(df2.hour6$comments)
df2.hour7 <- as.integer(df2.hour7$comments)
df2.hour8 <- as.integer(df2.hour8$comments)
df2.hour9 <- as.integer(df2.hour9$comments)
df2.hour10 <- as.integer(df2.hour10$comments)
df2.hour11 <- as.integer(df2.hour11$comments)
df2.hour12 <- as.integer(df2.hour12$comments)
df2.hour13 <- as.integer(df2.hour13$comments)
df2.hour14 <- as.integer(df2.hour14$comments)
df2.hour15 <- as.integer(df2.hour15$comments)
df2.hour16 <- as.integer(df2.hour16$comments)
df2.hour17 <- as.integer(df2.hour17$comments)
df2.hour18 <- as.integer(df2.hour18$comments)
df2.hour19 <- as.integer(df2.hour19$comments)
df2.hour20 <- as.integer(df2.hour20$comments)
df2.hour21 <- as.integer(df2.hour21$comments)
df2.hour22 <- as.integer(df2.hour22$comments)
df2.hour23 <- as.integer(df2.hour23$comments)
hour0 <- mean(as.integer(df2.hour0), na.rm = TRUE)
hour1 <- mean(as.integer(df2.hour1), na.rm = TRUE)
hour2 <- mean(as.integer(df2.hour2), na.rm = TRUE)
hour3 <- mean(as.integer(df2.hour3), na.rm = TRUE)
hour4 <- mean(as.integer(df2.hour4), na.rm = TRUE)
hour5 <- mean(as.integer(df2.hour5), na.rm = TRUE)
hour6 <- mean(as.integer(df2.hour6), na.rm = TRUE)
hour7 <- mean(as.integer(df2.hour7), na.rm = TRUE)
hour8 <- mean(as.integer(df2.hour8), na.rm = TRUE)
hour9 <- mean(as.integer(df2.hour9), na.rm = TRUE)
hour10 <- mean(as.integer(df2.hour10), na.rm = TRUE)
hour11 <- mean(as.integer(df2.hour11), na.rm = TRUE)
hour12 <- mean(as.integer(df2.hour12), na.rm = TRUE)
hour13 <- mean(as.integer(df2.hour13), na.rm = TRUE)
hour14 <- mean(as.integer(df2.hour14), na.rm = TRUE)
hour15 <- mean(as.integer(df2.hour15), na.rm = TRUE)
hour16 <- mean(as.integer(df2.hour16), na.rm = TRUE)
hour17 <- mean(as.integer(df2.hour17), na.rm = TRUE)
hour18 <- mean(as.integer(df2.hour18), na.rm = TRUE)
hour19 <- mean(as.integer(df2.hour19), na.rm = TRUE)
hour20 <- mean(as.integer(df2.hour20), na.rm = TRUE)
hour21 <- mean(as.integer(df2.hour21), na.rm = TRUE)
hour22 <- mean(as.integer(df2.hour22), na.rm = TRUE)
hour23 <- mean(as.integer(df2.hour23), na.rm = TRUE)
sumhour0 <- sum(df2.hour0)
sumhour1 <- sum(df2.hour1)
sumhour2 <- sum(df2.hour2)
sumhour3 <- sum(df2.hour3)
sumhour4 <- sum(df2.hour4)
sumhour5 <- sum(df2.hour5)
sumhour6 <- sum(df2.hour6)
sumhour7 <- sum(df2.hour7)
sumhour8 <- sum(df2.hour8)
sumhour9 <- sum(df2.hour9)
sumhour10 <- sum(df2.hour10)
sumhour11 <- sum(df2.hour11)
sumhour12 <- sum(df2.hour12)
sumhour13 <- sum(df2.hour13)
sumhour14 <- sum(df2.hour14)
sumhour15 <- sum(df2.hour15)
sumhour16 <- sum(df2.hour16)
sumhour17 <- sum(df2.hour17)
sumhour18 <- sum(df2.hour18)
sumhour19 <- sum(df2.hour19)
sumhour20 <- sum(df2.hour20)
sumhour21 <- sum(df2.hour21)
sumhour22 <- sum(df2.hour22)
sumhour23 <- sum(df2.hour23)

m = c(hour1, hour2, hour3, hour4, hour5, hour6, hour7, hour8, hour9, hour10, hour11, hour12, hour13, hour14, hour15, hour16, hour17, hour18, hour19, hour20, hour21, hour22, hour23, hour0)
plot(m, ylab="Average number of comments by hour", xlab="Hours", type = "o", col = "blue4")

#Максимальное число комментариев на гиктаймсе набрала статья, опубликованная в 9 часов вечера
df2$comments_lognorm <- NULL
df2$favs_lognorm <- NULL
df2$published = as.character(df2$published)
df2$year <- as.numeric(substring(df2$published, 1, 4))
df2$month <- as.numeric(substring(df2$published, 6, 7))
df2$day <- as.numeric(substring(df2$published, 9, 10))
df2$hour <- as.numeric(substring(df2$published, 12, 13))
df2.hour0 <- df2[df2$hour == 0, ]
df2.hour1 <- df2[df2$hour == 1, ]
df2.hour2 <- df2[df2$hour == 2, ]
df2.hour3 <- df2[df2$hour == 3, ]
df2.hour4 <- df2[df2$hour == 4, ]
df2.hour5 <- df2[df2$hour == 5, ]
df2.hour6 <- df2[df2$hour == 6, ]
df2.hour7 <- df2[df2$hour == 7, ]
df2.hour8 <- df2[df2$hour == 8, ]
df2.hour9 <- df2[df2$hour == 9, ]
df2.hour10 <- df2[df2$hour == 10, ]
df2.hour11 <- df2[df2$hour == 11, ]
df2.hour12 <- df2[df2$hour == 12, ]
df2.hour13 <- df2[df2$hour == 13, ]
df2.hour14 <- df2[df2$hour == 14, ]
df2.hour15 <- df2[df2$hour == 15, ]
df2.hour16 <- df2[df2$hour == 16, ]
df2.hour17 <- df2[df2$hour == 17, ]
df2.hour18 <- df2[df2$hour == 18, ]
df2.hour19 <- df2[df2$hour == 19, ]
df2.hour20 <- df2[df2$hour == 20, ]
df2.hour21 <- df2[df2$hour == 21, ]
df2.hour22 <- df2[df2$hour == 22, ]
df2.hour23 <- df2[df2$hour == 23, ]
df2.hour0.geek <- df2.hour0[df2.hour0$domain == "geektimes.ru", ]
df2.hour0.geek <- as.integer(df2.hour0.geek$comments)
df2.hour1.geek <- df2.hour1[df2.hour1$domain == "geektimes.ru", ]
df2.hour1.geek <- as.integer(df2.hour1.geek$comments)
df2.hour2.geek <- df2.hour2[df2.hour2$domain == "geektimes.ru", ]
df2.hour2.geek <- as.integer(df2.hour2.geek$comments)
df2.hour3.geek <- df2.hour3[df2.hour3$domain == "geektimes.ru", ]
df2.hour3.geek <- as.integer(df2.hour3.geek$comments)
df2.hour4.geek <- df2.hour4[df2.hour4$domain == "geektimes.ru", ]
df2.hour4.geek <- as.integer(df2.hour4.geek$comments)
df2.hour5.geek <- df2.hour5[df2.hour5$domain == "geektimes.ru", ]
df2.hour5.geek <- as.integer(df2.hour5.geek$comments)
df2.hour6.geek <- df2.hour6[df2.hour6$domain == "geektimes.ru", ]
df2.hour6.geek <- as.integer(df2.hour6.geek$comments)
df2.hour7.geek <- df2.hour7[df2.hour7$domain == "geektimes.ru", ]
df2.hour7.geek <- as.integer(df2.hour7.geek$comments)
df2.hour8.geek <- df2.hour8[df2.hour8$domain == "geektimes.ru", ]
df2.hour8.geek <- as.integer(df2.hour8.geek$comments)
df2.hour9.geek <- df2.hour9[df2.hour9$domain == "geektimes.ru", ]
df2.hour9.geek <- as.integer(df2.hour9.geek$comments)
df2.hour10.geek <- df2.hour10[df2.hour10$domain == "geektimes.ru", ]
df2.hour10.geek <- as.integer(df2.hour10.geek$comments)
df2.hour11.geek <- df2.hour11[df2.hour11$domain == "geektimes.ru", ]
df2.hour11.geek <- as.integer(df2.hour11.geek$comments)
df2.hour12.geek <- df2.hour12[df2.hour12$domain == "geektimes.ru", ]
df2.hour12.geek <- as.integer(df2.hour12.geek$comments)
df2.hour13.geek <- df2.hour13[df2.hour13$domain == "geektimes.ru", ]
df2.hour13.geek <- as.integer(df2.hour13.geek$comments)
df2.hour14.geek <- df2.hour14[df2.hour14$domain == "geektimes.ru", ]
df2.hour14.geek <- as.integer(df2.hour14.geek$comments)
df2.hour15.geek <- df2.hour15[df2.hour15$domain == "geektimes.ru", ]
df2.hour15.geek <- as.integer(df2.hour15.geek$comments)
df2.hour16.geek <- df2.hour16[df2.hour16$domain == "geektimes.ru", ]
df2.hour16.geek <- as.integer(df2.hour16.geek$comments)
df2.hour17.geek <- df2.hour17[df2.hour17$domain == "geektimes.ru", ]
df2.hour17.geek <- as.integer(df2.hour17.geek$comments)
df2.hour18.geek <- df2.hour18[df2.hour18$domain == "geektimes.ru", ]
df2.hour18.geek <- as.integer(df2.hour18.geek$comments)
df2.hour19.geek <- df2.hour19[df2.hour19$domain == "geektimes.ru", ]
df2.hour19.geek <- as.integer(df2.hour19.geek$comments)
df2.hour20.geek <- df2.hour20[df2.hour20$domain == "geektimes.ru", ]
df2.hour20.geek <- as.integer(df2.hour20.geek$comments)
df2.hour21.geek <- df2.hour21[df2.hour21$domain == "geektimes.ru", ]
df2.hour21.geek <- as.integer(df2.hour21.geek$comments)
df2.hour22.geek <- df2.hour22[df2.hour22$domain == "geektimes.ru", ]
df2.hour22.geek <- as.integer(df2.hour22.geek$comments)
df2.hour23.geek <- df2.hour23[df2.hour23$domain == "geektimes.ru", ]
df2.hour23.geek <- as.integer(df2.hour23.geek$comments)
hour0 <- max(as.integer(df2.hour0.geek), na.rm = TRUE)
hour1 <- max(as.integer(df2.hour1.geek), na.rm = TRUE)
hour2 <- max(as.integer(df2.hour2.geek), na.rm = TRUE)
hour3 <- max(as.integer(df2.hour3.geek), na.rm = TRUE)
hour4 <- max(as.integer(df2.hour4.geek), na.rm = TRUE)
hour5 <- max(as.integer(df2.hour5.geek), na.rm = TRUE)
hour6 <- max(as.integer(df2.hour6.geek), na.rm = TRUE)
hour7 <- max(as.integer(df2.hour7.geek), na.rm = TRUE)
hour8 <- max(as.integer(df2.hour8.geek), na.rm = TRUE)
hour9 <- max(as.integer(df2.hour9.geek), na.rm = TRUE)
hour10 <- max(as.integer(df2.hour10.geek), na.rm = TRUE)
hour11 <- max(as.integer(df2.hour11.geek), na.rm = TRUE)
hour12 <- max(as.integer(df2.hour12.geek), na.rm = TRUE)
hour13 <- max(as.integer(df2.hour13.geek), na.rm = TRUE)
hour14 <- max(as.integer(df2.hour14.geek), na.rm = TRUE)
hour15 <- max(as.integer(df2.hour15.geek), na.rm = TRUE)
hour16 <- max(as.integer(df2.hour16.geek), na.rm = TRUE)
hour17 <- max(as.integer(df2.hour17.geek), na.rm = TRUE)
hour18 <- max(as.integer(df2.hour18.geek), na.rm = TRUE)
hour19 <- max(as.integer(df2.hour19.geek), na.rm = TRUE)
hour20 <- max(as.integer(df2.hour20.geek), na.rm = TRUE)
hour21 <- max(as.integer(df2.hour21.geek), na.rm = TRUE)
hour22 <- max(as.integer(df2.hour22.geek), na.rm = TRUE)
hour23 <- max(as.integer(df2.hour23.geek), na.rm = TRUE)
m = c(hour1, hour2, hour3, hour4, hour5, hour6, hour7, hour8, hour9, hour10, hour11, hour12, hour13, hour14, hour15, hour16, hour17, hour18, hour19, hour20, hour21, hour22, hour23, hour0)
plot(m, ylab="Max number of comments by hour", xlab="Hours", type = "o", col = "blue4")

#На хабре дневные статьи комментируют чаще, чем вечерние
df2$comments_lognorm <- NULL
df2$favs_lognorm <- NULL
df2$published = as.character(df2$published)
df2$year <- as.numeric(substring(df2$published, 1, 4))
df2$month <- as.numeric(substring(df2$published, 6, 7))
df2$day <- as.numeric(substring(df2$published, 9, 10))
df2$hour <- as.numeric(substring(df2$published, 12, 13))
df2.hour0 <- df2[df2$hour == 0, ]
df2.hour1 <- df2[df2$hour == 1, ]
df2.hour2 <- df2[df2$hour == 2, ]
df2.hour3 <- df2[df2$hour == 3, ]
df2.hour4 <- df2[df2$hour == 4, ]
df2.hour5 <- df2[df2$hour == 5, ]
df2.hour6 <- df2[df2$hour == 6, ]
df2.hour7 <- df2[df2$hour == 7, ]
df2.hour8 <- df2[df2$hour == 8, ]
df2.hour9 <- df2[df2$hour == 9, ]
df2.hour10 <- df2[df2$hour == 10, ]
df2.hour11 <- df2[df2$hour == 11, ]
df2.hour12 <- df2[df2$hour == 12, ]
df2.hour13 <- df2[df2$hour == 13, ]
df2.hour14 <- df2[df2$hour == 14, ]
df2.hour15 <- df2[df2$hour == 15, ]
df2.hour16 <- df2[df2$hour == 16, ]
df2.hour17 <- df2[df2$hour == 17, ]
df2.hour18 <- df2[df2$hour == 18, ]
df2.hour19 <- df2[df2$hour == 19, ]
df2.hour20 <- df2[df2$hour == 20, ]
df2.hour21 <- df2[df2$hour == 21, ]
df2.hour22 <- df2[df2$hour == 22, ]
df2.hour23 <- df2[df2$hour == 23, ]
df2.hour0.habr <- df2.hour0[df2.hour0$domain == "habrahabr.ru", ]
df2.hour0.habr <- as.integer(df2.hour0.habr$comments)
df2.hour1.habr <- df2.hour1[df2.hour1$domain == "habrahabr.ru", ]
df2.hour1.habr <- as.integer(df2.hour1.habr$comments)
df2.hour2.habr <- df2.hour2[df2.hour2$domain == "habrahabr.ru", ]
df2.hour2.habr <- as.integer(df2.hour2.habr$comments)
df2.hour3.habr <- df2.hour3[df2.hour3$domain == "habrahabr.ru", ]
df2.hour3.habr <- as.integer(df2.hour3.habr$comments)
df2.hour4.habr <- df2.hour4[df2.hour4$domain == "habrahabr.ru", ]
df2.hour4.habr <- as.integer(df2.hour4.habr$comments)
df2.hour5.habr <- df2.hour5[df2.hour5$domain == "habrahabr.ru", ]
df2.hour5.habr <- as.integer(df2.hour5.habr$comments)
df2.hour6.habr <- df2.hour6[df2.hour6$domain == "habrahabr.ru", ]
df2.hour6.habr <- as.integer(df2.hour6.habr$comments)
df2.hour7.habr <- df2.hour7[df2.hour7$domain == "habrahabr.ru", ]
df2.hour7.habr <- as.integer(df2.hour7.habr$comments)
df2.hour8.habr <- df2.hour8[df2.hour8$domain == "habrahabr.ru", ]
df2.hour8.habr <- as.integer(df2.hour8.habr$comments)
df2.hour9.habr <- df2.hour9[df2.hour9$domain == "habrahabr.ru", ]
df2.hour9.habr <- as.integer(df2.hour9.habr$comments)
df2.hour10.habr <- df2.hour10[df2.hour10$domain == "habrahabr.ru", ]
df2.hour10.habr <- as.integer(df2.hour10.habr$comments)
df2.hour11.habr <- df2.hour11[df2.hour11$domain == "habrahabr.ru", ]
df2.hour11.habr <- as.integer(df2.hour11.habr$comments)
df2.hour12.habr <- df2.hour12[df2.hour12$domain == "habrahabr.ru", ]
df2.hour12.habr <- as.integer(df2.hour12.habr$comments)
df2.hour13.habr <- df2.hour13[df2.hour13$domain == "habrahabr.ru", ]
df2.hour13.habr <- as.integer(df2.hour13.habr$comments)
df2.hour14.habr <- df2.hour14[df2.hour14$domain == "habrahabr.ru", ]
df2.hour14.habr <- as.integer(df2.hour14.habr$comments)
df2.hour15.habr <- df2.hour15[df2.hour15$domain == "habrahabr.ru", ]
df2.hour15.habr <- as.integer(df2.hour15.habr$comments)
df2.hour16.habr <- df2.hour16[df2.hour16$domain == "habrahabr.ru", ]
df2.hour16.habr <- as.integer(df2.hour16.habr$comments)
df2.hour17.habr <- df2.hour17[df2.hour17$domain == "habrahabr.ru", ]
df2.hour17.habr <- as.integer(df2.hour17.habr$comments)
df2.hour18.habr <- df2.hour18[df2.hour18$domain == "habrahabr.ru", ]
df2.hour18.habr <- as.integer(df2.hour18.habr$comments)
df2.hour19.habr <- df2.hour19[df2.hour19$domain == "habrahabr.ru", ]
df2.hour19.habr <- as.integer(df2.hour19.habr$comments)
df2.hour20.habr <- df2.hour20[df2.hour20$domain == "habrahabr.ru", ]
df2.hour20.habr <- as.integer(df2.hour20.habr$comments)
df2.hour21.habr <- df2.hour21[df2.hour21$domain == "habrahabr.ru", ]
df2.hour21.habr <- as.integer(df2.hour21.habr$comments)
df2.hour22.habr <- df2.hour22[df2.hour22$domain == "habrahabr.ru", ]
df2.hour22.habr <- as.integer(df2.hour22.habr$comments)
df2.hour23.habr <- df2.hour23[df2.hour23$domain == "habrahabr.ru", ]
df2.hour23.habr <- as.integer(df2.hour23.habr$comments)
hour0 <- mean(as.integer(df2.hour0.habr), na.rm = TRUE)
hour1 <- mean(as.integer(df2.hour1.habr), na.rm = TRUE)
hour2 <- mean(as.integer(df2.hour2.habr), na.rm = TRUE)
hour3 <- mean(as.integer(df2.hour3.habr), na.rm = TRUE)
hour4 <- mean(as.integer(df2.hour4.habr), na.rm = TRUE)
hour5 <- mean(as.integer(df2.hour5.habr), na.rm = TRUE)
hour6 <- mean(as.integer(df2.hour6.habr), na.rm = TRUE)
hour7 <- mean(as.integer(df2.hour7.habr), na.rm = TRUE)
hour8 <- mean(as.integer(df2.hour8.habr), na.rm = TRUE)
hour9 <- mean(as.integer(df2.hour9.habr), na.rm = TRUE)
hour10 <- mean(as.integer(df2.hour10.habr), na.rm = TRUE)
hour11 <- mean(as.integer(df2.hour11.habr), na.rm = TRUE)
hour12 <- mean(as.integer(df2.hour12.habr), na.rm = TRUE)
hour13 <- mean(as.integer(df2.hour13.habr), na.rm = TRUE)
hour14 <- mean(as.integer(df2.hour14.habr), na.rm = TRUE)
hour15 <- mean(as.integer(df2.hour15.habr), na.rm = TRUE)
hour16 <- mean(as.integer(df2.hour16.habr), na.rm = TRUE)
hour17 <- mean(as.integer(df2.hour17.habr), na.rm = TRUE)
hour18 <- mean(as.integer(df2.hour18.habr), na.rm = TRUE)
hour19 <- mean(as.integer(df2.hour19.habr), na.rm = TRUE)
hour20 <- mean(as.integer(df2.hour20.habr), na.rm = TRUE)
hour21 <- mean(as.integer(df2.hour21.habr), na.rm = TRUE)
hour22 <- mean(as.integer(df2.hour22.habr), na.rm = TRUE)
hour23 <- mean(as.integer(df2.hour23.habr), na.rm = TRUE)

m = c(hour1, hour2, hour3, hour4, hour5, hour6, hour7, hour8, hour9, hour10, hour11, hour12, hour13, hour14, hour15, hour16, hour17, hour18, hour19, hour20, hour21, hour22, hour23, hour0)
plot(m, ylab="Average number of comments by hour", xlab="Hours", type = "o", col = "blue4")

"""## 4\. Кого из топ-20 авторов чаще всего минусуют?

* @Mordatyj
* @Mithgol
* @alizar
* @ilya42

"""

df2$comments_lognorm <- NULL
df2$favs_lognorm <- NULL
df2$published = as.character(df2$published)
df2$year <- as.numeric(substring(df2$published, 1, 4))
df2$month <- as.numeric(substring(df2$published, 6, 7))
df2$day <- as.numeric(substring(df2$published, 9, 10))
df2$hour <- as.numeric(substring(df2$published, 12, 13))
df2.Mordatyj <- df2[df2$author == "@Mordatyj", ]
df2.Mithgol <- df2[df2$author == "@Mithgol", ]
df2.alizar <- df2[df2$author == "@alizar", ]
df2.ilya42 <- df2[df2$author == "@ilya42", ]
df2.Mordatyj.votes <- as.integer(df2.Mordatyj$votes_minus)
df2.Mithgol.votes <- as.integer(df2.Mithgol$votes_minus)
df2.alizar.votes <- as.integer(df2.alizar$votes_minus)
df2.ilya42.votes <- as.integer(df2.ilya42$votes_minus)
df2.Mordatyj.average.votes <- mean(as.integer(df2.Mordatyj.votes), na.rm = TRUE)
df2.Mithgol.average.votes <- mean(as.integer(df2.Mithgol.votes), na.rm = TRUE)
df2.alizar.average.votes <- mean(as.integer(df2.alizar.votes), na.rm = TRUE)
df2.ilya42.average.votes <- mean(as.integer(df2.ilya42.votes), na.rm = TRUE)
df2.Mordatyj.average.votes
df2.Mithgol.average.votes
df2.alizar.average.votes
df2.ilya42.average.votes
m = rbind(c(df2.Mordatyj.average.votes, df2.Mithgol.average.votes, df2.alizar.average.votes, df2.ilya42.average.votes))
colnames(m) = c("Mordatyj", "Mithgol", "alizar", "ilya42")
rownames(m) = c("authors")
barplot(m, ylab="Average number of minus votes", xlab="authors", col = topo.colors(4),  border = "black", beside=TRUE)
print("Ответ:@Mithgol")

"""## 5\. Сравните субботы и понедельники

Правда ли, что по субботам авторы пишут в основном днём, а по понедельникам — в основном вечером?

"""

df2$published = as.character(df2$published)
df2$year <- as.numeric(substring(df2$published, 1, 4))
df2$month <- as.numeric(substring(df2$published, 6, 7))
df2$day <- as.numeric(substring(df2$published, 9, 10))
df2$dayofweek <- weekdays(as.Date(df2$published,'%Y-%m-%d'))
saturday0 <- nrow(subset(df2, (df2$hour == 0 & df2$dayofweek == "Saturday")))
saturday1 <- nrow(subset(df2, (df2$hour == 1 & df2$dayofweek == "Saturday")))
saturday2 <- nrow(subset(df2, (df2$hour == 2 & df2$dayofweek == "Saturday")))
saturday3 <- nrow(subset(df2, (df2$hour == 3 & df2$dayofweek == "Saturday")))
saturday4 <- nrow(subset(df2, (df2$hour == 4 & df2$dayofweek == "Saturday")))
saturday5 <- nrow(subset(df2, (df2$hour == 5 & df2$dayofweek == "Saturday")))
saturday6 <- nrow(subset(df2, (df2$hour == 6 & df2$dayofweek == "Saturday")))
saturday7 <- nrow(subset(df2, (df2$hour == 7 & df2$dayofweek == "Saturday")))
saturday8 <- nrow(subset(df2, (df2$hour == 8 & df2$dayofweek == "Saturday")))
saturday9 <- nrow(subset(df2, (df2$hour == 9 & df2$dayofweek == "Saturday")))
saturday10 <- nrow(subset(df2, (df2$hour == 10 & df2$dayofweek == "Saturday")))
saturday11 <- nrow(subset(df2, (df2$hour == 11 & df2$dayofweek == "Saturday")))
saturday12 <- nrow(subset(df2, (df2$hour == 12 & df2$dayofweek == "Saturday")))
saturday13 <- nrow(subset(df2, (df2$hour == 13 & df2$dayofweek == "Saturday")))
saturday14 <- nrow(subset(df2, (df2$hour == 14 & df2$dayofweek == "Saturday")))
saturday15 <- nrow(subset(df2, (df2$hour == 15 & df2$dayofweek == "Saturday")))
saturday16 <- nrow(subset(df2, (df2$hour == 16 & df2$dayofweek == "Saturday")))
saturday17 <- nrow(subset(df2, (df2$hour == 17 & df2$dayofweek == "Saturday")))
saturday18 <- nrow(subset(df2, (df2$hour == 18 & df2$dayofweek == "Saturday")))
saturday19 <- nrow(subset(df2, (df2$hour == 19 & df2$dayofweek == "Saturday")))
saturday20 <- nrow(subset(df2, (df2$hour == 20 & df2$dayofweek == "Saturday")))
saturday21 <- nrow(subset(df2, (df2$hour == 21 & df2$dayofweek == "Saturday")))
saturday22 <- nrow(subset(df2, (df2$hour == 22 & df2$dayofweek == "Saturday")))
saturday23 <- nrow(subset(df2, (df2$hour == 23 & df2$dayofweek == "Saturday")))
monday0 <- nrow(subset(df2, (df2$hour == 0 & df2$dayofweek == "Monday")))
monday1 <- nrow(subset(df2, (df2$hour == 1 & df2$dayofweek == "Monday")))
monday2 <- nrow(subset(df2, (df2$hour == 2 & df2$dayofweek == "Monday")))
monday3 <- nrow(subset(df2, (df2$hour == 3 & df2$dayofweek == "Monday")))
monday4 <- nrow(subset(df2, (df2$hour == 4 & df2$dayofweek == "Monday")))
monday5 <- nrow(subset(df2, (df2$hour == 5 & df2$dayofweek == "Monday")))
monday6 <- nrow(subset(df2, (df2$hour == 6 & df2$dayofweek == "Monday")))
monday7 <- nrow(subset(df2, (df2$hour == 7 & df2$dayofweek == "Monday")))
monday8 <- nrow(subset(df2, (df2$hour == 8 & df2$dayofweek == "Monday")))
monday9 <- nrow(subset(df2, (df2$hour == 9 & df2$dayofweek == "Monday")))
monday10 <- nrow(subset(df2, (df2$hour == 10 & df2$dayofweek == "Monday")))
monday11 <- nrow(subset(df2, (df2$hour == 11 & df2$dayofweek == "Monday")))
monday12 <- nrow(subset(df2, (df2$hour == 12 & df2$dayofweek == "Monday")))
monday13 <- nrow(subset(df2, (df2$hour == 13 & df2$dayofweek == "Monday")))
monday14 <- nrow(subset(df2, (df2$hour == 14 & df2$dayofweek == "Monday")))
monday15 <- nrow(subset(df2, (df2$hour == 15 & df2$dayofweek == "Monday")))
monday16 <- nrow(subset(df2, (df2$hour == 16 & df2$dayofweek == "Monday")))
monday17 <- nrow(subset(df2, (df2$hour == 17 & df2$dayofweek == "Monday")))
monday18 <- nrow(subset(df2, (df2$hour == 18 & df2$dayofweek == "Monday")))
monday19 <- nrow(subset(df2, (df2$hour == 19 & df2$dayofweek == "Monday")))
monday20 <- nrow(subset(df2, (df2$hour == 20 & df2$dayofweek == "Monday")))
monday21 <- nrow(subset(df2, (df2$hour == 21 & df2$dayofweek == "Monday")))
monday22 <- nrow(subset(df2, (df2$hour == 22 & df2$dayofweek == "Monday")))
monday23 <- nrow(subset(df2, (df2$hour == 23 & df2$dayofweek == "Monday")))
m <- rbind(c(monday0, monday1, monday2, monday3, monday4, monday5, monday6, monday7, monday8, monday9, monday10, monday11, monday12, monday13, monday14, monday15, monday16, monday17, monday18,
monday19, monday20, monday21, monday22, monday23),
c(saturday0, saturday1, saturday2, saturday3, saturday4, saturday5, saturday6, saturday7, saturday8, saturday9, saturday10, saturday11, saturday12, saturday13, saturday14, saturday15, saturday16, saturday17, saturday18,
saturday19, saturday20, saturday21, saturday22, saturday23))
colnames(m) <- c("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23")
rownames(m) <- c("Mondays", "Saturdays")

barplot(m, ylab="Number of texts by hour on mondays and saturdays", xlab="hours", beside=TRUE, legend = rownames(m), col = topo.colors(2),  border = "black")