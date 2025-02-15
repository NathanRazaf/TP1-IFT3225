#!/usr/bin/env python3
import argparse
import requests
from bs4 import BeautifulSoup, Comment


def get_media_text(media_type, src, alt):
    """Create a formatted string for media elements."""
    text = f"{media_type} "
    if src is not None:
        text += src
    if alt is not None:
        text += f' "{alt}"'
    return text


def find_images(soup):
    """Find all images in the soup, including those in comments."""
    images = []

    # Regular images
    for img in soup.find_all('img'):
        images.append(get_media_text("IMAGE", img.get('src'), img.get('alt')))

    # Images in comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment_soup = BeautifulSoup(comment, 'html.parser')
        for img in comment_soup.find_all('img'):
            images.append(get_media_text("IMAGE", img.get('src'), img.get('alt')))

    return images


def find_videos(soup):
    """Find all videos in the soup, including those in comments."""
    videos = []

    def process_video(video):
        # First check if video has src attribute
        src = video.get('src')
        if src is None:
            # If no src on video, look for first source element's src
            source = video.find('source')
            if source:
                src = source.get('src')
        return get_media_text("VIDEO", src, video.get('alt'))

    # Regular videos
    for video in soup.find_all('video'):
        videos.append(process_video(video))

    # Videos in comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment_soup = BeautifulSoup(comment, 'html.parser')
        for video in comment_soup.find_all('video'):
            videos.append(process_video(video))

    return videos


def main():
    # Create parser with descriptive help message
    parser = argparse.ArgumentParser(description='Extract media resources from a webpage')

    # Add all required arguments and options
    parser.add_argument('url', help='URL of the webpage to analyze')
    parser.add_argument('-r', help='only list resources matching this regex pattern')
    parser.add_argument('-i', action='store_true', help='do not list images')
    parser.add_argument('-v', action='store_true', help='do not list videos')
    parser.add_argument('-p', metavar='path', help='download resources to this path')

    args = parser.parse_args()

    # Fetch and parse the webpage
    response = requests.get(args.url)
    soup = BeautifulSoup(response.text, 'html.parser')

    print("PATH " + args.url.strip())

    # Find and print images if not disabled
    if not args.i:
        for image_text in find_images(soup):
            print(image_text)

    # Find and print videos if not disabled
    if not args.v:
        for video_text in find_videos(soup):
            print(video_text)


if __name__ == '__main__':
    main()