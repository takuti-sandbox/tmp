using Clustering

X = rand(5, 1000)

R = kmeans(X, 20; maxiter=200, display=:iter)

@assert nclusters(R) == 20

a = assignments(R)
print(a)

c = counts(R)
print(c)

M = R.centers
print(M)
