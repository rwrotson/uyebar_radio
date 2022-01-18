yurets = playlist(reload=1, reload_mode="rounds", "/home/user/yurets")

s = single("/home/user/traumprinz/stateofme.mp3")

yurets = fallback([yurets, s])

yurets = map_metadata(apply_metadata, yurets)

yurets = on_track(call_image_getter(n='2'), yurets)

output.icecast(%mp3(bitrate=320, samplerate = 44100, stereo = true),
	       host="icecast", port=8090, password="stille",
	       mount="yurets", yurets, fallible=true)
