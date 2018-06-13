import myouji_kenchi


# Given that the output depends on what goes into the attested myouji file I'm
# hesitant to write too many tests in the blast radius of changes to that file


class TestTransducer():
    nbt = myouji_kenchi.MyoujiBackTransliteration()

    def assert_transliteration(self, romaji, *expected_results):
        results = self.nbt.back_transliterate(romaji)
        strings = set(r[0] for r in results)
        assert strings == set(expected_results)

    def test_assorted(self):
        self.assert_transliteration('sa', 'サ')
        self.assert_transliteration('ＳＡ', 'サ')
        self.assert_transliteration('se', 'セ')
        self.assert_transliteration('shō', 'ショウ')  # composed
        self.assert_transliteration('shō', 'ショウ')  # decomposed
        self.assert_transliteration('sho', 'ショウ')
        self.assert_transliteration('syo', 'ショウ')
        self.assert_transliteration('ho', 'ホ', 'ホウ', 'ホオ')
        self.assert_transliteration('teppou', 'テッポウ')
        self.assert_transliteration('shibukawa', 'シブカワ')
        self.assert_transliteration('watamura', 'ワタムラ')
        self.assert_transliteration('Matsumoto', 'マツモト')
        self.assert_transliteration('Matumoto', 'マツモト')
        self.assert_transliteration('Tusima', 'ツシマ')
        self.assert_transliteration('IMAZU', 'イマヅ', 'イマズ')
        self.assert_transliteration('SATO', 'サトウ', 'サトオ', 'サト')
        self.assert_transliteration('Uchino', 'ウチノ', 'ウチノウ')
        self.assert_transliteration('Utino', 'ウチノ', 'ウチノウ')
        self.assert_transliteration('Chano', 'チャノ')
        self.assert_transliteration('Tyano', 'チャノ')
        self.assert_transliteration('Kojima', 'コジマ', 'コヂマ', 'コウジマ')
        self.assert_transliteration('Kozima', 'コジマ', 'コヂマ', 'コウジマ')
        self.assert_transliteration('Inuduka', 'イヌヅカ')
        self.assert_transliteration('Inuzuka', 'イヌヅカ', 'イヌズカ')
        self.assert_transliteration('Inudzuka', 'イヌヅカ')
        self.assert_transliteration('Betchaku', 'ベッチャク')
        self.assert_transliteration('Becchaku', 'ベッチャク')
        self.assert_transliteration('Uwozaki', 'ウヲザキ')
        self.assert_transliteration('Uozaki', 'ウヲザキ', 'ウオザキ')

    def test_oh(self):
        self.assert_transliteration('Ohnishi', 'オオニシ', 'オウニシ')

    def test_leading_m(self):
        self.assert_transliteration('Sampei', 'サンペイ')
        self.assert_transliteration('Sanpei', 'サンペイ')

    def test_glottal_stop(self):
        self.assert_transliteration('Shinyagaito', 'シンヤガイト')
        self.assert_transliteration('Sinyagaito', 'シンヤガイト')
        self.assert_transliteration('Shin\'yagaito', 'シンヤガイト')
        self.assert_transliteration('Shin-yagaito', 'シンヤガイト')

    def test_double_i(self):
        self.assert_transliteration('Ishii', 'イシイ')
        # To be clear, 'Ishî' is almost certainly a wrong transliteration
        # Nevertheless, the below is the expected behavior
        self.assert_transliteration('Ishî', 'イシイ')
        self.assert_transliteration('Isî', 'イシイ')

    def test_bad_characters(self):
        self.assert_transliteration('@')
