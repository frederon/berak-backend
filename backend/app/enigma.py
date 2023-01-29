'''
    Enigma Machine

    Based on one of the many variants of the Enigma Machine.
    Engima M3 UKW-B Reflector
'''


from typing import List, Dict
from enum import Enum

class EnigmaRotor(Enum):
    I = 0
    II = 1
    III = 2
    IV = 3

    '''
    Motor wiring reference
    https://en.wikipedia.org/wiki/Enigma_rotor_details
    '''
    @classmethod
    def get_wiring(cls, rotor: 'EnigmaRotor'):
        if rotor == EnigmaRotor.I:
#                  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#                  "JEKMFLGDQVZNTOWYHXUSPAIBRC"
#                  "CJEKMFLGDQVZNTOWYHXUSPAIBR"
            return "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
        if rotor == EnigmaRotor.II:
            return "AJDKSIRUXBLHWTMCQGZNPYFVOE"
        if rotor == EnigmaRotor.III:
            return "BDFHJLCPRTXVZNYEIWGAKMUSQO"
        if rotor == EnigmaRotor.IV:
            return "ESOVPZJAYQUIRHXLNFTGKDCMWB"

        raise ValueError()

    @classmethod
    def get_inverse_wiring(cls, rotor: 'EnigmaRotor'):
        if rotor == EnigmaRotor.I:
            return "UWYGADFPVZBECKMTHXSLRINQOJ"
        if rotor == EnigmaRotor.II:
            return "AJPCZWRLFBDKOTYUQGENHXMIVS"
        if rotor == EnigmaRotor.III:
            return "TAGBPCSDQEUFVNZHYIXJWLRKOM"
        if rotor == EnigmaRotor.IV:
            return "HZWVARTNLGUPXQCEJMBSKDYOIF"

        raise ValueError()

class EnigmaMachine:
    REFLECTOR = {
        "A":"Y",
        "Y":"A",
        "B":"R",
        "R":"B",
        "C":"U",
        "U":"C",
        "D":"H",
        "H":"D",
        "E":"Q",
        "Q":"E",
        "F":"S",
        "S":"F",
        "G":"L",
        "L":"G",
        "I":"P",
        "P":"I",
        "J":"X",
        "X":"J",
        "K":"N",
        "N":"K",
        "M":"O",
        "O":"M",
        "T":"Z",
        "Z":"T",
        "V":"W",
        "W":"V"
    }

    '''
    Enigma Machine constructor
    Arguments:
        rotors: 3 positional EnigmaRotor (left to right). 
    '''
    def __init__(self, rotors:List[EnigmaRotor], positions: List[int], plugboard: Dict[str,str]) -> None:
        self.rotors = rotors
        self.rotor_positions = positions
        self.plugboard = plugboard

    def _plugboard_substitution(self, letter: str) -> str:
        if letter in self.plugboard:
            return self.plugboard[letter]
        else:
            return letter

    def _reflector_substitution(self, letter:str) -> str:
        return self.REFLECTOR[letter]

    def _forward_substitution(self, letter:str)->str:
        rotor_positions = self.rotor_positions
        rotors = self.rotors
        for i in range(len(rotors)-1,-1,-1):
            rotor = rotors[i]
            rotor_wiring = EnigmaRotor.get_wiring(rotor)
            shift = rotor_positions[i]

            letter = rotor_wiring[(ord(letter) - ord("A") + shift) % 26]
            letter = chr(ord("A") + (ord(letter) - ord("A") + 26 - shift) % 26)
            print(f"Wheel {3-i} Encryption: ", letter, rotor_wiring, rotor_positions)

        return letter

    def _backward_substitution(self, letter:str)->str:
        rotor_positions = self.rotor_positions
        rotors = self.rotors
        for i in range(len(rotors)):
            rotor = rotors[i]
            rotor_inverse_wiring = EnigmaRotor.get_inverse_wiring(rotor)
            shift = rotor_positions[i]

            letter = rotor_inverse_wiring[(ord(letter) - ord("A") + shift) % 26]
            letter = chr(ord("A") + (ord(letter) - ord("A") + 26 - shift) % 26)
            print(f"Wheel {i} Encryption: ", letter)
        # for i, rotor in enumerate(rotors):
        #     rotor_wiring = EnigmaRotor.get_wiring(rotor)
        #     letter = rotor_wiring[(rotor_wiring.index(letter) - rotor_positions[i]) % 26]
        #     print(f"Wheel {i} Encryption: ", letter)
        return letter

    def _advance_rotors(self):
        carry = 1
        for i in range(len(self.rotors)-1, -1, -1):
            curr = self.rotor_positions[i]
            self.rotor_positions[i] = (curr + carry)
            carry = (curr + carry)//26

    def encrypt(self, message: str) -> str:
        cipher_text = ""
        for letter in message:
            self._advance_rotors()
            letter = self._plugboard_substitution(letter)
            letter = self._forward_substitution(letter)
            letter = self._reflector_substitution(letter)
            print("Reflector Encryption: ", letter)
            letter = self._backward_substitution(letter)
            letter = self._plugboard_substitution(letter)
            cipher_text += letter

        return cipher_text

# wirings = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "AJDKSIRUXBLHWTMCQGZNPYFVOE","BDFHJLCPRTXVZNYEIWGAKMUSQO", "ESOVPZJAYQUIRHXLNFTGKDCMWB"]
# rwiring = [["0" for _ in range(26)] for _ in range(4)]
# for i in range(0, 4):
#     wiring = wirings[i]
#     print(wiring, i)
#     for j in range(0, len(wiring)):
#         rwiring[i][ord(wiring[j]) - ord("A")] = chr(ord("A") + j)
#     print("HMM", rwiring)

# for rwire in rwiring:
#     print("".join(rwire))

enigma = EnigmaMachine(rotors=[EnigmaRotor.I, EnigmaRotor.IV, EnigmaRotor.II], positions=[0,0,1], plugboard={})
cipher = enigma.encrypt("HELLO")
print(cipher)