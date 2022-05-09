# query-streamlink

Streamlink tarafından desteklenen tüm bağlantıları canlı akışa yönlendirmek için tasarlanmış bir Python web uygulaması.

## Streamlink projesine bağış yapmak

Bu program Streamlink sayesinde mümkün olmuştur.

Onları desteklemek için lütfen [Open Collective sayfasına](https://opencollective.com/streamlink) bağış yapın.

## Nasıl çalışır :

Bu program Streamlink'e verdiğiniz URL'ye göre bu tarihe kadar bilinen tüm oyuncular için (neredeyse !) kullanılabilecek bir URL sorarak çalışır.
query-streamlink, son kullanıcı ile Streamlink arasında bir aracı/yönlendirici gibi davranır.

### Desteklenen web siteleri :

Temel olarak [Streamlink](https://streamlink.github.io/plugin_matrix.html) tarafından desteklenen herhangi bir web sitesi

> (bazı hizmetler için coğrafi konum sorunlarına dikkat edin)

## Sorgu parametreleri:

- stream-ip (zorunlu) : Bağlantıya ihtiyacınız olan akışın URL'si.

## Program yerel olarak nasıl yüklenir :

Basit: programı ```python main.py``` kullanarak başlatın

## Uzak bir hizmette sorgu akış bağlantısı nasıl kurulur :

- Heroku : [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https%3A%2F%2Fgithub.com%2FLaneSh4d0w%2Fquery-streamlink) ([@adrianpaniagualeon'a](https://github.com/adrianpaniagualeon)) teşekkürler..
- Diğer hizmetler (repl / glitch...):
Diğer türler için, belirli konfigürasyonları olup olmadığına bakın, ancak programın çalışması için hesabınızı kullanan basit bir fork yeterlidir!

## Teşekkürler :

- Uygulamanın desteklenmesi ve yeniden işlenmesi için [@keystroke3](https://github.com/keystroke3).

- Bunu mümkün kılan IPTV peepz'i (Nintendocustom / Dum4G sayesinde özel)

- Testçiler

- Bu harika araç için Streamlink üyeleri ve katkıda bulunanlar.

### Mevcut web siteleri (28/04/2022 itibariyle)

İnternette sorgu akışı bağlantısını kullanan gerçek yenilenmiş web siteleri şunlardır:

[FullSpeed ​​- DCT EU (dct-infra)](http://free.fullspeed.tv/)
[StreamLive2021](https://streamlive2021.herokuapp.com/)