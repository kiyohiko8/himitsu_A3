
"""
###プログラム概要
- 手法Aの改良版
- 収集したデータより入力データと教師データを作成
"""
#collected himitsu-data by google form 
import os, csv
import random
import himitsu_data_gd_5
import pandas as pd
import numpy as np
import collected_himitsu_sort
import re


##訓練データの作成
#all_word_list 全ひみつ道具データ
#collected     収集されたひみつ道具の既知情報データ
#sorted        全ひみつ道具が認知度の低い順にソートされたデータ
def mk_x_train(all_word_list, collected, sorted):
	
	#ユーザ毎のデータをまとめた全データ
	x_train = []
	
	##学習時入力用データの作成
	#items:集められたデータのうちの１ユーザ分
	for items in collected:
		x_data = np.zeros(271, int)
		cnt = 0
		for x in sorted:
			#知っている単語が3つになるまで抽出(2018/1/12変更)
			if cnt < 3:
				if x[1] in items:
					for i, word in enumerate(all_word_list):
						if word == x[1]:
							x_data[i] = 1
							cnt += 1	
						else:
							continue
				else:
					continue
			else:
				break

		x_train.append(x_data)
					
					
	return x_train


	
	
#教師データの作成
def mk_y_train(all_word_list, collected):
	y_train = []
	for know_list in collected:
		y_data = []
		#itemがknow_listにあれば1を追加する
		for item in all_word_list:
			if item in know_list:
				y_data.append(int(1))
			else:
				y_data.append(int(0))
			
		for i in range(1):
			y_train.append(y_data)
			
	y_train = np.array(y_train)
				
	return y_train



#csvを読み込んでデータ作成	
def read_csv(csv_data):
	collected = []
	# ファイルを読み込みモードでオープン
	with open(csv_data, 'r', encoding = "shift-jis") as f:
		# 行ごとのリストを処理する
		for row in f:
			row = row.rstrip()
			row = row.replace('\"', '')
			row = row.replace(' ', '')
			row = row.replace('インスタントミニュチュア製造カメラ', 'インスタントミニチュア製造カメラ')
			row = row.replace('かならず実現するメモ帳', 'かならず実現する予定メモ帳')
			row = row.replace('穴掘り機', '穴ほり機')
			row = row.replace('重量ペンキ', '重力ペンキ')
			row = row.replace('流行性ネコジャラシビールス', '流行性ネコシャクシビールス')
			row = row.replace('コンピュータペンシル', 'コンピューターペンシル')
			for i in range(101):
				row = row.replace(str(i), '')
			#line = row.split(",")
			line = [i for i in re.split(r',', row) if i != ""]
			collected.append(line)
			
			
	return collected




if __name__ == "__main__":

	collected = read_csv("himitsu_data2.csv")
	print(collected)
	
	himitsu  = himitsu_data_gd_5.mk_allword_list()
	word_vec = himitsu_data_gd_5.mk_vec(himitsu)
	sorted   = collected_himitsu_sort.count_sort(collected, himitsu)
	
	x_train  = mk_x_train(himitsu, collected, sorted)
	y_train  = mk_y_train(himitsu, collected)
	
	print("[")
	for item in collected:
		print(item)
	print("]")
	
	print("[")
	for item in x_train:
		print(item)
	print("]\n")
	print("[")
	for i in y_train:
		print(i)
	print("]")
	print("len of x_train:", len(x_train))
	print("len of y_train:", len(y_train))
	print("len of correct lavel:",len(y_train[0]))
	
	
	
	
