import numpy as np

import pywrapfst as fst
import pkg_resources
import unicodedata

from pywrapfst import Arc
from typing import List
from typing import Tuple

from .symbol_table import SYMBOL_TABLE, REVERSE_SYMBOL_TABLE, EPSILON


LEXICAL_FREQUENCY_FST_FILE = pkg_resources.resource_filename('myouji_kenchi',
                                                             'data/lexical_data_fst.txt')


class MyoujiBackTransliteration():
    def __init__(self):
        transliterator = _build_transliterator()
        acceptor = _build_attested_acceptor()
        self._transducer = fst.compose(transliterator, acceptor)

    def back_transliterate(self, romaji: str) -> List[Tuple[str, float]]:
        """Back transliterate romaji to candidate myouji readings and frequency scores

        :param romaji: romaji to back transliterate
        :returns: tuples of possible readings and frequency scores
        """
        # It is convenient to match on COMBINING MACRON and COMBINING CIRCUMFLEX
        # separately from their vowels
        normalized = unicodedata.normalize('NFKD', romaji).lower() + '$'
        try:
            input_fst = _make_input_fst(normalized)
        except ValueError:
            return []
        result_fst = fst.compose(input_fst, self._transducer)
        interned_results = _all_valid_strings(result_fst)
        deinterned_results = [(_deintern_tokens(ts[0]), ts[1]) for ts in interned_results]
        return sorted(deinterned_results, key=lambda x: x[1])


def _build_transliterator():
    td = fst.Fst()
    initial_state = td.add_state()
    final = td.add_state()
    td.set_start(initial_state)
    td.set_final(final)
    _char_arc(td, initial_state, '$', EPSILON, final)
    long_vowel_possibilities = {'u': 'ウ',
                                'i': 'イ',
                                'e': 'エ',
                                'o': ['オ', 'ウ'],
                                'a': 'ア'}
    long_vowel_states = {k: _long_vowel_mark_state(td, initial_state, v)
                         for k, v in long_vowel_possibilities.items()}
    end_states = {'n': initial_state,
                  'y': _build_small_y_state(td, long_vowel_states),
                  **long_vowel_states}
    _build_sjsh(td, initial_state, end_states)
    _build_vowels(td, initial_state, end_states)
    _build_tdch(td, initial_state, end_states)
    _build_big_y(td, initial_state, end_states)
    _build_hpb(td, initial_state, end_states)
    _build_kg(td, initial_state, end_states)
    _build_r(td, initial_state, end_states)
    _build_m(td, initial_state, end_states)
    _build_n(td, initial_state, end_states)
    _build_w(td, initial_state, end_states)
    return td


def _build_attested_acceptor():
    # The basic strategy of the transliterator is to generate all
    # theoretically (i.e. w/o lexical knowledge) possible strings, which we
    # filter down with reference to lexical knowledge
    fst_txt = ''.join(open(LEXICAL_FREQUENCY_FST_FILE, encoding='ascii'))
    compiler = fst.Compiler()
    compiler.write(fst_txt)
    return compiler.compile()


def _make_input_fst(string):
    # Input is passed as acceptors that accept a single string
    td = fst.Fst()
    curr = td.add_state()
    td.set_start(curr)
    for c in string:
        nxt = td.add_state()
        try:
            _char_arc(td, curr, c, c, nxt)
        except KeyError:
            raise ValueError('Character {} not in input symbol table'.format(c))
        curr = nxt
    td.set_final(curr)
    return td


def _build_sjsh(td, start_state, end_states):
    s_begin = _double_consonant_state(td, start_state, ['s', 'j', 'z'])

    _many_to_one_arc(td, s_begin, ['sh', 'sy'], 'シ', end_states['y'])
    _many_to_many_arc(td, s_begin, ['j', 'zy'], ['ジ', 'ヂ'], end_states['y'])

    _many_to_one_arc(td, s_begin, ['si', 'shi'], 'シ', end_states['i'])
    _multi_char_arc(td, s_begin, 'sa', 'サ', end_states['a'])
    _multi_char_arc(td, s_begin, 'se', 'セ', end_states['e'])
    _multi_char_arc(td, s_begin, 'so', 'ソ', end_states['o'])
    _multi_char_arc(td, s_begin, 'su', 'ス', end_states['u'])

    _many_to_many_arc(td, s_begin, ['zi', 'ji'], ['ジ', 'ヂ'], end_states['i'])
    _multi_char_arc(td, s_begin, 'za', 'ザ', end_states['a'])
    _multi_char_arc(td, s_begin, 'ze', 'ゼ', end_states['e'])
    _multi_char_arc(td, s_begin, 'zo', 'ゾ', end_states['o'])
    _one_to_many_arc(td, s_begin, 'zu', ['ズ', 'ヅ'], end_states['u'])


