import flet as ft
import yt_dlp
import time
import os

def main(page: ft.Page):
    page.title = "YouTube Video İndirici"
    downloadFiles = []

    def search_video(e):
        sorgu = aramaGirdisi.value
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                infoDict = ydl.extract_info(f"ytsearch:{sorgu}", download=False)['entries'][0]
                videoTitle.value = f"Başlık: {infoDict['title']}"
                thumbnail.src = infoDict['thumbnail']
                searchContainer.visible = False
                videoInfoContainer.visible = True
                page.update()
            except Exception as e:
                videoTitle.value = "Video bulunamadı."
                thumbnail.src = ""
                page.update()
                print(f"Arama hatası: {e}")

    def download_video(e):
        download_button.visible = False 
        downloading_text.visible = True  
        progress_bar.visible = True  
        progress_text.visible = True  

        video_url = aramaGirdisi.value
        format_selection = format_dropdown.value
        resolution = resolution_dropdown.value
        
        search_url = f"ytsearch:{video_url}"
        
        ydl_opts = {
            'format': format_selection,
            'outtmpl': f'./downloads/%(title)s.%(ext)s',
            'noplaylist': True,
            'progress_hooks': [progress_hook]
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(search_url, download=True)
                ext = info_dict.get('ext', 'mp4')
                downloadFiles.append(info_dict['title'] + '.' + ext)
        
            for i in range(101):
                time.sleep(0.05)
                progress_bar.value = i
                progress_text.value = f"{i}%"
                page.update()
            
            download_button.visible = True
            downloading_text.visible = False  
            progress_bar.visible = False  
            progress_text.visible = False  
            update_downloaded_files()
        except Exception as e:
            downloading_text.value = "İndirme hatası."
            print(f"İndirme hatası: {e}")
            page.update()

    def update_downloaded_files():
        files_list.controls = [ft.Text(value=file, size=18) for file in downloadFiles]
        page.update()

    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = int(d['downloaded_bytes'] / d['total_bytes'] * 100)
            progress_bar.value = percent
            progress_text.value = f"{percent}%"
            page.update()

    aramaGirdisi = ft.TextField(label="Video Arama", expand=True)
    search_button = ft.ElevatedButton(text="Ara", on_click=search_video)
    videoTitle = ft.Text(value="", size=24)
    thumbnail = ft.Image(src="", width=400, height=300)

    format_dropdown = ft.Dropdown(
        label="Format",
        options=[
            ft.dropdown.Option("mp4"),
            ft.dropdown.Option("mp3"),
            ft.dropdown.Option("webm"),
        ],
        value="mp4"
    )

    resolution_dropdown = ft.Dropdown(
        label="Çözünürlük",
        options=[
            ft.dropdown.Option("1080p"),
            ft.dropdown.Option("720p"),
            ft.dropdown.Option("480p"),
            ft.dropdown.Option("360p"),
        ],
        value="1080p"
    )

    download_button = ft.ElevatedButton(text="İndir", on_click=download_video)
    downloading_text = ft.Text(value="Video indiriliyor...", size=24, visible=False)
    progress_bar = ft.ProgressBar(value=0, width=400, visible=False)
    progress_text = ft.Text(value="0%", size=20, visible=False)

    searchContainer = ft.Container(
        content=ft.Row(
            controls=[aramaGirdisi, search_button],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        height=page.height
    )

    videoInfoContainer = ft.Container(
        content=ft.Column(
            controls=[
                videoTitle,
                thumbnail,
                ft.Row(
                    controls=[download_button, format_dropdown, resolution_dropdown],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                downloading_text,
                progress_bar,
                progress_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        alignment=ft.alignment.center,
        expand=True,
        visible=False
    )

    files_list = ft.Column(
        controls=[],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.START
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Video İndir",
                content=ft.Column(
                    controls=[searchContainer, videoInfoContainer],
                    alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                text="İndirilenler",
                content=ft.Container(
                    content=files_list,
                    alignment=ft.alignment.center,
                    expand=True
                ),
            ),
        ],
        expand=1,
    )

    page.add(tabs)

    if not os.path.exists('./downloads'):
        os.makedirs('./downloads')

ft.app(target=main)
