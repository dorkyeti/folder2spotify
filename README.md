# Folder2Spotify

Es un script hecho en python para poder pasar algunas canciones que tenia en mi telefono a una playlist de spotify

---

## ¿Como usarlo? 🤷🏻‍♂️

1. Clona este proyecto
2. Corre

```bash
pip install -r ./requirements.txt
```

3. Renombra el archivo `.env.template` a `.env`
4. Agrega tus credenciales de spotify en el archivo `.env` de esta forma (debes crear una [app dentro de spotify](https://developer.spotify.com/) y poner las credenciales en el `.env`)

```
SPOTIFY_CLIENT_ID=abc123
SPOTIFY_CLIENT_SECRET=abc123
```

5. Corre el comando

```bash
python ./main.py --dir={La direcion a la carpeta donde estén las canciones} --spotify_playlist_id={el id de la playlist de spotify donde se subiran las canciones}
```
