# N-gram Language Model Adaptation

This is an implementation of the method computing adapted language model in this paper:  
Federico, Marcello. "[Efficient language model adaptation through MDI estimation.](https://www.isca-speech.org/archive/archive_papers/eurospeech_1999/e99_1583.pdf)" *Sixth European Conference on Speech Communication and Technology*. 1999.

The idea is: 
* A background (out-domain) language model B is adapted to fit 
constraints on its marginal distributions that are derived from new observed (in-domain) data A.
* The adapted model A' is (1) **as close as possible** to the general background LM B and (2) **satisfies some constraints** empirically
derived from a relatively small adaptation sample A.
* When the constrains are unigram LM on A, there is **closed form** solution of A'.
* When B is a interpolated LM and the constraints are unigrams, there is **efficient** way to compute the solution.
