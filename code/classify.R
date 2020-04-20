library(classo)

data <- read.csv("../data/data_num.csv")
y <- data$Ret
x <- as.matrix(data[,c("MV","RM","BM","ROE","Inv")])
n <- 200
tt <- 120
lambda <- as.numeric( 0.5 * var(y) / (tt^(1/3)) )
pls_out <- PLS.cvxr(n, tt, y, x, K = 5, lambda = lambda)
write(pls_out$group.est,file="../result/classified.csv")
