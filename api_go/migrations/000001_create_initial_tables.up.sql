-- begin prereqs ---
CREATE EXTENSION IF NOT EXISTS "pg_idkit";

CREATE OR REPLACE FUNCTION update_modified_column()
    RETURNS TRIGGER AS
$$
BEGIN
    IF ROW (NEW.*) IS DISTINCT FROM ROW (OLD.*) THEN
        NEW.modified = now();
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
        NEW.is_edited = true;
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
    RETURN floor(random() * (max - min + 1) + min)::INTEGER;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION create_general_channel_after_guild_insert()
    RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO channels (name, guild, is_general)
    VALUES ('general', NEW.id, true);
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';
-- end prereqs ---

-- begin guilds --
CREATE TABLE IF NOT EXISTS guilds
(
    id       VARCHAR(36) DEFAULT idkit_uuidv7_generate(),
    created  TIMESTAMP   DEFAULT current_timestamp,
    modified TIMESTAMP   DEFAULT current_timestamp,
    name     VARCHAR(64) NOT NULL,
    avatar   TEXT,
    banner   TEXT,

    CONSTRAINT guilds_pk PRIMARY KEY (id),
    CONSTRAINT guilds_name_uq UNIQUE (name),
    CHECK ( length(name) > 0 ),
    CHECK ( CASE WHEN avatar IS NULL THEN true ELSE length(avatar) > 0 END ),
    CHECK ( CASE WHEN banner IS NULL THEN true ELSE length(banner) > 0 END )
);

CREATE INDEX guilds_id_ix ON guilds (id);
CREATE INDEX guilds_name_ix ON guilds (name);

CREATE TRIGGER update_guild_modified
    BEFORE UPDATE
    ON guilds
    FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER after_guild_insert_trigger
    AFTER INSERT
    ON guilds
    FOR EACH ROW
EXECUTE PROCEDURE create_general_channel_after_guild_insert();
-- end guilds --

-- begin channels --
CREATE TABLE IF NOT EXISTS channel_groups
(
    id       VARCHAR(36) DEFAULT idkit_uuidv7_generate(),
    created  TIMESTAMP   DEFAULT current_timestamp,
    modified TIMESTAMP   DEFAULT current_timestamp,
    name     VARCHAR(32)                                          NOT NULL,
    guild    VARCHAR(36) REFERENCES guilds (id) ON DELETE CASCADE NOT NULL,
    "order"  INTEGER,

    CONSTRAINT channel_groups_pk PRIMARY KEY (id),
    CONSTRAINT channel_groups_name_guild_uq UNIQUE (name, guild),
    CHECK ( length(name) > 0 )
);

CREATE INDEX channel_groups_id_ix ON channel_groups (id);
CREATE INDEX channel_groups_name_ix ON channel_groups (name);

CREATE TRIGGER update_channel_groups_modified
    BEFORE UPDATE
    ON channel_groups
    FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();

CREATE TYPE channel_type AS ENUM ('text', 'voice');

CREATE TABLE IF NOT EXISTS channels
(
    id            VARCHAR(36)                                                   DEFAULT idkit_uuidv7_generate(),
    created       TIMESTAMP                                                     DEFAULT current_timestamp,
    modified      TIMESTAMP                                                     DEFAULT current_timestamp,
    name          VARCHAR(32)                                          NOT NULL,
    guild         VARCHAR(36) REFERENCES guilds (id) ON DELETE CASCADE NOT NULL,
    channel_group VARCHAR(36) REFERENCES channel_groups (id) ON DELETE CASCADE,
    type          channel_type                                         NOT NULL DEFAULT 'text',
    is_general    BOOLEAN                                              NOT NULL DEFAULT FALSE,
    "order"       INTEGER,

    CONSTRAINT channels_pk PRIMARY KEY (id),
    CONSTRAINT channels_name_guild_uq UNIQUE (name, guild),
    CHECK ( length(name) > 0 )
);

