import DataCollector

hn_bzipped_comments_url = "https://archive.org/download/14566367HackerNewsCommentsAndStoriesArchivedByGreyPanthersHacker/14m_hn_comments_sorted.json.bz2"

bzipped_filename = "14m_hn_comments_sorted.json.bz2"
json_filename = "14m_hn_comments_sorted.json"
s3_location = "raw/hacker_news/" + json_filename

if __name__ == "__main__":
    DataCollector.download(hn_bzipped_comments_url, bzipped_filename)
    DataCollector.decompress(bzipped_filename, json_filename, "bz2")
    DataCollector.write_to_S3(json_filename, s3_location, "saywhat-warehouse")
