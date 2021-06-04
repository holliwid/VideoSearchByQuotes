import prepare_video
import some_data
import mongoDB

if __name__ == "__main__":
    prepare_video.get_all_video_in_channel(some_data.youtube_api_key, some_data.id_channel)
    prepare_video.download_waw('url_of_videos.txt')
    prepare_video.from_wav_to_text_IBM(some_data.IBM_PASSWORD)

    data_for_DB = (mongoDB.raw_to_prepared_data('prepared_text_of_video', 'url_of_videos.txt'))
    mongoDB.download_data_to_bs(data_for_DB)


