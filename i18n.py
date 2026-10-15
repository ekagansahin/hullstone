# UI strings. To add a language, add its code + name to LANGS and
# a translation for every key in STRINGS.

LANGS = {"en": "English", "tr": "Türkçe", "de": "Deutsch", "fr": "Français"}
DEFAULT_LANG = "en"

STRINGS = {
    "lang_label": {
        "en": "Language", "tr": "Dil", "de": "Sprache", "fr": "Langue"},
    "caption": {
        "en": "Edit the corner points; the shape is the convex hull of these points.",
        "tr": "Köşe noktalarını düzenle, şekil bu noktaların konveks zarfından oluşur.",
        "de": "Bearbeite die Eckpunkte; die Form ist die konvexe Hülle dieser Punkte.",
        "fr": "Modifiez les sommets ; la forme est l'enveloppe convexe de ces points."},
    "limits_header": {
        "en": "Size limits (mm)", "tr": "Boyut sınırları (mm)",
        "de": "Größengrenzen (mm)", "fr": "Limites de taille (mm)"},
    "limits_bad": {
        "en": "{axes}: min cannot be greater than max.",
        "tr": "{axes}: min değeri max'tan büyük olamaz.",
        "de": "{axes}: Min darf nicht größer als Max sein.",
        "fr": "{axes} : le min ne peut pas dépasser le max."},
    "limits_caption": {
        "en": "Random shapes take a size from this range on each axis. "
              "If an edited shape is out of range, a warning appears on the right.",
        "tr": "Rastgele şekil her eksende bu aralıktan bir boyut alır. "
              "Elle düzenlenen şekil sınır dışındaysa sağda uyarı çıkar.",
        "de": "Zufällige Formen erhalten auf jeder Achse eine Größe aus diesem Bereich. "
              "Liegt eine bearbeitete Form außerhalb, erscheint rechts eine Warnung.",
        "fr": "Les formes aléatoires prennent une taille dans cette plage sur chaque axe. "
              "Si une forme modifiée sort des limites, un avertissement s'affiche à droite."},
    "random_header": {
        "en": "Random shape", "tr": "Rastgele şekil",
        "de": "Zufällige Form", "fr": "Forme aléatoire"},
    "n_faces": {
        "en": "Number of faces", "tr": "Yüz sayısı",
        "de": "Anzahl der Flächen", "fr": "Nombre de faces"},
    "n_faces_help": {
        "en": "Number of planar faces including the base. Minimum 4 (tetrahedron).",
        "tr": "Taban dahil düzlemsel yüz sayısı. En az 4 (dörtyüzlü).",
        "de": "Anzahl ebener Flächen inklusive Grundfläche. Mindestens 4 (Tetraeder).",
        "fr": "Nombre de faces planes, base comprise. Minimum 4 (tétraèdre)."},
    "generate": {
        "en": "Generate", "tr": "Rastgele üret", "de": "Erzeugen", "fr": "Générer"},
    "gen_failed": {
        "en": "Could not generate a shape with {n} faces, try again.",
        "tr": "{n} yüzlü şekil üretilemedi, tekrar dene.",
        "de": "Form mit {n} Flächen konnte nicht erzeugt werden, bitte erneut versuchen.",
        "fr": "Impossible de générer une forme à {n} faces, réessayez."},
    "base_header": {
        "en": "Base points", "tr": "Taban noktaları",
        "de": "Basispunkte", "fr": "Points de base"},
    "top_header": {
        "en": "Top points", "tr": "Üst noktalar",
        "de": "Obere Punkte", "fr": "Points supérieurs"},
    "scale": {
        "en": "Scale", "tr": "Ölçek", "de": "Skalierung", "fr": "Échelle"},
    "apply": {
        "en": "Update shape", "tr": "Şekli güncelle",
        "de": "Form aktualisieren", "fr": "Mettre à jour"},
    "reset": {
        "en": "Reset to default", "tr": "Varsayılana dön",
        "de": "Zurücksetzen", "fr": "Réinitialiser"},
    "tip": {
        "en": "Tip: points inside the hull do not affect the shape. "
              "Keep z = 0 for the base points to get a flat bottom.",
        "tr": "İpucu: Zarfın içinde kalan noktalar şekli etkilemez. "
              "Düz bir alt yüzey için taban noktalarında z = 0 tut.",
        "de": "Tipp: Punkte innerhalb der Hülle beeinflussen die Form nicht. "
              "Für eine flache Unterseite z = 0 bei den Basispunkten beibehalten.",
        "fr": "Astuce : les points à l'intérieur de l'enveloppe n'influencent pas la forme. "
              "Gardez z = 0 pour les points de base afin d'obtenir un dessous plat."},
    "err_min_points": {
        "en": "At least 4 points are required.",
        "tr": "En az 4 nokta gerekli.",
        "de": "Mindestens 4 Punkte erforderlich.",
        "fr": "Au moins 4 points sont nécessaires."},
    "err_flat": {
        "en": "The points do not enclose a volume (they may all lie in one plane).",
        "tr": "Noktalar bir hacim oluşturmuyor (hepsi aynı düzlemde olabilir).",
        "de": "Die Punkte schließen kein Volumen ein (sie liegen evtl. alle in einer Ebene).",
        "fr": "Les points ne forment pas de volume (ils sont peut-être tous dans un même plan)."},
    "m_size": {
        "en": "Size (mm)", "tr": "Boyut (mm)", "de": "Größe (mm)", "fr": "Taille (mm)"},
    "m_volume": {
        "en": "Volume", "tr": "Hacim", "de": "Volumen", "fr": "Volume"},
    "m_faces": {
        "en": "Faces", "tr": "Yüz", "de": "Flächen", "fr": "Faces"},
    "m_tris": {
        "en": "Triangles", "tr": "Üçgen", "de": "Dreiecke", "fr": "Triangles"},
    "out_of_limits": {
        "en": "Outside the size limits: {items}",
        "tr": "Boyut sınırlarının dışında: {items}",
        "de": "Außerhalb der Größengrenzen: {items}",
        "fr": "Hors des limites de taille : {items}"},
    "violation_item": {
        "en": "{ax} = {v} mm (limit {mn}–{mx})",
        "tr": "{ax} = {v} mm (sınır {mn}–{mx})",
        "de": "{ax} = {v} mm (Grenze {mn}–{mx})",
        "fr": "{ax} = {v} mm (limite {mn}–{mx})"},
    "fit": {
        "en": "Fit to limits", "tr": "Sınırlara sığdır",
        "de": "An Grenzen anpassen", "fr": "Ajuster aux limites"},
    "fit_help": {
        "en": "Scales each out-of-range axis separately; face count and convexity are preserved.",
        "tr": "Sınır dışındaki eksenleri ayrı ayrı ölçekler; yüz sayısı ve konvekslik korunur.",
        "de": "Skaliert jede Achse außerhalb des Bereichs einzeln; "
              "Flächenanzahl und Konvexität bleiben erhalten.",
        "fr": "Met à l'échelle chaque axe hors limites séparément ; "
              "le nombre de faces et la convexité sont conservés."},
    "in_limits": {
        "en": "Dimensions are within limits.",
        "tr": "Boyutlar sınırlar içinde.",
        "de": "Abmessungen liegen innerhalb der Grenzen.",
        "fr": "Les dimensions respectent les limites."},
    "below_bed": {
        "en": "Some points are below z = 0; you may need to place the part on the bed in your slicer.",
        "tr": "Bazı noktalar z < 0'da; dilimleyicide parçayı tablaya oturtman gerekebilir.",
        "de": "Einige Punkte liegen unter z = 0; im Slicer muss das Teil ggf. "
              "auf das Druckbett gelegt werden.",
        "fr": "Certains points sont sous z = 0 ; il faudra peut-être poser la pièce "
              "sur le plateau dans le trancheur."},
    "download": {
        "en": "Download STL", "tr": "STL indir",
        "de": "STL herunterladen", "fr": "Télécharger le STL"},
}


def translator(lang: str):
    """Returns t(key, **kw) for lang; falls back to English if a translation is missing."""
    def t(key: str, **kw) -> str:
        entry = STRINGS[key]
        text = entry.get(lang) or entry[DEFAULT_LANG]
        return text.format(**kw) if kw else text
    return t
