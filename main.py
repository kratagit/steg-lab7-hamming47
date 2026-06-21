import numpy as np
from PIL import Image
import stego_hamming
import os
import sys

# Ustawienie kodowania na UTF-8 dla Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def generate_clean_image(width=512, height=512, output_path='clean_image.png'):
    # Generowanie zaszumionego gradientu, by obraz nie był idealnie gładki
    y, x = np.mgrid[0:height, 0:width]
    
    # Przejście tonalne
    r = (x / width * 255).astype(np.float32)
    g = (y / height * 255).astype(np.float32)
    b = ((x + y) / (width + height) * 255).astype(np.float32)
    
    # Dodanie szumu Gaussa (odchylenie 15)
    noise_r = np.random.normal(0, 15, (height, width))
    noise_g = np.random.normal(0, 15, (height, width))
    noise_b = np.random.normal(0, 15, (height, width))
    
    r = np.clip(r + noise_r, 0, 255).astype(np.uint8)
    g = np.clip(g + noise_g, 0, 255).astype(np.uint8)
    b = np.clip(b + noise_b, 0, 255).astype(np.uint8)
    
    img_array = np.stack((r, g, b), axis=-1)
    Image.fromarray(img_array).save(output_path)

def main():
    np.random.seed(42)
    
    print("=== Laboratorium 7: Steganografia Hamming(7,4) ===")
    
    # 1. Wygenerowanie obrazu
    print("\n--- Inicjalizacja ---")
    generate_clean_image(512, 512, 'clean_image.png')
    print("Wygenerowano 'clean_image.png' (512x512 RGB).")
    
    # 2. Scenariusz 1: Krótka wiadomość
    print("\n--- Przypadek testowy 1: Krótka wiadomość ---")
    short_msg = "Hello World"
    print(f"Wiadomość do ukrycia: '{short_msg}'")
    stego_hamming.hide_message('clean_image.png', short_msg, 'stego_test1.png')
    extracted_short = stego_hamming.extract_message('stego_test1.png')
    print(f"Odczytana wiadomość : '{extracted_short}'")
    if short_msg == extracted_short:
        print("[SUKCES] Odczyt zgadza się w 100%.")
    else:
        print("[BŁĄD] Odczyt jest niepoprawny.")
        
    # 3. Scenariusz 2: Długa wiadomość (znaczna część pojemności)
    print("\n--- Przypadek testowy 2: Długa wiadomość ---")
    base_text = "To jest dluga wiadomosc sluzaca do testowania pojemnosci. "
    long_msg = base_text * 250 # około 15 KB
    print(f"Długość wiadomości do ukrycia: {len(long_msg)} znaków.")
    stego_hamming.hide_message('clean_image.png', long_msg, 'stego_test2.png')
    extracted_long = stego_hamming.extract_message('stego_test2.png')
    print(f"Długość odczytanej wiadomości: {len(extracted_long)} znaków.")
    if long_msg == extracted_long:
        print("[SUKCES] Cała wiadomość została odzyskana poprawnie.")
    else:
        print("[BŁĄD] Wystąpiły różnice w długim tekście.")

    # 4. Scenariusz 3: Zapis jako PNG i odczyt
    print("\n--- Przypadek testowy 3: Zapis w formacie PNG i odczyt ---")
    png_msg = "Wiadomosc testujaca format PNG (bezstratny)."
    stego_hamming.hide_message('clean_image.png', png_msg, 'stego_test3.png')
    print("Zapisano specjalny obraz jako 'stego_test3.png'.")
    extracted_png = stego_hamming.extract_message('stego_test3.png')
    if png_msg == extracted_png:
        print("[SUKCES] Odczytano poprawnie z formatu PNG. Kompresja bezstratna zachowuje modyfikacje LSB.")
    else:
        print("[BŁĄD] Odczyt z formatu PNG nie powiódł się.")
        
    # 5. Scenariusz 4: Kompresja JPEG
    print("\n--- Przypadek testowy 4: Zapis w formacie JPEG (90% Quality) ---")
    img_test4 = Image.open('stego_test1.png')
    img_test4.convert('RGB').save('stego_test4.jpg', 'JPEG', quality=90)
    print("Zapisano 'stego_test1.png' jako 'stego_test4.jpg' (Quality=90).")
    
    extracted_jpeg = stego_hamming.extract_message('stego_test4.jpg')
    print("Próba odzyskania danych z JPEG:")
    disp_jpeg = extracted_jpeg[:60].replace('\n', ' ')
    print(f"Odczyt z JPEG: '{disp_jpeg}'")
    
    if extracted_jpeg == short_msg:
        print("[NIEOCZEKIWANY SUKCES] Odzyskano pomimo kompresji JPEG.")
    else:
        print("[OCZEKIWANY BŁĄD] Kompresja stratna JPEG bezpowrotnie zniszczyła strukturę LSB.")

if __name__ == "__main__":
    main()
