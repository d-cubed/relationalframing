
##https://github.com/ianhussey/simpleNLP

library(simpleNLP)
library(tidyverse)
library(effsize)

## use the python file scraper.py first
## then tidy up with tidy_up_strings.rmd
autism_data <- read_csv(file="data/3_alphanumberic_and_punctuation_only.csv")

like <- read_csv(file="data/whatisautismlike.csv")

colnames(like)
nrow(like)

understand <-  read_csv(file="data/autismunderstand.csv")

colnames(understand)
nrow(understand)

bikes <- read_csv(file="data/bikes.csv")


## |  _ \ ___ _ __   __ _ _ __ ___   ___ 
## | |_) / _ \ '_ \ / _` | '_ ` _ \ / _ \
## |  _ <  __/ | | | (_| | | | | | |  __/
## |_| \_\___|_| |_|\__,_|_| |_| |_|\___|

### not needed if:
## output_df <-  plyr::rename(output_df, c("identifier"="id", "comments"="parcel")) 
## is in tidy_up_strings.r

#names(autism_data)[names(autism_data)=="identifier"] <- "id"
#names(autism_data)[names(autism_data)=="comments"] <- "parcel"

colnames(autism_data)

tidy_data <- tidy_parcels(data = autism_data)

tidy_like <- tidy_parcels(data = like)
tidy_understand <- tidy_parcels(data = understand)

tidy_bikes <- tidy_parcels(data = bikes)

categorized_like <- categorize_parcels(data = tidy_like, dictionary = relations)
categorized_understand <- categorize_parcels(data = tidy_understand, dictionary = relations)

categorized_bikes <- categorize_parcels(data = tidy_bikes, dictionary = relations)


categorized_data <- categorize_parcels(data = tidy_data, dictionary = relations)

subset <- categorized_data %>%
    filter(category %in% c("Interpersonal", "Temporal"))

like_temp_subset <- categorized_like %>%
    filter(category %in% c("Interpersonal", "Temporal"))

understand_temp_subset <- categorized_understand %>%
    filter(category %in% c("Interpersonal", "Temporal"))


bikes_temp_subset <- categorized_bikes %>%
  filter(category %in% c("Interpersonal", "Temporal"))

png(filename="bikes-interpersonal-temporal-rev.png")
plot_percents(bikes_temp_subset)
dev.off()



png(filename="whatitslike-interpersonal-temporal.png")
plot_percentages(like_temp_subset)
dev.off()

png(filename="understand-interpersonal-temporal.png")
plot_percentages(understand_temp_subset)
dev.off()

png(filename="whatitslike-interpersonal-temporal-rev.png")
plot_percents(like_temp_subset)
dev.off()

png(filename="understand-interpersonal-temporal-rev.png")
plot_percents(understand_temp_subset)
dev.off()


like_self_subset <- categorized_like %>%
    filter(category %in% c("Self", "Others"))

understand_self_subset <- categorized_understand %>%
    filter(category %in% c("Self", "Others"))

bikes_self_subset <- categorized_bikes %>%
  filter(category %in% c("Self", "Others"))

png(filename="whatitslike-self-other.png")

   theme_update(text = element_text(size=142))
plot_percentages(like_self_subset)

plot_percents(like_self_subset)

dev.off()

png(filename="bikes-self-others-rev.png")
plot_percents(bikes_self_subset)
dev.off()

png(filename="understand-self-others-rev.png")
plot_percents(understand_self_subset)
dev.off()

png(filename="like-self-others-rev.png")
plot_percents(like_self_subset)
dev.off()

png(filename="200percent.png")
plot_frequencies(like_self_subset)
dev.off()

t.test(percent ~ category,
       data = like_self_subset,
       paired = FALSE)

cohen.d(formula = percent ~ category,
        data = like_self_subset,
        paired = FALSE)

t.test(percent ~ category,
       data = bikes_self_subset,
       paired = FALSE)

cohen.d(formula = percent ~ category,
        data = bikes_self_subset,
        paired = FALSE)


t.test(percent ~ category,
       data = understand_self_subset,
       paired = FALSE)

cohen.d(formula = percent ~ category,
        data = understand_self_subset,
        paired = FALSE)

### temp

t.test(percent ~ category,
       data = like_temp_subset,
       paired = FALSE)

cohen.d(formula = percent ~ category,
        data = like_temp_subset,
        paired = FALSE)

t.test(percent ~ category,
       data = bikes_temp_subset,
       paired = FALSE)

cohen.d(formula = percent ~ category,
        data = bikes_temp_subset,
        paired = FALSE)


t.test(percent ~ category,
       data = understand_temp_subset,
       paired = FALSE)

cohen.d(formula = percent ~ category,
        data = understand_temp_subset,
        paired = FALSE)





plot_percentages(subset)

whatitslike <- subset

png(filename="whatitslike.png")
subset <- categorized_data %>%
  filter(category %in% c("Interpersonal", "Temporal","Self", "Others"))
plot_percentages(subset)
dev.off()

png(filename="whatitslike-interpersonal-temporal.png")
subset <- categorized_data %>%
  filter(category %in% c("Interpersonal", "Temporal"))
plot_percentages(subset)
dev.off()

png(filename="whatitslike-self-others.png")
subset <- categorized_data %>%
  filter(category %in% c("Self", "Others"))
plot_percentages(subset)
dev.off()



t.test(percent ~ category,
       data = subset,
       paired = FALSE)

cohen.d(formula = percent ~ category,
        data = subset,
        paired = FALSE)


##             _                     
## __   ____ _| | ___ _ __   ___ ___ 
## \ \ / / _` | |/ _ \ '_ \ / __/ _ \
##  \ V / (_| | |  __/ | | | (_|  __/
##   \_/ \__,_|_|\___|_| |_|\___\___|
##                                   

valence_like <- categorize_parcels(data = tidy_like, dictionary = valence)

valence_understand <- categorize_parcels(data = tidy_understand, dictionary = valence)

valence_bikes <- categorize_parcels(data = tidy_bikes, dictionary = valence)


png(filename="whatitslike-valence.png")
plot_percents(valence_like)
dev.off()

png(filename="understand-valence.png")
plot_percents(valence_understand)
dev.off()

png(filename="bikes-valence.png")
plot_percents(valence_bikes)
dev.off()


