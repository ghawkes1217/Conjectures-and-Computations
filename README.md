# Conjectures-and-Computations

The point of this project is to provide convincing evidence that each of the conjectures covered is "almost certainly"
true.  Mathematically speaking, a statement only has three possible statuses: proven, disproven, or neither.  In principle, all members of the last category are on equal footing.  For instance, if I conjecture that the number of diagonals of an n-gon is bounded by n, this is on equal footing as the Riemann hypothesis until someone puts forth the 
counterexample of n=6 (or larger).  Intuitively, then, there are obvious differences among the set of all statements that have been neither proven nor disproven at the present time.   For one, if the problem has one or more parameters, we can ask for how many fixed settings of these parameters the conjecture has been checked and how representative of the general setting we think these choices of parameters are. 

As a simple example, suppose that Bob has a conjectural statement that applies to each n in the natural numbers.  Further,
suppose that he wishes to convince Alice that his conjecture has a 99% chance of being true for a "randomly" selected natural number. (Of course, we cannot select a random (with uniform probability) natural number. The best we can do is to select a number with probability p<sub>k</sub> for some monotonically decreasing sequence whose series converges (slowly) to 1.)   If Alice selects 999 random numbers and Bob's conjecture holds for each one, then since 0.99<sup>999</sup><0.0001, Alice can be at least 99.99% sure that Bob's claim about the accuracy of his conjecture is correct.

These files contain code which can be used to check (for fixed parameters) some of my conjectures in algebraic combinatorics. There is no known proof (Arroyo, Hamaker, H., and Pan are currently working on a proof for Conjectures 2 and 3) for any of these conjectures and there is no known counter-example to any of them.  (There is also one file containing a computation needed for a proof in a paper of mine).  In general the situation is much more complicated than Bob and Alice's but similarly arguments could be made to quantify "how sure" we can be each of the conjectures given.  I will leave it up to the reader to use the code supplied to come up with their own determination of how likely each statement is to be true.



<strong>Computer Assisted Proof</strong>

The file <strong>qt-assisted.py()</strong> in the folder qt-catalan carries out the computations needed to complete the proof of Lemma 2 and Lemma 3 of Section 9 of <a href="https://arxiv.org/pdf/2208.00577.pdf"><i>A conjectured formula for the rational qt-Catalan polynomial</i></a>.  Simply running this file without altering any parameters is sufficient to check the Lemmas.
  
 <strong>Conjecture 1: qt-Catalan Numbers</strong>

The file <strong>qt-conjecture.py()</strong> in the folder qt-catalan contains code to check Conjecture 1 of <a href="https://arxiv.org/pdf/2208.00577.pdf"><i>A conjectured formula for the rational qt-Catalan polynomial</i></a> for any pair of relatively prime integers.  The function conjecture(r,n) returns True if the conjecture holds for the pair (r,n) and False otherwise and also prints additional data.  The conjecture will NOT hold for non relatively prime numbers in general.
  
  
<strong>Conjecture 2: On type C Grothendieck functions:</strong>

We conjecture a definition (given within the code) for a type C unimodal tableau such that for any fixed signed permutation there is bijection from the set of Hecke words of a given length, L, to pairs of tableau (P,Q) where P is a type C unimodal tableau corresponding to the signed permutation and Q is a shifted set valued tableau of the same shape as P with entries 1,2,...,L. 

The function <strong>all_check(L,M)</strong> found in <strong>c-grothendieck.py</strong> in the c-grothendieck folder checks the conjecture for length L for  all signed permutations of (1,2,...,M+1). For each such signed permutation the code prints a triple.  The first entry is a representative for the signed permutation, the second entry is the number of pairs of Hecke tableaux (for the signed permutation) and shifted set tableaux (with L entries) of the same shape. The third entry is the number of Hecke words of  length L for the signed permutation.  The second and third entries should always be equal if the conjecture is correct.  The final output of the function is [number of permutations where conjecture holds, number of permutations where conjecture fails].

<strong>Conjecture 3: Type C Grothendieck functions--strong version:</strong>


In the c-grothendieck folder <strong>c-grothendieck-strong.py</strong> tests a similar but stronger conjecture.  In this case we do not allow Hecke words which have any pair of adjacent entries equal and at the same time we do not allow shifted set valued tableaux which have consecutive entries in the same box.

<strong>Conjecture 4: Shifted set-valued Littlewood-Richardson coefficients--GQ version:</strong>

In the shifted-LR folder <strong>skew-GQ-expansion.py</strong> tests a conjectural rule for computing the coefficients in the expansion of a skew GQ function in terms of (non-skew) GQ functions.
  The code actually tests the rule for what I call GR functions but this implies that the GQ functions have the same expansion. The difference is as follows:  Whereas GQ corresponds to all shifted set-valued tableaux, GR corresponds to the subset of shifted set-valued tableaux that satisfy that the first i or i' to appear in the left to right, bottom to top reading word must be an i (for each i).  Equivalently, we could define GR to be generated by the subset of tableaux whose first i or i' is an i' that appears in a box without an i.  The latter definition is more convenient for defining our conjectural lattice property.  

  The function compare(degree,skew,shape,num_vars) returns True if the conjecture is true for the expansion of GQ_{shape/skew} for the given degree and number of variables and False otherwise.  Up to degree 10 or 11 can be checked relatively quickly.

  <strong>Conjecture 5: Shifted set-valued skew Littlewood-Richardson coefficients--GQ version:</strong>

In the shifted-LR folder <strong>skew-GQ-expansion.py</strong> tests a conjectural rule for computing the coefficients in the expansion of a skew GQ function in terms of (non-skew) GQ functions.
  The code actually tests the rule for what I call GR functions but this implies that the GQ functions have the same expansion. The difference is as follows:  Whereas GQ corresponds to all shifted set-valued tableaux, GR corresponds to the subset of shifted set-valued tableaux that satisfy that the first i or i' to appear in the left to right, bottom to top reading word must be an i (for each i).  Equivalently, we could define GR to be generated by the subset of tableaux whose first i or i' is an i' that appears in a box without an i.  The latter definition is more convenient for defining our conjectural lattice property.  

  The function compare(degree,skew,shape,num_vars) returns True if the conjecture is true for the expansion of GQ_{shape/skew} for the given degree and number of variables and False otherwise.  Up to degree 10 or 11 can be checked relatively quickly.

<strong>Conjecture 6: Shifted set-valued skew Littlewood-Richardson coefficients--GP version:</strong>

In the shifted-LR folder <strong>skew-GP-expansion.py</strong> tests a similar but slightly simpler conjectural rule for computing the coefficients in the expansion of a skew GP function in terms of (non-skew) GP functions.
 T. Ikeda also claims to have a conjecture for these coefficients but he has not shared with me what it is or how rigorously he has checked it.

  The function compare(degree,skew,shape,num_vars) returns True if the conjecture is true for the expansion of GQ_{shape/skew} for the given degree and number of variables and False otherwise.  Up to degree 10 or 11 can be checked relatively quickly.