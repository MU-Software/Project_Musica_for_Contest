#!/usr/bin/env python
# -*- coding: utf-8 -*-
class GUI_title:
	class image_background:
		pos   = "center","center"
		size  = "100%", "100%"
		style = "LIGHT_BLACK_BORDER"
	class image_logo:
		pos   = "center","15%"
		size  = "40%", "45%"
		style = "LIGHT_BLACK_BORDER"
	class text_game_next:
		pos   = "center","70%"
		size  = 500, 50
		type  = "label"
		text  = "Insert Coin(s)"
		#text  = "동전을 넣어주세요."
		style = "LIGHT_BLACK_BORDER"
	class text_copyright:
		pos   = "center","bottom"
		size  = 500, 50
		type  = "label"
		text  = "Copyright 2016 MUsoftware"
		style = "LIGHT_BLACK_BORDER"

class GUI_select:
	class select_help:
		pos   = "left","top"
		size  = "75%", "15%"
		style = "LIGHT_BLACK_BORDER"
	class timer:
		pos   = "right","top"
		size  = "25%", "15%"
		style = "LIGHT_BLACK_BORDER"
	class mode:
		pos   = "0%","center"
		size  = "25%", "70%"
		style = "LIGHT_BLACK_BORDER"
	class song:
		pos   = "25%","center"
		size  = "25%", "70%"
		style = "LIGHT_BLACK_BORDER"
	class difficulty:
		pos   = "50%","center"
		size  = "25%", "70%"
		style = "LIGHT_BLACK_BORDER"
	class select_show:
		pos   = "75%","center"
		size  = "25%", "70%"
		style = "LIGHT_BLACK_BORDER"
	class key_help:
		pos   = "center","bottom"
		size  = "100%", "15%"
		style = "LIGHT_BLACK_BORDER"

bool_pause = True
class GUI_playing:
	class user_info:
		pos   = "5%","top"
		size  = "10%", "15%"
		style = "LIGHT_BLACK_BORDER"
		hide  = bool_pause
	class song_status:
		pos   = "center","top"
		size  = "70%", "15%"
		style = "LIGHT_BLACK_BORDER"
		hide  = bool_pause
	class song_info:
		pos   = "85%","top"
		size  = "10%", "15%"
		style = "LIGHT_BLACK_BORDER"
		hide  = bool_pause
	
	class image_background:
		pos   = "center","center"
		size  = "100%", "100%"
		style = "LIGHT_BLACK_BORDER"
		hide  = not bool_pause
	class image_music_info:
		pos   = "55%","center"
		size  = "30%", "65%"
		style = "LIGHT_BLACK_BORDER"
		hide  = not bool_pause
	class text_return_to_game:
		pos   = "15%","25%"
		size  = 500, 100
		style = "LIGHT_BLACK_BORDER"
		type  = "label"
		text  = "게임으로 돌아가기"
		hide  = not bool_pause
	class text_give_up_select_song_list:
		pos   = "15%","45%"
		size  = 500, 100
		style = "LIGHT_BLACK_BORDER"
		type  = "label"
		text  = "포기하고 곡 선택 화면으로 돌아가기"
		hide  = not bool_pause
	class text_give_up_:
		pos   = "15%","65%"
		size  = 500, 100
		style = "LIGHT_BLACK_BORDER"
		type  = "label"
		text  = "포기하고 게임 끝내기"
		hide  = not bool_pause
		

class GUI_score:
	pass

class GUI_thankyou:
	class image_background:
		pos   = "center","center"
		size  = "100%", "100%"
		style = "LIGHT_BLACK_BORDER"
	class text_thanks_for_playing:
		pos   = "center","center"
		size  = 500, 50
		style = "LIGHT_BLACK_BORDER"
		type  = "label"
		text  = "Thanks for playing!"