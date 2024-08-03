-- name: CreateGuild :one
INSERT INTO guilds (name, avatar, banner)
VALUES ($1, $2, $3)
RETURNING *;

-- name: RetrieveGuilds :many
SELECT *
FROM guilds
LIMIT sqlc.arg('limit') OFFSET sqlc.arg('offset');

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
