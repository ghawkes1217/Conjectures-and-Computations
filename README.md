# Conjectures
Computational evidence for my various of my conjectures in algebraic combinatorics


<strong>Conjecture 1: On type C Grothendieck functions:</strong>

We conjecture a definition (given within the code) for a type C unimodal tableau such that for any fixed signed permutation there is bijection from the set of Hecke words of a given length, L, to pairs of tableau (P,Q) where P is a type C unimodal tableau corresponding to the signed permutation and Q is a shifted set valued tableau of the same shape as P with entries 1,2,...,L. 

The function <strong>all_check(L,M)</strong> found in <strong>c-grothendieck.py</strong> in the c-grothendieck folder checks the conjecture for length L for  all signed permutations of (1,2,...,M+1). For each such signed permutation the code prints a triple.  The first entry is a representative for the signed permutation, the second entry is the number of pairs of Hecke tableaux (for the signed permutation) and shifted set tableaux (with L entries) of the same shape. The third entry is the number of Hecke words of  length L for the signed permutation.  The second and third entries should always be equal if the conjecture is correct.  The final output of the function is [number of permutations where conjecture holds, number of permutations where conjecture fails].

<strong>Conjecture 2: Type C Grothendieck functions--strong version:</strong>
In the c-grothendieck folder <strong>c-grothendieck-strong.py</strong> tests a similar but stronger conjecture.  In this case we do not allow Hecke words which have any pair of adjacent entries equal and at the same time we do not allow shifted set valued tableaux which have consecutive entries in the same box.

