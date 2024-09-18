import random
import hashlib

class FiboCaeser:
    def __init__(self, user_id: int, chat_id: int):
        self.start_shift = user_id + chat_id
        self.character_list = list("abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=[]|;':,.<>?`~")
    
    def randomize_character_list(self):
        # Hash the seed to get a unpredictable number
        hash_seed = hashlib.sha256(str(self.start_shift).encode('utf-8')).digest()
        random.seed(hash_seed)
        random.shuffle(self.character_list)

    def fibonaaci(self, n: int) -> int:
        seq = []
        a, b = self.start_shift, self.start_shift 
        for _ in range(n):
            a, b = b, a + b
            seq.append(a)
        return seq

    def encrypt(self, text: str) -> str:
        token_list = list(text)
        fibonaaci_seq = self.fibonaaci(len(token_list))
        self.randomize_character_list()
        encrypted_text = ""
        modulo = len(self.character_list)
        for i, char in enumerate(token_list):
            index = self.character_list.index(char)
            shift = fibonaaci_seq[i]
            encrypted_text += self.character_list[(index + shift) % modulo]
        return encrypted_text
    
    def decrypt(self, text: str) -> str:
        token_list = list(text)
        fibonaaci_seq = self.fibonaaci(len(token_list))
        self.randomize_character_list()
        decrypted_text = ""
        modulo = len(self.character_list)
        for i, char in enumerate(token_list):
            index = self.character_list.index(char)
            shift = fibonaaci_seq[i]
            decrypted_text += self.character_list[(index - shift) % modulo]
        return decrypted_text
    