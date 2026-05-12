import cv2
import numpy as np
import random
import customtkinter as ctk
from tkinter import filedialog, Tk
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk


def gri_yap(resim):
    h, w, c = resim.shape
    cikti = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            b, g, r = resim[i, j]
            cikti[i, j] = int(0.299 * r + 0.587 * g + 0.114 * b)
    return cikti


def blur_yap(gri):
    h, w = gri.shape
    cikti = np.zeros((h, w), dtype=np.uint8)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            toplam = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    toplam += int(gri[i + x, j + y])
            cikti[i, j] = toplam // 9
    return cikti


def binary_yap(gri, threshold=127):
    h, w = gri.shape
    cikti = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            cikti[i, j] = 255 if gri[i, j] > threshold else 0
    return cikti


def hsv_yap(resim):
    h, w, c = resim.shape
    cikti = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            b, g, r = resim[i, j] / 255.0
            cmax = max(r, g, b)
            cmin = min(r, g, b)
            diff = cmax - cmin

            if diff == 0:
                h_val = 0
            elif cmax == r:
                h_val = (60 * ((g - b) / diff) + 360) % 360
            elif cmax == g:
                h_val = (60 * ((b - r) / diff) + 120) % 360
            else:
                h_val = (60 * ((r - g) / diff) + 240) % 360

            s_val = 0 if cmax == 0 else diff / cmax
            v_val = cmax
            cikti[i, j] = [h_val / 2, s_val * 255, v_val * 255]
    return cikti


def rotate_image(image, angle):
    rad = angle * np.pi / 180
    height, width, channels = image.shape

    center_x = width // 2
    center_y = height // 2

    rotated = np.zeros_like(image)

    for i in range(height):
        for j in range(width):
            x = j - center_x
            y = i - center_y

            old_x = int(x * np.cos(rad) + y * np.sin(rad))
            old_y = int(-x * np.sin(rad) + y * np.cos(rad))

            old_j = old_x + center_x
            old_i = old_y + center_y

            if 0 <= old_i < height and 0 <= old_j < width:
                for c in range(channels):
                    rotated[i, j, c] = image[old_i, old_j, c]
    return rotated


def increase_brightness(image, value):
    height, width, channels = image.shape
    bright = np.zeros_like(image)

    for i in range(height):
        for j in range(width):
            for c in range(channels):
                new_val = int(image[i, j, c]) + value

                # Sınır kontrolleri
                if new_val > 255:
                    new_val = 255
                elif new_val < 0:
                    new_val = 0

                bright[i, j, c] = new_val
    return bright


def resize_image(img, nh, nw):

    if len(img.shape) == 3:
        h, w, c = img.shape
        out = np.zeros((nh, nw, c), dtype=img.dtype)
        for i in range(nh):
            for j in range(nw):
                oi = int(i * h / nh)
                oj = int(j * w / nw)
                out[i, j] = img[oi, oj]
    else:
        h, w = img.shape
        out = np.zeros((nh, nw), dtype=img.dtype)
        for i in range(nh):
            for j in range(nw):
                oi = int(i * h / nh)
                oj = int(j * w / nw)
                out[i, j] = img[oi, oj]
    return out


def iki_resmi_topla(a, b):
    if a.shape != b.shape:
        print("HATA: Resim boyutlari birebir ayni olmali!")
        return None
    h, w, c = a.shape
    out = np.zeros_like(a)
    for i in range(h):
        for j in range(w):
            for k in range(c):
                val = int(a[i, j, k]) + int(b[i, j, k])
                out[i, j, k] = min(val, 255)
    return out


def iki_resmi_carp(a, b):
    if a.shape != b.shape:
        print("HATA: Resim boyutlari birebir ayni olmali!")
        return None
    h, w, c = a.shape
    out = np.zeros_like(a)
    for i in range(h):
        for j in range(w):
            for k in range(c):
                val = (int(a[i, j, k]) * int(b[i, j, k])) / 255
                out[i, j, k] = int(val)
    return out


