-- name: CreateGuild :one
INSERT INTO guilds (
    name, avatar, banner, owner_id
)
VALUES (
           $1, $2, $3, $4
       )
RETURNING *;

-- name: RetrieveGuilds :many
SELECT *
FROM guilds;

-- name: RetrieveGuild :one
SELECT *
FROM guilds
WHERE id = $1;

-- name: UpdateGuild :one
UPDATE guilds
SET name   = COALESCE(sqlc.narg('name'), name),
    avatar = COALESCE(sqlc.narg('avatar'), avatar),
    banner = COALESCE(sqlc.narg('banner'), banner)
WHERE id = @id
RETURNING *;

-- name: DeleteGuild :one
DELETE
FROM guilds
WHERE id = $1
RETURNING id;
