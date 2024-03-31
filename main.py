import requests

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

    if response.status_code == 200:
        with open(f"{beatmap_id} - {song_title}.osz", "wb") as osx:
            osx.write(response.content)
        return response.status_code
    else:
        print(f"Failed to download {beatmap_id}, {song_title}" )
        return beatmap_id 

def download_beatmaps(beatmaps: list[dict]):
    progress = 0 
    failed_downloads = []
    try:
        for beatmap in beatmaps:
            beatmapset_id = beatmap["beatmap"]["beatmapset_id"] 
            song_title = beatmap["beatmapset"]["title"]
            print(f"Downloading {beatmapset_id} - {song_title}.") 
            is_success = download_single_beatmap(beatmapset_id, song_title)
            if is_success == 0:
                progress += 100/len(beatmaps)
                print(f"Progress: {progress}%")
            else:
                failed_downloads.append(is_success)
    except:
        print(f"Error downloading beatmaps")
    finally:
        with open("failed_downloads1.txt", "wb") as failed_downloads_txt:
            for failed_download in failed_downloads:
                failed_downloads_txt.write(failed_download)
            failed_downloads_txt.flush()

def retrieve_most_played_beatmaps(user_id:str, limit:int, offs:int = 0) -> list[dict]:
    '''
    user_id = Osu! User ID \n
    limit = number of entries 
    '''
    beatmaps: list[dict] = [] 
    offset = offs

    for offset in range(offs , limit, 10):
        try:
            response: requests.Response = requests.get(url=f"https://osu.ppy.sh/users/{user_id}/beatmapsets/most_played?limit=10&offset={offset}")
            if response.status_code != 200:
                print(f"encountered status code: {response.status_code}")
                continue
            beatmaps.extend(response.json())
            download_beatmaps(response.json())
        except:
            print(f"Error encountered at beatmaps {offset} - {offset + 10}")

def main():
     retrieve_most_played_beatmaps("18453878", 1037, 12)

if __name__ == "__main__":
    main()