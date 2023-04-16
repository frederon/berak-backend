from enum import Enum
from typing import NamedTuple

# reference: https://keccak.team/keccak_specs_summary.html

class SHA3Instance(Enum):
    SHA224 = 0
    SHA256 = 1
    SHA384 = 2
    SHA512 = 3

class SHA3Specification(NamedTuple):
    r: int
    c: int
    output_length: int
    mbits: str

class SHA3():
    specs: SHA3Specification

    def __init__(self, instance: SHA3Instance) -> None:
        self.specs = self._instance_param_to_specs(instance)

    def _instance_param_to_specs(self, instance: SHA3Instance) -> SHA3Specification:
        if instance == SHA3Instance.SHA224:
            return SHA3Specification(1152,448, 224,"01")

        if instance == SHA3Instance.SHA256:
            return SHA3Specification(1088,512, 256,"01")

        if instance == SHA3Instance.SHA384:
            return SHA3Specification(832,768, 384,"01")

        if instance == SHA3Instance.SHA512:
            return SHA3Specification(576,1024, 512,"01")

        raise ValueError()

    def _pad_message(self, message: str) -> str:
        """
        Return the padded message

        Message is padded such that it's divisible by r
        """
        r = self.specs.r

        if len(message) % r == 0:
            return message

        padded_message = message + (r - len(message) % r) * b"\x00"
        return padded_message

    def digest(self, message: str) -> bytes:
        # Encodes and hexify message, this assumes message is in UTF-8 format
        intermediate = message.encode()
        print(intermediate, type(intermediate))
        intermediate = self._pad_message(intermediate)

        digest = intermediate

        return digest

# Example usage

plain = "Hello world!"
sha3 = SHA3(SHA3Instance.SHA256)
digest = sha3.digest(plain)
text = digest.decode("utf-8")

print(digest)
print(text)
