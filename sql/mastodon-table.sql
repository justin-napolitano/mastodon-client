CREATE TABLE toots (
    id BIGINT PRIMARY KEY, -- Numerical id of this toot
    created_at DATETIME, -- Creation time
    in_reply_to_id BIGINT, -- Numerical id of the toot this toot is in response to
    in_reply_to_account_id BIGINT, -- Numerical id of the account this toot is in response to
    `sensitive` BOOLEAN, -- Denotes whether media attachments to the toot are marked sensitive
    spoiler_text TEXT, -- Warning text that should be displayed before the toot content
    visibility ENUM('public', 'unlisted', 'private', 'direct'), -- Toot visibility
    language CHAR(2), -- The language of the toot, as ISO 639-1 (two-letter) language code
    uri VARCHAR(255), -- Descriptor for the toot
    url VARCHAR(255), -- URL of the toot
    replies_count INT, -- The number of replies to this status
    reblogs_count INT, -- Number of reblogs
    favourites_count INT, -- Number of favourites
    edited_at DATETIME, -- Edit time
    favourited BOOLEAN, -- Denotes whether the logged-in user has favourited this toot
    reblogged BOOLEAN, -- Denotes whether the logged-in user has boosted this toot
    muted BOOLEAN, -- Boolean denoting whether the user has muted this status
    bookmarked BOOLEAN, -- True if the status is bookmarked by the logged-in user, False if not
    pinned BOOLEAN, -- Boolean denoting whether or not the status is currently pinned for the associated account
    content TEXT, -- Content of the toot, as HTML
    filtered JSON, -- Filtered content
    reblog JSON, -- Denotes whether the toot is a reblog. If so, set to the original toot dict.
    application JSON, -- Application dict for the client used to post the toot
    account JSON, -- User dict for the account which posted the status
    media_attachments JSON, -- A list of media dicts of attached files
    mentions JSON, -- A list of user dicts mentioned in the toot
    tags JSON, -- A list of hashtags used in the toot
    emojis JSON, -- A list of custom emojis used in the toot
    card JSON, -- A preview card for links from the status
    poll JSON, -- A poll dict if a poll is attached to this status
    site_url VARCHAR(255) -- this is the id to reference to determine if a post exists within the posts table
);

