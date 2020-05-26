library(devtools)

install.packages("devtools")
install.packages("effsize")

install.packages("RedditExtractoR")
#install.packages("usethis")
#install.packages("glue_collapse")

install_github("ianhussey/simpleNLP")

#install_github('NLP', repos="https://github.com/ianhussey/simpleNLP")
#install_github("NLP",username="ianhussey")

#install.packages('RMySQL', repos='http://cran.us.r-project.org')
library(NLP)
library(simpleNLP)
library(tidyverse)
library(effsize)
library(RedditExtractoR)

autismdesc_url = "reddit.com/r/AskReddit/comments/5q9ppf/autistic_people_of_reddit_what_is_autism_really/"
url_data = reddit_content(autismdesc_url)
graph_object = construct_graph(url_data)

closeAllConnections() 
write.table(url_data,"whatisautismreally.csv",sep="|")

print(url_data)
cat(url_data)
url_data
colnames(url_data)


typeof(url_data)
reddit_data = get_reddit(search_terms = "autism,mind",subreddit = "AskReddit",cn_threshold=10)

example_urls = reddit_urls(search_terms="autism")

## Ian Hussey NLP
## https://github.com/ianhussey/simpleNLP/blob/master/vignettes/demo.Rmd
library(tidyverse)
library(simpleNLP)
library(tidyverse)
library(effsize)

                                        # process data
#tidy_data <- tidy_parcels(data = reddit_suicide_data)

autism_data <- read_csv(file="data/3_alphanumberic_and_punctuation_only.csv")

## don't use ply and rename it breaks dplyr
#library(plyr)
#rename(autism_data, c("identifier"="id", "comments"="parcel"))
#


colnames(reddit_suicide_data)
colnames(autism_data)


?tidy_parcels

tidied_data <- tidy_parcels(data = autism_data)

tidy_data <- tidy_parcels(data = autism_data)
ls(parcels)
ls()
?tidy_parcels



###### Let's try this from scratch
## https://github.com/ianhussey/simpleNLP/blob/master/vignettes/usage.Rmd
library(simpleNLP)
library(tidyverse)
library(effsize)

tidy_data <- tidy_parcels(data = reddit_suicide_data)
autism_data <- read_csv(file="data/3_alphanumberic_and_punctuation_only.csv")

nrow(autism_data)

names(autism_data)
names(reddit_suicide_data)
colnames(autism_data)

autism_data <- read_csv(file="data/3_alphanumberic_and_punctuation_only.csv")


##  ____                                 
## |  _ \ ___ _ __   __ _ _ __ ___   ___ 
## | |_) / _ \ '_ \ / _` | '_ ` _ \ / _ \
## |  _ <  __/ | | | (_| | | | | | |  __/
## |_| \_\___|_| |_|\__,_|_| |_| |_|\___|
##                                       
names(autism_data)[names(autism_data)=="identifier"] <- "id"
names(autism_data)[names(autism_data)=="comments"] <- "parcel"


tidy_data <- tidy_parcels(data = autism_data)
categorized_data <- categorize_parcels(data = tidy_data, dictionary = relations)
# plot
subset <- categorized_data %>%
  filter(category %in% c("Interpersonal", "Temporal"))

plot_percentages(subset)

png(filename="whatitslike.png")

png(filename="suicide.png")

subset <- categorized_data %>%
  filter(category %in% c("Interpersonal", "Temporal","Self", "Others"))
plot_percentages(subset)

dev.off()

colnames(categorized_data)
table(categorized_data[[2]])
categorized_data[[2]]


t.test(percent ~ category,
       data = subset,
       paired = FALSE)
cohen.d(formula = percent ~ category,
        data = subset,
        paired = FALSE)








devtools::install_github("bradleyboehmke/harrypotter")
### sentiment analysis
##https://uc-r.github.io/sentiment_analysis
library(tidyverse)      # data manipulation & plotting
library(stringr)        # text cleaning and regular expressions
library(tidytext)       # provides additional text mining functions
library(harrypotter)    # provides the first seven novels of the Harry Potter series

get_sentiments("afinn")
get_sentiments("bing")
get_sentiments("nrc")

titles <- c("Philosopher's Stone", "Chamber of Secrets", "Prisoner of Azkaban",
            "Goblet of Fire", "Order of the Phoenix", "Half-Blood Prince",
            "Deathly Hallows")

books <- list(philosophers_stone, chamber_of_secrets, prisoner_of_azkaban,
           goblet_of_fire, order_of_the_phoenix, half_blood_prince,
           deathly_hallows)

titles <- c("What is autism really like")
books <- list(url_data)



series <- tibble()

for(i in seq_along(titles)) {     
        clean <- tibble(chapter = seq_along(books[[i]]),
                        text = books[[i]]) %>%
             unnest_tokens(word, text) %>%
             mutate(book = titles[i]) %>%
             select(book, everything())
        series <- rbind(series, clean)
}

df[url_data[13]]
class(url_data[13])
colnames(url_data[13])

tibble(url_data)

# set factor to keep books in order of publication



series$book <- factor(series$book, levels = rev(titles))
