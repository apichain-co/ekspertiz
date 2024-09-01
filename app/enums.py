from enum import Enum


class TransmissionType(Enum):
    MANUAL = "Düz vites"
    AUTOMATIC = "Otomatik"
    SEMI_AUTOMATIC = "Yarı otomatik"


class FuelType(Enum):
    GASOLINE = "Benzin"
    LPG = "Benzin + LPG"
    DIESEL = "Dizel"
    ELECTRIC = "Elektrikli"
    HYBRID = "Hibrit"


class Color(Enum):
    BEIGE = "Bej"
    WHITE = "Beyaz"
    BURGUNDY = "Bordo"
    SMOKE = "Füme"
    GRAY = "Gri"
    SILVER_GRAY = "Gümüş Gri"
    BROWN = "Kahverengi"
    RED = "Kırmızı"
    NAVY_BLUE = "Lacivert"
    BLUE = "Mavi"
    PURPLE = "Mor"
    PINK = "Pembe"
    YELLOW = "Sarı"
    BLACK = "Siyah"
    CHAMPAGNE = "Şampanya"
    TURQUOISE = "Turkuaz"
    ORANGE = "Turuncu"
    GREEN = "Yeşil"


class ReportStatus(Enum):
    OPENED = "Açılmış"
    COMPLETED = "Tamamlanmış"
    CANCELLED = "İptal edilmiş"


class ExpertiseAnswer:

    class BasicControl(Enum):
        pass

