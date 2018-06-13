import myouji_kenchi


class TestKenchi():
    def test_assorted(self):
        assert_ordered(True, 'Shougo', 'ITO')
        assert_ordered(False, 'ITO', 'Shougo')
        assert_ordered(True, 'Satoshi', 'Yamada')
        assert_ordered(False, 'Yamada', 'Satoshi')
        assert_ordered(True, 'Ryuusuke', 'Takahama')
        assert_ordered(True, 'A', 'Oshiro')
        assert_ordered(True, 'Yuta', 'Nishimori')
        assert_ordered(True, 'naoki', 'wakou')
        assert_ordered(True, 'KANA', 'NAKAJIMA')
        assert_ordered(True, 'Kaori', 'Sato')
        assert_ordered(False, 'Hanaoka', 'Hiroshi')
        assert_ordered(False, 'Hayasi', 'Tie')

    def test_foreign(self):
        assert_ordered(True, 'Legokichi', 'Duckscallion')
        assert_ordered(True, 'Duckscallion', 'Legokichi')
        assert_ordered(False, 'Yamada', 'Legokichi')

    def test_bad_characters(self):
        assert_ordered(True, '@', 'Yamada')

    def test_initial_with_period(self):
        assert_ordered(True, 'K.', 'Yoshida')
        assert_ordered(False, 'Yoshida', 'K.')

    def test_prior(self):
        # Note: below tests are in the blast radius of data changes
        assert_ordered(True, 'Takashi', 'Ise')
        assert_ordered(False, 'Takashi', 'Ise', prior=0.75)

    def test_capital_heuristic(self):
        assert_ordered(True, 'Takegawa', 'Sho')
        assert_ordered(False, 'TAKEGAWA', 'Sho')
        assert_ordered(False, 'Ito', 'Sho')
        assert_ordered(True, 'Ito', 'SHO')
        assert_ordered(False, 'ITO', 'SHO')
        assert_ordered(True, 'Ito', 'SHŌ')  # composed macron
        assert_ordered(True, 'Ito', 'SHŌ')  # decomposed macron


def assert_ordered(ordered, *names, **kwargs):
    ordering_result = myouji_kenchi.order_names(names, **kwargs)
    if ordered:
        assert list(names) == ordering_result
    else:
        assert list(reversed(names)) == ordering_result
