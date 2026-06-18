# steg-lab7-hamming47

# Laboratorium 7

### Instructions

## Implementacja steganografii z wykorzystaniem kodu Hamminga (7,4)

### Cel zadania
Celem zadania jest implementacja algorytmu steganograficznego wykorzystującego kodowanie syndromami z użyciem kodu Hamminga (7,4) do ukrywania informacji w obrazach cyfrowych.

### Opis zadania
Zaimplementuj system steganograficzny, który będzie ukrywał wiadomość w obrazie cyfrowym przy użyciu kodu Hamminga (7,4). System powinien składać się z dwóch głównych funkcji:
1. Funkcja ukrywająca wiadomość w obrazie
2. Funkcja ekstrahująca ukrytą wiadomość z obrazu

### Wymagania implementacyjne
1. Użyj języka Python lub MATLAB do implementacji.
2. Wykorzystaj biblioteki do przetwarzania obrazów (np. PIL dla Pythona lub wbudowane funkcje MATLABa).
3. Zaimplementuj kod Hamminga (7,4) do kodowania syndromami.
4. Ukryj wiadomość w najmniej znaczących bitach (LSB) pikseli obrazu.
5. Zapewnij możliwość ukrywania wiadomości tekstowych.

### Wskazówki implementacyjne
1. **Ukrywanie wiadomości:**
   * Konwertuj wiadomość tekstową na ciąg bitów.
   * Podziel ciąg bitów na grupy po 3 bity (k=3 dla kodu Hamminga (7,4)).
   * Dla każdej grupy 3 bitów, oblicz odpowiedni syndrom używając macierzy H.
   * Ukryj syndrom w LSB pikseli obrazu.
2. **Ekstrakcja wiadomości:**
   * Odczytaj syndromy z LSB pikseli obrazu.
   * Użyj tablicy liderów warstw do znalezienia oryginalnych 3 bitów wiadomości dla każdego syndromu.
   * Połącz odzyskane bity w pełną wiadomość i przekonwertuj na tekst.

### Kryteria akceptacji
1. System poprawnie ukrywa i odzyskuje wiadomości tekstowe o różnych długościach.
2. Zmiany w obrazie są niewidoczne gołym okiem.

### Przypadki testowe
1. Ukryj krótką wiadomość (np. "Hello World") w obrazie i odzyskaj ją.
2. Ukryj dłuższą wiadomość, wykorzystującą znaczną część pojemności obrazu.
3. Ukryj wiadomość, zapisz obraz w formacie PNG, a następnie odczytaj wiadomość.
4. Ukryj wiadomość, zapisz obraz w formacie JPEG z wysoką jakością (np. 90%), a następnie spróbuj odczytać wiadomość.
