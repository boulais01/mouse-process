library(factoextra)
library(cluster)
library(dplyr)
#library(fpc)

moves_data <- read.csv("C:/Users/Exalt/cmpsci/comp/data-analysis/processed/final_moves.csv", header=TRUE)
states_data <- read.csv("C:/Users/Exalt/cmpsci/comp/data-analysis/processed/final_states.csv", header=TRUE)
print("data opened")
# Compute divisive hierarchical clustering
hc <- diana(states_data)
print("computation 1 complete")
# Divise coefficient
hc$dc
print("computation complete")
# Plot obtained dendrogram
pltree(hc, cex = 0.6, hang = -1, main = "Dendrogram of Player States")
print("plot done")
kmeans <- pam(states_data, 3)
plot(kmeans)

files <- list.files(path="C:/Users/Exalt/cmpsci/comp/data-analysis/processed/passages/", pattern="*.csv", full.names = TRUE)
counter <- 0
# Iterate over each file
for (file in files) {
  # Separate the name
  file_name <- sub("C:/Users/Exalt/cmpsci/comp/data-analysis/processed/passages/*", "", file)
  
  # Read the file
  data <- read.csv(file, header=TRUE)
  grouped_df <- df %>% group_by(Player_Num)
  # Compute divisive hierarchical clustering
  hc <- diana(data)
  # Divise coefficient
  hc$dc
  print("computation complete")
  # Plot obtained dendrogram
  pltree(hc, cex = 0.6, hang = -1, main = sprintf("Dendrogram of Player Moves in %s", file_name))
  print("plot done")
  df <- scale(data)
  #fviz_nbclust(df, FUNcluster = kmeans(df, centers = 4, nstart = 25), method = "wss")
  #calculate gap statistic based on number of clusters
  #gap_stat <- clusGap(df,
   #                   FUNcluster = kmeans(df, centers = 4, nstart = 25),
    #                  nstart = 25,
     #                 K.max = 10,
      #                B = 50)
  
  #plot number of clusters vs. gap statistic
  #fviz_gap_stat(gap_stat)
  
  #perform k-means clustering with k = 4 clusters
  km <- kmeans(df, centers = 4, nstart = 25)
  
  #view results
  km
  
  #plot results of final k-means model
  fviz_cluster(km, data = df)
  
  #find means of each cluster
  aggregate(data, by=list(cluster=km$cluster), mean)
  
  final_data <- cbind(data, cluster = km$cluster)
  
  head(final_data)
}
