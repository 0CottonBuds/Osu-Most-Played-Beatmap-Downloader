import requests
import time

def download_single_beatmap(beatmap_id, song_title):
    '''downloads single beatmap by beatmap id and song title'''
    
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"}
    response: requests.Response = requests.get(f"https://api.nerinyan.moe/d/{beatmap_id}?noVideo=true", allow_redirects=True)

    if not response.status_code == 200:
        print(f"API ERROR:{response.status_code} \nFailed to download {beatmap_id}, {song_title}." )
        return False 
    
    try:
        with open(f"./Downloads/{beatmap_id} - {song_title}.osz", "wb") as file:
                file.write(response.content)
        return True
    except:
        print(f"Error while downloading {beatmap_id}, {song_title}!" )
        return False

def download_beatmaps(beatmaps: list[dict]):
    '''
    Tries to download list of beatmaps(JSON from osu! API call)\n
    Creates a txt file containing all failed downloads
    '''
    
    progress = 0 
    failed_downloads = []

    try:
        for beatmap in beatmaps:
            beatmapset_id = beatmap["beatmap"]["beatmapset_id"] 
            song_title = beatmap["beatmapset"]["title"]
            print(f"Downloading {beatmapset_id} - {song_title}.") 

            isSuccess: bool = download_single_beatmap(beatmapset_id, song_title)
            if isSuccess: # success
                progress += 100/len(beatmaps)
                print(f"Progress: {progress}%")
            else:
                failed_downloads.append(beatmapset_id)
    except:
        print(f"Unexpected error occurred! \nSome beatmaps may not be downloaded. see failed_downloads.txt for list of beatmap id of failed downloads.")
        with open("failed_downloads.txt", "wb") as failed_downloads_txt:
            for failed_download in failed_downloads:
                failed_downloads_txt.write(failed_download)
            failed_downloads_txt.flush()
        return

    print("Finished downloading all beatmaps. Some beatmaps may not be downloaded. see failed_downloads.txt for list of beatmap id of failed downloads")
    with open("failed_downloads.txt", "wb") as failed_downloads_txt:
        for failed_download in failed_downloads:
            failed_downloads_txt.write(failed_download)
        failed_downloads_txt.flush()

def retrieve_most_played_beatmaps(user_id:str, limit:int, offs:int = 0, step:int = 10, sleep:float = 2.0) -> list[dict]:
    '''
    Retrieves most played beatmaps with following parameters\n
    \n
    user_id = Osu! User ID \n
    limit = number of most played beatmaps to be downloaded \n
    offs (default 0) = offset from the start of list \n
    step (default 10, max 40) = number of beatmaps per API call\n
    sleep (default 2.0) = sleep time per API call. NOTE: you might be ip blocked by osu\n 
    if you send too much requests at a single time so set this value too low.\n
    '''

    beatmaps: list[dict] = [] 

    for offset in range(offs , limit, step):
        try:
            response: requests.Response = requests.get(url=f"https://osu.ppy.sh/users/{user_id}/beatmapsets/most_played?limit={step}&offset={offset}")

            if response.status_code != 200:
                print(f"encountered status code: {response.status_code}")
                continue

            print(response.json())
            beatmaps.extend(response.json())

            time.sleep(sleep)
            
        except:
            print(f"Error encountered at beatmaps {offset} - {offset + 10}")
            print(f"Returning {len(beatmaps)}")
            return beatmaps

    return beatmaps

def check_if_user_exists(userID):
    print("Checking if user exists")
    response = requests.get(url=f"https://osu.ppy.sh/users/{userID}")

    if response.status_code != 200:
        print(f"There is no user with id of: {userID}")
        print("Exiting...")
        exit()


# main 
if __name__ == "__main__":
    print(
"""
Welcome to osu! most played beatmap downloader. 
As the name suggest this downloads your most played beatmaps using your user id.
To start please answer the prompts 
"""
        )

    print("User ID can be obtained trough osu! website")
    user_id = int(input("Enter your user ID: "))
    check_if_user_exists(user_id)

    print("How many beatmaps would you like to download (number)")
    limit = int(input("qty: "))
    print("Where would you want to start downloading (1 if you want to skip the first beatmap)")
    offset = int(input("Offset: "))


    beatmaps = retrieve_most_played_beatmaps(user_id, limit, offset)
    download_beatmaps(beatmaps)

