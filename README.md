# Docker Compose Locally

Currently the docker compose runs two instance of the yolo worker. They are connected to a shared volume bound to the local ./test-videos folder

## Setup

* Run `./create_video_volume` (possible `remove_video_volume.sh` if you are doing a fresh setup overtop an existing )one
* Run `docker-compose up --build` 