def _build_tdch(td, start_state, end_states):
    # Having only one state for generating 'ッ' is partially for economy of
    # code, partially because accepting incorrect strings is acceptable, and
    # partially because in Hepburn 'ッチ' is indeed 'tchi'
    t_begin = _double_consonant_state(td, start_state, ['c', 't', 'd'])

    _many_to_one_arc(td, t_begin, ['ch', 'ty'], 'チ', end_states['y'])
    _many_to_one_arc(td, t_begin, ['dy'], 'ヂ', end_states['y'])

    _many_to_one_arc(td, t_begin, ['ti', 'chi'], 'チ', end_states['i'])
    _multi_char_arc(td, t_begin, 'ta', 'タ', end_states['a'])
    _multi_char_arc(td, t_begin, 'te', 'テ', end_states['e'])
    _multi_char_arc(td, t_begin, 'to', 'ト', end_states['o'])
    _many_to_one_arc(td, t_begin, ['tsu', 'tu'], 'ツ', end_states['u'])

    _multi_char_arc(td, t_begin, 'di', 'ヂ', end_states['i'])
    _multi_char_arc(td, t_begin, 'da', 'ダ', end_states['a'])
    _multi_char_arc(td, t_begin, 'de', 'デ', end_states['e'])
    _multi_char_arc(td, t_begin, 'do', 'ド', end_states['o'])
    _many_to_one_arc(td, t_begin, ['du', 'dzu'], 'ヅ', end_states['u'])


def _build_vowels(td, start_state, end_states):
    _char_arc(td, start_state, 'u', 'ウ', end_states['u'])
    _one_to_many_arc(td, start_state, 'o', ['オ', 'ヲ'], end_states['o'])
    _char_arc(td, start_state, 'a', 'ア', end_states['a'])
    _char_arc(td, start_state, 'i', 'イ', end_states['i'])
    _char_arc(td, start_state, 'e', 'エ', end_states['e'])
    _multi_char_arc(td, start_state, 'wo', 'ヲ', end_states['o'])


def _build_n(td, start_state, end_states):
    n = td.add_state()
    _char_arc(td, start_state, 'n', EPSILON, n)

    _many_to_one_arc(td, n, ['n',       # wapuro
                             '\'',      # Kunrei-shiki and Nihon-shiki
                             '-',       # Hepburn
                             EPSILON],  # a common omission
                     'ン',
                     end_states['n'])
    _char_arc(td, n, 'i', 'ニ', end_states['i'])
    _char_arc(td, n, 'e', 'ネ', end_states['e'])
    _char_arc(td, n, 'o', 'ノ', end_states['o'])
    _char_arc(td, n, 'a', 'ナ', end_states['a'])
    _char_arc(td, n, 'u', 'ヌ', end_states['e'])

    _char_arc(td, n, 'y', 'n', end_states['y'])


def _build_kg(td, start_state, end_states):
    k_begin = _double_consonant_state(td, start_state, 'k')

    _multi_char_arc(td, k_begin, 'ki', 'キ', end_states['i'])
    _multi_char_arc(td, k_begin, 'ke', 'ケ', end_states['e'])
    _multi_char_arc(td, k_begin, 'ko', 'コ', end_states['o'])
    _multi_char_arc(td, k_begin, 'ka', 'カ', end_states['a'])
    _multi_char_arc(td, k_begin, 'ku', 'ク', end_states['u'])

    g_begin = _double_consonant_state(td, start_state, 'g')

    _multi_char_arc(td, g_begin, 'gi', 'ギ', end_states['i'])
    _multi_char_arc(td, g_begin, 'ge', 'ゲ', end_states['e'])
    _multi_char_arc(td, g_begin, 'go', 'ゴ', end_states['o'])
    _multi_char_arc(td, g_begin, 'ga', 'ガ', end_states['a'])
    _multi_char_arc(td, g_begin, 'gu', 'グ', end_states['u'])

    _multi_char_arc(td, k_begin, 'ky', 'ky', end_states['y'])
    _multi_char_arc(td, g_begin, 'gy', 'gy', end_states['y'])


