Realistically this is a pretty pointless script. I put it together as an experiment...

It connects to a dump1090 install on your network and puts the data it receives from dump1090 into a single SQLite database table so that you can query it.

I wouldn't use this as is, but it may serve as something you can build on.

Don't run this on a Pi as it'll thrash your SD card to bits, and I'd think twice about running it on any other computer for very long, as it'll eventually fill your disk up.
