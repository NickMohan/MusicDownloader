from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import config

def youtube_search(options):

    print("Starting Youtube search...")

    youtube = build(
        config.Youtube.SERVICE_NAME,
        config.Youtube.VERSION,
        developerKey=config.Youtube.DEVELOPER_KEY
    )

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q="The Moment I Knew",
        part="id,snippet",
        maxResults=options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []

    count = 0
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        count += 1
        try:
            kind = search_result["id"]["kind"]
        except KeyError:
            pass
        else:
            if kind == "youtube#video":
                videos.append("%s" % (search_result["id"]["videoId"]))
            elif kind == "youtube#channel":
                channels.append("%s (%s)" % (
                    search_result["snippet"]["title"],
                    search_result["id"]["channelId"])
                )
            elif kind == "youtube#playlist":
                playlists.append("%s (%s)" % (
                    search_result["snippet"]["title"],
                    search_result["id"]["playlistId"])
                )

    print("Search returned %d items." % count)

    return(videos)

if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Programming")
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()

    try:
        youtube_search(args)
    except (HttpError, e):
        print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
