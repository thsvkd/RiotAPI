import json
import os
import requests

DEV_API_KEY = "RGAPI-fbde16b2-99f8-4fd8-8ff2-f12060291a7c"
base_url = "https://kr.api.riotgames.com/"
HEADER = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    # "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    # "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    # "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": DEV_API_KEY
}
json_path = "json/"


def ChamKey2Name(key):

    # LOL champions mapping data from github -> "https://github.com/ngryman/lol-champions"
    champions_data = open(json_path + "champions.json", 'rt', encoding='UTF8')
    champions_map = json.loads(champions_data.read())
    # print(champions_map)

    for item in champions_map:
        if key == int(item['key']):
            return item['id']


def SUMMONER_V4_by_name(summonerName):
    add_url = "lol/summoner/v4/summoners/by-name/"
    full_url = base_url + add_url + summonerName

    header = HEADER
    result = json.loads(requests.get(full_url, headers=header).text)
    print(result)
    return result['accountId']


def MATCH_V4_matchlists_by_account(encryptedAccountId):
    add_url = "lol/match/v4/matchlists/by-account/"
    full_url = base_url + add_url + encryptedAccountId

    header = HEADER
    result = json.loads(requests.get(full_url, headers=header).text)
    # print(result)
    return result['matches'][0]['gameId']

# 1607336238906 -> 1970년 1월 1일 1초로 부터 지난 ms
# 1607333376437
# 1607331169581
# 2206856


def MATCH_V4_matches_matchId(matchId):
    add_url = "lol/match/v4/matches/"
    full_url = base_url + add_url + str(matchId)

    header = HEADER
    result = json.loads(requests.get(full_url, headers=header).text)
    teams = result['teams']
    participants = result['participants']
    participantIdentities = result['participantIdentities']

    game_header = {
        "gameId": result['gameId'],
        "platformId": result['platformId'],
        "gameCreation": result['gameCreation'],
        "gameDuration": result['gameDuration'],
        "queueId": result['queueId'],
        "mapId": result['mapId'],
        "seasonId": result['seasonId'],
        "gameVersion": result['gameVersion'],
        "gameMode": result['gameMode'],
        "gameType": result['gameType']
    }

    # print("game_header")
    # print(game_header)
    # print("teams")
    # print(teams)
    # print("participants")
    # print(participants)
    # print("participantIdentities")
    # print(participantIdentities)
    # print("result")
    # print(result)
    f = open(json_path + "match_info.json", 'w')
    json.dump(result, f)
    f.close()


def MATCH_V4_timelines_by_match(matchId):
    add_url = "lol/match/v4/timelines/by-match/"
    full_url = base_url + add_url + str(matchId)

    header = HEADER
    result = json.loads(requests.get(full_url, headers=header).text)
    print(result)
    f = open(json_path + "in-game_info.json", 'w')
    json.dump(result, f)
    f.close()


if __name__ == "__main__":
    # print(ChamKey2Name(2))
    accountId = SUMMONER_V4_by_name("Hide on bush")
    # gameId = MATCH_V4_matchlists_by_account(accountId)
    # MATCH_V4_matches_matchId(gameId)
    # MATCH_V4_timelines_by_match(gameId)
