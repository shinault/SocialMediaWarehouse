import DataCollector

hn_bzipped_comments_url = "https://archive.org/download/14566367HackerNewsCommentsAndStoriesArchivedByGreyPanthersHacker/14m_hn_comments_sorted.json.bz2"

bzipped_filename = "14m_hn_comments_sorted.json.bz2"
json_filename = "14m_hn_comments_sorted.json"
s3_location = "raw/hacker_news/" + json_filename

if __name__ == "__main__":
    print("Downloading file")
    DataCollector.download(hn_bzipped_comments_url, bzipped_filename)
    print("Decompressing file")
    DataCollector.decompress(bzipped_filename, "bz2")
    print("Transferring file to S3")
    DataCollector.write_to_S3(json_filename, s3_location, "saywhat-warehouse")
