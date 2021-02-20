# Invisible Defender (Mobile)

> Current Version: v2.0.0

This repository made by İstanbul Üniversitesi-Cerrahpaşa Sustainable Energy Research Laboratuary BSc. Students. You must have server files (_invisible defender server_) in order to connect it from the application.

Contributors: @electricalgorithm and @sirtryingsomething

![Login Panel](https://github.com/electricalgorithm/invisible-defender/blob/main/assets-GIT/loginPanel.png?raw=true)
![Control Panel](https://github.com/electricalgorithm/invisible-defender/blob/main/assets-GIT/controlPanel.png?raw=true)

### Last Updates (TR)
> 20 Feb 21: Programdaki genel fonksiyonlar yeni bir dosya olan `utils.py`'da toplandı. `config.py`'daki gereksiz değişkenler silindi. Bağlantının sunucudan kesilebilmesi için gerekli kod bloğu eklendi. Joystick'teki bir süre sonra ortaya çıkan hata düzeltildi. Ekranda çıkan bildirimler (toast) düzeltildi, `update_data()` fonksiyonun içindeki gereksiz kodlar temizlendi -- process'e eklendi. `is not` şeklinde hatalı yazılmış olan koşullar düzeltildi.
>
> 19 Feb 21: Program, mobil yazılım haline çevrildi. APK hazırlandı. *GÖRÜNTÜ AKTARIMI SORUNLU!*. PyCryptodome kütüphanesine yapılmış olan değişiklikler yok edildi. Requirements.txt güncellendi. Görüntü aktarımı için mobilde opencv sorun çıkarttığından struct/pickle koduna geçildi.

### Notes to Ourselves
* Don't install PyCrypto and PyCryptodome at same project. Don't use PyCrypto since its vulnerable.
* PyCryptodomex doesn't have recipe for p4a. Don't use it, either.
* `adb devices` can be used for listing connected Android devices (adb is in your `~/.buildozer` directory.). Also, `adb logcat *:S python:D` can be used for outputs. Don't forget that zsh won't recognize the asteriks, so that put a escape character before it: `adb logcat \*:S python:D`.

### Installing
1. Download the repository.
2. Create a virtual environment with `virtualenv . --python=python3.7`. It should use Python version 3.7.
3. Activate the virtual enviroment.
4. Use pip to install all requirements with `pip install -r requirements.txt`.
5. Now, you can launch the application in your computer with `python main.py` or you can create an -debug- APK with `buildozer -v android debug`. See buildozer for details and further readings.

---

### What to do next? (TR)

- [ ]  Kameranın görüntü aktardığı sunucu, mobilde işe yaramıyor. Numpy kütüphanesi `ImportError: dlopen failed:` hatası veriyor. Bunun düzeltilmesi için yeni bir görüntü paylaşımı algoritması kurulması gerek. (Acil!)
- [x] `is not` şeklinde yazılmış koşullar `=!`'a dönüşütürlmeli.
- [ ] Kullanıcının şifresi hashlenip sunucuya yollanmalı ve sunucuda hashlenmiş hali tutulmalı.
- [ ] Tüm veri aktarımı RSA ile yapılmasından ziyade, RSA ile handshake yapılmalı ve diğer iletişim paylaşılmış olan anahtar aracılığı ile AES ile yürütülmeli.
- [x] `type_conversion` gibi genel fonksiyonlar ayrı bir Python dosyası olarak yazılmalı.
- [ ] Tüm byte olarak hazırlanmış veriler, bitlere çevirilmeli.
- [ ] `username@IP:port` şeklinde olan giriş kısmına eğer düzgün bir şekilde girilmezse uygulamadan atıyor. Bunun yerine hata fırlatması ayarlanmalı.
- [ ] Kamera aktarımı da şifrelenmeli.
- [ ] Giriş ekranındaki kutu, telefonda ilk kez açıldığnda görünmez bir pozisyonda oluyor. Düzeltilmeli.
- [ ] Bir simge ve açılış ekranı görselleri hazırlanmalı.
- [ ] Başlıklar düzeltilmeli.

