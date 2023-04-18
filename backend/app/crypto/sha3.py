from enum import Enum

# reference: https://keccak.team/keccak_specs_summary.html

class SHA3Instance(Enum):
    SHA224 = 0
    SHA256 = 1
    SHA384 = 2
    SHA512 = 3

class SHA3Specification():
    r: int
    c: int
    output_length: int
    mbits: list[int]

    b: int
    l: int
    nr: int
    w: int

    def __init__(self,r:int,c:int,output_length:int, mbits:list[int]) -> None:
        """
        Specification assumes Keccak (SHA3) with b = 1600
        """
        self.r = r
        self.c = c
        self.output_length = output_length
        self.mbits = mbits

        self.b = 1600
        assert self.b == r + c

        self.l = 6
        self.nr = 24
        self.w = 64


class SHA3():
    specs: SHA3Specification

    def __init__(self, instance: SHA3Instance) -> None:
        self.specs = self._instance_param_to_specs(instance)

    def _instance_param_to_specs(self, instance: SHA3Instance) -> SHA3Specification:
        if instance == SHA3Instance.SHA224:
            return SHA3Specification(1152,448, 224,[0,1])

        if instance == SHA3Instance.SHA256:
            return SHA3Specification(1088,512, 256,[0,1])

        if instance == SHA3Instance.SHA384:
            return SHA3Specification(832,768, 384,[0,1])

        if instance == SHA3Instance.SHA512:
            return SHA3Specification(576,1024, 512,[0,1])

        raise ValueError()

    def _pad_message(self, intermediate: list[int]) -> str:
        """
        Return the padded binary list (intermediate)

        Intermediate is padded such that it's divisible by r
        """
        r = self.specs.r

        if len(intermediate) % r == 0:
            return intermediate

        # add pad of P (mbits)
        intermediate.extend(self.specs.mbits)

        # add pad of 10*1
        intermediate.extend([1,0])
        while (len(intermediate) + 1) % r != 0:
            intermediate.append(0)
        intermediate.append(1)

        return intermediate

    def _xor_word(self, l1:list[int], l2:list[int]) -> list[int]:
        print(l1)
        print(l2)
        assert len(l1) == len(l2)

        l3 = [0 for _ in range(len(l1))]

        for i in range(len(l1)):
            l3[i] = l1[i] ^ l2[i]

        return l3

    def digest(self, message: str) -> str:
        # Convert message to a binary list
        intermediate = [int(b) for ch in message for b in bin(ord(ch))[2:].zfill(8)]

        intermediate = self._keccak(intermediate)

        return intermediate

    def _keccak(self, intermediate:list[int]) -> list[int]:
        r = self.specs.r
        w = self.specs.w

        # Padding
        intermediate = self._pad_message(intermediate)

        # Initialization
        S = [[[0 for _ in range(w)] for _ in range(5)] for _ in range(5)]

        # Absorbing phase
        # for i in range(0, int(len(intermediate)/r), r):
        #     pi = intermediate[i:i+r]

        #     for y in range(len(S)):
        #         for x in range(len(S)):
        #             if x + 5*y < r/w:
        #                 S[y][x] = self._xor_word(S[y][x], pi[x+5*y:x+5*y+w])
        #                 S = self._keccak_f1600_permutation(S)

        # Squeezing phase, we assumes only 1 output that is requested (fixed length)
        Z = []
        for y in range(len(S)):
            for x in range(len(S)):
                if x + 5*y < r/w:
                    Z.append(S[y][x])

        return intermediate

    def _keccak_f1600_permutation(self, state: list[int]) -> list[int]:
        return state

# Example usage

# plain = "ABC"
# sha3 = SHA3(SHA3Instance.SHA256)
# digest = sha3.digest(plain)

# print(digest)
