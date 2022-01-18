prinz = playlist(reload=1, reload_mode="rounds",
		 "/home/user/traumprinz")

s = single("/home/user/traumprinz/stateofme.mp3")

prinz_fb = fallback([prinz, s])

prinz_fb = map_metadata(apply_metadata, prinz_fb)

prinz_fb = on_track(call_image_getter(n='1'), prinz_fb)

prinz_cf = crossfade(fade_out=5., fade_in=7.,
                     duration=10., prinz_fb)

output.icecast(%mp3(bitrate=320, samplerate = 44100, stereo = true),
	       host="icecast", port=8090, password="stille",
	       mount="traumprinz", prinz_cf, fallible=true)
