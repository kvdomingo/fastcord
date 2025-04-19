-- begin prereqs ---
CREATE OR REPLACE FUNCTION update_modified_column()
    RETURNS TRIGGER AS
$$
BEGIN
    IF ROW (NEW.*) IS DISTINCT FROM ROW (OLD.*) THEN
        NEW.modified = NOW();
        RETURN NEW;
    ELSE
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION update_is_edited_column()
    RETURNS TRIGGER AS
$$
BEGIN
    IF ROW (NEW.*) IS DISTINCT FROM ROW (OLD.*) THEN
        NEW.is_edited = TRUE;
        RETURN NEW;
    ELSE
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION randint(min INTEGER, max INTEGER)
    RETURNS INTEGER AS
$$
BEGIN
    RETURN FLOOR(RANDOM() * (max - min + 1) + min)::INTEGER;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION create_default_channels_after_guild_insert()
    RETURNS TRIGGER AS
$$
DECLARE
    channel_group_id VARCHAR(26);
BEGIN
    INSERT INTO channel_groups (
        name, guild_id, "order"
    )
    VALUES (
               'Text Channels', NEW.id, 0
           )
    RETURNING id INTO channel_group_id;

    INSERT INTO channels (
        name, guild_id, channel_group_id, is_general, "order"
    )
    VALUES (
               'general', NEW.id, channel_group_id, TRUE, 0
           );

    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';
-- end prereqs ---

-- begin users --
CREATE TYPE AVAILABILITY_STATUS AS ENUM ('online', 'idle', 'dnd', 'offline');

CREATE TABLE IF NOT EXISTS users (
    id                    VARCHAR(26) DEFAULT idkit_ulid_generate()                                                     NOT NULL,
    created               TIMESTAMP   DEFAULT CURRENT_TIMESTAMP                                                         NOT NULL,
    modified              TIMESTAMP   DEFAULT CURRENT_TIMESTAMP                                                         NOT NULL,
    username              VARCHAR(32)                                                                                   NOT NULL,
    discriminator         SMALLINT                                                                                      NOT NULL DEFAULT randint(0, 9999),
    full_username         VARCHAR(36) GENERATED ALWAYS AS (username || '#' || LPAD(discriminator::TEXT, 4, '0')) STORED NOT NULL,
    email                 TEXT                                                                                          NOT NULL,
    avatar                TEXT,
    cover                 TEXT,
    "availability_status" AVAILABILITY_STATUS                                                                           NOT NULL DEFAULT 'offline',

    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT users_username_discriminator_uq UNIQUE (username, discriminator),
    CHECK ( LENGTH(username) > 0 ),
    CHECK ( discriminator >= 0 AND discriminator <= 9999 )
);

CREATE INDEX users_id_ix ON users (id);
CREATE INDEX users_username_ix ON users (username);
CREATE INDEX users_discriminator_ix ON users (discriminator);
CREATE INDEX users_email_ix ON users (email);
CREATE INDEX users_full_username_ix ON users (full_username);

CREATE TRIGGER update_users_modified
    BEFORE UPDATE
    ON users
    FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();
-- end users --

-- begin guilds --
CREATE TABLE IF NOT EXISTS guilds (
    id       VARCHAR(26) DEFAULT idkit_ulid_generate() NOT NULL,
    created  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP     NOT NULL,
    modified TIMESTAMP   DEFAULT CURRENT_TIMESTAMP     NOT NULL,
    name     VARCHAR(64)                               NOT NULL,
    avatar   TEXT,
    banner   TEXT,
    owner_id TEXT                                      NOT NULL,

    CONSTRAINT guilds_pk PRIMARY KEY (id),
    CONSTRAINT guilds_name_uq UNIQUE (name),
    CONSTRAINT guilds_owner_id_fk FOREIGN KEY (owner_id) REFERENCES users (id),
    CHECK ( LENGTH(name) > 0 ),
    CHECK ( CASE WHEN avatar IS NULL THEN TRUE ELSE LENGTH(avatar) > 0 END ),
    CHECK ( CASE WHEN banner IS NULL THEN TRUE ELSE LENGTH(banner) > 0 END )
);

CREATE INDEX guilds_id_ix ON guilds (id);
CREATE INDEX guilds_name_ix ON guilds (name);

CREATE TRIGGER update_guild_modified
    BEFORE UPDATE
    ON guilds
    FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();

CREATE TABLE user_guilds_order (
    user_id  VARCHAR(26) NOT NULL,
    guild_id VARCHAR(26) NOT NULL,
    "order"  INTEGER     NOT NULL,

    CONSTRAINT user_guilds_order_pk PRIMARY KEY (user_id, guild_id),
    CONSTRAINT user_guilds_order_user_id_fk FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT user_guilds_order_guild_id_fk FOREIGN KEY (guild_id) REFERENCES guilds (id) ON DELETE CASCADE
);
-- end guilds --

