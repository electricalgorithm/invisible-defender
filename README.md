# Invisible Defender (Mobile)

> Current Version: v2.0.6 | Last APK version: v2.0.6

This repository made by İstanbul Üniversitesi-Cerrahpaşa Sustainable Energy Research Laboratuary BSc. Students. You must have server files (_invisible defender server_) in order to connect it from the application.

Contributors: @electricalgorithm and @sirtryingsomething

![Login Panel](https://github.com/electricalgorithm/invisible-defender/blob/main/assets-GIT/loginPanel.png?raw=true)
![Control Panel](https://github.com/electricalgorithm/invisible-defender/blob/main/assets-GIT/controlPanel.png?raw=true)

### Last Updates (TR)

> 25 Feb 21: Kullanıcı şifresinin hashlenip gönderilmesi halledildi. Şifreleme baştan aşağı değiştirildi, RSA ile handshake yapıldıktan sonra AES-256 şifreleme kullanıldı. `RSA.generate()` fonksiyonu `__init__` içine alındı, böylece giriş yapılması için beklenen süre azaltıldı. Hatalar giderildi. Sınıfların içerisinde yer almayan tüm fonksiyonlar statik metot olarak MainApp sınıfının içine tanımlandı. Global değişkenler MainApp sınıfının içinde property olarak eklendi, ancak diğer sınıflar tarafından instance olarak çağırıldı -- bu yüzden `App` isimli objenin ismi değiştirildiğinde tüm koddaki ilgili yerlerin güncellenmesi gerekecektir. Küçük hatalar giderildi. Joystick aktarımdaki `Cipher` hataları çoğunlukla AES ile düzeltildi. `template.kv` içerisinde eskiden kalmış olan menü kodları silindi.
>
> 22 Feb 21: Yan bardaki pil, sıcaklık gibi göstergeler için `exc` komutunun kullanılması için zemin hazırlandı, sistem kuruldu. `template.kv`deki bazı hatalar giderildi. Bazı fonksiyonlar ilgili sınıfların altına statik metot olarak eklendi.
>
> 21 Feb 21: Giriş ekranı ilk açıldığında ekran yerleşimindeki sorun düzeltildi.Giriş kısmındaki başlık değiştirildi. Çarpı butonuna basmamıza rağmen kapanmamasının sebebinin thread oluşturması ve daha göndermeden kapanması olduğu düşünülerek gönderilen `!dis` mesajı ana process'te gönderilmeye başlandı. Kapanmama sorunu halloldu. (Teste ihtiyacı var!) 
>
> 21 Feb 21: İşleri karmaşıklaştıran ve gereksiz yere "sanki" bitlermiş gib gönderilen _byte stringler_ için yeni bir sistem geliştirildi. Bu sistem, `id:type:setting:value` şeklindedir. `id`, rastgele oluşturulmuş, 5 haneli bir tam sayıdır. `type`; INFO, ERROR gibi mesajın tipini kapsayan bir sayıdır. `setting`; `tempshield_status` gibi güncellenen verinin nereye ait olduğunu kapsayan bir sayıdır. `value` ise bu ayarlanmak isteyen verinin ayarlanacağı bilgidir. Tam sayı, boolean olabilir ya da string olabilir. Buna ek olarak giriş ekranındaki `user@IP:port`  girilmediği taktirde uygulamanının hata verip kapanması düzeltildi.
>
> 20 Feb 21: Önemli bir hata olan mobil uygulamaya (APK) derlendiğinde numpy sıkıntısı yok edildi. Görüntü aktarımındaki yavaşlık yüzünden çözünürlük 160x140'a düşürüldü. `assets-GIT` klasöründeki APK dosyası kaldırıldı, yeni versiyonlar "relase" olarak konulacak.
>
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

- [x]  Kameranın görüntü aktardığı sunucu, mobilde işe yaramıyor. Numpy kütüphanesi `ImportError: dlopen failed:` hatası veriyor. Bunun düzeltilmesi için yeni bir görüntü paylaşımı algoritması kurulması gerek. 
- [x] `is not` şeklinde yazılmış koşullar `=!`'a dönüşütürlmeli.
- [x] Kullanıcının şifresi hashlenip sunucuya yollanmalı ve sunucuda hashlenmiş hali tutulmalı.
- [x] Tüm veri aktarımı RSA ile yapılmasından ziyade, RSA ile handshake yapılmalı ve diğer iletişim paylaşılmış olan anahtar aracılığı ile AES ile yürütülmeli.
- [x] `type_conversion` gibi genel fonksiyonlar ayrı bir Python dosyası olarak yazılmalı.
- [x] ~~Tüm byte olarak hazırlanmış veriler, bitlere çevirilmeli.~~ Yeni bir sistem geliştirildi, bu sistem sayesinde ileride oluşabilecek sıkıntılar gidirilmesi düşünüldü.
- [x] `username@IP:port` şeklinde olan giriş kısmına eğer düzgün bir şekilde girilmezse uygulamadan atıyor. Bunun yerine hata fırlatması ayarlanmalı.
- [x] Kapatma tuşuna basıldıktan sonra bazen karşı tarafa kapatma bilgisi gönderilmiyor, bu yüzden araçtaki bilgiler kapanmıyor. Düzeltilmeli.
- [ ] Kamera aktarımı da şifrelenmeli.
- [x] Giriş ekranındaki kutu, telefonda ilk kez açıldığnda görünmez bir pozisyonda oluyor. Düzeltilmeli.
- [ ] Bir simge ve açılış ekranı görselleri hazırlanmalı.
- [x] Başlıklar düzeltilmeli.
- [x] Yan bardaki verilerin güncellenebilmesi için sistem kurulmalı.
- [ ] `Stop` komutu gittiğinde `Untrusted` hatası veriyor. Düzeltilmesi gerek.

