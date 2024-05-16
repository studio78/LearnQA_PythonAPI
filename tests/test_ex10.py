_author__ = 'Stangli Adadurov'


class TestEx10:

    def test_ex10(self):
        phrase = input("Введите любую фразу короче 15 символов: ")
        assert len(phrase) < 15, f"Фраза '{phrase}' длиннее либо равна 15 символам"
