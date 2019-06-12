import DataCollector

base_url = "https://files.pushshift.io/reddit/comments/"
s3_folder = "raw/reddit/"

def year_month_list(yr, begin, end, ext):
    return [("RC_" + str(yr) + "-" + str(month), ext) for month in range(begin, end+1)]

bz2_files = [("RC_2005-12", "bz2")]
for year in range(2006, 2017):
    bz2_files += year_month_list(year, 1, 12, "bz2")
bz2_files +=  year_month_list(2017, 1, 11, "bz2")

reddit_files = bz2_files

if __name__ == "__main__":
    for (filename, ext) in reddit_files:
        full_url = base_url + filename + "." + ext
        print("Downloading file: " + filename)
        DataCollector.download(full_url, filename)
        print("Decompressing file: " + filename)
        DataCollector.decompress(filename + "." + ext, ext)
        print("Transferring file to S3")
        DataCollector.write_to_S3(filename, s3_folder, "saywhat-warehouse")
