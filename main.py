from argsparse import args
from helpers import walk_folders, save_to_database, find_tracks_spotify_id, push_songs_to_playlist

print('Iniciando...')
walk_folders(args.dir)
print('Listo!')
print('Registrando en la base de datos')
rows = save_to_database()
print('{} Canciones registradas en la base de datos'.format(rows))
total = find_tracks_spotify_id()
print('{} Canciones encontradas en spotify'.format(total))
push_songs_to_playlist()
