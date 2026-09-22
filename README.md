# RSAcademy – RSA attack suite

أداة تعليمية Pure Python لاسترجاع الملفات من الصور الثنائية عبر Magic Bytes، Header/Footer Matching، التحقق البنيوي، Entropy، Hashes، خرائط offsets وتقارير JSON/HTML.

## التشغيل

```bash
python3 main.py --help
python3 main.py carve samples/mixed.bin --output results
python3 main.py batch samples --recursive --pattern '*.bin'
```

النواة لا تعتمد على مكتبات خارجية. Backend `yara` اختياري ومصمم ليُفشل بوضوح إذا لم تكن `yara-python` مثبتة أو لم تُجهز قواعده.

## المراحل

تم الحفاظ على المراحل الخمس عشرة الرسمية في `docs/phases.html`. الإصدار الحالي يركز على مسار Pure Python القابل للدفاع الأكاديمي، مع الاعتراف بحدود استخراج الملفات المجزأة والأنظمة الملفات الكاملة.

## الاختبارات

```bash
python3 -m unittest discover -s tests -v
```
