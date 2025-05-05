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

files <- list.files(path="C:/Users/Exalt/cmpsci/comp/data-analysis/processed/passages", pattern="*.csv", full.names = TRUE)
#files <- list.files(path="C:/Users/Exalt/cmpsci/comp/data-analysis/processed/research-data/data", pattern="*moves.csv", full.names = TRUE)
counter <- 0
# Iterate over each file
for (file in files) {
  # Separate the name
  file_name <- sub("C:/Users/Exalt/cmpsci/comp/data-analysis/processed/passages/*", "", file)
  #file_name <- sub("C:/Users/Exalt/cmpsci/comp/data-analysis/processed/research-data/data/*", "", file)
  file_name <- sub(".csv", "", file_name)
  
  # Read the file
  data <- read.csv(file, header=TRUE)
  
  move_data <- data[, which(names(data) != "Player_Num")]
  uniq_data <- move_data %>% distinct(Move_Label, .keep_all = TRUE)
  df <- data.frame(uniq_data, row.names = "Move_Label")
  
  # apply kmeans
  km_res <- kmeans(df,10,iter.max = 1000,
                   nstart=10,algorithm="MacQueen")
  
  sil <- silhouette(km_res$cluster, dist(df))
  
  # plot silhouette
  fviz_silhouette(sil)
  plot(sil, main = sprintf("Silhouette of Player Moves in %s", file_name))
  
  
  #hc <- diana(data)
  #hc$dc
  #pltree(hc, main = sprintf("Dendrogram of Passage Moves in %s", file_name))
  file.create(sprintf("C:/Users/Exalt/cmpsci/comp/data-analysis/processed/passages/pngs/%s.png", file_name))
  png(sprintf("C:/Users/Exalt/cmpsci/comp/data-analysis/processed/passages/pngs/%s.png", file_name))
  
  dclust_data <- diana(df)
  print(dclust_data$dc)
  pltree(dclust_data, hang = -1, cex = 0.6, main = sprintf("Dendrogram of Player Moves in %s", file_name))
  dev.off()
  
  
  file.create(sprintf("C:/Users/Exalt/cmpsci/comp/data-analysis/processed/passages/tables/%s.txt", file_name))
  cat(dclust_data$dc, file = sprintf("C:/Users/Exalt/cmpsci/comp/data-analysis/processed/passages/tables/%s.txt", file_name), sep = "")
  
  file.create(sprintf("C:/Users/Exalt/cmpsci/comp/data-analysis/processed/passages/pngs/notime_%s.png", file_name))
  png(sprintf("C:/Users/Exalt/cmpsci/comp/data-analysis/processed/passages/pngs/notime_%s.png", file_name))
  
  move_data <- data[, which(names(data) != "Player_Num")]
  no_time <- data[, which(names(data) != "Time_ms")]
  uniq_data <- no_time %>% distinct(Move_Label, .keep_all = TRUE)
  df <- data.frame(uniq_data, row.names = "Move_Label")
  
  dclust_data <- diana(df)
  print(dclust_data$dc)
  pltree(dclust_data, hang = -1, cex = 0.6, main = sprintf("Dendrogram of Player Moves in %s", file_name))
  dev.off()
  
  
  #aggregate(dclust_data, by=list(cluster=dclust_data$cluster))
  #print(dclust_data$height)
  #plot(cut(dclust_data, h=dclust_data$height)$upper, 
  #     main="Upper tree of cut at half length")
  #plot(cut(dclust_data, h=75)$lower[[2]], 
  #     main="Second branch of lower tree with cut at half length")
  
  #print()

}
