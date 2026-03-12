import requests

from datetime import datetime

now = datetime.now()

date=now.date()

url='http://rihou.cc:567/gggg.nzk/'

res=requests.get(url)

txt_nontime = res.text

first=txt_nontime.splitlines()[1].split(',')[1]

print(first)

txt=f'更新时间{date},#genre#\n{date},{first}\n'+txt_nontime

def rihou_playlist_m3u(url=url, output="playlist.m3u"):

    #print(res)



    #print(txt)

    with open(f'rihou{date}.txt', 'w', encoding='utf-8')as f1:

        f1.write(txt)
    with open('rihou.txt', 'w', encoding='utf-8')as f3:

        f3.write(txt)

   



    # 转换并保存

    with open(f'rihou{date}.m3u', 'w', encoding='utf-8') as f2:

        f2.write("#EXTM3U\n")

        group = ""

        for line in txt.splitlines():

            line = line.strip()

            if line.endswith(",#genre#"):

                group = line.split(",")[0]

                #headline=

                #print(group)

            elif line and "," in line and not line.endswith("#genre#"):

                name, url = line.split(",", 1)

                group_part = f' group-title="{group}"' if group else ''

                f2.write(f'#EXTINF:-1 tvg-name="{name}"{group_part},{name}\n{url}\n')

    with open('rihou.m3u', 'w', encoding='utf-8') as f4:

         f4.write(f'#EXTM3U\n#EXTINF:-1 tvg-name="{name}"{group_part},{name}\n{url}\n')

    

    print(f"✓ 完成: {output}")





# 立即执行

rihou_playlist_m3u()

