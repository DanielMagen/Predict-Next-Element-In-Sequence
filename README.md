# Predict-Next-Element-In-Sequence

Predict the next element of a sequence by the first n-1 elements.

To predict the next element of a sequence first select a predictor and initialize it. 
For example
```python
from predictors import *

predictor_class = SlopeAndBias
predictor = predictor_class()
```

The available predictors can be viewed in the predictors.py file.

Finally, to get the predicted item simply feed the sequence to the predict function

```python
predictor.predict(seq)
```

To see

Some predictors were tested on all the sequences in the OEIS website. The testing was done by comparing 
the known n'th element in the sequence to the predicted n'th element given the first n-1 elements.
the tests can be seen in testing_on_oeis/main_testing.py and in the predictors documentation.
The tests were done up to various error margins, and the predictor was deemed successful if 

```python
real_value / error_margin <= predicted_value <= real_value * error_margin
```

For example, the results for the ImprovedDivision predictor were

    ImprovedDivision
    skipped 13386
    +--------------+--------+--------+
    | error margin | passed | failed |
    +--------------+--------+--------+
    |      5       | 268622 | 51496  |
    |      2       | 241871 | 78247  |
    |     1.1      | 175680 | 144438 |
    |     1.01     | 102621 | 217497 |
    |    1.001     | 60209  | 259909 |
    |  1.0000001   | 19897  | 300221 |
    |      1       | 10918  | 309200 |
    +--------------+--------+--------+
    
    
    ImprovedDivisionCanDealWithZero
    skipped 9
    +--------------+--------+--------+
    | error margin | passed | failed |
    +--------------+--------+--------+
    |      5       | 272015 | 61480  |
    |      2       | 243389 | 90106  |
    |     1.1      | 176240 | 157255 |
    |     1.01     | 104270 | 229225 |
    |    1.001     | 63291  | 270204 |
    |  1.0000001   | 24856  | 308639 |
    |      1       | 15290  | 318205 |
    +--------------+--------+--------+
    

note that some sequences were skipped as some predictors can not deal with some sequences, and 9 sequences contained only 1 element 
