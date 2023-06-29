# epic-games-notification-bot
Ongoing project to create a python based bot to send email notifications when free games become available on the EPIC games store.


make sure .env is added

```
docker build --tag epic-games-notification-bot-image .

docker run -d --name epic-games-notification-bot-container -v epic-games-notification-bot-volume:/app/persistent_data epic-games-notification-bot-image
```
