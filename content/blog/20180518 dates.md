Title: Dates are hard
Date: 2018-05-18 12:00:00-07:00
Entry-ID: 398
UUID: 5f4cc46b-fd8d-4e49-9938-63d8ecf6d08a
Tag: design
Tag: rant

There's an old joke in programming, that the two hardest things to do are naming things, cache invalidation, and off-by-one errors. But this doesn't pay sufficient respect to one of the other hardest things, namely handling date and time.

.....

Many systems don't bother handling dates in any sort of universal way; they just
treat all entry times as being local time and call it a day. But this has a
problem: whenever the time zone changes, it means that every date it refers to
is now different than how it was when it first happened. Any traveling
photographer who has tried reconciling EXIF times in their photo software after
going across the world understands this pain. So does anyone who attempts to
schedule recurring meetings between different time zones (or even different
hemispheres), especially when Daylight Saving changes in one locale but not in
the other (or in opposite directions).

This is also a problem for any given CMS, and it's an intractable problem.

### A naïve approach

An approach I've seen several times is to simply store entry dates in local
time, and format them accordingly. But this messes up anything that's timezone-
aware; scheduled posts made for 2:30 AM will appear, then disappear, then
reappear again when daylight saving ends, and Atom feeds will have items slip
around whenever there's a time change (or if the person running the site decides
to move into a different timezone or whatever). So, this makes the data
unstable; it's only a minor hassle in the grand scheme of things but it still
represents a data integrity error.

### Publ's attempt at being clever

At present, what Publ does is to store dates based on their local time of
writing, but keeps them with a timezone, and indexes them based on UTC for the
purpose of pagination and so on. It formats the date based on its original post
time in its respective time zone, and this seems to work okay; dates always
appear the same no matter when you look at them, and the relative time offset is
stable with respect to when it's being calculated.

But date-based pagination always has to be based on *something*, and I chose
local time for that. And this can cause all sorts of weirdness to happen,
especially for entries posted between 11 PM and 1 AM (depending on
circumstances).

Say an entry is posted at 11:30 PM on January 31; for me (pacific time) this
puts it at 23:30-08:00, which is the same as 07:30 UTC on February 1. Then
later, Daylight Saving kicks in. The entry is still at 23:30-08:00 (i.e. 07:30
UTC).

Now say someone is looking at January entries. During standard time their
pagination range is going to be 00:00-08:00 on January 1 thru 23:59-08:00 on
January 31, which translates to UTC as 08:00 January 1 - 08:00 February 1. Okay,
so 07:30 UTC on February 1 comes before 08:00 February 1. Great, my January 31
entry still appears in January.

But then they come back during DST, and the local timezone is now -07:00. So
someone browsing the site for January entries now gets a pagination range of
07:00 January 1 - 07:00 February 1. Suddenly my last-minute-of-January entry is
now part of February's page instead.

Let's say down the road I move to New York, which means my local timezone is now
-05:00 standard or -04:00 daylight saving. Oops, all of the pagination for my
site has changed again. And what's worse, all the older entries no longer make
*any* sort of sense, especially my posted-near-midnight comics.

Incidentally, this violates one of the core tenets of Publ — that pagination
should be *stable*.

### Splitting the difference?

So, how about this approach: always paginate and sort entries based on what
their *local* time is (so an entry posted on 01/31/2017 always appears to be on
the page for 01/31/2017 regardless of the indicated time zone), and only use the
UTC normalization for determining a relative interval to the current time (i.e.
whether it's in the future for scheduled posts, and how many seconds ago it was
posted for the "N seconds ago" display). This *seems* like an okay compromise,
although it does mean that if a person is traveling between time zones things
might get a little weird around the boundaries, and sorting might not always
make perfect temporal sense (but it exposes fewer boundary conditions that will
make pagination break, so while it's not [technically
correct](https://www.youtube.com/watch?v=hou0lU8WMgo) it's at least
predictable).

But, that seems less broken than other possibilities. It satisfies the principle
of least surprise, it keeps pagination stable, and it keeps the presented date
consistent with the authored date (even if it might cause some weird jumping-
around in some cases).

So, I think that is what I will change Publ to do. It's (slightly) more code and
more annoyance but it seems like the best path forward.

Even if it means time will sometimes run backward.
