import math
import time
import wget

def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]


speeder = lambda current, start: get_size(current / (time.time() - start)) + "/sec"



def measure_progress(current, total, start, task_name="URL download", time_gap=3.00):
    now = time.time()
    diff = now - start
    if not total or int(total) == 0:
        return "empty"
    else:
        try:
            if (
                round(diff % float(time_gap)) == 0.00
                or current == total
                and int(current) != 0
            ):
                if "upload" in task_name.lower():
                    method = "<b>Uploading"
                else:
                    method = "<b>Downloading"
                percentage = current * 100 / total
                speed = current / diff
                elapsed_time = round(diff) * 1000
                time_to_completion = round((total - current) / speed) * 1000
                estimated_total_time = elapsed_time + time_to_completion
                progress_str = "{3} : {2}%</b>\n[{0}{1}]\n".format(
                    "".join(["▪" for i in range(math.floor(percentage / 10))]),
                    "".join(["▫" for i in range(10 - math.floor(percentage / 10))]),
                    "%.2f" % (percentage),
                    method,
                )
                tmp = progress_str + (
                    f"{get_size(current)} of {get_size(total)}\nSpeed : {speeder(current, start)}\nETA : {time_formatter(estimated_total_time)}"
                )
                print(f"\n{task_name}\n{tmp}")
                bot_text = (
                    tmp)
                return bot_text
            else:
                return "empty"
        except Exception as e:
            print(str(e))



def progress_bar_for_wget(current, total, start, msg, method="URL Download", Time_gap=3):
    text = measure_progress(current, total, start, method, 5)
    if not text == "empty" and text != None:
        try:
        	#print(text)
            msg.edit_text(text, parse_mode="HTML")
        except Exception as identifier:
            print(str(identifier))
            
def wget_dl(url, msg):
	print("Download Start")
	start = time.time()
	try:
		file_path = wget.download(url, bar=lambda c, t, w: progress_bar_for_wget(c, t, start, msg))
		return file_path
	except Exception as e:
		return "Error" + str(e)