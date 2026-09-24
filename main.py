import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_preview import get_spotify_preview_url
import streamlit as st
from dotenv import load_dotenv
import os
import random
import time

load_dotenv() # Loads the environment variables from .env

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'spotify-playlist-quiz-nd7ckdgeq9sab3dqnbc6fb'

# Spotify login
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='playlist-read-private'
    )
)

def question1(): # Which year is the song [SONGNAME] from?
    tracks = st.session_state.tracks
    track = random.choice(tracks)
    wrong_answers = []
    while len(wrong_answers) < 3:
        wrong_track = random.choice(tracks)
        wrong_answer = wrong_track[4]
        if wrong_answer not in wrong_answers and wrong_answer != track[4]:
            wrong_answers.append(wrong_answer)
    choices = [track[4]] + wrong_answers
    random.shuffle(choices)
    st.session_state.current_question = {
        "question_number": "question1",
        "question": f":musical_note: Which year is the song '{track[0]}' from?",
        "options": choices,
        'correct_answer': track[4],
        }

def question2(): # Which song is this?
    tracks = st.session_state.tracks
    track = random.choice(tracks)
    wrong_answers = []
    while len(wrong_answers) < 3:
        wrong_track = random.choice(tracks)
        wrong_answer = wrong_track[0]
        if wrong_answer not in wrong_answers and wrong_answer != track[0]:
            wrong_answers.append(wrong_answer)
    choices = [track[0]] + wrong_answers
    random.shuffle(choices)
    st.session_state.current_question = {
        "question_number": "question2",
        "question": f':musical_note: Which song is this?',
        "options": choices,
        'correct_answer': track[0],
        "preview_url": get_audio(track)
        }

def question3(): # Which album does this song come from?
    tracks = st.session_state.tracks
    track = random.choice(tracks)
    wrong_answers = []
    while len(wrong_answers) < 3:
        wrong_track = random.choice(tracks)
        wrong_answer = wrong_track[2]
        if wrong_answer not in wrong_answers and wrong_answer != track[2]:
            wrong_answers.append(wrong_answer)
    choices = [track[2]] + wrong_answers
    random.shuffle(choices)
    st.session_state.current_question = {
        "question_number": "question3",
        "question": f':musical_note: Which album is this song from?',
        "options": choices,
        'correct_answer': track[2],
        "preview_url": get_audio(track)
        }

def question4(): # [ARTISTNAME] made the album [ALBUMNAME].
    tracks = st.session_state.tracks
    track = random.choice(tracks)
    displayed_data = random.choice([track[2], random.choice(tracks)[2]])
    is_correct = displayed_data == track[2]
    st.session_state.current_question = {
        "question_number": "question4",
        "question": f":musical_note: The album '{displayed_data}' is by {track[1]}.",
        "options": ["True", "False"],
        'correct_answer': 'True' if is_correct else 'False',
        }

def question5(): # What's this songs birthyear?
    tracks = st.session_state.tracks
    track = random.choice(tracks)
    wrong_answers = []
    while len(wrong_answers) < 3:
        wrong_track = random.choice(tracks)
        wrong_answer = wrong_track[4]
        if wrong_answer not in wrong_answers and wrong_answer != track[4]:
            wrong_answers.append(wrong_answer)
    choices = [track[4]] + wrong_answers
    random.shuffle(choices)
    st.session_state.current_question = {
        "question_number": "question5",
        "question": f":musical_note: What's this songs birthyear?",
        "options": choices,
        'correct_answer': track[4],
        "preview_url": get_audio(track)
        }

def question6(): # Which album is from [YEAR]?
    tracks = st.session_state.tracks
    track = random.choice(tracks)
    albums = []
    while len(albums) < 3:
        wrong_track1 = random.choice(tracks)
        if wrong_track1[4] not in track and wrong_track1[3] not in albums:
            albums.append(wrong_track1[3])
        wrong_track2 = random.choice(tracks)
        if wrong_track2[4] not in track:
            if wrong_track2[4] not in wrong_track1:
                if wrong_track2[3] not in albums:
                    albums.append(wrong_track2[3])
        wrong_track3 = random.choice(tracks)
        if wrong_track3[4] not in track:
            if wrong_track3[4] not in wrong_track1:
                if wrong_track3[4] not in wrong_track2:
                    if wrong_track3[3] not in albums:
                        albums.append(random.choice([track[3], wrong_track3[3]]))
    if albums[0] == track[3]:
        correct_answer = "A"
    elif albums[1] == track[3]:
        correct_answer = "B"
    elif albums [2] == track[3]:
        correct_answer = "C"
    else:
        correct_answer = "None"
    st.session_state.current_question = {
        "question_number": "question6",
        "question": f":musical_note: Which of these albums is from {track[4]}?",
        "options": ["A", "B", "C", "None"],
        'correct_answer': correct_answer,
        "image1": albums[0],
        "image2": albums[1],
        "image3": albums[2]
        }
    

# Generates a random question
def generate_question():
    list_of_questions = [question1, question2, question3, question4, question5, question6]
    random.choice(list_of_questions)()


