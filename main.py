import os
import json
import get_stationIDs


def main():
    if not os.path.exists(get_stationIDs.ACTIVESTATIONS):
        print("初始化測站清單，請稍候...")
        latest_data = get_stationIDs.get_active_stations()
        get_stationIDs.save_to_json(latest_data)

    with open(get_stationIDs.ACTIVESTATIONS, 'r', encoding='utf-8') as f:
        stations_dict = json.load(f)

    user_input = input("請輸入測站名稱或站號: ").strip()

    if get_stationIDs.check_station(user_input, stations_dict):
        print(f"驗證成功：'{user_input}' 是一個有效的測站。")
    else:
        print(f"驗證失敗：找不到 '{user_input}'，請檢查輸入是否正確。")


if __name__ == '__main__':
    main()
