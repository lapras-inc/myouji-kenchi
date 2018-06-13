import myouji_kenchi
import regex
import unicodedata

from typing import List


_TRANSLITERATOR = None


def order_names(names: List[str], prior=0.5) -> List[str]:
    """Order strings based on the chance they are Japanese surnames.

    Uses scores from get_score_as_myouji, as well as a few heuristics.
    Specifying prior changes the likelihood of reordering.

    :param names: names to order_names
    :param prior: the prior probability that the names are in the correct order
    :returns: names in order estimated to be correct
    """
    if prior < 0 or prior > 1:
        raise ValueError('Prior is not valid')
    if len(names) != 2:
        raise ValueError('names must have length two')

    reverse_order = list(reversed(names))
    same_order = list(names)

    # First heuristic: if one name looks like an initial
    # Hypothetically, if both should look like initials, follow the precautionary principle
    if _is_initial(names[1]) and not _is_initial(names[0]):
        return reverse_order
    elif _is_initial(names[0]) and not _is_initial(names[1]):
        return same_order

    # Second heuristic: if only one name is all uppercase
    if _is_all_uppercase(names[0]) and not _is_all_uppercase(names[1]):
        return reverse_order
    if _is_all_uppercase(names[1]) and not _is_all_uppercase(names[0]):
        return same_order

    scores = [get_score_as_myouji(name) for name in names]
    scores[0] *= prior
    scores[1] *= 1 - prior
    if scores[0] > scores[1]:
        return reverse_order
    return same_order


def get_score_as_myouji(name: str) -> float:
    """Calculate a frequency score for a string as a Japanese surname.

    :param name: name to score
    """
    transliterator = _load_transliterator()
    back_transliteration_results = transliterator.back_transliterate(name)
    scores = [r[1] for r in back_transliteration_results]
    return max(scores, default=0)


def _load_transliterator():
    global _TRANSLITERATOR
    if _TRANSLITERATOR is None:
        _TRANSLITERATOR = myouji_kenchi.MyoujiBackTransliteration()
    return _TRANSLITERATOR


def _is_all_uppercase(name):
    return regex.match(r'(\p{Uppercase}|[-\']})+$', unicodedata.normalize('NFKC', name)) is not None


def _is_initial(name):
    return regex.match(r'\p{Uppercase}\.?$', unicodedata.normalize('NFKC', name)) is not None
