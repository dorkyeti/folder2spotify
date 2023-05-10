import os

import mutagen
import database
import spotify

_data = []


def file_get_info_or_none(file, attr):
    if (attr in file):
        return file[attr][0]
    else:
        return None


def get_file_info(file):
    fields = ['artist', 'album', 'title']

    return {
        field: file_get_info_or_none(file, field) for field in fields
    }


def init_everything(file_item):
    file_mutagen = mutagen.File(file_item, easy=True)

    if (file_mutagen is None):
        return None

    file_data = get_file_info(file_mutagen)
    file_data['path'] = file_item.path

    return file_data


def _should_pass_the_loop(item) -> bool:
    name = item.name

    if (item.is_dir()):
        return (name in ['Music'])
    elif (name.startswith('.')):
        return True
    elif (item.is_file() and (name.endswith('.mp3') or name.endswith('.m4a'))):
        return False


def remove_nulls_from_track(track):
    for key in track:
        if type(track[key]) is str:
            track[key] = track[key].replace("\0", "")
    return track


def _add_to_data_to_database(track):
    if (track is None):
        return

    track['spotify_id'] = None
    track['is_uploaded'] = 0

    track = remove_nulls_from_track(track)

    _data.append(track)


def walk_folders(dir: str):
    for item in os.scandir(dir):
        if (_should_pass_the_loop(item)):
            continue

        if (item.is_dir()):
            walk_folders(item.path)
        elif(item.is_file()):
            data = init_everything(item)

            _add_to_data_to_database(data)


def save_to_database():
    return database.insert_many('music', _data)


def find_tracks_spotify_id():
    total = 0
    response = database.select(
        "SELECT * FROM music WHERE spotify_id is NULL AND (title is not NULL AND artist is not NULL AND album is not NULL) ORDER BY title ASC")

    response_total = len(response)

    for track in response:
        result = spotify.search_track(track)

        if result is False:
            print('Intente de nuevo mas tarde')
            return
        elif result is not None:
            track['spotify_id'] = result['uri']
            database.update_one('music', track)
            total += 1
            print("{} de {} canciones".format(total, response_total))

    return total


def push_songs_to_playlist():
    list_of_ids = []
    ids = []
    response = database.select(
        "SELECT * FROM music WHERE spotify_id is NOT NULL ORDER BY title ASC")

    for id, track in enumerate(response):
        ids.append(track['spotify_id'])

        if ((id + 1) % 100 == 0):
            list_of_ids.append(ids)
            ids = []

    list_of_ids.append(ids)
    ids = []

    for id, items in enumerate(list_of_ids):
        spotify.push_tacks_to_playlist(items)
        print("Lista {} insertada en la playlist".format(id))

    print("listo")