# Displays the program's interface with Streamlit elements
def display_page():
    # Displays starting page
    if st.session_state.page_state == 0:
        st.set_page_config(page_title="Spotify quiz game")
        st.title(':notes: Spotify playlist quiz')
        st.write("This program is lightly inspired by iQuiz, a game on Apple iPods that quizzes you on random songs, albums and artists from your iPod library. This program does exactly that, but uses Spotify playlists instead. There are 10 questions, you get 3 lives, and do be warned there is auto-playing audio.\n\nTo begin testing your knowledge on the songs you like, enter a link to a Spotify playlist below! (P.S. the larger the playlist, the better the experience)")
        playlist_link = st.text_input('Paste a playlist link here:')
        if st.button('Begin'):
            get_data(playlist_link)
            if st.session_state.tracks:
                generate_question()
                st.session_state.page_state = 1
                st.rerun()

    # Displays questions
    elif st.session_state.page_state == 1:
        # Checks the number of lives the user has left
        if st.session_state.lives == 3:
            st.session_state.hearts = ":heart::heart::heart:"
        elif st.session_state.lives == 2:
            st.session_state.hearts = ":heart::heart:"
        elif st.session_state.lives == 1:
            st.session_state.hearts = ":heart:"
        # Displays the title of the question
        question = st.session_state.current_question
        st.subheader(question['question'])
        # Displays and autoplays the audio for the question if it requires audio
        if 'preview_url' in question:
            st.audio(question['preview_url'], autoplay=True)
        # Displays the images for the question if it requires images
        if 'image1' in question:
            with st.container(height=160, horizontal=True, border=False):
                st.image(question['image1'], width=150)
                st.image(question['image2'], width=150)
                st.image(question['image3'], width=150)
        # Displays the options for the user to choose from
        selected_answer = st.radio(
            'Choose your answer:',
            question['options'],
            key=f'answer_{question['question_number']}')
        # A container displaying the submit button and the amount of lives the user has left
        with st.container(horizontal=True, vertical_alignment='center'):
            submitbutton = st.button('Submit', key=f"submit_{question['question_number']}")
            st.write(f'Lives: {st.session_state.hearts}')
        # Will check the user's answer when they click the submit button
        if submitbutton:
            check_answer(selected_answer)

    # Displays end page
    elif st.session_state.page_state == 2:
        st.subheader(":tada: You won!")
        if st.session_state.points == 10:
            st.write(f"You got {st.session_state.points} out of 10 questions correct! Wow, you really know your stuff.")
        elif st.session_state.points == 9:
            st.write(f"You got {st.session_state.points} out of 10 questions correct! You know your stuff pretty well, almost perfectly.")
        elif st.session_state.points >= 7:
            st.write(f"You got {st.session_state.points} out of 10 questions correct! You know your stuff pretty well, but not perfectly.")
        st.write('Thank you for playing!')
        if st.button("Play again?"):
            # Resets the game
            st.session_state.question_count = 0
            st.session_state.current_question = None
            st.session_state.lives = 3
            st.session_state.points = 0
            st.session_state.tracks = []
            st.session_state.page_state = 0
            st.rerun()

    # Displays losing page
    elif st.session_state.page_state == 3:
        st.subheader(":broken_heart: You lost!")
        st.write(f"You ran out of lives... Better luck next time.")
        if st.button("Play again?"):
            # Resets the game
            st.session_state.question_count = 0
            st.session_state.current_question = None
            st.session_state.lives = 3
            st.session_state.tracks = []
            st.session_state.points = 0
            st.session_state.page_state = 0
            st.rerun()

# Checks if the answer the user chose is correct or incorrect
def check_answer(selected_answer):
    question = st.session_state.current_question
    if selected_answer == question['correct_answer']:
        st.success(f':white_check_mark: Correct!')
        st.session_state.points += 1
    else: 
        st.error(f':x: Incorrect! The answer was {question['correct_answer']}')
        st.session_state.lives -= 1
    time.sleep(0.7) # Pauses for a little before continuing (Gives user a bit more time to read their result)
    st.session_state.question_count += 1
    if st.session_state.question_count >= 10:
        st.session_state.page_state = 2
    if st.session_state.lives == 0:
        st.session_state.page_state = 3
    else:
        generate_question()
    st.rerun()


# Gets the data of the tracks within the user's playlist
def get_data(playlist_link):
    try:
        playlist_ID = playlist_link.split('/')[-1].split('?')[0] # Isolates the playlist ID from the rest of the link
        results = sp.playlist_tracks(playlist_ID)
        while results:
            for x in results['items']: # Loops through every track in the playlist, collecting and storing the data of each one
                if x['track'] is None:
                    continue
                if x['is_local'] == True:
                    continue
                track_name = x['track']['name']
                artist_name = x['track']['artists'][0]['name']
                album_name = x['track']['album']['name']
                album_cover = x['track']['album']['images'][0]['url']
                album_year = x['track']['album']['release_date'].split('-')[0]
                track_id = x['track']['id']
                st.session_state.tracks.append([track_name, artist_name, album_name, album_cover, album_year, track_id]) # Stores the data of a track in a list
            results = sp.next(results)
    except spotipy.exceptions.SpotifyException:
        st.error('Please enter a valid playlist link!')


# Gets an audio sample necessary for certain questions
def get_audio(track):
    preview_url = get_spotify_preview_url(track[5])
    return preview_url


# Program initialisation
if 'page_state' not in st.session_state:
    st.session_state.page_state = 0 # State 0 displays the starting page, state 1 displays the questions, state 2 displays the end page
if 'tracks' not in st.session_state:
    st.session_state.tracks = [] # Contains the data of each individual track from the user's playlist
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0 # Goes up by 1 for each question answered
if 'current_question' not in st.session_state:
    st.session_state.current_question = None # Contains the data for the question the program is currently displaying
if 'lives' not in st.session_state:
    st.session_state.lives = 3 # 
if 'points' not in st.session_state:
    st.session_state.points = 0 #
display_page()
