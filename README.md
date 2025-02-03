# GUI-Video-Downloader

![main_screen](src/main_screen.jpg)

> [!NOTE]  
> **Deprecated Project**<br>
> This project has been discontinued and rebuilt as **[new-video-downloader](https://github.com/Serori1923/new-video-downloader)**, featuring a completely restructured architecture, an improved UI, and an enhanced user experience.

## Overview
The **UI Video Downloader** is a user-friendly application for downloading videos from popular platforms such as YouTube, X (Twitter), TikTok, and Instagram.

Built on the open-source **Cobalt** project, this tool provides a secure and reliable way to download and save videos for purposes such as editing or creating backups.

## Features
- **Multi-language Support**: Switch between **Traditional Chinese**, **English**, and **Japanese** interfaces.
- **Local Download History**: Keeps a record of all downloaded videos stored locally, allowing users to easily track and access original video links.
- **Platform Compatibility**: Supports downloading from major platforms like YouTube, X (Twitter), TikTok, and Instagram.
- **Secure & Reliable**: Based on the open-source **Cobalt** project, ensuring transparency and safety.
- **Intuitive UI**: Built with Tkinter for a seamless user experience.

## How It Works
1. The API server, based on **Cobalt**, is run in a Docker container with port forwarding configured via Nginx.
2. Users interact with the API through a Tkinter-based graphical interface.
3. The application processes user requests, downloads the desired video, and logs the download history locally for future reference.

![Flowchart](src/Flowchart.jpg)

## Acknowledgments
- **[cobalt](https://github.com/imputnet/cobalt)**: The open-source library powering the core functionality.
- All contributors and the open-source community.
> Disclaimer: This tool is intended for personal use only. Please ensure compliance with the terms of service of the platforms you download content from.
