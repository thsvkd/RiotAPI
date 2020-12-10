import json
import os
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as animation
import numpy as np
import time

DEV_API_KEY = "RGAPI-f0013a9b-12da-4790-8f50-34f6d64ea418"
base_url = "https://kr.api.riotgames.com/"
HEADER = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    # "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    # "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    # "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": DEV_API_KEY
}
json_path = "json/"

data = []
data_index = 0

# y축에 표현할 값을 반환해야하고 scope 객체 선언 전 선언해야함.


def ChamKey2Name(key):

    # LOL champions mapping data from github -> "https://github.com/ngryman/lol-champions"
    champions_data = open(
        json_path + "champions.json", 'rt', encoding='UTF8')
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
    # print(result)
    return result['accountId']


def MATCH_V4_matchlists_by_account(encryptedAccountId):
    add_url = "lol/match/v4/matchlists/by-account/"
    full_url = base_url + add_url + encryptedAccountId

    header = HEADER
    result = json.loads(requests.get(full_url, headers=header).text)
    # print(result)
    return result['matches'][0]['gameId']


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
    json.dump(result, f, indent="\t")
    f.close()


def MATCH_V4_timelines_by_match(matchId):
    add_url = "lol/match/v4/timelines/by-match/"
    full_url = base_url + add_url + str(matchId)

    header = HEADER
    result = json.loads(requests.get(full_url, headers=header).text)
    print(result)
    f = open(json_path + "in-game_info.json", 'w')
    json.dump(result, f, indent="\t")
    f.close()


def DrawTrail():
    img = mpimg.imread("minimap.jpg")
    print(img)
    plt.axis(option='auto')
    plt.imshow(img)
    plt.show()


class Scope(object):

    # 초기 설정
    def __init__(self,
                 ax, fn,
                 xmax=10, ymax=10,
                 xstart=0, ystart=0,
                 title='Title', xlabel='X value', ylabel='Y value'):

        self.xmax = xmax
        self.xstart = xstart
        self.ymax = ymax
        self.ystart = ystart

        # 그래프 설정
        self.ax = ax
        self.ax.set_xlim((self.xstart, self.xmax))
        self.ax.set_ylim((self.ystart, self.ymax))
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

        self.x = [0]
        self.y = [0]
        self.value = 0
        self.fn = fn
        a = 0
        self.line, = ax.plot([], [], 'g')

        self.ti = time.time()
        print("초기화 완료")

    # 그래프 설정
    def update(self, item):

        tempo = time.time()-self.ti
        self.ti = time.time()

        # 값 넣기
        self.value = self.fn()
        self.y.append(self.value[1]/7)
        self.value = self.fn()
        self.x.append(self.value[0]/7)
        self.line.set_data(self.x, self.y)

        # 화면에 나타낼 x축 범위 업데이트
        # # 전체 x값중 반을 화면 옆으로 밀기
        if self.x[-1] >= self.xstart + self.xmax:
            self.xstart = self.xstart + self.xmax/2
            self.ax.set_xlim(self.xstart, self.xstart + self.xmax)

            self.ax.figure.canvas.draw()

        return (self.line, )


def insert_rand(scale):
    value = np.random.rand(1)
    return value[0]*scale


def insert_element():
    return data.pop(0)


def init_plt(insert_fn, xstart=0, xmax=10, ystart=0, ymax=10):
    fig, ax = plt.subplots()
    ax.grid(True)

    img = np.flipud(mpimg.imread("minimap.jpg"))

    scope = Scope(ax, insert_fn, xstart=xstart,
                  xmax=img.shape[1], ystart=ystart, ymax=img.shape[0])

    ani = animation.FuncAnimation(fig, scope.update, interval=500, blit=True)

    plt.imshow(img)
    plt.show()


if __name__ == "__main__":
    # print(ChamKey2Name(2))
    accountId = SUMMONER_V4_by_name("미북이")
    gameId = MATCH_V4_matchlists_by_account(accountId)
    # MATCH_V4_matches_matchId(gameId)
    MATCH_V4_timelines_by_match(gameId)
    # DrawTrail()

    f = open(json_path + "in-game_info.json", 'r')
    timeline = json.load(f)

    for item in timeline['frames']:

        player1 = item['participantFrames']['2']
        try:
            x = player1['position']['x']
            y = player1['position']['y']
            data.append([x, y])
        except KeyError:
            pass

    init_plt(insert_element, xstart=0, xmax=14000,
             ystart=0, ymax=14000)