def _build_r(td, start_state, end_states):
    _multi_char_arc(td, start_state, 'ri', 'リ', end_states['i'])
    _multi_char_arc(td, start_state, 're', 'レ', end_states['e'])
    _multi_char_arc(td, start_state, 'ro', 'ロ', end_states['o'])
    _multi_char_arc(td, start_state, 'ra', 'ラ', end_states['a'])
    _multi_char_arc(td, start_state, 'ru', 'ル', end_states['u'])

    _multi_char_arc(td, start_state, 'ry', 'ry', end_states['y'])


def _build_m(td, start_state, end_states):
    _multi_char_arc(td, start_state, 'mi', 'ミ', end_states['i'])
    _multi_char_arc(td, start_state, 'me', 'メ', end_states['e'])
    _multi_char_arc(td, start_state, 'mo', 'モ', end_states['o'])
    _multi_char_arc(td, start_state, 'ma', 'マ', end_states['a'])
    _multi_char_arc(td, start_state, 'mu', 'ム', end_states['u'])

    _multi_char_arc(td, start_state, 'my', 'ミ', end_states['y'])


def _build_w(td, start_state, end_states):
    _multi_char_arc(td, start_state, 'wa', 'ワ', end_states['a'])


def _build_small_y_state(td, end_states):
    start_state = td.add_state()
    _char_arc(td, start_state, 'a', 'ャ', end_states['a'])
    _char_arc(td, start_state, 'u', 'ュ', end_states['u'])
    _char_arc(td, start_state, 'o', 'ョ', end_states['o'])
    return start_state


def _build_big_y(td, start_state, end_states):
    _multi_char_arc(td, start_state, 'yo', 'ヨ', end_states['o'])
    _multi_char_arc(td, start_state, 'ya', 'ヤ', end_states['a'])
    _multi_char_arc(td, start_state, 'yu', 'ユ', end_states['u'])


def _build_hpb(td, start_state, end_states):
    pb_next = td.add_state()
    _char_arc(td, start_state, 'm', 'ン', pb_next)
    _eps_arc(td, start_state, pb_next)

    p_begin = _double_consonant_state(td, pb_next, 'p')

    _multi_char_arc(td, p_begin, 'pi', 'ピ', end_states['i'])
    _multi_char_arc(td, p_begin, 'pe', 'ペ', end_states['e'])
    _multi_char_arc(td, p_begin, 'po', 'ポ', end_states['o'])
    _multi_char_arc(td, p_begin, 'pa', 'パ', end_states['a'])
    _multi_char_arc(td, p_begin, 'pu', 'プ', end_states['u'])

    b_begin = _double_consonant_state(td, pb_next, 'b')

    _multi_char_arc(td, b_begin, 'bi', 'ビ', end_states['i'])
    _multi_char_arc(td, b_begin, 'be', 'ベ', end_states['e'])
    _multi_char_arc(td, b_begin, 'bo', 'ボ', end_states['o'])
    _multi_char_arc(td, b_begin, 'ba', 'バ', end_states['a'])
    _multi_char_arc(td, b_begin, 'bu', 'ブ', end_states['u'])

    _multi_char_arc(td, start_state, 'hi', 'ヒ', end_states['i'])
    _multi_char_arc(td, start_state, 'he', 'ヘ', end_states['e'])
    _multi_char_arc(td, start_state, 'ho', 'ホ', end_states['o'])
    _multi_char_arc(td, start_state, 'ha', 'ハ',  end_states['a'])
    _many_to_one_arc(td, start_state, ['hu', 'fu'], 'フ', end_states['u'])

    _multi_char_arc(td, p_begin, 'py', 'ピ', end_states['y'])
    _multi_char_arc(td, b_begin, 'by', 'ビ', end_states['y'])
    _multi_char_arc(td, start_state, 'hy', 'ヒ', end_states['y'])


