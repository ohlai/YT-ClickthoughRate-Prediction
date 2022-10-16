import csv
import pandas

def check_data_loss():
    list2 = pandas.read_csv('channelData.csv')
    list1 = pandas.read_csv('correcteddata.csv')
    print(list(set(list2).difference(list1)))

def remove_duplicates():
    videosdata = pandas.read_csv('channelData.csv')
    print(videosdata.iloc[1]['ThumbnailURL'])

    seen = []
    result = []
    dups =0
    for itemnum in videosdata.index:
        if itemnum != 0:
            print(itemnum)
            if videosdata.iloc[itemnum]["ThumbnailURL"] not in seen:
                result.append(videosdata.iloc[itemnum])
                seen.append(videosdata.iloc[itemnum]['ThumbnailURL'])
            else:
                dups +=1

    print(f"num of duplicates: f{dups}")

    with open("correcteddata.csv", 'a', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result)

def create_zscores():
    videosdata = pandas.read_csv('channelData.csv')
    print(videosdata)

    for r in videosdata.index:
        curChannel = str(videosdata.iloc[r]['ChannelID'])
        surrounding = []
        a=0
        for v in range(8):
            surrounding.append(videosdata.iloc[r+a])
            a+=1
        a=7
        for i in range(7):
            surrounding.append(videosdata.iloc[r-a])
            a-=1
        
        print(surrounding)
        balls = 0
        for i in surrounding:
            aaa=str(i['ChannelID'])
            if  aaa!= curChannel: # if channel not the same
                surrounding.pop(balls)
            balls+=1

        print(surrounding)