def adaptif_esikleme(img, k=15, C=5):
    h, w = img.shape
    out = np.zeros((h, w), dtype=np.uint8)
    pad = k // 2
    for i in range(h):
        for j in range(w):
            y1 = max(0, i - pad)
            y2 = min(h, i + pad + 1)
            x1 = max(0, j - pad)
            x2 = min(w, j + pad + 1)
            pencere = img[y1:y2, x1:x2]
            ort = np.sum(pencere) / pencere.size
            out[i, j] = 255 if img[i, j] > ort - C else 0
    return out


def crop_image(img, r, c, h, w):
    out = np.zeros((h, w, 3), dtype=img.dtype)
    for i in range(h):
        for j in range(w):
            for k in range(3):
                out[i, j, k] = img[r + i, c + j, k]
    return out


def add_noise(img, p):
    noisy = np.copy(img)
    h, w, c = img.shape
    for i in range(h):
        for j in range(w):
            r = random.random()
            if r < p:
                noisy[i, j] = 255
            elif r > 1 - p:
                noisy[i, j] = 0
    return noisy


def mean_filter_color(img, k=5):
    h, w, c = img.shape
    pad = k // 2
    out = np.zeros_like(img)
    for ch in range(c):
        for i in range(pad, h - pad):
            for j in range(pad, w - pad):
                toplam = 0
                for x in range(-pad, pad + 1):
                    for y in range(-pad, pad + 1):
                        toplam += int(img[i + x, j + y, ch])
                out[i, j, ch] = toplam // (k * k)
    return out


def median_filter_color(img, k=5):
    h, w, c = img.shape
    pad = k // 2
    out = np.zeros_like(img)
    for ch in range(c):
        for i in range(pad, h - pad):
            for j in range(pad, w - pad):
                arr = []
                for x in range(-pad, pad + 1):
                    for y in range(-pad, pad + 1):
                        arr.append(int(img[i + x, j + y, ch]))
                arr.sort()
                out[i, j, ch] = arr[len(arr) // 2]
    return out


def erosion(image, kernel_size):
    height, width, channels = image.shape
    pad = kernel_size // 2
    eroded = np.zeros_like(image)
    for i in range(pad, height - pad):
        for j in range(pad, width - pad):
            for c in range(channels):
                min_val = 255
                for ki in range(-pad, pad + 1):
                    for kj in range(-pad, pad + 1):
                        val = image[i + ki, j + kj, c]
                        if val < min_val:
                            min_val = val
                eroded[i, j, c] = min_val
    return eroded


def dilation(image, kernel_size):
    height, width, channels = image.shape
    pad = kernel_size // 2
    dilated = np.zeros_like(image)
    for i in range(pad, height - pad):
        for j in range(pad, width - pad):
            for c in range(channels):
                max_val = 0
                for ki in range(-pad, pad + 1):
                    for kj in range(-pad, pad + 1):
                        val = image[i + ki, j + kj, c]
                        if val > max_val:
                            max_val = val
                dilated[i, j, c] = max_val
    return dilated


def opening(image, kernel_size):
    eroded = erosion(image, kernel_size)
    opened = dilation(eroded, kernel_size)
    return opened


def closing(image, kernel_size):
    dilated = dilation(image, kernel_size)
    closed = erosion(dilated, kernel_size)
    return closed


def zoom_in_center(image, zoom_factor=2):
    height, width = image.shape[:2]
    center_y, center_x = height // 2, width // 2
    crop_height = height // zoom_factor
    crop_width = width // zoom_factor

    y1 = center_y - crop_height // 2
    y2 = center_y + crop_height // 2
    x1 = center_x - crop_width // 2
    x2 = center_x + crop_width // 2

    cropped = image[y1:y2, x1:x2]
    zoomed = resize_image(cropped, height, width)
    return zoomed


def zoom_out_center(image, scale=0.5):
    height, width = image.shape[:2]

    small_height = max(1, int(height * scale))
    small_width = max(1, int(width * scale))
    small_image = resize_image(image, small_height, small_width)

    result = np.zeros_like(image)
    start_y = (height - small_height) // 2
    start_x = (width - small_width) // 2
    result[start_y:start_y + small_height, start_x:start_x + small_width] = small_image
    return result


def apply_convolution(image, kernel):
    height, width = image.shape
    kernel_size = kernel.shape[0]
    pad = kernel_size // 2

    padded_image = np.pad(image, pad, mode="constant", constant_values=0)
    output = np.zeros((height, width), dtype=np.float32)

    for y in range(height):
        for x in range(width):
            region = padded_image[y:y + kernel_size, x:x + kernel_size]
            output[y, x] = np.sum(region * kernel)
    return np.clip(output, 0, 255).astype(np.uint8)


def gaussian_filter_color(image):
    gaussian_kernel = np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ], dtype=np.float32) / 16

    blue = apply_convolution(image[:, :, 0], gaussian_kernel)
    green = apply_convolution(image[:, :, 1], gaussian_kernel)
    red = apply_convolution(image[:, :, 2], gaussian_kernel)
    return cv2.merge([blue, green, red])


