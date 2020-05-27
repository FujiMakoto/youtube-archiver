import logging
import os

import youtube_dl

from ytarchiver.config import config


class YtArchiver:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.output_path = str(config.get('YouTube', 'output_directory')).rstrip('/').rstrip('\\').rstrip()

    def run(self) -> None:
        """
        Execute the search queries and download whatever is available
        Returns:
            None
        """
        monitored_keywords = str(config.get('YouTube', 'monitored_keywords'))
        if not monitored_keywords:
            self.log.critical("No keywords defined in the configuration, closing application")
            exit(1)

        monitored_keywords = [k.strip() for k in monitored_keywords.split(',')]

        for keyword in monitored_keywords:
            self.log.info(f"Executing search query: {keyword}")

            # Make sure the keyword is path safe
            keyword_path = "".join([c for c in keyword if c.isalpha() or c.isdigit() or c == ' ']).strip()

            # Initialize youtube_dl
            ytdl_format_options = {
                'format'            : 'bestvideo/best',
                'outtmpl'           : f'{self.output_path}/{keyword_path}/%(title)s (%(id)s).%(ext)s',
                'restrictfilenames' : True,
                'noplaylist'        : True,
                'nocheckcertificate': True,
                'ignoreerrors'      : False,
                'logtostderr'       : False,
                'quiet'             : True,
                'no_warnings'       : True,
                'default_search'    : 'auto',
                'progress_hooks'    : [self.progress_hook],
            }

            with youtube_dl.YoutubeDL(ytdl_format_options) as ytdl:
                ytdl.download([f'ytsearchdate5:{keyword}'])

    def progress_hook(self, data):
        """
        Progress monitoring
        Args:
            data (dict): Progress data from youtube_dl

        Returns:

        """
        if data['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(data['filename']))
            self.log.info(f"Download complete: {file_tuple[1]}")
        if data['status'] == 'downloading':
            self.log.debug(f"Downloading {data['filename']}: {data['_percent_str']} ({data['_eta_str']})")

