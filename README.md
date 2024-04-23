# Libricasts
Tool to automate fixing and uploading rss feeds from librivox.org to Pocketcasts
## Background
Librivox.org hosts public domain audiobooks recorded by volunteers, they also provide rss feeds so you can import them into your favourate podcast app to listen. PocketCasts allows you to import custom rss feeds using their website. However the 2 are incompatible, the details are listed here in this great reddit [post](https://www.reddit.com/r/pocketcasts/comments/ekin6r/i_finally_found_ways_to_overcome_the_librivox/) but the gist is that the librivox rss file has the publish date commented out, but pocketcasts requires it to be there. This tool automates the process of fixing the rss file, uploding it to Github Gist then generating the PocketCasts url.

## Usage

### Installation

1. Clone the repo
    - `git clone https://github.com/adhipk/libricasts.git`
2. Install the requirements
    - `pip install -r requirements.txt`

3. Setup Redis store, this will cache Github gist urls, preventing redundant rss file uploads.
3. Copy the .env.example file to .env and fill in the values
### Running the app

1. From the root of the repo run `python server.py`


### Licence
MIT License