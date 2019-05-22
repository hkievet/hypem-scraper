A database replication through webcrawler project

The goal of this project is to gather data of the most popular songs from the music blog aggregation site http://hypem.com.

Ideally I will have a collection of data as such:

Tool used: Cypress

Initial raw data will include the hypem links to spotify, soundcloud, and apple music.

1. Gather links to all the different time machine pages.

Example: https://hypem.com/popular/week:Oct-22-2007
How to:  https://hypem.com/popular/lastweek


href of :div.stage > ul#flux-capacitor > li.year > ul.months > li.month > div.full > a
Those final a tags have a link like:  /popular/week:Nov-05-2007

Another way would be to generate all Mondays between now and 11/22/07.  But doing the link way would yield everything.

2.  Save the links as JSON, giving each a scanned boolean attribute

3. Scan each link one by one performing the steps 4:

4. visit a link like /popular/week:Nov-05-2007
all the tracks are contained in div#track-list


each track is contained within a div.section.section-track.haarp-section-track
this element also has a data-itemid on it which is the hypem identifier

The following attributes can all begotten from the div.section-player
The trackName and trackArtist is in a h3.track_name
trackArtist text of:h3.track_name>a.artist
trackName: text of:h3.track_name>a.track>span.base-title
There might be a special remix, since hypem is known for their remixes.
trackRemix: text of:h3.track_name>a.track>span.remix-link
trackRemixCount: text of:h3.track_name>a.track>span.remix-count

To see if the track is still around and accessible check for the presense of...
ul.tools > li.playdiv

inside of the div.meta > span.download you can find the download links...
grab all the a tags within this span, they might be at multiple level
Look at the link text to determine it's source:
Enum: "Spotify", "Apple Music", "SoundCloud"
Then the href on those is what you're about...

Nifty super neat that should be all the info that you need to get going on this project!!!

