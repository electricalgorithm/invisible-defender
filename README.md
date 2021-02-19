# Invisible Defender (Mobile)

> Current Version: v2.0.0

This repository made by İstanbul Üniversitesi-Cerrahpaşa Sustainable Energy Research Laboratuary BSc. Students.

Contributors: @electricalgorithm and @sirtryingsomething

### Last Updates (TR)
> 19 Feb 21: Program, mobil yazılım haline çevrildi. APK hazırlandı. *GÖRÜNTÜ AKTARIMI SORUNLU!*. PyCryptodome kütüphanesine yapılmış olan değişiklikler yok edildi. Requirements.txt güncellendi. Görüntü aktarımı için mobilde opencv sorun çıkarttığından struct/pickle koduna geçildi.

### Notes to Ourselves
* Don't install PyCrypto and PyCryptodome at same project. Don't use PyCrypto since its vulnerable.
* PyCryptodomex doesn't have recipe for p4a. Don't use it, either.

### Installing
1. Download the repository.
2. Create a virtual environment with `virtualenv . --python=python3.7`. It should use Python version 3.7.
3. Use pip to install all requirements with `pip install -r requirements.txt`.
4. Now, you can launch the application in your computer with `python main.py` or you can create an -debug- APK with `buildozer -v android debug`. See buildozer for details and further readings.
