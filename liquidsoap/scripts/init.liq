# Tag encodings
set("tag.encodings",["UTF-8", "CP1251", "ISO-8859-1", "UTF-16"])
set("encoder.encoder.export",["artist","title","album"])

# Log directory
tech = "/home/user/log"
set("log.file.path","#{tech}/liquidsoap.log")
set("log.level", 3)

# Functions
def apply_metadata(m) =
  title = m["title"]
  artist = m["artist"]
  album = m["album"]
  year = m["year"]
  label = m["comment"]
  path = m["filename"]
  [("artist", ""),("title", '{"artist": "#{artist}", "song_title": "#{title}", "album": "#{album}", "year": "#{year}", "label": "#{label}", "path": "#{path}"}')]
end

def call_image_getter(m, ~n="0") =
  path = m["filename"]
  log.important("Getter is called for: #{path}, #{n}")
  ignore(run_process("python3 /home/user/python/image_getter.py '#{path}' #{n}"))
  log.important("Function executed")
end