def sobel_edge_detection(image):
    sobel_x_kernel = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32)

    sobel_y_kernel = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ], dtype=np.float32)

    height, width = image.shape
    padded_image = np.pad(image, 1, mode="constant", constant_values=0)
    gradient_x = np.zeros((height, width), dtype=np.float32)
    gradient_y = np.zeros((height, width), dtype=np.float32)

    for y in range(height):
        for x in range(width):
            region = padded_image[y:y + 3, x:x + 3]
            gradient_x[y, x] = np.sum(region * sobel_x_kernel)
            gradient_y[y, x] = np.sum(region * sobel_y_kernel)

    sobel_result = np.sqrt((gradient_x ** 2) + (gradient_y ** 2))
    return np.clip(sobel_result, 0, 255).astype(np.uint8)


#Arayüz kısmı

def dosya_sec():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(title="Resim Sec")
    root.destroy()
    return path


def show_window(name, image, x, y, width=400, height=300):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, width, height)
    cv2.moveWindow(name, x, y)
    cv2.imshow(name, image)


#Tkinter arayüzü

class AnimatedBackground(Canvas):
    def __init__(self, parent, width=1250, height=820):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg="#121212",
            highlightthickness=0
        )

        self.width = width
        self.height = height
        self.circles = []
        colors = ["#1f2937", "#111827", "#374151", "#0f172a"]

        for i in range(12):
            x = random.randint(0, width)
            y = random.randint(0, height)
            r = random.randint(30, 90)
            dx = random.choice([-1, 1]) * random.uniform(0.2, 0.6)
            dy = random.choice([-1, 1]) * random.uniform(0.2, 0.6)
            color = random.choice(colors)

            circle = self.create_oval(
                x - r, y - r, x + r, y + r,
                fill=color, outline=""
            )
            self.circles.append([circle, dx, dy])

        self.animate()

    def animate(self):
        for item in self.circles:
            circle, dx, dy = item
            self.move(circle, dx, dy)
            x1, y1, x2, y2 = self.coords(circle)

            if x1 <= -100 or x2 >= self.width + 100:
                item[1] = -item[1]
            if y1 <= -100 or y2 >= self.height + 100:
                item[2] = -item[2]

        self.after(30, self.animate)


class ImageProcessingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Görüntü İşleme Uygulaması")
        self.bg = AnimatedBackground(root, width=1250, height=820)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        root.lower(self.bg)
        self.root.geometry("1250x820")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.img = None
        self.result = None

        self.parameter_operations = [
            "Blur",
            "Binary",
            "Adaptif Eşikleme",
            "Crop",
            "Resize",
            "Salt & Pepper Noise",
            "Mean Filter",
            "Median Filter",
            "Zoom In",
            "Zoom Out",
            "Gauss Konvolüsyon",
            "Sobel Kenar Bulma",
            "Döndürme (Rotation)",
            "Parlaklık",
            "Erosion",
            "Dilation",
            "Opening",
            "Closing"
        ]

        title = ctk.CTkLabel(
            root,
            text="Görüntü İşleme Uygulaması",
            font=("Segoe UI", 40, "bold"),
            text_color="#ffffff",
            fg_color="#1e1e1e",
            bg_color="#121212",
            corner_radius=10
        )
        title.pack(pady=(20, 5))

        subtitle = Label(
            root,
            text="Python ile temel görüntü işleme algoritmaları",
            font=("Segoe UI", 18),
            bg="#1e1e1e",
            fg="#aaaaaa"
        )
        subtitle.pack(pady=(0, 15))


        top_frame = ctk.CTkFrame(
            root,
            fg_color="#1e1e1e",
            bg_color="#121212",
            corner_radius=10
        )
        top_frame.pack(pady=5)

        buton_width_ctk = 300
        buton_height_ctk = 80

        ctk.CTkButton(
            top_frame,
            text="Resim Seç",
            command=self.load_image,
            width=buton_width_ctk,
            height=buton_height_ctk,
            corner_radius=16,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            text_color="white",
            font=("Segoe UI", 20, "bold")
        ).pack(side=LEFT, padx=8)

        ctk.CTkButton(
            top_frame,
            text="Sonucu Kaydet",
            command=self.save_result,
            width=buton_width_ctk,
            height=buton_height_ctk,
            corner_radius=16,
            fg_color="#16a34a",
            hover_color="#15803d",
            text_color="white",
            font=("Segoe UI", 20, "bold")
        ).pack(side=LEFT, padx=8)

        ctk.CTkButton(
            top_frame,
            text="Temizle",
            command=self.clear_images,
            width=buton_width_ctk,
            height=buton_height_ctk,
            corner_radius=16,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            text_color="white",
            font=("Segoe UI", 20, "bold")
        ).pack(side=LEFT, padx=8)


        operation_frame = Frame(root, bg="#1e1e1e")
        operation_frame.pack(pady=10)

        Label(
            operation_frame,
            text="Uygulanacak İşlem:",
            font=("Arial", 19, "bold"),
            bg="#1e1e1e",
            fg="white"
        ).pack(side=LEFT, padx=10)

        self.operation_var = ctk.StringVar(value="Gri Ton")

        self.operation_combo = ctk.CTkComboBox(
            operation_frame,
            variable=self.operation_var,
            values=[
                "Gri Ton",
                "Blur",
                "Binary",
                "HSV",
                "Adaptif Eşikleme",
                "Crop",
                "Resize",
                "Salt & Pepper Noise",
                "Mean Filter",
                "Median Filter",
                "Zoom In",
                "Zoom Out",
                "Gauss Konvolüsyon",
                "Sobel Kenar Bulma",
                "İki Resmi Topla",
                "İki Resmi Çarp",
                "Döndürme (Rotation)",
                "Parlaklık",
                "Erosion",
                "Dilation",
                "Opening",
                "Closing"
            ],
            width=260,
            height=38,
            font=("Segoe UI", 14),
            dropdown_font=("Segoe UI", 14),
            fg_color="#1f1f1f",
            button_color="#2563eb",
            button_hover_color="#1d4ed8",
            text_color="white",
            dropdown_fg_color="#1f1f1f",
            dropdown_text_color="white",
            dropdown_hover_color="#2563eb",
            state="readonly",
            command=self.update_slider_visibility
        )

        self.operation_combo.pack(side=LEFT, padx=10)

        Button(
            operation_frame,
            text="İşlemi Uygula",
            command=self.apply_selected_operation,
            width=18,
            height=1,
            bg="#ffc107",
            fg="black",
            font=("Segoe UI", 18, "bold"),
        ).pack(side=LEFT, padx=10)

        self.status_label = Label(
            root,
            text="Durum: Lütfen bir resim seçin.",
            font=("Arial", 18),
            bg="#1e1e1e",
            fg="#cccccc"
        )
        self.status_label.pack(pady=10)


        self.slider_frame = ctk.CTkFrame(
            root,
            fg_color="#1e1e1e",
            bg_color="#121212",
            corner_radius=10
        )
        self.slider_frame.pack(pady=10)

        self.slider_title_label = ctk.CTkLabel(
            self.slider_frame,
            text="İşlem Yoğunluğu:",
            font=("Segoe UI", 13, "bold"),
            text_color="white"
        )
        self.slider_title_label.pack(side=LEFT, padx=10)

        self.intensity_var = ctk.IntVar(value=50)

        self.intensity_slider = ctk.CTkSlider(
            self.slider_frame,
            from_=1,
            to=100,
            number_of_steps=99,
            variable=self.intensity_var,
            width=320,
            height=18,
            progress_color="#2563eb",
            button_color="#2563eb",
            button_hover_color="#1d4ed8",
            fg_color="#374151",
            command=self.update_slider_label
        )

        self.intensity_slider.pack(side=LEFT, padx=10)
        self.intensity_slider.set(50)

        self.intensity_value_label = ctk.CTkLabel(
            self.slider_frame,
            text="50",
            width=40,
            height=30,
            corner_radius=12,
            fg_color="#2563eb",
            text_color="white",
            font=("Segoe UI", 13, "bold")
        )

        self.intensity_value_label.pack(side=LEFT, padx=10)


        image_frame = Frame(root, bg="#1e1e1e")
        image_frame.pack(pady=15)

        left_frame = Frame(image_frame, bg="#1f1f1f", padx=14, pady=14)
        left_frame.pack(side=LEFT, padx=18)

        right_frame = Frame(image_frame, bg="#1f1f1f", padx=14, pady=14)
        right_frame.pack(side=LEFT, padx=18)

        Label(
            left_frame,
            text="Orijinal Görüntü",
            font=("Segoe UI", 30, "bold"),
            bg="#1f1f1f",
            fg="#ffffff"
        ).pack(pady=(0, 8))

        self.original_label = Label(
            left_frame,
            bg="#0b0b0b",
            width=700,
            height=525,
            relief="flat"
        )
        self.original_label.pack()

        Label(
            right_frame,
            text="İşlem Sonucu",
            font=("Segoe UI", 30, "bold"),
            bg="#1f1f1f",
            fg="#ffffff"
        ).pack(pady=(0, 8))

        self.result_label = Label(
            right_frame,
            bg="#0b0b0b",
            width=700,
            height=525,
            relief="flat"
        )
        self.result_label.pack()

        self.update_slider_visibility()

    def update_slider_visibility(self, event=None):
        selected = self.operation_var.get()
        if selected in self.parameter_operations:
            self.intensity_slider.configure(
                state="normal", progress_color="#2563eb", button_color="#2563eb",
                button_hover_color="#1d4ed8", fg_color="#374151"
            )
            self.intensity_value_label.configure(fg_color="#2563eb", text_color="white")
            self.slider_title_label.configure(text_color="white")
        else:
            self.intensity_slider.configure(
                state="disabled", progress_color="#4b5563", button_color="#6b7280",
                button_hover_color="#6b7280", fg_color="#374151"
            )
            self.intensity_value_label.configure(fg_color="#4b5563", text_color="#d1d5db")
            self.slider_title_label.configure(text_color="#6b7280")

    def update_slider_label(self, value):
        value = int(float(value))
        self.intensity_var.set(value)
        self.intensity_value_label.configure(text=str(value))

    def load_image(self):
        path = filedialog.askopenfilename(
            title="Resim Seç",
            filetypes=[("Resim Dosyaları", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"), ("Tüm Dosyalar", "*.*")]
        )
        if not path:
            return

        self.img = cv2.imdecode(np.fromfile(path, np.uint8), 1)
        if self.img is None:
            messagebox.showerror("Hata", "Resim okunamadı!")
            return


        self.img = resize_image(self.img, 350, 500)
        self.result = None
        self.show_image(self.img, self.original_label)
        self.result_label.config(image="")
        self.status_label.config(text="Durum: Resim başarıyla yüklendi.")

    def show_image(self, image, label):
        if len(image.shape) == 2:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        pil_image = Image.fromarray(image_rgb)
        pil_image = pil_image.resize((700, 525))
        tk_image = ImageTk.PhotoImage(pil_image)
        label.config(image=tk_image)
        label.image = tk_image

    def check_image(self):
        if self.img is None:
            messagebox.showwarning("Uyarı", "Önce bir resim seçmelisiniz!")
            return False
        return True

    def show_result(self, result, process_name):
        if result is not None:
            self.result = result
            self.show_image(result, self.result_label)
            self.status_label.config(text=f"Durum: {process_name} işlemi tamamlandı.")


    def apply_gray(self):
        if self.check_image():
            result = gri_yap(self.img)
            self.show_result(result, "Gri Ton")

    def apply_blur(self, value=50):
        if self.check_image():
            gray = gri_yap(self.img)
            k = int(value / 10)
            if k < 1: k = 1
            result = gray.copy()
            for _ in range(k):
                result = blur_yap(result)
            self.show_result(result, f"Blur - Yoğunluk {value}")

    def apply_binary(self, value=50):
        if self.check_image():
            gray = gri_yap(self.img)
            threshold = int(value * 2.55)
            result = binary_yap(gray, threshold)
            self.show_result(result, f"Binary - Eşik {threshold}")

    def apply_hsv(self):
        if self.check_image():
            result = hsv_yap(self.img)
            self.show_result(result, "HSV")

    def apply_adaptive(self, value=50):
        if self.check_image():
            gray = gri_yap(self.img)
            c_value = int(value / 5)
            result = adaptif_esikleme(gray, k=15, C=c_value)
            self.show_result(result, f"Adaptif Eşikleme - C {c_value}")

    def apply_crop(self, value=50):
        if self.check_image():
            h, w = self.img.shape[:2]
            oran = value / 100
            crop_w = int(w * oran)
            crop_h = int(h * oran)
            if crop_w < 50: crop_w = 50
            if crop_h < 50: crop_h = 50
            start_x = (w - crop_w) // 2
            start_y = (h - crop_h) // 2
            result = crop_image(self.img, start_y, start_x, crop_h, crop_w)

            result = resize_image(result, h, w)
            self.show_result(result, f"Crop - Oran %{value}")

    def apply_resize(self, value=50):
        if self.check_image():
            h, w = self.img.shape[:2]
            scale = value / 100
            if scale < 0.1: scale = 0.1
            new_w = int(w * scale)
            new_h = int(h * scale)
            result = resize_image(self.img, new_h, new_w)


            result = resize_image(result, h, w)
            self.show_result(result, f"Resize - Ölçek {scale:.2f}")

    def apply_noise(self, value=50):
        if self.check_image():
            p = value / 1000
            result = add_noise(self.img, p)
            self.show_result(result, f"Salt & Pepper Noise - Oran {p:.3f}")

    def apply_mean(self, value=50):
        if self.check_image():
            noisy = add_noise(self.img, 0.05)
            k = int(value / 20) * 2 + 1
            if k < 3: k = 3
            if k > 9: k = 9
            result = mean_filter_color(noisy, k)
            self.show_result(result, f"Mean Filter - Kernel {k}x{k}")

    def apply_median(self, value=50):
        if self.check_image():
            noisy = add_noise(self.img, 0.05)
            k = int(value / 20) * 2 + 1
            if k < 3: k = 3
            if k > 9: k = 9
            result = median_filter_color(noisy, k)
            self.show_result(result, f"Median Filter - Kernel {k}x{k}")

    def apply_zoom_in(self, value=50):
        if self.check_image():
            zoom_factor = max(2, int(value / 25) + 1)
            result = zoom_in_center(self.img, zoom_factor=zoom_factor)
            self.show_result(result, f"Zoom In - Oran {zoom_factor}x")

    def apply_zoom_out(self, value=50):
        if self.check_image():
            scale = max(0.1, 1 - value / 120)
            result = zoom_out_center(self.img, scale=scale)
            self.show_result(result, f"Zoom Out - Ölçek {scale:.2f}")

    def apply_gauss(self, value=50):
        if self.check_image():
            repeat = max(1, int(value / 20))
            result = self.img.copy()
            for _ in range(repeat):
                result = gaussian_filter_color(result)
            self.show_result(result, f"Gauss Konvolüsyon - Tekrar {repeat}")

    def apply_sobel(self, value=50):
        if self.check_image():
            gray = gri_yap(self.img)
            sobel = sobel_edge_detection(gray)
            threshold = int(value * 2.55)
            h, w = sobel.shape
            result = np.zeros((h, w), dtype=np.uint8)
            for i in range(h):
                for j in range(w):
                    result[i, j] = 255 if sobel[i, j] > threshold else 0
            self.show_result(result, f"Sobel Kenar Bulma - Eşik {threshold}")

    def apply_add_two_images(self):
        if self.check_image():
            path = filedialog.askopenfilename(title="İkinci Resmi Seç")
            if not path: return
            img2 = cv2.imdecode(np.fromfile(path, np.uint8), 1)
            if img2 is None:
                messagebox.showerror("Hata", "İkinci resim okunamadı!")
                return


            img2 = resize_image(img2, self.img.shape[0], self.img.shape[1])
            result = iki_resmi_topla(self.img, img2)
            self.show_result(result, "İki Resmi Toplama")

    def apply_multiply_two_images(self):
        if self.check_image():
            path = filedialog.askopenfilename(title="İkinci Resmi Seç")
            if not path: return
            img2 = cv2.imdecode(np.fromfile(path, np.uint8), 1)
            if img2 is None:
                messagebox.showerror("Hata", "İkinci resim okunamadı!")
                return


            img2 = resize_image(img2, self.img.shape[0], self.img.shape[1])
            result = iki_resmi_carp(self.img, img2)
            self.show_result(result, "İki Resmi Çarpma")


    def apply_rotation(self, value=50):
        if self.check_image():
            angle = int((value / 100) * 360)
            result = rotate_image(self.img, angle)
            self.show_result(result, f"Döndürme - Açı {angle}°")

    def apply_brightness(self, value=50):
        if self.check_image():
            b_val = int((value - 50) * 5.1)
            result = increase_brightness(self.img, b_val)
            self.show_result(result, f"Parlaklık - Değişim Değeri {b_val}")

    def apply_erosion(self, value=50):
        if self.check_image():
            k = max(3, int(value / 20) * 2 + 1)
            result = erosion(self.img, k)
            self.show_result(result, f"Erosion - Kernel {k}x{k}")

    def apply_dilation(self, value=50):
        if self.check_image():
            k = max(3, int(value / 20) * 2 + 1)
            result = dilation(self.img, k)
            self.show_result(result, f"Dilation - Kernel {k}x{k}")

    def apply_opening(self, value=50):
        if self.check_image():
            k = max(3, int(value / 20) * 2 + 1)
            result = opening(self.img, k)
            self.show_result(result, f"Opening - Kernel {k}x{k}")

    def apply_closing(self, value=50):
        if self.check_image():
            k = max(3, int(value / 20) * 2 + 1)
            result = closing(self.img, k)
            self.show_result(result, f"Closing - Kernel {k}x{k}")


    def save_result(self):
        if self.result is None:
            messagebox.showwarning("Uyarı", "Kaydedilecek bir sonuç yok!")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Dosyası", "*.png"), ("JPG Dosyası", "*.jpg"), ("Tüm Dosyalar", "*.*")]
        )
        if not path: return
        cv2.imencode(".png", self.result)[1].tofile(path)
        self.status_label.config(text="Durum: Sonuç başarıyla kaydedildi.")
        messagebox.showinfo("Başarılı", "Sonuç kaydedildi.")

    def clear_images(self):
        self.img = None
        self.result = None
        self.original_label.config(image="")
        self.result_label.config(image="")
        self.status_label.config(text="Durum: Ekran temizlendi.")

    def apply_selected_operation(self):
        selected = self.operation_var.get()
        value = int(self.intensity_var.get())

        if selected == "Gri Ton":
            self.apply_gray()
        elif selected == "Blur":
            self.apply_blur(value)
        elif selected == "Binary":
            self.apply_binary(value)
        elif selected == "HSV":
            self.apply_hsv()
        elif selected == "Adaptif Eşikleme":
            self.apply_adaptive(value)
        elif selected == "Crop":
            self.apply_crop(value)
        elif selected == "Resize":
            self.apply_resize(value)
        elif selected == "Salt & Pepper Noise":
            self.apply_noise(value)
        elif selected == "Mean Filter":
            self.apply_mean(value)
        elif selected == "Median Filter":
            self.apply_median(value)
        elif selected == "Zoom In":
            self.apply_zoom_in(value)
        elif selected == "Zoom Out":
            self.apply_zoom_out(value)
        elif selected == "Gauss Konvolüsyon":
            self.apply_gauss(value)
        elif selected == "Sobel Kenar Bulma":
            self.apply_sobel(value)
        elif selected == "İki Resmi Topla":
            self.apply_add_two_images()
        elif selected == "İki Resmi Çarp":
            self.apply_multiply_two_images()
        elif selected == "Döndürme (Rotation)":
            self.apply_rotation(value)
        elif selected == "Parlaklık":
            self.apply_brightness(value)
        elif selected == "Erosion":
            self.apply_erosion(value)
        elif selected == "Dilation":
            self.apply_dilation(value)
        elif selected == "Opening":
            self.apply_opening(value)
        elif selected == "Closing":
            self.apply_closing(value)
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir işlem seçin.")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = ImageProcessingGUI(root)
    root.mainloop()