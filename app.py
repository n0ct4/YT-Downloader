import yt_dlp as youtube_dl
import streamlit as st

class YtDownloader:
    def __init__(self, url):
        self.url = url
        self.video_info = None
        self.stream = None

    def fetch_video_info(self):
        """Fetch video information without downloading."""
        ydl_opts = {'quiet': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            self.video_info = ydl.extract_info(self.url, download=False)

    def showTitle(self):
        """Display video title and show available streams."""
        if self.video_info:
            st.write(f"**Title:** {self.video_info['title']}")
            self.showStreams()

    def showStreams(self):
        """Display available streams to select for download."""
        formats = [f for f in self.video_info['formats'] if f.get('filesize')]

        if not formats:
            st.write("No available streams to show.")
            return
        
        stream_options = [
            f"Resolution: {f.get('format_note', 'N/A')} / Type: {f['ext']} / Size: {f['filesize'] / 1000000:.2f} MB"
            for f in formats
        ]
        
        choice = st.selectbox("Choose the stream option: ", stream_options)
        self.stream = formats[stream_options.index(choice)]

    def getFileSize(self):
        """Get file size of the selected stream."""
        if self.stream and 'filesize' in self.stream:
            return self.stream['filesize'] / 1000000  
        return 0

    def getPermissionContinue(self, file_size):
        """Display file info and ask for download permission."""
        st.write(f"**Size: ** {file_size:.2f} MB")
        if st.button("Download"):
            self.download()

    def download(self):
        """Download the selected stream."""
        if self.stream:
            ydl_opts = {
                'format': self.stream['format_id'],
                'quiet': True,
                'outtmpl': f"{self.video_info['title']}.%(ext)s"
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            st.success("Download successful")

if __name__ == "__main__":
    st.title("N0ct4 Youtube Videos Downloader")
    url = st.text_input("Type here the video URL: ")

    if url:
        downloader = YtDownloader(url)
        downloader.fetch_video_info()
        downloader.showTitle()
        if downloader.stream:
            file_size = downloader.getFileSize()
            downloader.getPermissionContinue(file_size)
