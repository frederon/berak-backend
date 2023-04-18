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

KECCAK_RC = [
    "0x0000000000000001",
    "0x0000000000008082",
    "0x800000000000808A",
    "0x8000000080008000",
    "0x000000000000808B",
    "0x0000000080000001",
    "0x8000000080008081",
    "0x8000000000008009",
    "0x000000000000008A",
    "0x0000000000000088",
    "0x0000000080008009",
    "0x000000008000000A",
    "0x000000008000808B",
    "0x800000000000008B",
    "0x8000000000008089",
    "0x8000000000008003",
    "0x8000000000008002",
    "0x8000000000000080",
    "0x000000000000800A",
    "0x800000008000000A",
    "0x8000000080008081",
    "0x8000000000008080",
    "0x0000000080000001",
    "0x8000000080008008",
]

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
        assert len(l1) == len(l2)

        l3 = [0 for _ in range(len(l1))]

        for i in range(len(l1)):
            l3[i] = l1[i] ^ l2[i]

        return l3

    def _rotl(self, x:list[int], n:int) -> list[int]:
        return x[n:] + x[:n]

    def _neg_word(self, x:list[int]) -> list[int]:
        return [~bit & 1 for bit in x]

    def _and_word(self, l1:list[int], l2:list[int]) -> list[int]:
        assert len(l1) == len(l2)

        return [l1[i] & l2[i] for i in range(len(l1))]

    def digest(self, message: str) -> str:
        # Convert message to a binary list
        intermediate = [int(b) for ch in message for b in bin(ord(ch))[2:].zfill(8)]

        intermediate = self._keccak(intermediate)

        return intermediate

    def _keccak(self, intermediate:list[int]) -> list[int]:
        r = self.specs.r
        w = self.specs.w
        output_length = self.specs.output_length

        # Padding
        intermediate = self._pad_message(intermediate)

        # Initialization
        S = [[[0 for _ in range(w)] for _ in range(5)] for _ in range(5)]

        # Absorbing phase
        for i in range(0, int(len(intermediate)/r), r):
            pi = intermediate[i:i+r]

            for y in range(len(S)):
                for x in range(len(S)):
                    if x + 5*y < r/w:
                        offset = (x + 5 *y) * w
                        S[y][x] = self._xor_word(S[y][x], pi[offset:offset+w])
                        S = self._keccak_f1600_permutation(S)

        # Squeezing phase, we assumes only 1 output that is requested (fixed length)
        Z = []
        for y in range(len(S)):
            for x in range(len(S)):
                if len(Z) >= output_length:
                    break

                if x + 5*y < r/w:
                    Z.extend(S[y][x])

        return Z[:output_length]

    def _keccak_f1600_permutation(self, state: list[int]) -> list[int]:
        nr = self.specs.nr
        w = self.specs.w

        def round1600(A: list[list[int]], RC:list[int]) -> list[int]:
            # Theta
            C = [[0 for _ in range(w)] for _ in range(5)]
            D = [[0 for _ in range(w)] for _ in range(5)]

            for x in range(5):
                C[x] = self._xor_word(self._xor_word(self._xor_word(self._xor_word(A[0][x], A[1][x]), A[2][x]), A[3][x]), A[4][x])

            for x in range(5):
                D[x] = self._xor_word(C[(x-1) % 5], self._rotl(C[(x+1) % 5], 1))

            A = [[self._xor_word(A[y][x], D[x]) for x in range(5)] for y in range(5)]

            # Rho Pi
            x, y = 1, 0
            current = A[y][x]
            for t in range(24):
                x, y = y, (2*x+3*y) % 5
                current, A[y][x] = A[y][x], self._rotl(current, (t+1)*(t+2)//2)

            # Chi
            for y in range(5):
                T = [A[y][x] for x in range(5)]
                for x in range(5):
                    A[y][x] = self._xor_word(T[x], self._and_word(self._neg_word(T[(x+1)%5]), T[(x+2) % 5]))

            # Iota
            A[0][0] = self._xor_word(A[0][0], RC)

            return A

        for i in range(nr):
            state = round1600(state, [int(bit) for byte in bytes.fromhex(KECCAK_RC[i][2:]) for bit in f"{byte:08b}"][-w:])
        return state

# Example usage

plain = "ABCD"
sha3 = SHA3(SHA3Instance.SHA256)
digest = sha3.digest(plain)

print(digest)
