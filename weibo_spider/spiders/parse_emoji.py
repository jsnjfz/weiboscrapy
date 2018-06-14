# -*- coding: utf-8 -*-
import json
import io

#配置成你自己的路径
def load_emoji_map(fn = 'C:\Users\Administrator\Desktop\weiboscrapy\weibo_spider\spiders\emoji_ios6.json'):
    data_file = io.open(fn, "r", encoding='utf-8')
    json_data = json.load(data_file)
    sb_dict = {}
    for m in json_data:
        sb_dict[m['sb'].lower()]=m['utf8']
	return sb_dict


def softband_to_utf8(emoji):
    hex_emoji = sb_dict.get(emoji.lower(), '')
    if hex_emoji:
        return bytes.fromhex(hex_emoji).decode('utf-8')
    else:
        return '' 

sb_dict = load_emoji_map()

