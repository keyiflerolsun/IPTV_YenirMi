# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Kekik.cli    import konsol
from cloudscraper import CloudScraper
from httpx        import Client
import re

class TRGoals:
    def __init__(self, m3u_dosyasi):
        self.m3u_dosyasi = m3u_dosyasi
        self.oturum      = CloudScraper()
        self.httpx       = Client()

    def referer_domainini_al(self):
        referer_deseni = r'#EXTVLCOPT:http-referrer=(https?://[^/]*trgoals[^/]*\.[^\s/]+)'
        with open(self.m3u_dosyasi, "r") as dosya:
            icerik = dosya.read()

        if eslesme := re.search(referer_deseni, icerik):
            return eslesme[1]
        else:
            raise ValueError("M3U dosyasında 'trgoals' içeren referer domain bulunamadı!")

    def trgoals_domaini_al(self):
        istek        = self.httpx.post("http://51.145.215.21:1453/api/v1/cf", json={"url": "https://trgoalsgiris.xyz/"})
        redirect_url = re.search(r"href=\"([^\"]*redirect[^\"]*)\"", istek.text)[1]
        istek        = self.httpx.post("http://51.145.215.21:1453/api/v1/url", json={"url": redirect_url})
        redirect_url = istek.json().get("url")

        return redirect_url[:-1] if redirect_url.endswith("/") else redirect_url

    def m3u_guncelle(self):
        eldeki_domain = self.referer_domainini_al()
        konsol.log(f"[yellow][~] Bilinen Domain : {eldeki_domain}")

        try:
            istek       = self.oturum.get(eldeki_domain, allow_redirects=True)
            yeni_domain = istek.url[:-1] if istek.url.endswith("/") else istek.url
        except Exception:
            yeni_domain = self.trgoals_domaini_al()

        konsol.log(f"[green][+] Yeni Domain    : {yeni_domain}")

        kontrol_url = f"{yeni_domain}/channel.html?id=yayin1"

        with open(self.m3u_dosyasi, "r") as dosya:
            m3u_icerik = dosya.read()

        if not (eski_yayin_url := re.search(r'https?://[^/]+\.workers\.dev/?', m3u_icerik)):
            raise ValueError("M3U dosyasında eski yayın URL'si bulunamadı!")

        eski_yayin_url = eski_yayin_url[0]
        konsol.log(f"[yellow][~] Eski Yayın URL : {eski_yayin_url}")

        response = self.oturum.get(kontrol_url)

        if not (yayin_ara := re.search(r'var baseurl = "(https?://[^"]+)"', response.text)):
            raise ValueError("Base URL bulunamadı!")

        yayin_url = yayin_ara[1]
        konsol.log(f"[green][+] Yeni Yayın URL : {yayin_url}")

        yeni_m3u_icerik = m3u_icerik.replace(eski_yayin_url, yayin_url)
        yeni_m3u_icerik = yeni_m3u_icerik.replace(eldeki_domain, yeni_domain)

        with open(self.m3u_dosyasi, "w") as dosya:
            dosya.write(yeni_m3u_icerik)

if __name__ == "__main__":
    guncelleyici = TRGoals("Kanallar/KekikAkademi.m3u")
    guncelleyici.m3u_guncelle()