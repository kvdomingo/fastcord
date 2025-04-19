-- name: CreateUser :one
INSERT INTO users (
    username, email, avatar, cover
)
VALUES (
           $1, $2, $3, $4
       )
RETURNING *;

-- name: ListUsers :many
SELECT *
FROM users;

-- name: GetUser :one
SELECT *
FROM users
WHERE id = $1;

-- name: UpdateUser :one
UPDATE users
SET username              = COALESCE(sqlc.narg('username'), username),
    discriminator         = COALESCE(sqlc.narg('discriminator'), discriminator),
    email                 = COALESCE(sqlc.narg('email'), email),
    avatar                = COALESCE(sqlc.narg('avatar'), avatar),
    cover                 = COALESCE(sqlc.narg('cover'), cover),
    "availability_status" = COALESCE(sqlc.narg('availability_status')::AVAILABILITY_STATUS, "availability_status")
WHERE id = @id
RETURNING *;

-- name: DeleteUser :one
DELETE
FROM users
WHERE id = $1
RETURNING id;