CREATE INDEX channels_id_ix ON channels (id);
CREATE INDEX channels_name_ix ON channels (name);

CREATE TRIGGER update_channels_modified
    BEFORE UPDATE
    ON channels
    FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();
-- end channels --

-- begin users --
CREATE TYPE availability_status AS ENUM ('online', 'idle', 'dnd', 'offline');

CREATE TABLE IF NOT EXISTS users
(
    id                    VARCHAR(36)                                                                                            DEFAULT idkit_uuidv7_generate(),
    created               TIMESTAMP                                                                                              DEFAULT current_timestamp,
    modified              TIMESTAMP                                                                                              DEFAULT current_timestamp,
    username              VARCHAR(32)                                                                                   NOT NULL,
    discriminator         SMALLINT                                                                                      NOT NULL DEFAULT randint(1, 9999),
    full_username         VARCHAR(36) GENERATED ALWAYS AS (username || '#' || lpad(discriminator::TEXT, 4, '0')) STORED NOT NULL,
    email                 TEXT                                                                                          NOT NULL,
    avatar                TEXT,
    cover                 TEXT,
    "availability_status" availability_status                                                                           NOT NULL DEFAULT 'offline',

    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT users_username_discriminator_uq UNIQUE (username, discriminator),
    CHECK ( length(username) > 0 ),
    CHECK ( discriminator >= 1 AND discriminator <= 9999 )
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

CREATE TABLE user_guilds_order
(
    "user"  VARCHAR(36) REFERENCES users (id) ON DELETE CASCADE  NOT NULL,
    guild   VARCHAR(36) REFERENCES guilds (id) ON DELETE CASCADE NOT NULL,
    "order" INTEGER                                              NOT NULL,

    CONSTRAINT user_guilds_order_pk PRIMARY KEY ("user", guild)
);
-- end users --

-- begin messages --
CREATE TABLE IF NOT EXISTS messages
(
    id        VARCHAR(36)                                                     DEFAULT idkit_uuidv7_generate(),
    created   TIMESTAMP                                                       DEFAULT current_timestamp,
    modified  TIMESTAMP                                                       DEFAULT current_timestamp,
    author    VARCHAR(36)                                            REFERENCES users (id) ON DELETE SET NULL,
    channel   VARCHAR(36) REFERENCES channels (id) ON DELETE CASCADE NOT NULL,
    content   VARCHAR(2048)                                          NOT NULL,
    is_edited BOOLEAN                                                NOT NULL DEFAULT false,

    CONSTRAINT messages_pk PRIMARY KEY (id),
    CHECK ( length(content) > 0 )
);

CREATE INDEX messages_id_ix ON messages (id);
CREATE INDEX messages_author_ix ON messages (author);
CREATE INDEX messages_channel_ix ON messages (channel);

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
CREATE TABLE IF NOT EXISTS emojis
(
    id       VARCHAR(36) DEFAULT idkit_uuidv7_generate(),
    created  TIMESTAMP   DEFAULT current_timestamp,
    modified TIMESTAMP   DEFAULT current_timestamp,
    name     VARCHAR(16)                                          NOT NULL,
    source   TEXT                                                 NOT NULL,
    guild    VARCHAR(36) REFERENCES guilds (id) ON DELETE CASCADE NOT NULL,
    author   VARCHAR(36)                                          REFERENCES users (id) ON DELETE SET NULL,

    CONSTRAINT emojis_pk PRIMARY KEY (id),
    CONSTRAINT emojis_name_guild_uq UNIQUE (name, guild),
    CHECK ( length(name) > 0 AND length(name) <= 16 ),
    CHECK ( length(source) > 0 )
);

CREATE INDEX emojis_id_ix ON emojis (id);
CREATE INDEX emojis_name_ix ON emojis (name);
CREATE INDEX emojis_guild_ix ON emojis (guild);

CREATE TRIGGER update_emojis_modified
    BEFORE UPDATE
    ON emojis
    FOR EACH ROW
EXECUTE PROCEDURE update_modified_column();
-- end emojis --
