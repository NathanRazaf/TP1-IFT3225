#!/usr/bin/env python3
import argparse
import os
import re
import sys
from urllib.parse import urljoin, urlparse

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


def matches_regex(path, regex_pattern):
    """
    Check if path matches the regex pattern
    Returns True if:
    - regex_pattern is None (no filtering requested)
    - or if path matches the regex pattern
    """
    if regex_pattern is None:
        return True

    try:
        return bool(re.search(regex_pattern, path))
    except re.error as e:
        print(f"Invalid regex pattern: {e}", file=sys.stderr)
        return False


def get_absolute_url(base_url, relative_url):
    """Convert relative URL to absolute URL."""
    # Return the relative URL if it's already absolute
    if bool(urlparse(relative_url).netloc):
        return relative_url
    # Otherwise, join the base URL with the relative URL
    return urljoin(base_url, relative_url)


def download_media(url, output_path):
    """Download media from url to output_path and return the local filename."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Get the filename from the URL
        filename = os.path.basename(urlparse(url).path)
        if not filename:  # Handle case where URL doesn't end with filename
            filename = 'unnamed_file'

        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        # Save the file
        local_path = os.path.join(output_path, filename)
        with open(local_path, 'wb') as f:
            f.write(response.content)

    except Exception as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)


def main():
    # Create parser with descriptive help message
    parser = argparse.ArgumentParser(
        description='Extract media resources from a webpage\nWritten by Nathan Razafindrakoto 20254813 and Yasmine Ben Youssef 20237210',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

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

    # Print the URL to stdout
    sys.stdout.write(f"PATH {args.url.strip()}\n")

    images = None
    videos = None

    # Compile regex pattern if provided
    regex = re.compile(args.r) if args.r else None

    # Find images if not disabled
    if not args.i:
        images = find_images(soup)
        images = [image for image in images if matches_regex(image.split()[1], regex)]

    # Find videos if not disabled
    if not args.v:
        videos = find_videos(soup)
        videos = [video for video in videos if matches_regex(video.split()[1], regex)]

    # Download medias if output path is provided
    if args.p:
        for media_text in (images or []) + (videos or []):
            media_url = media_text.split()[1]
            download_media(get_absolute_url(args.url, media_url), args.p)


    # Print images and videos to stdout
    for image in images:
        sys.stdout.write(f"{image}\n")
    for video in videos:
        sys.stdout.write(f"{video}\n")

    # Flush stdout to ensure output is sent to the next program in the pipeline
    sys.stdout.flush()

if __name__ == '__main__':
    main()