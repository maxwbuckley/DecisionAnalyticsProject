library("reshape2")
library("expm")
setwd("~/Downloads/")
data<-read.csv("Example Preference Aggregator (Responses) - Form Responses 1 (1).csv", stringsAsFactors=FALSE)

data<-data[,c(2:length(data))]




melted_data<-melt(data)
df1<-cbind(gsub("\\.or.*", "", melted_data$variable),8-melted_data$value)
df2<-cbind(gsub(".*or\\.", "", melted_data$variable),melted_data$value)

df_joined<-cbind(df1,df2)

keys<-unique(c(df_joined[,1],df_joined[,3]))

zeromatrix<-matrix(0,nrow=length(keys),ncol=length(keys))
rownames(zeromatrix)<-keys
colnames(zeromatrix)<-keys

for(i in 1:nrow(df_joined)){
  row<-df_joined[i,]
  zeromatrix[row[1],row[3]] <- zeromatrix[row[1],row[3]] + as.numeric(row[2])
  zeromatrix[row[3],row[1]] <- zeromatrix[row[3],row[1]] + as.numeric(row[4])
}
countmat<-zeromatrix
rowSums(countmat)
colSums(countmat)

normmat<-t(countmat)/colSums(countmat)


scores<-rep(1/4,4)%*%(normmat%^%1000)
scores

genRowLevelMatrix <- function(data_row){
  melted_data<-melt(data_row)
  adj_value<-4-melted_data$value
  #print(adj_value)
  df1<-cbind(gsub("\\.or.*", "", melted_data$variable), 4-melted_data$value)
  df2<-cbind(gsub(".*or\\.", "", melted_data$variable), -(4-melted_data$value))
  df_joined<-cbind(df1,df2)
  #print(df_joined)

  
  
  keys<-unique(c(df_joined[,1],df_joined[,3]))
  
  basematrix<-diag(length(keys))
  rownames(basematrix)<-keys
  colnames(basematrix)<-keys
  
  for(i in 1:nrow(df_joined)){
    row<-df_joined[i,]
    if(row[2]==row[4]){
      basematrix[row[1],row[3]] <- basematrix[row[1],row[3]] + 1
      basematrix[row[3],row[1]] <- basematrix[row[3],row[1]] + 1
      
    }
    else{
        if(row[2]>row[4]){
      basematrix[row[1],row[3]] <- basematrix[row[1],row[3]] + abs(as.numeric(row[2]))
      basematrix[row[3],row[1]] <- basematrix[row[3],row[1]] + abs(1/as.numeric(row[4]))
      }
      else{
        basematrix[row[1],row[3]] <- basematrix[row[1],row[3]] + abs(1/as.numeric(row[2]))
        basematrix[row[3],row[1]] <- basematrix[row[3],row[1]] + abs(as.numeric(row[4])) 
      }
    }
  }
  
  return(basematrix)
}

combineRowLevelMatrices<- function(data_frame, size){
  basemat<-diag(size)
  for(i in 1:nrow(data_frame)){
    if(i==1){
      newmat<-genRowLevelMatrix(data[i,])
    }
    tempmat = genRowLevelMatrix(data[i,])
    newmat = newmat * tempmat
    print(newmat)
  }
  return(newmat^(1/nrow(data_frame)))
}
a<-genRowLevelMatrix(data[1,])
b<-genRowLevelMatrix(data[3,])
#genRowLevelMatrix(data[4,])
mat<- combineRowLevelMatrices(data, 4)

##Returns the same ordered list but much wider spread
princomp(mat)$scores[,1]


princomp(genRowLevelMatrix(data[1,]))$scores[,1]

