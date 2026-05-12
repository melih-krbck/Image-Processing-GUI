# 🖼️ Görüntü İşleme ve Filtreleme Uygulaması (Image Processing GUI)

Bu proje, temel görüntü işleme algoritmalarının matematiksel matris işlemleriyle sıfırdan (from scratch) kodlandığı ve modern bir arayüzle sunulduğu bir masaüstü uygulamasıdır. 

Uygulamanın en büyük özelliği; filtreleme, morfolojik işlemler ve kenar bulma gibi çekirdek algoritmaların hazır OpenCV fonksiyonları yerine **tamamen NumPy kullanılarak manuel olarak geliştirilmiş** olmasıdır.

## ✨ Özellikler ve Algoritmalar

Uygulama üzerinden yoğunluk dereceleri (slider) ayarlanarak aşağıdaki işlemler gerçek zamanlı uygulanabilir:

### 1. Renk Uzayı ve Eşikleme İşlemleri
- **Gri Tonlama & Binary:** RGB piksellerinin formülize edilerek dönüştürülmesi.
- **HSV Dönüşümü:** Renk kanallarının Hue, Saturation, Value değerlerine çevrilmesi.
- **Eşikleme:** Standart Binary ve Adaptif Eşikleme algoritmaları.
- **Parlaklık:** Görüntü matrisine piksel bazlı müdahale.

### 2. Filtreleme ve Gürültü (Noise & Filters)
- **Tuz ve Biber Gürültüsü:** Manuel gürültü ekleme simülasyonu.
- **Mean & Median Filter:** Çekirdek (kernel) matrisi gezdirilerek gürültü temizleme.
- **Gauss Konvolüsyonu:** Özel Gauss matrisi ile yumuşatma (blur) işlemi.

### 3. Morfolojik İşlemler
- **Erosion & Dilation:** Aşındırma ve yayma algoritmaları.
- **Opening & Closing:** Nesne temizleme ve boşluk doldurma işlemleri.

### 4. Geometrik Dönüşümler ve Kenar Bulma
- **Döndürme (Rotation):** Trigonometrik matris çarpımlarıyla piksel taşıma.
- **Crop, Resize & Zoom:** Piksellerin yeniden boyutlandırılması ve merkeze odaklanma.
- **Sobel Kenar Bulma:** X ve Y türev matrisleriyle kenar tespiti.

## 🚀 Kurulum ve Çalıştırma

**1. Repoyu Klonlayın:**
```bash
git clone [https://github.com/melih-krbck/Image-Processing-GUI-from-Scratch.git](https://github.com/melih-krbck/Image-Processing-GUI-from-Scratch.git)
cd Image-Processing-GUI-from-Scratch
```

**2. Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

## 🛠️ Kullanılan Teknolojiler
Arayüz (GUI): CustomTkinter, Tkinter, Pillow (PIL)

Matematik & Matris İşlemleri: NumPy

Dosya Okuma/Yazma: OpenCV (cv2)

## Geliştirici: Melih Karabacak
