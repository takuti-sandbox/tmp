using Recommendation

R = [0 1 1;
     1 0 1;
     0 1 0;
     1 0 1;
     1 0 0]

Predicted = [0.6 0.8 0.31;
             0.7 0.2 0.25;
             0.5 0.9 0.46;
             0.3 0.1 0.81;
             0.9 0.4 0.5]

is_test = [0 0 0;
           1 0 1;
           0 1 0;
           0 0 1;
           1 0 0]

n_item, n_user = size(R)

MPRs = []
for user in 1:n_user
    test_indices = find(flg -> flg == 1, is_test[:, user])

    truth = find(r -> r == 1, R[test_indices, user])
    rank = sortperm(Predicted[test_indices, user], rev=true)

    mpr = measure(MPR(), truth, rank)
    push!(MPRs, mpr)
end

println(MPRs)
println(mean(MPRs))

