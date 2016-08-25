#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright 2016 MU Software(@MUsoftware on twitter), All Rights Reserved.
#Musica Basic Score Server - Main server side module(main)
import sys; sys.dont_write_bytecode = True #PYC 생성을 막기 위함
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
DB = db_module.DB_control()
CSS_LANK = """
	<style>
	table.mytable {
		font-family: times;
		font-size:12px;
		color:#000000;
		border-width: 1px;
		border-color: #0081a7;
		border-collapse: collapse;
		background-color: #ffffff;
		width=100%;
		min-width:400px;
		max-width:550px;
		text-align: center;
		margin: auto;
		margin-top: 10px;
		table-layout:fixed;
	}
	table.mytable th {
		border-width: 1px;
		padding: 8px;
		border-style: solid;
		border-color: #0081a7;
		background-color: #add8fe;
		color:#000000;
	}
	table.mytable td {
		border-width: 1px;
		padding: 8px;
		border-style: solid;
		border-color: #0081a7;
	}
	#code {
		display:inline;
		font-family: courier;
		color: #3d9400;
	}
	#string {
		display:inline;
		font-weight: bold;
	}
	</style>"""
HTML_MAIN = """
	<!doctype html>
	<meta charset="utf-8">
	<link rel="icon"
		type="image/png"
		href="/static/favicon.png">
	<title>MUSICA Score Chart</title>
	<style>
	body {background-color: lightblue;}

	h1 {
		font-family: verdana;
		font-size: 50px;
		color: DarkCyan;
		text-align: center;
		vertical-align: middle;
	}
	div {
		color: DarkCyan ;
		font-family: verdana;
		font-size: 25px;
		text-align: center;
	}
	p {
		color: DarkCyan ;
		font-family: verdana;
		font-size: 15px;
		text-align: center;
	}
	</style>
	%s
	<h1>Musica, MIDI based Rhythm Game.</h1>
	<div>%s</div>
	%s

	<p>Written by MU Software</p> """
HTML_404 = """
	<!doctype html>
	<meta charset="utf-8">
	<link rel="icon"
		type="image/png"
		href="/static/favicon.png">
	<title>404 Page Not Found</title>
	<style>
	body {
		background-color: lightblue;
	}

	h1 {
		margin-top: 300px;
		font-family: verdana;
		font-size: 50px;
		color: DarkCyan;
		text-align: center;
		vertical-align: middle;
	}
	div {
		color: DarkCyan ;
		font-family: verdana;
		font-size: 25px;
		text-align: center;
	}
	p {
		color: DarkCyan ;
		font-family: verdana;
		font-size: 15px;
		text-align: center;
	}
	</style>
	<div style="display:inline-block;vertical-align:top;">
		<img src="/static/404_820x820.png">
	</div>
	<div style="display:inline-block;">
		<h1>Umm...Page doesn't exist.</h1>
		<div>Maybe you mis-spelled URL.  <a href="/">Go to Main</a></div>
	</div>

	<p>Written by MU Software</p>"""
HTML_LOGIN = """
	<!doctype html>
	<meta charset="utf-8">
	<link rel="icon"
		type="image/png"
		href="/static/favicon.png">
	<style>
	body {background-color: lightblue;}

	h1 {
		font-family: verdana;
		font-size: 50px;
		color: DarkCyan;
		text-align: center;
		vertical-align: middle;
	}
	h2 {
		text-align: center;
	}
	</style>
	<html>
		<head>
			<title>로그인</title>
		</head>
		<body>
			<h1>Musica, MIDI based Rhythm Game.</h1>
			<h2>
			<form action = "/login" method = "post">
			<input type = "text" name = "id" value = "" placeholder="유저 ID"> <p>
			<input type = "password" name = "pwd" value = "" placeholder="비밀번호"> <p>
			<input type = "submit" value = "로그인">
			</form></h2>
		</body>
	</html>"""

