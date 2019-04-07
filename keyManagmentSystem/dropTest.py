import dropbox
import inspect, os
print(inspect.getfile(inspect.currentframe())) # script filename (usually with path))
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory


client  = dropbox.Dropbox('0Asgs_ev8WAAAAAAAAAAC0-q3yhO457uLv2Po_XlSDe2wICZoevQ8CYabOgJr-Su')
p = client.users_get_current_account()
print(p.email)
file = open("test.txt")

with open("test.txt", "rb") as f:
    bytes = f.read()
    client.files_upload(bytes, '/test4.txt', mute = True)
      