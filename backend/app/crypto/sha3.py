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

    def binary_list_to_string(self, binary_list: list[int]) -> str:
        binary_string = "".join(str(bit) for bit in binary_list)
        n = int(binary_string, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

    def digest(self, message: str) -> str:
        # Convert message to a binary list
        intermediate = [int(b) for ch in message for b in bin(ord(ch))[2:].zfill(8)]

        intermediate = self._pad_message(intermediate)

        digest_string = self.binary_list_to_string(intermediate)

        return digest_string

# Example usage

plain = "ABC"
sha3 = SHA3(SHA3Instance.SHA256)
digest = sha3.digest(plain)

print(digest)
