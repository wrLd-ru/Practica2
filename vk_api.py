import requests
import vk_api
import json
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp

# список одногруппников
USER_IDs1 = [165767945, 105865465] #139152940, 208680903, 371876190, 77944783, 553584556, 267864778,
            # 413053892, 190094644, 316943615, 643341439, 151384567, 374696066, 207338470, 305239541]
USER_IDs2 = []
USER_IDs3 = []

# как безопасно передать токен?????
ACCESS_TOKEN = "Your token???"


# получение друзей одногруппников
for USER_ID in USER_IDs1:
    try:
        r = requests.get("https://api.vk.com/method/friends.get", params={
            "user_id": USER_ID,
            "order": "name",
            "count": 10000,
            "offset": 0,
            "access_token": ACCESS_TOKEN,
            "v": 5.122
        }).json()["response"]["items"]
        USER_IDs2 += r
    except (RuntimeError, TypeError, NameError, KeyError):
        pass


if len(USER_IDs2):
    print("Общее количество друзей: ", len(USER_IDs2))
else:
	print('Ошибка:список пуст!')


g = nx.Graph() # создание пустого графа

# добавление узлов и дуг
All_Friends = USER_IDs1 + USER_IDs2  # + USER_IDs3
for i in All_Friends:
    try:
        r = requests.get("https://api.vk.com/method/friends.get", params={
            "user_id": i,
            "order": "name",
            "count": 10000,
            "offset": 0,
            "access_token": ACCESS_TOKEN,
            "v": 5.122
        }).json()["response"]["items"]
        for j in All_Friends:
            if j in r:
                g.add_edge(i, j)
    except (RuntimeError, TypeError, NameError, KeyError):
        pass

# Информация о графе + отрисовка графа
print(nx.info(g)) # граф с х узлами и y дугами
plt.figure(figsize=(15, 15))
nx.draw_networkx(g, with_labels=True)
plt.show()


# close centrality Вычисление центральности близости для узлов
print("Winner of closeness centrality:")
close_centrality = nx.closeness_centrality(g)
close_c = dict(sorted(close_centrality.items(), key=lambda item: item[1], reverse=True))
close_keys = list(close_c.keys())
for i in close_keys:
    if i in USER_IDs1:
        r = requests.get("https://api.vk.com/method/users.get", params={
            "user_id": i,
            "order": "name",
            "count": 10000,
            "offset": 0,
            "access_token": ACCESS_TOKEN,
            "v": 5.122
        }).json()["response"]
        print(r[0]["first_name"])
        print(r[0]["last_name"])
        break

# between centrality Вычисление центральности кратчайшего пути между узлами
print("Winner of betweenness centrality:")
bet_centrality = nx.betweenness_centrality(g, normalized=True,
                                           endpoints=False)
bet_c = dict(sorted(bet_centrality.items(), key=lambda item: item[1], reverse=True))
bet_keys = list(bet_c.keys())
for i in bet_keys:
    if i in USER_IDs1:
        r = requests.get("https://api.vk.com/method/users.get", params={
            "user_id": i,
            "order": "name",
            "count": 10000,
            "offset": 0,
            "access_token": ACCESS_TOKEN,
            "v": 5.122
        }).json()["response"]
        print(r[0]["first_name"])
        print(r[0]["last_name"])
        break

# vector centrality Вычисление центральности собственного вектора для графа G.
print("Winner of eigenvector centrality:")
pr = nx.pagerank(g, alpha=0.8)
pr_sorted = dict(sorted(pr.items(), key=lambda item: item[1], reverse=True))
pr_keys = list(pr_sorted.keys())
for i in pr_keys:
    if i in USER_IDs1:
        r = requests.get("https://api.vk.com/method/users.get", params={
            "user_id": i,
            "order": "name",
            "count": 10000,
            "offset": 0,
            "access_token": ACCESS_TOKEN,
            "v": 5.122
        }).json()["response"]
        print(r[0]["first_name"])
        print(r[0]["last_name"])
        break
