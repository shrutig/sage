r"""
Common combinatorial tools


REFERENCES:

.. [NCSF] Gelfand, Krob, Lascoux, Leclerc, Retakh, Thibon,
   *Noncommutative Symmetric Functions*, Adv. Math. 112 (1995), no. 2, 218-348.

.. [QSCHUR] Haglund, Luoto, Mason, van Willigenburg,
   *Quasisymmetric Schur functions*, J. Comb. Theory Ser. A 118 (2011), 463-490.

.. [Tev2007] Lenny Tevlin,
   *Noncommutative Analogs of Monomial Symmetric Functions,
   Cauchy Identity, and Hall Scalar Product*,
   :arXiv:`0712.2201v1`.
"""
from sage.misc.misc_c import prod
from sage.functions.other import factorial
from sage.misc.cachefunc import cached_function
from sage.combinat.composition import Composition, Compositions
from sage.combinat.composition_tableau import CompositionTableaux


# The following might call for defining a morphism from ``structure
# coefficients'' / matrix using something like:
# Complete.module_morphism( coeff = coeff_pi, codomain=Psi, triangularity="finer" )
# the difficulty is how to best describe the support of the output.

def coeff_pi(J,I):
    r"""
    Returns the coefficient `\pi_{J,I}` as defined in [NCSF]_.

    INPUT:

    - ``J`` -- a composition
    - ``I`` -- a composition refining ``J``

    OUTPUT:

    - integer

    EXAMPLES::

        sage: from sage.combinat.ncsf_qsym.combinatorics import coeff_pi
        sage: coeff_pi(Composition([1,1,1]), Composition([2,1]))
        2
        sage: coeff_pi(Composition([2,1]), Composition([3]))
        6
    """
    return prod(prod(K.partial_sums()) for K in J.refinement_splitting(I))

def coeff_lp(J,I):
    r"""
    Returns the coefficient `lp_{J,I}` as defined in [NCSF]_.

    INPUT:

    - ``J`` -- a composition
    - ``I`` -- a composition refining ``J``

    OUTPUT:

    - integer

    EXAMPLES::

        sage: from sage.combinat.ncsf_qsym.combinatorics import coeff_lp
        sage: coeff_lp(Composition([1,1,1]), Composition([2,1]))
        1
        sage: coeff_lp(Composition([2,1]), Composition([3]))
        1
    """
    return prod(K[-1] for K in J.refinement_splitting(I))

def coeff_ell(J,I):
    r"""
    Returns the coefficient `\ell_{J,I}` as defined in [NCSF]_.

    INPUT:

    - ``J`` -- a composition
    - ``I`` -- a composition refining ``J``

    OUTPUT:

    - integer

    EXAMPLES::

        sage: from sage.combinat.ncsf_qsym.combinatorics import coeff_ell
        sage: coeff_ell(Composition([1,1,1]), Composition([2,1]))
        2
        sage: coeff_ell(Composition([2,1]), Composition([3]))
        2
    """
    return prod(map(len, J.refinement_splitting(I)))

def coeff_sp(J,I):
    r"""
    Returns the coefficient `sp_{J,I}` as defined in [NCSF]_.

    INPUT:

    - ``J`` -- a composition
    - ``I`` -- a composition refining ``J``

    OUTPUT:

    - integer

    EXAMPLES::

        sage: from sage.combinat.ncsf_qsym.combinatorics import coeff_sp
        sage: coeff_sp(Composition([1,1,1]), Composition([2,1]))
        2
        sage: coeff_sp(Composition([2,1]), Composition([3]))
        4
    """
    return prod(factorial(len(K))*prod(K) for K in J.refinement_splitting(I))

def coeff_dab(I, J):
    r"""
    Return the number of standard composition tableaux of shape `I` with
    descent composition `J`.

    INPUT:

    - ``I, J`` -- compositions

    OUTPUT:

    - An integer

    EXAMPLES::

        sage: from sage.combinat.ncsf_qsym.combinatorics import coeff_dab
        sage: coeff_dab(Composition([2,1]),Composition([2,1]))
        1
        sage: coeff_dab(Composition([1,1,2]),Composition([1,2,1]))
        0
    """
    d = 0
    for T in CompositionTableaux(I):
        if (T.is_standard()) and (T.descent_composition() == J):
            d += 1
    return d

