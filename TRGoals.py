# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Kekik.cli import konsol
from httpx     import Client
from parsel    import Selector
import re

class TRGoals:
    def __init__(self, m3u_dosyasi):
        self.m3u_dosyasi = m3u_dosyasi
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
        istek        = self.httpx.post("http://10.0.2.0:1221/api/v1/cf", json={"url": "https://bit.ly/m/taraftarium24hd"})
        # redirect_url = re.search(r"href=\"([^\"]*redirect[^\"]*)\"", istek.text)[1]
        secici       = Selector(istek.text)
        redirect_url = secici.xpath("(//section[@class='links']/a)[1]/@href").get()

        return self.redirect_gec(self.redirect_gec(redirect_url))

    def redirect_gec(self, redirect_url:str):
        istek        = self.httpx.post("http://10.0.2.0:1221/api/v1/url", json={"url": redirect_url})
        redirect_url = istek.json().get("url")

        domain = redirect_url[:-1] if redirect_url.endswith("/") else redirect_url

        if "error" in domain:
            raise ValueError("Redirect domain hatalı..")

        return domain

    def m3u_guncelle(self):
        eldeki_domain = self.referer_domainini_al()
        konsol.log(f"[yellow][~] Bilinen Domain : {eldeki_domain}")

        try:
            yeni_domain = self.trgoals_domaini_al()
        except Exception:
            try:
                yeni_domain = self.redirect_gec("https://bit.ly/3Byg5Iw?r=lp&m=Mo35cuwH2jM")
            except Exception:
                try:
                    yeni_domain = self.redirect_gec(eldeki_domain)
                except Exception:
                    rakam = int(eldeki_domain.split("trgoals")[1].split(".")[0]) + 1
                    yeni_domain = f"https://trgoals{rakam}.xyz"

        konsol.log(f"[green][+] Yeni Domain    : {yeni_domain}")

        kontrol_url = f"{yeni_domain}/channel.html?id=yayin1"

        with open(self.m3u_dosyasi, "r") as dosya:
            m3u_icerik = dosya.read()

        if not (eski_yayin_url := re.search(r'https?:\/\/[^\/]+\.(workers\.dev|shop)\/?', m3u_icerik)):
            raise ValueError("M3U dosyasında eski yayın URL'si bulunamadı!")

        eski_yayin_url = eski_yayin_url[0]
        konsol.log(f"[yellow][~] Eski Yayın URL : {eski_yayin_url}")

        response = self.httpx.get(kontrol_url)

        if not (yayin_ara := re.search(r'var baseurl = "(https?:\/\/[^"]+)"', response.text)):
            konsol.print(response.text)
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
