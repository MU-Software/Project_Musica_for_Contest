#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright 2016 MU Software(@MUsoftware on twitter), All Rights Reserved.
#Musica Basic Score Server - DB Control module

import sqlite3, json, string, random, time, operator
musica_db_file	= sqlite3.connect("musica.db")
musica_db  = musica_db_file.cursor()

def randomID(size=6, chars=string.ascii_uppercase + string.digits):
	return 'A{0}'.format(''.join(random.choice(chars) for _ in range(size)))

#DB side
class DB_control(object):
	def __init__(self):
		pass
	def setupDB(self):
		#CAUTION - This function resets all DB.
		try:
			musica_db.execute("DROP TABLE IF EXISTS user")
			musica_db_file.commit()
			userDB_setupDB_str	 = "NUM			INTEGER PRIMARY KEY AUTOINCREMENT, "
			userDB_setupDB_str	+= "CARD_ID		TEXT NOT NULL UNIQUE, "
			userDB_setupDB_str	+= "NAME		TEXT NOT NULL UNIQUE, "
			userDB_setupDB_str	+= "PASSWORD	TEXT NOT NULL, "
			userDB_setupDB_str	+= "ADMIN		INT	 NOT NULL DEFAULT 0"
			
			musica_db.execute("DROP TABLE IF EXISTS song")
			musica_db_file.commit()
			songDB_setupDB_str	 = "NUM			INTEGER PRIMARY KEY AUTOINCREMENT, "
			songDB_setupDB_str	+= "SONG_ID		INT	 NOT NULL UNIQUE, "
			songDB_setupDB_str	+= "NAME		TEXT NOT NULL UNIQUE, "
			songDB_setupDB_str	+= "FINGERPRINT TEXT NOT NULL UNIQUE"
			
			musica_db.execute("DROP TABLE IF EXISTS score")
			musica_db_file.commit()
			scoreDB_setupDB_str	 = "USER_ID		TEXT NOT NULL UNIQUE"
			
			musica_db.execute('CREATE TABLE user({0}) '.format(userDB_setupDB_str))
			musica_db.execute('CREATE TABLE song({0}) '.format(songDB_setupDB_str))
			musica_db.execute('CREATE TABLE score({0})'.format(scoreDB_setupDB_str))
			musica_db_file.commit()
			
			self.add_user(randomID(), 'MU_Admin', 'yj809042', admin=True) #Create admin account.
			self.add_song(randomID(), 'Tutorial', randomID()) #Create tutorial(dummy) song
			print("DB setuped.")
		except:
			print("Error raised while setuping DB")
			raise
	def add_user(self, cardID, name, password, admin=False):
		try:
			musica_db.execute("INSERT INTO user VALUES(null, ?, ?, ?, 0)",(cardID, name, password))
			if admin:
				musica_db.execute("UPDATE user SET ADMIN = 1 WHERE CARD_ID = ?",(cardID,))
			musica_db.execute("INSERT INTO score(USER_ID) VALUES(?)",(cardID,))
			musica_db_file.commit()
			if admin:
				print("Admin account(ID: {0}, name: {1}) created.".format(cardID, name))
			else:
				print("User {0}(ID: {1}) created.".format(name, cardID))
		except:
			print("Error raised while adding User ID {0}. Rolling back DB...".format(cardID))
			self.rollback_DB()
	def del_user(self, cardID, password):
		try:
			user_info = musica_db.execute("SELECT * FROM user WHERE CARD_ID = ?",(cardID,)).fetchall()
			admin_bool = True if user_info[0][4] is 1 else False
			user_password = user_info[0][3]
			if admin_bool is not True and user_password == password:
				musica_db.execute("DELETE FROM user	 WHERE CARD_ID = ?",(cardID,))
				musica_db.execute("DELETE FROM score WHERE USER_ID = ?",(cardID,))
				musica_db_file.commit()
				print("User ID {0} removed.".format(cardID))
			else:
				print("Permission denied.")
		except:
			print("Error raised while removing User ID {0}. Rolling back DB...".format(cardID))
			self.rollback_DB()
	def update_user_name(self, cardID, newName, password):
		try:
			user_info = musica_db.execute("SELECT * FROM user WHERE CARD_ID = ?",(cardID,)).fetchall()
			admin_bool = True if user_info[0][4] is 1 else False
			user_password = user_info[0][3]
			if admin_bool is not True and user_password == password:
				musica_db.execute("UPDATE user SET NAME = ? WHERE CARD_ID = ?",(newName, cardID,))
				musica_db_file.commit()
				print("User ID {0}'s name is now {1}.".format(cardID, newName))
			else:
				print("Permission denied.")
		except:
			print("Error raised while updating ID {0}'s user name to {1}. Rolling back DB...".format(cardID, newName))
			self.rollback_DB()
	def update_user_password(self, cardID, prevPassword, newPassword):
		try:
			user_info = musica_db.execute("SELECT * FROM user WHERE CARD_ID = ?",(cardID,)).fetchall()
			admin_bool = True if user_info[0][4] is 1 else False
			user_password = user_info[0][3]
			if admin_bool is not True and user_password == prevPassword:
				musica_db.execute("UPDATE user SET PASSWORD = ? WHERE CARD_ID = ?",(newPassword, cardID,))
				musica_db_file.commit()
				print("User ID {0}'s password is now {1}.".format(cardID, newPassword))
			else:
				print("Permission denied.")
		except:
			print("Error raised while updating ID {0}'s user password to {1}. Rolling back DB...".format(cardID, newPassword))
			self.rollback_DB()
	def update_user_score(self, cardID, songID, score):
		try:
			update_score_str = "UPDATE score SET {0} = {1} WHERE USER_ID = '{2}'".format(songID, score, cardID)
			print update_score_str
			musica_db.execute(update_score_str)
			musica_db_file.commit()
			print("User ID {0}'s score is now {1}.".format(cardID, score))
		except:
			print("Error raised while updating ID {0}'s score to {1}. Rolling back DB...".format(cardID, score))
			self.rollback_DB()
	def add_song(self, songID, name, fingerprint):
		try:
			alter_command = "ALTER TABLE score ADD {0} INTEGER DEFAULT 0".format(songID)
			musica_db.execute(alter_command)
			musica_db.execute("INSERT INTO song VALUES(null, ?, ?, ?)",(songID, name, fingerprint))
			musica_db_file.commit()
			print("Song {0}(ID: {1}) added.".format(name, songID))
		except:
			print("Error raised while adding song. Rolling back DB...")
			self.rollback_DB()
	def del_song(self, songID):
		#Should create new table without selected songID's column and drop the old one.
		try:
			musica_db.execute("DROP TABLE IF EXISTS score_tmp")
			column_cmd = musica_db.execute("SELECT * FROM score")
			song_ID_list = list(map(lambda x: x[0], column_cmd.description))
			song_ID_location_in_column = song_ID_list.index(songID)
			scoreDB_setupDB_str	 = "USER_ID TEXT NOT NULL UNIQUE"
			for s in range(len(song_ID_list) - 1):
				if songID != song_ID_list[s + 1]:
					scoreDB_setupDB_str += ", {0} INTEGER DEFAULT 0".format(song_ID_list[s + 1])
			musica_db.execute("CREATE TABLE score_tmp({0}) ".format(scoreDB_setupDB_str))
			copy_target_column_tmp = " "
			for s in range(len(song_ID_list)):
				if songID != song_ID_list[s]:
					copy_target_column_tmp += "{0}, ".format(song_ID_list[s])
			copy_target_column = copy_target_column_tmp[:len(copy_target_column_tmp) - 2]
			copy_target_str	 = "INSERT INTO score_tmp(" + copy_target_column
			copy_target_str += ") SELECT " + copy_target_column + " FROM score"
			musica_db.execute(copy_target_str)
			musica_db.execute("DROP TABLE score")
			musica_db.execute("ALTER TABLE score_tmp RENAME TO score")
			musica_db.execute("DELETE FROM song WHERE SONG_ID = ?",(songID,))
			musica_db_file.commit()
			print("Song ID: {0} removed.".format(songID))
		except:
			print("Error raised while removing Song. Rolling back DB...")
			self.rollback_DB()
	def rollback_DB(self):
		try:
			musica_db_file.rollback()
			musica_db_file.commit()
			print("DB Successfully rolled back")
		except:
			print("Error raised while rolling back DB. Critical.")
			raise
	def close_DB(self):
		try:
			musica_db_file.commit()
			musica_db_file.close()
		except:
			print("Error raised while closing DB. Critical.")
			raise
	
	
	def table_json_parser(self, tableName, return_json_str=True):
		try:
			table_data_json = {}
			table_data = musica_db.execute("SELECT * FROM {0}".format(tableName)).fetchall()
			if tableName == "song":
				song_num = len(table_data)
				for s in range(song_num):
					songInfo = {}
					songInfo['NAME'] = table_data[s][2]
					songInfo['FINGERPRINT'] = table_data[s][3]
					table_data_json[table_data[s][1]] = songInfo
			elif tableName == "user":
				user_num = len(table_data)
				for u in range(user_num):
		
					userInfo = {}
					userInfo['NAME'] = table_data[u][2]
					userInfo['ADMIN'] = True if table_data[u][4] else False
					table_data_json[table_data[u][1]] = userInfo
			elif tableName == "score":
				column_cmd = musica_db.execute("SELECT * FROM score")
				song_ID_list = list(map(lambda x: x[0], column_cmd.description))
				user_num = len(table_data)
				song_num = len(song_ID_list) - 1
				for s in range(song_num):
					user_score = {}
					for u in range(user_num):
						user_score[table_data[u][0]] = table_data[u][s + 1]
					table_data_json[song_ID_list[s + 1]] = user_score
			else:
				print("Error raised while exporting table to json : Unknown table")
				return None
			if return_json_str:
				return json.dumps(table_data_json)
			else:
				return table_data_json
		except:
			print("Error raised while exporting table to json")
			return None
	def getUserName(self, cardID):
		user_table = self.table_json_parser(tableName='user',return_json_str=False)
		return user_table[cardID]['NAME'] if user_table.has_key(cardID) else None
	def getSongName(self, songID):
		song_table = self.table_json_parser(tableName='song',return_json_str=False)
		return song_table[songID]['NAME'] if song_table.has_key(songID) else None
	def topRank(self, song, top5=True):
		score_table = self.table_json_parser(tableName='score',return_json_str=False)
		if score_table == None:
			print('Failed to get rank from DB')
			return None
		try:
			rank_list = score_table[song]
			for l in rank_list.items():
				if not l[1]:
					del(rank_list[l[0]])
			rank_list_sorted = sorted(rank_list.iteritems(), key=operator.itemgetter(1), reverse=True)
		except:
			print('Failed to sort rank from score table')
			return None
		if top5 and len(rank_list_sorted) > 5:
			rank_list_sorted = rank_list_sorted[:5]
		return rank_list_sorted