def compositions_order(n):
    r"""
    Return the compositions of `n` ordered as defined in [QSCHUR]_.

    Let `S(\gamma)` return the composition `\gamma` after sorting. For
    compositions `\alpha` and `\beta`, we order `\alpha \rhd \beta` if

    1) `S(\alpha) > S(\beta)` lexicographically, or
    2) `S(\alpha) = S(\beta)` and `\alpha > \beta` lexicographically.

    INPUT:

    - ``n`` -- a positive integer

    OUTPUT:

    - A list of the compositions of ``n`` sorted into decreasing order
      by `\rhd`

    EXAMPLES::

        sage: from sage.combinat.ncsf_qsym.combinatorics import compositions_order
        sage: compositions_order(3)
        [[3], [2, 1], [1, 2], [1, 1, 1]]
        sage: compositions_order(4)
        [[4], [3, 1], [1, 3], [2, 2], [2, 1, 1], [1, 2, 1], [1, 1, 2], [1, 1, 1, 1]]
    """
    def _myorder(I,J):
        pI = sorted(I, reverse=True)
        pJ = sorted(J, reverse=True)
        if pI == pJ:
            return cmp(list(J), list(I))
        else:
            return cmp(pJ , pI)
    return sorted(Compositions(n), cmp=_myorder)

def m_to_s_stat(R, I, K):
    r"""
    Return the coefficient of the complete non-commutative symmetric
    function `S^K` in the expansion of the monomial non-commutative
    symmetric function `M^I` with respect to the complete basis
    over the ring `R`. This is the coefficient in formula (36) of
    Tevlin's paper [Tev2007]_.

    INPUT:

    - ``R`` -- A ring, supposed to be a `\QQ`-algebra
    - ``I``, ``K`` -- compositions

    OUTPUT:

    - The coefficient of `S^K` in the expansion of `M^I` in the
      complete basis of the non-commutative symmetric functions
      over ``R``.

    EXAMPLES::

        sage: from sage.combinat.ncsf_qsym.combinatorics import m_to_s_stat
        sage: m_to_s_stat(QQ, Composition([2,1]), Composition([1,1,1]))
        -1
        sage: m_to_s_stat(QQ, Composition([3]), Composition([1,2]))
        -2
        sage: m_to_s_stat(QQ, Composition([2,1,2]), Composition([2,1,2]))
        8/3
    """
    stat = 0
    for J in Compositions(I.size()):
        if (I.is_finer(J) and  K.is_finer(J)):
            pvec = [0] + Composition(I).refinement_splitting_lengths(J).partial_sums()
            pp = prod( R( len(I) - pvec[i] ) for i in range( len(pvec)-1 ) )
            stat += R((-1)**(len(I)-len(K)) / pp * coeff_lp(K,J))
    return stat

@cached_function
def number_of_fCT(content_comp, shape_comp):
    r"""
    Return the number of Immaculate tableaux of shape
    ``shape_comp`` and content ``content_comp``.

    See [BBSSZ2012]_, Definition 3.9, for the notion of an
    immaculate tableau.

    INPUT:

    - ``content_comp``, ``shape_comp`` -- compositions

    OUTPUT:

    - An integer

    EXAMPLES::

        sage: from sage.combinat.ncsf_qsym.combinatorics import number_of_fCT
        sage: number_of_fCT(Composition([3,1]), Composition([1,3]))
        0
        sage: number_of_fCT(Composition([1,2,1]), Composition([1,3]))
        1
        sage: number_of_fCT(Composition([1,1,3,1]), Composition([2,1,3]))
        2
    """
    if content_comp.to_partition().length() == 1:
        if shape_comp.to_partition().length() == 1:
            return 1
        else:
            return 0
    C = Compositions(content_comp.size()-content_comp[-1], outer = list(shape_comp))
    s = 0
    for x in C:
        if len(x) >= len(shape_comp)-1:
            s += number_of_fCT(Composition(content_comp[:-1]),x)
    return s

