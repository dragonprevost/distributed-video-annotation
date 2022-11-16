sudo docker run -p 6000:6000  --name=master --mount source=test-video-volume,target=/data  --mount source=test-video-volume-results,target=/results master
