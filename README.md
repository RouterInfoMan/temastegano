# Tema Steganografie

Rulare:
docker build -t iap-tema2 .
docker run -p 8080:80 -it iap-tema2

Accesare web server:
http://localhost:8080

Utilizare:
Intrati pe /image/encode sau apasati pe "Encode" pentru a incarca o imagine
Dupa ce incarcati o imagine (asumand ca nu a aparut o eroare), o sa va apara imaginea codificata
Puteti sa descarcati imaginea fie apasand click dreapta, "Save Image As", sau apasati pe Download Last Encoded

Pentru decodificare, incarcati imaginea pe form-ul de pe /image/encode si dati submit. Va va aparea mesajul pe pagina

Pentru a obtine ultimul mesaj ca plain/text, dati Get Last Decoded
Pentru a obinte ultima imagine codificata, dati Download Last Encoded
