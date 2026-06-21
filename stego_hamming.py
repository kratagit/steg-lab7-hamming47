import numpy as np
from PIL import Image

def text_to_bits(text):
    text_bytes = text.encode('utf-8')
    length = len(text_bytes)
    # Store length in 30 bits (10 groups of 3)
    length_bits = [int(x) for x in format(length, '030b')]
    
    msg_bits = []
    for b in text_bytes:
        msg_bits.extend([int(x) for x in format(b, '08b')])
        
    bits = length_bits + msg_bits
    
    # Pad to multiple of 3
    if len(bits) % 3 != 0:
        bits.extend([0] * (3 - (len(bits) % 3)))
        
    return bits

def bits_to_text(bits):
    if len(bits) < 30:
        return ""
    length_bits = bits[:30]
    length = int("".join(str(b) for b in length_bits), 2)
    
    msg_bits = bits[30:30 + 8 * length]
    if len(msg_bits) < 8 * length:
        return ""
        
    msg_bytes = bytearray()
    for i in range(0, len(msg_bits), 8):
        byte = int("".join(str(b) for b in msg_bits[i:i+8]), 2)
        msg_bytes.append(byte)
        
    try:
        return msg_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return "<Błąd dekodowania UTF-8 - prawdopodobnie uszkodzone dane>"

def calculate_syndrome(block):
    """Oblicza syndrom dla bloku 7 bitów"""
    s = 0
    for i in range(7):
        if block[i] == 1:
            s ^= (i + 1)
    return s

def hide_message(image_path, text, output_path):
    bits = text_to_bits(text)
    
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    img_array = np.array(img)
    shape = img_array.shape
    
    flat_img = img_array.flatten()
    
    # Potrzebujemy 7 pikseli (kanałów) na każde 3 bity wiadomości
    num_groups = len(bits) // 3
    required_pixels = num_groups * 7
    
    if required_pixels > len(flat_img):
        raise ValueError(f"Obraz jest zbyt mały. Potrzeba {required_pixels} wartości, dostępnych jest {len(flat_img)}.")
        
    for i in range(num_groups):
        m1, m2, m3 = bits[i*3:i*3+3]
        m = (m1 << 2) | (m2 << 1) | m3 # Grupa 3 bitów jako liczba 0-7
        
        block_idx = i * 7
        # Pobierz 7 najmniej znaczących bitów
        block_lsb = flat_img[block_idx:block_idx+7] & 1
        
        # Oblicz syndrom
        s = calculate_syndrome(block_lsb)
        
        # Znajdź pozycję, którą trzeba zmienić (1-indexed, 0 oznacza brak zmian)
        err = s ^ m
        
        if err != 0:
            # Odwróć bit na odpowiedniej pozycji (err - 1, bo err jest 1-indexed)
            flat_img[block_idx + err - 1] ^= 1
            
    # Przywróć kształt i zapisz
    stego_img = flat_img.reshape(shape)
    Image.fromarray(stego_img).save(output_path)

def extract_message(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    flat_img = np.array(img).flatten()
    
    # Najpierw wyciągnij 30 bitów długości (10 grup po 7 kanałów = 70 kanałów)
    if len(flat_img) < 70:
        return ""
        
    bits = []
    
    # Odczytaj 10 grup, aby zdobyć długość
    for i in range(10):
        block_idx = i * 7
        block_lsb = flat_img[block_idx:block_idx+7] & 1
        s = calculate_syndrome(block_lsb)
        
        # Rozdziel syndrom na 3 bity (z powrotem)
        bits.extend([(s >> 2) & 1, (s >> 1) & 1, s & 1])
        
    # Odzyskaj długość w bajtach
    length = int("".join(str(b) for b in bits[:30]), 2)
    
    # Zabezpieczenie przed absurdanymi długościami z szumu
    max_bytes = (len(flat_img) // 7 * 3 - 30) // 8
    if length > max_bytes or length <= 0:
        return "<Nie znaleziono poprawnej długości wiadomości>"
        
    # Ile grup musimy jeszcze odczytać?
    bits_needed = length * 8
    groups_needed = (bits_needed + 2) // 3 # ceil(bits_needed / 3)
    
    # Zabezpieczenie rozmiaru
    if (10 + groups_needed) * 7 > len(flat_img):
        return "<Wskazana długość wykracza poza pojemność obrazu>"
        
    for i in range(10, 10 + groups_needed):
        block_idx = i * 7
        block_lsb = flat_img[block_idx:block_idx+7] & 1
        s = calculate_syndrome(block_lsb)
        bits.extend([(s >> 2) & 1, (s >> 1) & 1, s & 1])
        
    return bits_to_text(bits)
