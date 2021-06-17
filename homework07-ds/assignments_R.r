# -*- coding: utf-8 -*-
library(ggplot2)
library(dplyr)
library(tidyverse)
library(lubridate)
library(scales)
library(readxl)

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
y_2015_m_03 <- subset(y_2015, month == 3)
y_2015_m_04 <- subset(y_2015, month == 4)
y_2016_m_03 <- subset(y_2016, month == 3)
y_2016_m_04 <- subset(y_2016, month == 4)

m <- rbind(c(nrow(y_2015_m_03), nrow(y_2016_m_03)), c(nrow(y_2015_m_04), nrow(y_2016_m_04)))
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

# Первый вариант

library(data.table)

y_2015_m_03_days <- y_2015_m_03$day
table <- data.table(y_2015_m_03_days)
grouped_table <- table[, .N, by = names(table)]
data <- grouped_table$N
m = rbind(c(data[1:31]))
colnames(m) = c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
rownames(m) = c("number of texts")
barplot(m, ylab=rownames(m), xlab="days", beside=TRUE, col = rainbow(31),  border = "black")

#Второй вариант

y_2015_m_03_habr <- subset(y_2015_m_03, domain == "habrahabr.ru")
y_2015_m_03_geek <- subset(y_2015_m_03, domain == "geektimes.ru")
y_2015_m_03_habr_days <- y_2015_m_03_habr$day
table_habr <- data.table(y_2015_m_03_habr_days)
grouped_table_habr <- table_habr[, .N, by = names(table_habr)]
data_habr <- grouped_table_habr$N
y_2015_m_03_geek_days <- y_2015_m_03_geek$day
table_geek <- data.table(y_2015_m_03_geek_days)
grouped_table_geek <- table_geek[, .N, by = names(table_geek)]
data_geek <- grouped_table_geek$N
m = rbind(c(data_geek[1:31]), c(data_habr[1:31]))
colnames(m) = c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
rownames(m) = c("geektimes.ru", "habrahabr.ru")
barplot(m, ylab="Number of texts on each site", xlab="days", beside=TRUE, legend = rownames(m), col = topo.colors(2),  border = "black")

#Третий вариант

Saturdays <- function(year, month) {
    days <- as.POSIXlt(paste(year, month, 1:31, sep="-"), format="%Y-%m-%j")
    Std <- (days[days$wday==6])
    Std[!is.na(Std)]
}
a <- (Saturdays(2015, 3))

fst_saturday <- as.character(a[1])
day1 <- as.numeric(substring(fst_saturday, 9, 10))
snd_saturday <- as.character(a[2])
day2 <- as.numeric(substring(snd_saturday, 9, 10))
trd_saturday <- as.character(a[3])
day3 <- as.numeric(substring(trd_saturday, 9, 10))
fth_saturday <- as.character(a[4])
day4 <- as.numeric(substring(fth_saturday, 9, 10))

fst_saturday_habr <- nrow(subset(y_2015_m_03_habr, y_2015_m_03_habr$day == day1))
snd_saturday_habr <- nrow(subset(y_2015_m_03_habr, y_2015_m_03_habr$day == day2))
trd_saturday_habr <- nrow(subset(y_2015_m_03_habr, y_2015_m_03_habr$day == day3))
fth_saturday_habr <- nrow(subset(y_2015_m_03_habr, y_2015_m_03_habr$day == day4))

fst_saturday_geek <- nrow(subset(y_2015_m_03_geek, y_2015_m_03_geek$day == day1))
snd_saturday_geek <- nrow(subset(y_2015_m_03_geek, y_2015_m_03_geek$day == day2))
trd_saturday_geek <- nrow(subset(y_2015_m_03_geek, y_2015_m_03_geek$day == day3))
fth_saturday_geek <- nrow(subset(y_2015_m_03_geek, y_2015_m_03_geek$day == day4))

m = rbind(c(fst_saturday_geek, snd_saturday_geek, trd_saturday_geek, fth_saturday_geek),
c(fst_saturday_habr, snd_saturday_habr, trd_saturday_habr, fth_saturday_habr))
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

#Первый вариант

df2 %>%
  group_by(hour = hour(published)) %>%
  summarise(views = sum(views)) %>% 
  ggplot(aes(x = hour, y = views))+
  geom_line(color = "#CC0033", size = 1.25) +
  geom_point(size = 3)

dataf <- read.csv("howpop_train.csv", header = TRUE, sep = ',')
to.remove <- c('views_lognorm', 'favs_lognorm', 'comments_lognorm') 
dataf <- dataf[, !colnames(dataf) %in% to.remove]

