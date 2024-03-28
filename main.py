import requests
# example api call https://osu.ppy.sh/users/18453878/beatmapsets/most_played?limit=51&offset=5

def download_single_beatmap(beatmap_id, song_title):
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"}
    response: requests.Response = requests.get(f"https://api.chimu.moe/v1/download/{beatmap_id}?n=1", allow_redirects=True)

    open(f"{beatmap_id} - {song_title}.osz", "wb").write(response.content)
    pass

def download_beatmaps(beatmaps: list[dict]):
    progress = 0 
    for beatmap in beatmaps:
        beatmapset_id = beatmap["beatmap"]["beatmapset_id"] 
        song_title = beatmap["beatmapset"]["title"]
        print(f"Downloading {beatmapset_id} - {song_title}.") 
        download_single_beatmap(beatmapset_id, song_title)
        progress += 100/len(beatmaps)
        print(f"Progress: {progress}%")
        pass


def retrieve_most_played_beatmaps(user_id:str, limit:int) -> list[dict]:
    '''
    user_id = Osu! User ID \n
    limit = number of entries 
    '''
    beatmaps: list[dict] = [] 

    for offset in range(0, limit, 10):
        response: requests.Response = requests.get(url=f"https://osu.ppy.sh/users/{user_id}/beatmapsets/most_played?limit=10&offset={offset}")
        if response.status_code != 200:
            print(f"encountered status code: {response.status_code}")
        beatmaps.extend(response.json())

    return beatmaps 

def main():
    beatmaps = retrieve_most_played_beatmaps("18453878", 10)
    download_beatmaps(beatmaps=beatmaps)

if __name__ == "__main__":
    main()