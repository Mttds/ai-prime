# uncertainty

## pagerank

```
λ python pagerank.py corpus2
PageRank Results from Sampling (n = 10000)
  ai.html: 0.1848
  algorithms.html: 0.1096
  c.html: 0.1238
  inference.html: 0.1230
  logic.html: 0.0265
  programming.html: 0.2336
  python.html: 0.1262
  recursion.html: 0.0725
PageRank Results from Iteration
  ai.html: 0.1921
  algorithms.html: 0.1103
  c.html: 0.1283
  inference.html: 0.1320
  logic.html: 0.0264
  programming.html: 0.2043
  python.html: 0.1283
  recursion.html: 0.0782
```

## heredity (Bayes net)

```
λ python heredity.py data/family2.csv
Arthur:
  Gene:
    2: 0.0147
    1: 0.0344
    0: 0.9509
  Trait:
    True: 0.0000
    False: 1.0000
Hermione:
  Gene:
    2: 0.0608
    1: 0.1203
    0: 0.8189
  Trait:
    True: 0.0000
    False: 1.0000
Molly:
  Gene:
    2: 0.0404
    1: 0.0744
    0: 0.8852
  Trait:
    True: 0.0768
    False: 0.9232
Ron:
  Gene:
    2: 0.0043
    1: 0.2149
    0: 0.7808
  Trait:
    True: 0.0000
    False: 1.0000
Rose:
  Gene:
    2: 0.0088
    1: 0.7022
    0: 0.2890
  Trait:
    True: 1.0000
    False: 0.0000
```
