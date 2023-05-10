import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dir', '-d', dest='dir', type=str, help='El directorio donde buscar las canciones', required=True)
parser.add_argument('--recursive', '-r', dest='recursive', type=bool, default=False, help='Usar recursividad para buscar dentro de las carpetas de la misma carpeta')
parser.add_argument('--database', dest='database', type=str, default='database.db', help='Nombre de la Base de datos a usar para guardar los datos de la canciones')
parser.add_argument('--spotify_playlist_id', dest="spotify_playlist_id", required=True)
args = parser.parse_args()
