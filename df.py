import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QListWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTime


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('music player.ui', self)  # Load your .ui file here

        # Initialize the media player and playlist
        self.media_player = QMediaPlayer()
        self.playlist = []
        self.current_song_index = -1

        # Setup playlist widget
        self.playlist_widget = self.findChild(QListWidget, 'playlist')

        # Connect item selection to play the song
        self.playlist_widget.itemClicked.connect(self.item_selected)

        # Connect buttons to functions
        self.play.clicked.connect(self.play_music)
        self.pause.clicked.connect(self.pause_music)
        self.stop.clicked.connect(self.stop_music)
        self.previous.clicked.connect(self.previous_music)
        self.next.clicked.connect(self.next_music)
        self.load_songs_1.clicked.connect(self.load_songs)  # Connect load songs button

        # Volume Control
        self.volume.setValue(50)
        self.volume.valueChanged.connect(self.set_volume)

        # Seek Bar
        self.progresscontrol.sliderMoved.connect(self.set_position)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)

    def add_to_playlist(self, file_paths):
        """ Add songs to the playlist and update the display. """
        for file_path in file_paths:
            self.playlist.append(file_path)
            self.playlist_widget.addItem(QListWidgetItem(file_path.split('/')[-1]))

    def load_songs(self):
        """ Open a file dialog to select music files to add to the playlist. """
        file_dialog = QtWidgets.QFileDialog(self, "Open Audio Files")
        file_dialog.setNameFilter("Audio Files (*.mp3);;All Files (*)")
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.add_to_playlist(selected_files)

    def item_selected(self, item):
        self.current_song_index = self.playlist_widget.row(item)
        self.play_music()

    def play_music(self):
        """ Play the current song if one is selected. """
        if self.current_song_index == -1 and self.playlist:
            self.current_song_index = 0

        if self.current_song_index >= 0:
            # Set media only if it's not already set
            if self.media_player.media() is None or self.media_player.currentMedia().canonicalUrl().toLocalFile() != \
                    self.playlist[self.current_song_index]:
                media_url = QUrl.fromLocalFile(self.playlist[self.current_song_index])
                self.media_player.setMedia(QMediaContent(media_url))

            # Start playing
            self.media_player.play()  # Continue playing from the last position

    def pause_music(self):
        """ Pause or resume the current song. """
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()  # Pause playback
        elif self.media_player.state() == QMediaPlayer.PausedState:
            self.media_player.play()
    def stop_music(self):
        """ Stop the current song. """
        self.media_player.stop()
        self.current_song_index = -1  # Reset to no song playing

    def previous_music(self):
        """ Play the previous song in the playlist. """
        if self.current_song_index > 0:
            self.current_song_index -= 1
            self.play_music()

    def next_music(self):
        """ Play the next song in the playlist. """
        if self.current_song_index < len(self.playlist) - 1:
            self.current_song_index += 1
            self.play_music()

    def set_volume(self, value):
        """ Set the player volume. """
        self.media_player.setVolume(value)

    def set_position(self, position):
        """ Set the player position. """
        self.media_player.setPosition(position)

    def update_position(self, position):
        """ Update the seek slider based on the current playback position. """
        self.progresscontrol.setValue(position)
        current_time = QTime(0, 0, 0).addMSecs(position)
        duration = QTime(0, 0, 0).addMSecs(self.media_player.duration())

        if self.media_player.duration() > 0:
            self.labelTime.setText(current_time.toString("mm:ss") + " / " + duration.toString("mm:ss"))

    def update_duration(self, duration):
        """ Set the range of the seek slider to match the duration of the media. """
        if duration > 0:
            self.progresscontrol.setRange(0, duration)
        else:
            self.progresscontrol.setRange(0, 0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

