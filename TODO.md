

## API clients

- [x] AsyncClient facade – `akimrx`
- [x] [Authentication](https://developers.yclients.com/ru/#tag/Avtorizaciya) – `akimrx`
- [ ] [Booking](https://developers.yclients.com/ru/#tag/Onlajn-zapis) - `akimrx`
    - [ ] [User records](https://developers.yclients.com/ru/#tag/Zapisi-polzovatelya) – `akimrx`
    - [ ] [Booking users](https://developers.yclients.com/ru/#tag/Polzovateli-onlajn-zapisi) - `akimrx`
- [ ] [Companies](https://developers.yclients.com/ru/#tag/Kompanii) - `akimrx`
- [ ] [Services](https://developers.yclients.com/ru/#tag/Uslugi) — `AlexanderZharyuk`
    - [ ] [Service Categories]((https://developers.yclients.com/ru/#tag/Kategoriya-uslug)) – `AlexanderZharyuk`
- [ ] Company
    - [ ] [Company Users](https://developers.yclients.com/ru/#tag/Polzovateli)
    - [ ] [Company User](https://developers.yclients.com/ru/#tag/Polzovatel)
    - [ ] [Company Staff](https://developers.yclients.com/ru/#tag/Sotrudniki)
    - [ ] [Company Staff Schedule](https://developers.yclients.com/ru/#tag/Raspisanie-raboty-sotrudnika)
    - [ ] [Company Positions](https://developers.yclients.com/ru/#tag/Dolzhnosti)
    - [ ] [Company Clients](https://developers.yclients.com/ru/#tag/Klienty)
    - [ ] [Company Chain Clients](https://developers.yclients.com/ru/#tag/Setevye-klienty)
    - [ ] [Company Records](https://developers.yclients.com/ru/#tag/Zapisi)
    - [ ] [Company Visits](https://developers.yclients.com/ru/#tag/Vizity)
    - [ ] [Company Group Activity](https://developers.yclients.com/ru/#tag/Gruppovye-sobytiya)
    - TODO: timetable dates


## Webhook dispatcher

> Not now.

- [ ] Dispatcher
    - [ ] AbstractWebhookRegistry/Subscriber, for subscribe to webhooks
    - [ ] AbstractDispatcher
        - [ ] FastAPIAdapter
    - [ ] WebhookStrategy
        - [ ] Callback (basic)
        - [ ] QueueStrategy
            - [ ] RabbitMQ
            - [ ] RedisPubSub
        - [ ] StorageStrategy
            - [ ] RedisStorage


## Utils & other

- [x] Skeleton – `akimrx`
- [x] Expo backoff with jitter – `akimrx`
    - [x] Configurable by env – `akimrx`
- [x] Debug log – `akimrx`
- [ ] Paginator for ApiAdapter
- [ ] Response caching
    - [ ] Basic
    - [ ] Invalidation
- [ ] Timeslots / date parsers
- [ ] Boolean adapter


## Git & Dev-tools

- [ ] Pre-commit hooks – `akimrx`
    - [ ] Syntax linter & formatter - `akimrx`
    - [ ] Security linter - `akimrx`
- [ ] Package setup.py & config – `akimrx`
- [ ] Makefile – `akimrx`
- [ ] CI Github Actions – `akimrx`
- [ ] Version bumper (?)

## Example

## Tests

- [ ] Auth
