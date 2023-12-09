# Calminaro Simple Video Editor

Semplice programma per automatizzare task ricorrenti.



# Installazione

`git clone https://github.com/calminaro/common_video_editor`

Richiede [ffmpeg](https://ffmpeg.org/) installato nel sistema.

Su Linux: `sudo apt install ffmpeg` o altro package manager

Su Windows: `winget install ffmpeg`

Installare le dipendenze: `pip install -r requirements.txt`

---

# Funzioni disponibili

`python3 simple_editor.py`

```textile
Simple Video Editor

[?] File Path?: /path/to/file/input.mp4
[?] What do you want to do?: change video codec to h264
   extract multiple photo from a video
   make a simple start-end cut
 > change video codec to h264
   quit

[?] Inserisci il nome del file output: output.mp4

Sto esportando...
```
