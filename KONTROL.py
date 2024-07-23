# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Kekik.cli    import konsol
from Kekik        import satir_ekle
from httpx        import Client
from re           import compile, MULTILINE
from os           import path, remove

class IPTVParser:
    def __init__(self, dosya_yolu: str):
        self.HATALAR = "HATALAR.md"
        if path.isfile(self.HATALAR):
            remove(self.HATALAR)

        self.dosya_yolu   = dosya_yolu
        self.kanallar     = []
        self.hata_bulundu = False
        self.oturum       = Client(verify=False, timeout=5)

    def dosya_parse(self):
        with open(self.dosya_yolu, "r", encoding="utf-8") as dosya:
            satirlar = dosya.readlines()

        extinf_re     = compile(r'#EXTINF:-1 tvg-name="([^"]+)"')
        url_re        = compile(r'^(https?://[^\s]+)', MULTILINE)
        user_agent_re = compile(r'#EXTVLCOPT:http-user-agent=(.*)')
        referer_re    = compile(r'#EXTVLCOPT:http-referrer=(.*)')

        mevcut_kanal  = {}

        for satir in satirlar:
            if satir.startswith("#EXTINF"):
                if match := extinf_re.search(satir):
                    if mevcut_kanal:
                        self.kanallar.append(mevcut_kanal)

                    mevcut_kanal = {"ad": match[1], "user-agent": None, "referer": None}

            elif satir.startswith("#EXTVLCOPT:http-user-agent"):
                if match := user_agent_re.search(satir):
                    mevcut_kanal["user-agent"] = match[1]

            elif satir.startswith("#EXTVLCOPT:http-referrer"):
                if match := referer_re.search(satir):
                    mevcut_kanal["referer"] = match[1]

            elif satir.startswith("http"):
                if match := url_re.search(satir):
                    mevcut_kanal["yayin"] = match[0]
                    self.kanallar.append(mevcut_kanal)
                    mevcut_kanal = {}

        if mevcut_kanal:
            self.kanallar.append(mevcut_kanal)

    def kanallar_kontrol(self):
        satir_ekle(self.HATALAR, """
***

> # [![Yayın Kontrolü](https://github.com/keyiflerolsun/IPTV_YenirMi/actions/workflows/Kontrol.yml/badge.svg)](https://github.com/keyiflerolsun/IPTV_YenirMi/actions/workflows/Kontrol.yml)
> ### [Kanallar/KekikAkademi.m3u](https://github.com/keyiflerolsun/IPTV_YenirMi/blob/main/Kanallar/KekikAkademi.m3u)

***

| AD | HATA | YAYIN |
|----|------|-------|
        """.strip())

        for kanal in self.kanallar:
            print("\n")
            konsol.log(f"[~] Kontrol Ediliyor : {kanal['ad']}")

            if kanal["user-agent"]:
                self.oturum.headers.update({"User-Agent": kanal["user-agent"]})

            if kanal["referer"]:
                self.oturum.headers.update({"Referer": kanal["referer"]})

            try:
                istek = self.oturum.get(kanal["yayin"])
            except Exception as hata:
                konsol.log(f"[!] {type(hata).__name__} : {hata}")
                satir_ekle(self.HATALAR, f"|  **{kanal['ad']}**  |  `{type(hata).__name__}`  |  *{kanal['yayin']}*  |")
                self.hata_bulundu = True
                continue

            if istek.status_code in [200, 301, 302, 307]:
                konsol.log(f"[+] Kontrol Edildi   : {kanal['ad']}")
            else:
                konsol.log(f"[!] {istek.status_code} » {kanal['yayin']} » {kanal['ad']}")
                satir_ekle(self.HATALAR, f"|  **{kanal['ad']}**  |  `{istek.status_code}`  |  *{kanal['yayin']}*  |")
                self.hata_bulundu = True

        if not self.hata_bulundu:
            remove(self.HATALAR)
            print("\n")
            konsol.log("[+] Hata Bulunamadı.")

    def run(self):
        self.dosya_parse()
        self.kanallar_kontrol()

if __name__ == "__main__":
    parser = IPTVParser("Kanallar/KekikAkademi.m3u")
    parser.run()