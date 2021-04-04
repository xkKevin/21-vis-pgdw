# URL= http://stackoverflow.com/questions/30374143/recursive-error-in-dplyr-mutate

library(tidyr)
library(dplyr)

p34_input1 = read.csv("r34_input1.csv")
p34_input2 = read.csv("r34_input2.csv")
# TBL_3=inner_join(p34_input2, p34_input1, by="mult")
TBL_3=inner_join(p34_input2, p34_input1)
TBL_1=mutate(TBL_3,total=value / size)
morpheus=select(TBL_1,-`value`)
morpheus=as.data.frame(morpheus)
morpheus=select(morpheus,2,1,3)
# write.csv(morpheus, "r34_output1.csv", row.names=F)