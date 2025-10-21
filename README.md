Wybrane fragmenty raportu:

Raport - TRNG
Laboratorium Bezpieczeństwa Systemów Teleinformatycznych


Analiza źródła entropii:

Naszym źródłem entropii jest różnica czasu dostępu do danych w pamięci RAM między kolejnymi, takimi samymi działaniami z poziomu kodu języka wysokopoziomowego (C). Algorytm mierzy czas wykonania się działań zapisu wartości do zmiennych, a następnie porównuje je z poprzednim uzyskanym czasem. Wyniki zapisuje jako liczby całkowite, w tym ujemne - jako wynik odejmowania. Typowe uzyskane wartości próbek to: 0,-1,2,-4 itp.. 
Wybrana przez nas liczba próbek na jedno uruchomienie to 102400. W celu analizy źródła entropii, pobierane jest ostatnie 8 bitów każdej z zapisanych próbek.



Entropia wyliczona zgodnie ze wzorem: 𝑒 = − ∑𝑖 𝑝𝑖𝑙𝑜𝑔2(𝑝𝑖), dla powyższego
rozkładu wynosi 3,326 bita.



Metoda poprawy właściwości statystycznych - preprocessing

8-bitowe próbki zostały przycięte do 3 ostatnich bitów. W ten sposób pozbyliśmy się przeważającej liczby zerowych bitów w przypadku małych liczb. Takie 3-bitowe fragmenty zostały spakowane do paczki, z której następnie pobierano po 8 kolejnych bitów i zapisywano jako nowe liczby. Liczba wyników po preprocessingu zmniejszyła się do ⅜ początkowego rozmiaru. 



Uzyskana entropia po preprocessingu wynosi 7,091 bita


Metoda poprawy właściwości statystycznych - szyfrowanie

Aby jeszcze bardziej poprawić właściwości statystyczne, sięgnęliśmy po bibliotekę Cryptodome dla Python i szyfrowanie trybem ECB - Electronic Codebook.

Ten sposób szyfrowania danych wymaga podania 16-bitowego klucza. Minimalna ilość danych, jaką można zaszyfrować za jednym razem wynosi 16 bitów. Szyfrowanie ECB dzieli dane na bloki, a następnie szyfruje je jednakowym kluczem. Po zaszyfrowaniu, kod dla jednego bloku ma 128 bitów. Jeśli dwa bloki mają tę samą wartość, to zaszyfrowana wartość będzie również jednakowa. Ten brak działania na zasadzie kontekstu powoduje, że w przypadku utraty danych w wyniku transmisji, nadal można rozszyfrować pomyślnie przesłaną część. Wadą tego rozwiązania jest utrata bezpieczeństwa, która w tym aspekcie nie dotyczy naszych zastosowań. 

Aby zaszyfrować dane po preprocessingu, zostają one spakowane jako 8-bitowe ciągi zer i jedynek do pliku, a następnie są odczytywane jako 16-bitowe wyrazy typu “string”. W wyniku szyfrowania ECB w Cryptodome, z jednego 16-bitowego wyrazu przed szyfrowaniem, zostaje utworzony 128-bitowy wyraz zaszyfrowany. Następnie, ciągi zaszyfrowanych danych są konwertowane na ich binarną reprezentację i w taki sposób zapisywane do pliku.

W wyniku szyfrowania wyrazów o minimalnej długości, otrzymujemy dane o 8 razy większej objętości. Przemnażając to przez wydajność poprzedniego etapu, uzyskujemy ostatecznie 3 razy więcej bitów na wyjściu, niż w 8-bitowych kawałkach wartości próbek generatora szumu.

W celu analizy danych po zaszyfrowaniu, ciąg zer i jedynek został ponownie podzielony na 8-bitowe kawałki, które zapisywane są jako próbki.


Uzyskana entropia po szyfrowaniu wynosi 7,985 bita.




Przepływność bitowa rozwiązania

Napisany przez nas kod zawiera się w językach C oraz Python. Zbadaliśmy łączny czas wykonywania się kodów dla różnych rozmiarów wymaganych próbek początkowych do wygenerowania.
Kod w C jest odpowiedzialny za zbieranie danych i wydawanie surowych próbek z kolumny "Liczba próbek początkowych (źródło szumu)" do pliku.								
Natomiast kod w Python przetwarza próbki (zbiera ostatnie 3 bity próbek i łączy do paczek) oraz szyfruje je.

W wyniku testów, można zauważyć, że dla bardzo małych paczek z próbkami ostateczna przepływność bitowa jest bardzo niska. Optymalnym wyborem będzie generowanie paczek z co najmniej kilkudziesięcioma tysiącami liczb, aby entropia nie była niższa niż 7,97 bita, a przepływność była na stałym poziomie powyżej 0,9 MB/s.

Powyższe testy wykonano w środowisku serwerowym:

Procesor: Intel(R) Xeon(R) CPU E5-1650 v4 @ 3.60GHz
Pamięć RAM: Samsung M393A2K40BB1-CRC, DDR4, 2400 MHz.	



Dodatkowe uwagi

Zaproponowane przez nas rozwiązanie straci swoje właściwości statystyczne, jeśli zostanie odtworzone w systemach Windows. Częstotliwość taktowania systemowego zegara w systemach z rodziny Linux jest określona z dokładnością do jednej nanosekundy. Z kolei na Windows, wyniki pomiarów mogą być określane z dokładnością do jednej mikrosekundy. W efekcie, zamiast początkowych wyników podobnych do “0, 1, -1, 0, 231, -133, -3”, otrzymalibyśmy “0, 100, -100, 300, -200, -100”, co znacznie pogarsza różnorodność danych. 

Przepływność bitowa na pewno może zostać poprawiona na kilka sposobów:
- Implementacja całości lub części kodu Pythona w dalszym etapie programu napisanego C. Język C ma znaczącą przewagę w czasie wykonywania względem podobnych programów napisanych w Python. Dlatego, działania na bitach, takie jak wydobywanie 3 ostatnich bitów lub zapis wyrazów do pliku mogłyby zostać przeniesione między programami. Działanie biblioteki Cryptodome użytej do szyfrowania byłoby o wiele trudniejszym zadaniem w implementacji.
- Użycie mocniejszej jednostki obliczeniowej oraz szybszych pamięci RAM poza środowiskiem zwirtualizowanym, jakim jest serwer WWW. 
- Minimalizacja wykonanych operacji zapisu/odczytu do pliku oraz usunięcie fragmentów kodu odpowiedzialnego za przeprowadzenie pomiarów czasu wykonywania się programu.




