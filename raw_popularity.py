#!/usr/bin/python


def get_popular_songs():
    f = open('kaggle_visible_evaluation_triplets.txt', 'r')
    song_to_count = dict()
    for line in f:
        _, song, _ = line.strip().split('\t')
        if song in song_to_count:
            song_to_count[song] += 1
        else:
            song_to_count[song] = 1
    f.close()
    songs_ordered = sorted(song_to_count.keys(),
                           key=lambda s: song_to_count[s],
                           reverse=True)
    return songs_ordered


def get_user_listening_history():
    f = open('kaggle_visible_evaluation_triplets.txt', 'r')
    user_to_songs = dict()
    for line in f:
        user, song, _ = line.strip().split('\t')
        if user in user_to_songs:
            user_to_songs[user].add(song)
        else:
            user_to_songs[user] = set([song])
    f.close()
    return user_to_songs


def get_canonical_users():
    f = open('kaggle_users.txt', 'r')
    canonical_users = map(lambda line: line.strip(),
                          f.readlines())
    f.close()
    return canonical_users


def get_canonical_songs():
    f = open('kaggle_songs.txt', 'r')
    song_to_index = dict(map(lambda line:
                         line.strip().split(' '),
                         f.readlines()))
    f.close()
    return song_to_index


def create_submission():
    f = open('submission.txt', 'w')
    canonical_users = get_canonical_users()
    canonical_songs = get_canonical_songs()
    popular_songs = get_popular_songs()
    listening_history = get_user_listening_history()
    for user in canonical_users:
        songs_to_recommend = []
        for song in popular_songs:
            if len(songs_to_recommend) >= 500:
                break
            if not song in listening_history[user]:
                songs_to_recommend.append(song)
        indices = map(lambda s: canonical_songs[s],
                      songs_to_recommend)
        f.write(' '.join(indices) + '\n')
    f.close()

if __name__ == "__main__":
    create_submission()
