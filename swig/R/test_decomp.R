
test_SparseProject <- function () {
  set.seed(0)
  X = matrix(rnorm(20000 * 100),nrow = 20000,ncol = 100,byrow = FALSE)
  X = X / matrix(rep(sqrt(colSums(X*X)),nrow(X)),nrow(X),ncol(X),byrow=T)
  .printf( "\n  Projection on the l1 ball\n")
  tic = proc.time()
  X1 = spams.SparseProject(X,numThreads = -1, pos = FALSE,mode= 1,thrs = 2)
  tac = proc.time()
  t = (tac - tic)[['elapsed']]
  .printf("  Time : %f\n", t)
  if (t != 0)
    .printf("%f signals of size %d projected per second\n",(ncol(X) / t),nrow(X))
  s = colSums(abs(X1))
  .printf("Checking constraint: %f, %f\n",min(s),max(s))

  .printf("\n  Projection on the Elastic-Net\n")
  lambda1 = 0.15
  tic = proc.time()
  X1 = spams.SparseProject(X,numThreads = -1, pos = FALSE,mode= 2,thrs = 2,lambda1= lambda1)
  tac = proc.time()
  t = (tac - tic)[['elapsed']]
  .printf("  Time : %f\n", t)
  if (t != 0)
    .printf("%f signals of size %d projected per second\n",(ncol(X) / t),nrow(X))
  constraints = colSums(X1*X1) + lambda1 * colSums(abs(X1))
  .printf("Checking constraint: %f, %f (Projection is approximate : stops at a kink)\n",min(constraints),max(constraints))

  .printf("\n  Projection on the FLSA\n")
  lambda1 = 0.7
  lambda2 = 0.7
  lambda3 = 0.7
  X = matrix(runif(2000 * 100,0,1),nrow = 2000,ncol = 100,byrow = FALSE)
  X = X / matrix(rep(sqrt(colSums(X*X)),nrow(X)),nrow(X),ncol(X),byrow=T)
 # matlab : X=X./repmat(sqrt(sum(X.^2)),[size(X,1) 1]);
  tic = proc.time()
  X1 = spams.SparseProject(X,numThreads = -1, pos = FALSE,mode= 6,thrs = 2,lambda1= lambda1,lambda2= lambda2,lambda3= lambda3)
  tac = proc.time()
  t = (tac - tic)[['elapsed']]
  .printf("  Time : %f\n", t)
  if (t != 0)
    .printf("%f  signals of size %d projected per second\n",ncol(X) / t,nrow(X))
#  constraints = 0.5 * param[['lambda3']] * colSums(X1*X1) + param[['lambda1']] * colSums(abs(X1)) + param[['lambda2']] * abs(X1[3:nrow(X1),]) - colSums(X1[2,])
  constraints = 0.5 * lambda3 * colSums(X1*X1) + lambda1 * colSums(abs(X1)) + lambda2 * abs(X1[3:nrow(X1),])  - colSums(matrix(X1[2,],nrow=1))
  .printf("Checking constraint: %f, %f (Projection is approximate : stops at a kink)\n",min(constraints),max(constraints))
  return(NULL)
}

test_Lasso <- function() {
  set.seed(0)
  .printf("test Lasso\n")
##############################################
# Decomposition of a large number of signals
##############################################
# data generation
  X = matrix(rnorm(100 * 100000),nrow = 100,ncol = 100000,byrow = FALSE)
  X = X / matrix(rep(sqrt(colSums(X*X)),nrow(X)),nrow(X),ncol(X),byrow=T)
  D = matrix(rnorm(100 * 200),nrow = 100,ncol = 200,byrow = FALSE)
  D = D / matrix(rep(sqrt(colSums(D*D)),nrow(D)),nrow(D),ncol(D),byrow=T)
  tic = proc.time()
  alpha = spams.Lasso(X,D,return_reg_path = FALSE,lambda1 = 0.15,numThreads = -1,mode = 'PENALTY' )
  tac = proc.time()
  t = (tac - tic)[['elapsed']]
  .printf("%f signals processed per second\n",as.double(ncol(X)) / t)
########################################
# Regularization path of a single signal 
########################################
  X = matrix(rnorm(64),nrow = 64,ncol = 1,byrow = FALSE)
  D = matrix(rnorm(64 * 10),nrow = 64,ncol = 10,byrow = FALSE)
  D = D / matrix(rep(sqrt(colSums(D*D)),nrow(D)),nrow(D),ncol(D),byrow=T)
  res = spams.Lasso(X,D,return_reg_path = TRUE,lambda1 = 0.15,numThreads = -1,mode = 'PENALTY' )
  alpha = res[[1]]
  path = res[[2]]
  return(NULL)
}


#
test_decomp.tests =list( 
  'SparseProject' = test_SparseProject,
  'Lasso' = test_Lasso)