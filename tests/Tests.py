import unittest
from escalas.functions import get_from_file

class TestGetFromFile(unittest.TestCase):
    
    def test_1(self):
        frases = [
            'Take this time, Francis, to know your other attendees.',
            "Tell me you're not peddling influence with your wife?",
            'The Russian research vessel.',
            "Let's reconvene when you know more."
        ]
        file = 'frasesTeste.txt'
        phrases = get_from_file(file)
        self.assertEqual(phrases, frases)        
    

if __name__ == '__main__':
    unittest.main()