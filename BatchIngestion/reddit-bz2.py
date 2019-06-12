import DataCollector

base_url = "https://files.pushshift.io/reddit/comments/"
s3_folder = "raw/reddit/"

def year_month_list(yr, begin, end, ext):
    return [("RC_" + str(yr) + "-" + str(month).zfill(2), ext) for month in range(begin, end+1)]

bz2_files = [("RC_2005-12", "bz2")]
for year in range(2006, 2017):
    bz2_files += year_month_list(year, 1, 12, "bz2")
bz2_files +=  year_month_list(2017, 1, 11, "bz2")

reddit_files = bz2_files

if __name__ == "__main__":
    for (filename, ext) in reddit_files:
        dl_name = filename + "." + ext
        full_url = base_url + dl_name
        print("Downloading file: " + dl_name)
        DataCollector.download(full_url, dl_name)
        print("Decompressing file: " + dl_name)
        DataCollector.decompress(dl_name, ext)
        print("Transferring file to S3")
        DataCollector.write_to_S3(filename, s3_folder + filename, "saywhat-warehouse")
        os.remove(filename)