-- begin channels --
CREATE TABLE IF NOT EXISTS channel_groups (
    id       VARCHAR(26) DEFAULT idkit_ulid_generate() NOT NULL,
    created  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP     NOT NULL,
    modified TIMESTAMP   DEFAULT CURRENT_TIMESTAMP     NOT NULL,
    name     VARCHAR(32)                               NOT NULL,
    guild_id VARCHAR(26)                               NOT NULL,
    "order"  INTEGER                                   NOT NULL,

    CONSTRAINT channel_groups_pk PRIMARY KEY (id),
    CONSTRAINT channel_groups_name_guild_id_uq UNIQUE (name, guild_id),
    CONSTRAINT channel_groups_guild_fk FOREIGN KEY (guild_id) REFERENCES guilds (id) ON DELETE CASCADE,
    CHECK ( LENGTH(name) > 0 )
);

CREATE INDEX channel_groups_id_ix ON channel_groups (id);
CREATE INDEX channel_groups_name_ix ON channel_groups (name);

CREATE TRIGGER update_channel_groups_modified
    BEFORE UPDATE
    ON channel_groups
    FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();

CREATE TYPE CHANNEL_TYPE AS ENUM ('text', 'voice');

CREATE TABLE IF NOT EXISTS channels (
    id               VARCHAR(26) DEFAULT idkit_ulid_generate() NOT NULL,
    created          TIMESTAMP   DEFAULT CURRENT_TIMESTAMP     NOT NULL,
    modified         TIMESTAMP   DEFAULT CURRENT_TIMESTAMP     NOT NULL,
    name             VARCHAR(32)                               NOT NULL,
    guild_id         VARCHAR(26)                               NOT NULL,
    channel_group_id VARCHAR(26),
    type             CHANNEL_TYPE                              NOT NULL DEFAULT 'text',
    is_general       BOOLEAN                                   NOT NULL DEFAULT FALSE,
    "order"          INTEGER,

    CONSTRAINT channels_pk PRIMARY KEY (id),
    CONSTRAINT channels_name_guild_uq UNIQUE (name, guild_id),
    CONSTRAINT channels_guild_id_fk FOREIGN KEY (guild_id) REFERENCES guilds (id) ON DELETE CASCADE,
    CONSTRAINT channels_channel_group_id_fk FOREIGN KEY (channel_group_id) REFERENCES channel_groups (id) ON DELETE CASCADE,
    CHECK ( LENGTH(name) > 0 )
);

CREATE INDEX channels_id_ix ON channels (id);
CREATE INDEX channels_name_ix ON channels (name);

CREATE TRIGGER update_channels_modified
    BEFORE UPDATE
    ON channels
    FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER after_guild_insert_trigger
    AFTER INSERT
    ON guilds
    FOR EACH ROW
EXECUTE PROCEDURE create_default_channels_after_guild_insert();
-- end channels --

-- begin messages --
CREATE TABLE IF NOT EXISTS messages (
    id         VARCHAR(26) DEFAULT idkit_ulid_generate() NOT NULL,
    created    TIMESTAMP   DEFAULT CURRENT_TIMESTAMP     NOT NULL,
    modified   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP     NOT NULL,
    author_id  VARCHAR(26),
    channel_id VARCHAR(26)                               NOT NULL,
    content    VARCHAR(4096)                             NOT NULL,
    is_edited  BOOLEAN                                   NOT NULL DEFAULT FALSE,

    CONSTRAINT messages_pk PRIMARY KEY (id),
    CONSTRAINT messages_author_id_fk FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE SET NULL,
    CONSTRAINT messages_channel_id_fk FOREIGN KEY (channel_id) REFERENCES channels (id) ON DELETE CASCADE,
    CHECK ( LENGTH(content) > 0 )
);

CREATE INDEX messages_id_ix ON messages (id);
CREATE INDEX messages_author_ix ON messages (author_id);
CREATE INDEX messages_channel_ix ON messages (channel_id);

CREATE TRIGGER update_messages_modified
    BEFORE UPDATE
    ON messages
    FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_messages_is_edited
    BEFORE UPDATE
    ON messages
    FOR EACH ROW
EXECUTE PROCEDURE update_is_edited_column();
-- end messages --

-- begin emojis --
CREATE TABLE IF NOT EXISTS emojis (
    id        VARCHAR(26) DEFAULT idkit_ulid_generate() NOT NULL,
    created   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP     NOT NULL,
    modified  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP     NOT NULL,
    name      VARCHAR(16)                               NOT NULL,
    source    TEXT                                      NOT NULL,
    guild_id  VARCHAR(26)                               NOT NULL,
    author_id VARCHAR(26),

    CONSTRAINT emojis_pk PRIMARY KEY (id),
    CONSTRAINT emojis_name_guild_uq UNIQUE (name, guild_id),
    CONSTRAINT emojis_guild_id_fk FOREIGN KEY (guild_id) REFERENCES guilds (id) ON DELETE CASCADE,
    CONSTRAINT emojis_author_id_fk FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE SET NULL,
    CHECK ( LENGTH(name) > 0 AND LENGTH(name) <= 16 ),
    CHECK ( LENGTH(source) > 0 )
);

CREATE INDEX emojis_id_ix ON emojis (id);
CREATE INDEX emojis_name_ix ON emojis (name);
CREATE INDEX emojis_guild_ix ON emojis (guild_id);

CREATE TRIGGER update_emojis_modified
    BEFORE UPDATE
    ON emojis
    FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();
-- end emojis --