dataf %>%
  group_by(hour = hour(published)) %>%
  summarise(views = sum(views)) %>% 
  ggplot(aes(x = hour, y = views))+
  geom_col(color = "#99FFFF")+
  geom_line(color = "#CC0033", size = 1.25) +
  geom_point(size = 2)

#Второй вариант

df2 %>%
  group_by(hour = hour(published)) %>%
  summarise(views = sum(views)) %>% 
  ggplot(aes(x = hour, y = views))+
  geom_line(color = "#CC3300") +
  geom_point(size = 2)

df2 %>%
  group_by(hour = hour(published)) %>%
  summarise(views = sum(views)) %>%
  ggplot(aes(x = hour, y = views))+
  geom_col(color = "#99FFFF") 

#Третий вариант

df2 %>%
  group_by(hour = hour(published)) %>%
  summarise(comments = sum(comments)) %>% 
  ggplot(aes(x = hour, y = comments))+
  geom_line(color = "#CC0033", size = 1.25) +
  geom_point(size = 3)

dataf %>%
  group_by(hour = hour(published)) %>%
  summarise(comments = sum(comments)) %>% 
  ggplot(aes(x = hour, y = comments))+
  geom_col(color = "#99FFFF")

#Четвёртый вариант

dfgt <- subset(df2, domain == "geektimes.ru")
dfgt %>%
  group_by(hour = hour(published)) %>%
  summarise(comments = max(comments)) %>% 
  ggplot(aes(x = hour, y = comments))+
  geom_line(color = "#CC0033", size = 1.25) +
  geom_point(size = 3)

datafg <- subset(dataf, domain == "geektimes.ru")
datafg %>%
  group_by(hour = hour(published)) %>%
  summarise(comments = max(comments)) %>% 
  ggplot(aes(x = hour, y = comments))+
  geom_col(color = "#99FFFF")

#Пятый вариант

dfhabr <- subset(df2, domain == "habrahabr.ru")
dfhabr %>%
  group_by(hour = hour(published)) %>%
  summarise(comments = mean(comments)) %>% 
  ggplot(aes(x = hour, y = comments))+
  geom_line(color = "#CC0033", size = 1.25) +
  geom_point(size = 3)

datafh <- subset(dataf, domain == "habrahabr.ru")
datafh %>%
  group_by(hour = hour(published)) %>%
  summarise(comments = mean(comments)) %>%
  ggplot(aes(x = hour, y = comments))+
  geom_col(color = "#99FFFF")

"""## 4\. Кого из топ-20 авторов чаще всего минусуют?
* @Mordatyj
* @Mithgol
* @alizar
* @ilya42
"""

df2 <- na.omit(df2)
Mordatyj <- mean(df2[df2["author"] == '@Mordatyj', 'votes_minus'])
Mithgol <- mean(df2[df2["author"] == '@Mithgol', 'votes_minus'])
alizar <- mean(df2[df2["author"] == '@alizar', 'votes_minus'])
ilya42 <- mean(df2[df2["author"] == '@ilya42', 'votes_minus'])
m = rbind(c(Mordatyj, Mithgol, alizar, ilya42))
colnames(m) = c("Mordatyj", "Mithgol", "alizar", "ilya42")
rownames(m) = c("authors")
barplot(m, ylab="Comments", xlab="Authors", col = topo.colors(4), border = "black", beside=TRUE)

"""## 5\. Сравните субботы и понедельники
Правда ли, что по субботам авторы пишут в основном днём, а по понедельникам — в основном вечером?
"""

df2$published <- as.Date(df2$published)
df2$weekday = weekdays(df2$published)
Saturdays <- subset(df2, weekday == "Saturday")
Mondays <- subset(df2, weekday == "Monday")
Saturdays_hours <- as.integer(Saturdays$hour)
table_saturday <- data.table(Saturdays_hours)
table_saturday <- table_saturday[order(table_saturday, decreasing = FALSE),] 
grouped_table_saturday <- table_saturday[, .N, by = names(table_saturday)]
data_saturday <- grouped_table_saturday$N
Mondays_hours <- as.integer(Mondays$hour)
table_monday <- data.table(Mondays_hours)
table_monday <- table_monday[order(table_monday, decreasing = FALSE),]
grouped_table_monday <- table_monday[, .N, by = names(table_monday)]
data_monday <- grouped_table_monday$N
m = rbind(c(data_monday[1:24]), c(data_saturday[1:24]))
colnames(m) <- c("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23")
rownames(m) <- c("Mondays", "Saturdays")
barplot(m, ylab="Number of texts by hour on mondays and saturdays", xlab="hours", beside=TRUE, legend = rownames(m), col = topo.colors(2),  border = "black")