<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>
    <main>
        <?php
            exec('/var/www/instaqram.pl/trng_source_generator');
            exec('cd /var/www/instaqram.pl/; python3 trng_encryptor.py');
            $filename = 'final_trn.txt';
            $lines = file($filename); // wczytaj zawartość pliku do tablicy

            foreach ($lines as $line) {
                echo $line . "<br>"; // wyświetl każdą linie w oddzielnej linii HTML
            }
        ?>
    </main>
</body>
</html>
