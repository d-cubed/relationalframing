```{r}

###################################################################
# Take the output created by the reddit scraper and tidy up strings 
# for qualitative analysis. 
# - Removes line breaks and carriage returns
# - Removes all non alphanumberic and punctuation
# - adds identifier

###################################################################
# dependencies
library(stringr)
library(readr)
library(dplyr)

###################################################################
#data acquisition
#setwd("../Data acquisition and cleaning/data")


df <- 
  read.csv("data/2_first_level_comments.csv", header = FALSE) %>%  ## why is this false??
  rename(first_level_comments = V1)

###################################################################
# Data processing

# remove deleted and removed comments 
processing_df <- 
  filter(df, first_level_comments != '[removed]' & first_level_comments != '[deleted]')  # remove all removed and deleted answers

# remove &nbsp; strings
processing_df$first_level_comments_noParagraphs <- str_replace_all(processing_df$first_level_comments, pattern = "&nbsp;", " ")

# remove line breaks - both windows and unix formatted
processing_df$first_level_comments_noParagraphsOrLineBreaks <- str_replace_all(processing_df$first_level_comments_noParagraphs, "[\r?\n|\r]" , " ")

# remove all non-alphanumberic characters and punctuation
processing_df$comments <- gsub("[^[:alnum:][:punct:]///' ]", "", processing_df$first_level_comments_noParagraphsOrLineBreaks)

# select only the last row for output
output_df <- 
  select(processing_df, comments) %>%
  tibble::rownames_to_column("identifier")



###################################################################
# write to disk
write.csv(output_df, "data/3_alphanumberic_and_punctuation_only.csv", row.names = FALSE)

```
