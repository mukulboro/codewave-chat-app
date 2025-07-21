# AnonChat - Chat With Anonymity

AnonChat is a real-time anonymous chat application developed during the Codewave 2024 Hackathon. It focuses on user privacy and control by securing conversations with a modified Caesar encryption algorithm and allowing users to gradually reveal their identities at their own pace.

## Key Features

*   **Real-Time Communication:** Instant messaging powered by Django Channels for a seamless chat experience.
*   **Enhanced Anonymity:** Engage in conversations without revealing your identity upfront.
*   **Unique Encryption:** Messages are secured using a modified Caesar cipher, adding a layer of privacy.
*   **Gradual Identity Reveal:** Users can choose to decrypt their usernames, letter by letter, giving them full control over their anonymity.
*   **Sleek Interface:** A clean and modern user interface designed with Tailwind CSS.

## How It Works

The application ensures that when a user enters a chat room, their username is initially encrypted. As they interact and feel more comfortable, they have the option to press a button that decrypts one letter of their username at a time for all participants in the room. This unique feature allows for a controlled and gradual reveal of identity, putting user discretion at the forefront.

## Tech Stack

*   **Backend:** Django
*   **Frontend:** Tailwind CSS
*   **Database:** SQLite
*   **Real-Time/WebSockets:** Django Channels

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python
*   Pip

### Installation

1.  **Clone the repo**
    ```sh
    git clone https://github.com/mukulboro/codewave-chat-app.git
    ```
2.  **Navigate to the project directory**
    ```sh
    cd codewave-chat-app
    ```
3.  **Install Python packages**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Apply database migrations**
    ```sh
    python manage.py migrate
    ```
5.  **Run the development server**
    ```sh
    python manage.py runserver
    ```
The application will be available at `http://127.0.0.1:8000/`.

## Acknowledgments

This project was conceived and developed as part of the **Codewave 2024 Hackathon**.

## License

Distributed under the MIT License. See `LICENSE` for more information.
