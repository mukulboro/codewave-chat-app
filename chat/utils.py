import random
import hashlib
from profanity_check import predict

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
    
    def decrypt(self, text: str, pattern:str) -> str: # Decrypt at certain position according to the pattern
        token_list = list(text)
        pattern_list = list(pattern)
        fibonaaci_seq = self.fibonaaci(len(token_list))
        self.randomize_character_list()
        decrypted_text = ""
        modulo = len(self.character_list)
        for i, char in enumerate(token_list):
            index = self.character_list.index(char)
            shift = fibonaaci_seq[i]
            if pattern_list[i] == '1':
                decrypted_text += self.character_list[(index - shift) % modulo]
            else:
                decrypted_text += char
        return decrypted_text

def similarity_score(user1_interest_list: list, user2_interest_list: list) -> float:
    # Calculate similarity score between two list of strings
    # This is a simple implementation of Jaccard Similarity
    user1_interest_list = [ str(i).upper() for i in user1_interest_list ]
    user2_interest_list = [ str(i).upper() for i in user2_interest_list ]
    set1 = set(user1_interest_list)
    set2 = set(user2_interest_list)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def censor_profanity(text: str) -> str:
    word_list = text.split(" ")
    prediction = predict(word_list)
    for i, word in enumerate(word_list):
        if prediction[i] == 1:
            word_list[i] = f"{word[0]}{'*' * (len(word)-2)}{word[-1]}"
    return " ".join(word_list)