def _long_vowel_mark_state(td, end_state, vowels):
    result = td.add_state()
    for vowel in vowels:
        _many_to_one_arc(td,
                         result,
                         [unicodedata.lookup('COMBINING MACRON'),  # Hepburn
                          unicodedata.lookup('COMBINING CIRCUMFLEX ACCENT'),  # Kunrei-shiki and Nihon-shiki
                          'h',  # passport Hepburn
                          EPSILON],  # commonly omitted
                         vowel,
                         end_state)
    _eps_arc(td, result, end_state)
    return result


def _double_consonant_state(td, start_state, consonants):
    state = td.add_state()
    _many_to_one_arc(td, start_state, consonants, 'ッ', state)
    _eps_arc(td, start_state, state)
    return state


def _many_to_one_arc(td, start_state, input_strs, output_str, end_state):
    for input_str in input_strs:
        _multi_char_arc(td, start_state, input_str, output_str, end_state)


def _many_to_many_arc(td, start_state, input_strs, output_strs, end_state):
    for input_str in input_strs:
        _one_to_many_arc(td, start_state, input_str, output_strs, end_state)


def _one_to_many_arc(td, start_state, input_str, output_strs, end_state):
    for output_str in output_strs:
        _multi_char_arc(td, start_state, input_str, output_str, end_state)


def _multi_char_arc(td, start_state, input_str, output_str, end_state):
    curr = start_state
    i = 0
    while i < min(len(input_str), len(output_str)):
        nxt = td.add_state()
        _char_arc(td, curr, input_str[i], output_str[i], nxt)
        curr = nxt
        i += 1
    while i < len(input_str):
        nxt = td.add_state()
        _char_arc(td, curr, input_str[i], EPSILON, nxt)
        curr = nxt
        i += 1
    while i < len(output_str):
        nxt = td.add_state()
        _char_arc(td, curr, EPSILON, output_str[i], nxt)
        curr = nxt
        i += 1
    _char_arc(td, curr, EPSILON, EPSILON, end_state)


def _char_arc(td, start_state, input_char, output_char, next_state):
    td.add_arc(start_state,
               Arc(SYMBOL_TABLE[input_char],
                   SYMBOL_TABLE[output_char],
                   _const_w(td),
                   next_state))


def _eps_arc(td, start_state, end_state):
    _char_arc(td, start_state, EPSILON, EPSILON, end_state)


def _const_w(td):
    # All transliteration arcs are of constant weight
    return fst.Weight.One(td.weight_type())


def _all_valid_strings(td: fst.Fst) -> List[Tuple[List[int], float]]:
    """Return an enumeration of the emission language. Essentially the equivalent of
    fstprint, but not handling the de-interning of strings.

    The weight returned is not the weight of the whole sequence, but the weight
    of the final state in the sequence as a final state.

    Does not check for duplicate emissions or cycles in the transducer.

    :param td: transducer, the emission language of which to enumerate
    :returns: a list of (interned emission symbols, weight) tuples

    """
    if td.start() == -1:
        return []
    stack = [(td.start(), [])]
    complete_emissions = []
    while stack:
        state, output = stack.pop()
        final_weight = float(td.final(state))
        if np.isfinite(final_weight):
            complete_emissions.append((output, final_weight))
        stack += [(a.nextstate, output + [a.olabel]) for a in td.arcs(state)]
    return complete_emissions


def _deintern_tokens(tokens):
    return ''.join([REVERSE_SYMBOL_TABLE[t] for t in tokens if t != 0])


def acceptor_for_strings(strings: List[str], weights: List[float]) -> fst.Fst:
    """Create an acceptor for strings with weights"""
    strings, weights = zip(*sorted(zip(strings, weights)))
    td = fst.Fst()
    start_state = td.add_state()
    td.set_start(start_state)
    _build_acceptor_recursive(td, strings, weights, start_state, 0, 0, len(strings))
    return td


def _build_acceptor_recursive(td, strings, weights, start_state, str_idx, si, sj):
    if si == sj:
        return
    i = si
    set_final = False
    # look for finished strings
    while i < sj and len(strings[i]) <= str_idx:
        if not set_final:
            set_final = True
            td.set_final(start_state, weights[i])
        i += 1

    # descend further into the strings
    while i < sj:
        first_char = strings[i][str_idx]
        next_state = td.add_state()
        j = i
        while j < sj and strings[j][str_idx] == first_char:
            j += 1
        _char_arc(td, start_state, first_char, first_char, next_state)
        _build_acceptor_recursive(td, strings, weights, next_state, str_idx + 1, i, j)
        i = j
