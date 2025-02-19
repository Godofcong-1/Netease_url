import os
import certifi
import requests
import urllib3

# 设置环境变量，指定证书文件的路径，避免 FileNotFoundError
os.environ["SSL_CERT_FILE"] = certifi.where()

# 忽略 InsecureRequestWarning 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_song_urls_from_playlist(playlist_id):
    limit = 10
    offset = 0  # 初始 offset 为 0，得到第1-10首歌曲
    all_ids = []
    while True:
        detail_url = f"https://netease-cloud-music-api.vercel.app/playlist/track/all?id={playlist_id}&limit={limit}&offset={offset}"
        # 添加 verify=False 防止 SSL 错误
        detail_resp = requests.get(detail_url, verify=False).json()
        songs = detail_resp.get("songs", [])
        # 如果没有歌曲了，就退出循环
        if not songs:
            print("获取歌曲失败")
            break
        # 如果歌曲数量小于 limit，则按实际数量获取，然后增加对应数量的 offset
        if len(songs) < limit:
            # 用 list 的 extend() 替换 update()
            all_ids.extend([song["id"] for song in songs])
            offset += limit - len(songs)
        # 否则，直接获取 limit 首歌曲，offset 增加 limit
        else:
            # 用 list 的 extend() 替换 update()
            all_ids.extend([song["id"] for song in songs])
            offset += 10
        print(f"已获取 {len(all_ids)} 首歌曲（含重复）")
        with open("song_ids.txt", "w") as f:
            for sid in all_ids:
                f.write(str(sid) + "\n")
    return all_ids

def remove_duplicate_lines(input_file, output_file):
    seen = set()
    unique_lines = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
    with open(output_file, 'w') as f:
        for line in unique_lines:
            f.write(line + "\n")
    return unique_lines

if __name__ == "__main__":
    pid = input("请输入歌单ID (默认 000000000): ") or "000000000"
    all_ids = get_song_urls_from_playlist(pid)
    unique_lines = remove_duplicate_lines("song_ids.txt", "song_ids.txt")
    print("获取歌曲ID完成！去重后共", len(unique_lines), "首歌曲")
    print("歌曲ID已保存到 song_ids.txt 文件中")
