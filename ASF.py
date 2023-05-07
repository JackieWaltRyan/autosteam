from datetime import datetime, timedelta
from json import loads, dump
from os import system
from time import sleep
from traceback import format_exc

from requests import get

DEL, ADD = 0, 0

if __name__ == "__main__":
    while True:
        system("cls||clear")
        try:
            del_all, add_all = 1, 1
            with open(file="ASF/config/Jackie Ryan.json",
                      mode="r",
                      encoding="UTF-8") as input_json_file:
                data = loads(s=str(input_json_file.read()))
                games = loads(s=get(url="http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key="
                                        "&steamid=76561198277342930&include_played_free_games=true&s"
                                        "kip_unvetted_apps=false").text)["response"]["games"]
                times, times_keys = [], {}
                for game in games:
                    if game["appid"] in data["GamesPlayedWhileIdle"] and game["playtime_forever"] >= 60000:
                        data["GamesPlayedWhileIdle"].remove(game["appid"])
                        print(f"Удалено {del_all}: {game['appid']}")
                        del_all += 1
                        DEL += 1
                    if game["appid"] not in data["GamesPlayedWhileIdle"] and game["playtime_forever"] < 60000:
                        times.append(game["playtime_forever"])
                        times_keys.update({game["playtime_forever"]: game["appid"]})
                times.sort(reverse=True)
                while len(data["GamesPlayedWhileIdle"]) < 32:
                    data["GamesPlayedWhileIdle"].append(times_keys[times[0]])
                    print(f"Добавлено {add_all}: {times_keys[times[0]]}")
                    add_all += 1
                    ADD += 1
                    times.pop(0)
                if del_all > 1 or add_all > 1:
                    with open(file="ASF/config/Jackie Ryan.json",
                              mode="w") as output_json_file:
                        dump(obj=data,
                             fp=output_json_file)
                    print("\n")
        except Exception:
            print(format_exc())
        print(f"{'-' * 45}\n"
              f"Всего удалено: {DEL}, Всего добавлено: {ADD}\n\n"
              f"{'-' * 45}\n"
              f"Ждем один час. Следующая проверка: {(datetime.now() + timedelta(hours=1)).strftime('%H:%M:%S')}")
        sleep(3600)