class MyHandler(BaseHTTPRequestHandler):
	def do_GET(self): #GET & DELETE 처리
		parsed_path = urlparse.urlparse(self.path)
		if self.path == '/favicon.ico':#잘못된 파비콘 처리용
			self.path = '/static/favicon.png'
		if self.path.endswith(".png"): #PNG 이미지 처리용
			f = open(self.path[1:], 'rb')
			self.send_response(200)
			self.send_header('Content-type', 'image/png')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
			return
		if self.path.endswith(".jpg"): #JPG 이미지 처리용
			f = open(self.path[1:], 'rb')
			self.send_response(200)
			self.send_header('Content-type', 'image/jpg')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
			return

		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		
		#Query 파싱
		query_list = filter(None, parsed_path.query.split('&'))
		query_dict = dict()
		for i in query_list:
			if len(filter(None, i.split('='))) > 1:
				query_dict[i.split('=')[0]] = i.split('=')[1]
		
		if parsed_path.path in ['/', '/main', '/index']: #GET으로 메인 요청
			self.wfile.write(HTML_MAIN % (CSS_LANK, 'This is main page', ''))			
		elif parsed_path.path == '/login': #GET으로 로그인 폼 요청
			self.wfile.write(HTML_LOGIN)
		elif parsed_path.path == '/view_score': #GET으로 랭킹 요청
			if not query_dict or not query_dict.has_key('songID'): #파싱된 쿼리 내용이 없을 때 || 파싱된 쿼리 내용에 songID가 없을 때
				self.wfile.write(HTML_MAIN % (CSS_LANK, 'Query parsing failed. 쿼리 파싱에 실패하였습니다.', ''))
			else:
				userID = None if not query_dict.has_key('userID') else query_dict['userID']
				self.wfile.write(HTML_MAIN % (CSS_LANK, 'Score Rank - {0}'.format(DB.getSongName(query_dict['songID'])),
								 self.htmlRankWriter(query_dict['songID'], userID)))
		else: #요청이 존재하지 않는 페이지일때-404에러 페이지 표시
			self.wfile.write(HTML_404)
	def do_POST(self): #POST & PUT 처리
		parsed_path = urlparse.urlparse(self.path)
		length = int(self.headers['Content-Length'])
		data = self.rfile.read(length).decode('utf-8')
		if parsed_path.path == '/update_score': #점수 바꾸기 !!DB 점수가 더 높으면 바꾸지 말게
			try:
				update_score_data = json.loads(data)
			except:
				return
			if set(('userID','songID','score')) <= set(update_score_data):
				self.send_response(200)
				self.send_header("Content-type", "application/octet-stream")
				self.end_headers()
				DB.update_user_score(update_score_data['userID'],
									 update_score_data['songID'],
									 update_score_data['score'] )
			else:
				self.send_response(404)
				self.send_header("Content-type", "application/octet-stream")
				self.end_headers()
			return
		elif parsed_path.path == '/view_score_client':
			self.send_response(200)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			try:
				requested_data = json.loads(data)
			except:
				return
			if requested_data.has_key('songID') and DB.topRank(requested_data['songID']):
				#튜플 두번째에 userName 추가
				rank = DB.topRank(requested_data['songID'])
				rank_userName = []
				for i in rank:
					rank_userName.append(tuple((i[0], DB.getUserName(i[0]),i[1])))
				self.wfile.write(rank_userName)
			return
		elif parsed_path.path == '/login':
			self.send_response(200)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			query_list = filter(None, data.split('&'))
			query_dict = dict()
			for i in query_list:
				if len(filter(None, i.split('='))) > 1:
					query_dict[i.split('=')[0]] = i.split('=')[1]
			print query_dict
		else: #요청이 존재하지 않는 페이지일때-404에러 헤더 전송
			self.send_response(404)
			self.send_header("Content-type", "application/octet-stream")
			self.end_headers()
	
	do_PUT = do_POST    #PUT을 POST로 처리하도록
	do_DELETE = do_GET #DELETE를 GET으로 처리하도록

	def htmlRankWriter(self, song, user=None): #노래의 랭크 목록을 HTML로 파싱
		rank = DB.topRank(song, False)
		if rank: #랭크가 정상적으로 반환되었는지 검사
			rank_userName = []
			for i in rank:
				rank_userName.append(tuple((DB.getUserName(i[0]),i[1])))
			rank_html_table = simpletable.SimpleTable(rows       = rank_userName,
													  header_row = ['유저 ID','점수'],
													  css_class  = 'mytable')
			if user: #유저가 랭크 안에 있는지 검사
				if [i for i in rank if i[0] == user]:
					grade = [rank.index(i) for i in rank if i[0] == user][0] + 1
					rank_html_table = '<div>유저 {0}는 {1}등 입니다.</div>'.format(DB.getUserName(user), grade) + str(rank_html_table)
		else:
			rank_html_table = '<div>Failed to get score rank list. 랭크 목록을 가져오지 못했습니다.</div>'
		return rank_html_table

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='MU Software MUSICA Score Server')
	parser.add_argument('port', type=int, help='Port for Server')
	args = parser.parse_args()

	try:
		print("Run Server on {0}".format(args.port))
		server = HTTPServer(('', args.port), MyHandler)
		server.serve_forever()
	except KeyboardInterrupt:
		print("KeyboardInterrupt raised. Shutting down the server...")
		server.socket.close()
	except:
		print("Unexpected error raised.")
		raise