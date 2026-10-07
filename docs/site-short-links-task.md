# Задание разработчику: короткие ссылки-редиректы с UTM (для описаний видео и постов)

**Зачем.** В описаниях Rutube, VK, YouTube, Pinterest и Яндекс Бизнеса длинная ссылка с UTM-метками выглядит неаккуратно. Нужны короткие красивые адреса, которые перенаправляют на сайт с метками, чтобы источник считался в Метрике.

**Что сделать (лимит агента сбросится 9.10, не срочно):**
1. Добавить редиректы (HTTP 302, не 301) на главную с UTM, например:
   - `/rutube` → `/?utm_source=rutube&utm_medium=clip&utm_campaign=foto_v_kartochku`
   - `/vk` → `/?utm_source=vk&utm_medium=clip&utm_campaign=foto_v_kartochku`
   - `/youtube` → `/?utm_source=youtube&utm_medium=clip&utm_campaign=foto_v_kartochku`
   - `/pin` → `/?utm_source=pinterest&utm_medium=pin&utm_campaign=cards`
   - `/biznes` → `/?utm_source=yandex_business&utm_medium=profile&utm_campaign=cards`
2. Короткие адреса не должны попасть в индекс Яндекса и Google: отдавать `X-Robots-Tag: noindex` на самих редиректах, не добавлять в `sitemap.xml`, не менять `robots.txt` для остальных страниц.
3. Не ломать существующие страницы и канонические адреса. Проверить, что Метрика фиксирует визит после редиректа (метки сохраняются, цели работают).
4. Проверить, что адреса работают с `https://absolutecard.ru/...` и с `www` (редирект на основной домен уже есть).

**Как проверить.** `curl -I https://absolutecard.ru/rutube` отдаёт 302 и `Location` с метками. Визит виден в Метрике с `utm_source=rutube`.

**После внедрения.** В описаниях писать `absolutecard.ru/rutube` и так далее (см. журнал `docs/cardroom-backlinks-task.md`).
